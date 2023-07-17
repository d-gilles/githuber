import os
import random
import requests

from bs4 import BeautifulSoup as bs4
from datetime import datetime, time, timedelta
from time import sleep
from github import Github
from github import Auth

# using an access token
auth = Auth.Token(os.getenv('GITHUB_TOKEN'))

# Public Web Github
g = Github(auth=auth)

# setup Github
REPO_NAME = os.getenv('REPO_NAME')
repo = g.get_user().get_repo(REPO_NAME)

# setup variables
push_min = int(os.getenv('PUSH_MIN', '1'))
push_max = int(os.getenv('PUSH_MAX', '12'))
prob = int(os.getenv('PROB', '12'))
prob_we = int(os.getenv('PROB_WE', '85'))

URL = os.environ.get('URL', 'http://gutenberg.net.au/ebooks03/0300771h.html')

# scrape the book
def scrape():
    # get the url
    if URL is not None:
        page = requests.get(URL)
        # parse the html
        soup = bs4(page.text, 'html.parser')
        # find the elements
        elements = soup.find_all(['h2', 'p'])
        # return the text
        lines = [element.text for element in elements]
        book = '\n'.join(lines[0:2] + lines[3:9])
        return book
    else:
        return ''

# push to github
def push_to_github(do=True):

    # get the book
    book = scrape()
    filename = 'the_book.txt'

    # pull the file from github
    contents = repo.get_contents(filename, ref='master')
    if len(contents.decoded_content.decode()) > 1:
        lob = [x for x in contents.decoded_content.decode().split('\n')]
        print('book at github:', lob)
    else:
        lob = []

    l1 = len(lob)
    line_to_append = book.split('\n')[l1:l1+1]
    lob += line_to_append

    if do:
        repo.update_file(contents.path, f'add line nr.: {l1+1}', '\n'.join(lob), contents.sha, branch='master')
    else:
        print('lines of book at github: ', l1)
        print('line to append: ', line_to_append)
        print('lenth of book after append: ', len(lob))
        print('book after append: ', lob)

    return

# schedule the pushes
def schedule_pushes(push_min=1, push_max=12, prob=20, prob_we=85):

    is_weekend = datetime.today().weekday() >= 5
    mood = random.random()
    lazy = random.random()
    print("GITHUBER - The nice guy who pushes to github \n")
    print('Is it a weekend?: ', is_weekend)
    if is_weekend:
        print('Mood threshold for weekends is: ', prob_we,'%')
        print('Mood is at: ', round(mood,2)*100,'% do something: ', (mood > prob_we/100))
    else:
        print('Mood threshold for weekdays is: ', prob,'%')
        print('Mood is at: ', round(mood,2)*100,'% do something: ', (mood > prob/100))

    if (is_weekend and (mood < prob_we/100)) or ((not is_weekend) and (mood < prob/100)):
        print('do nothing today')
        return 0
    else:
        num_pushes = random.randint(push_min, push_max)
        print(f"Will push {num_pushes} times today \n")

        return num_pushes

if __name__ == '__main__':

    # do the pushes
    num_pushes = schedule_pushes(push_min, push_max, prob, prob_we)
    for push in range(num_pushes):
        push_to_github(do=False)
        print (push)
        sleep(3)
