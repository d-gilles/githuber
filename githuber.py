import os
import random
import requests

from bs4 import BeautifulSoup as bs4
from datetime import datetime, time, timedelta
from time import sleep
from github import Github


# setup Github
g = Github(os.getenv('GITHUB_TOKEN'))
REPO_NAME = os.getenv('REPO_NAME')
repo = g.get_user().get_repo(REPO_NAME)

# setup variables
push_min = int(os.getenv('PUSH_MIN', '1'))
push_max = int(os.getenv('PUSH_MAX', '5'))
prob = int(os.getenv('PROB', '30'))
prob_we = int(os.getenv('PROB_WE', '10'))
start = int(os.getenv('START', '9'))
stop = int(os.getenv('STOP', '17'))

URL = os.environ.get('URL')

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
def push_to_github():
    # get the book
    book = scrape()
    filename = 'the_book.txt'

    # pull the file from github
    contents = repo.get_contents(filename, ref='master')
    lob = [x for x in contents.decoded_content.decode().split('\n') if x != '']
    l1 = len(lob)
    line_to_append = book.split('\n')[l1:l1+1]+['\n']
    lob += line_to_append

    repo.update_file(contents.path, f'add line nr.: {l1+1}', '\n'.join(lob), contents.sha, branch='master')
    print(f'pushed line nr.: {l1+1}')
    return lob

def schedule_pushes(push_min=1, push_max=12, prob=20, prob_we=85, start=11, stop=20):

    is_weekend = datetime.today().weekday() >= 5
    mood = random.random()
    lazy = random.random()

    print('weekend: ', is_weekend)
    print('threadhold: ', prob_we/100)
    print('mood is: ', mood, (mood < prob_we/100) )
    print('lazy? : ', lazy, (lazy < prob/100))

    if (is_weekend and (mood < prob_we/100)) or ((not is_weekend) and (lazy < prob/100)):
        print('do nothing today')
        return 0
    else:
        num_pushes = random.randint(push_min, push_max)
        print(f"Will push {num_pushes} times today starting at {start}am and ending at {stop}pm")

        x = datetime.now() + timedelta(minutes=1)
        y = datetime.now() + timedelta(hours=stop - start)
        n = (stop - start) / (num_pushes)

        interval_in_secounds = n*60*60
        jitter = interval_in_secounds/2*0.9

        print('start at', x)
        print('stop at', y)
        print('interval', n)
        print('interval in seconds = ', interval_in_secounds)
        print('jitter = ', interval_in_secounds/2*0.9)

        return num_pushes

if __name__ == '__main__':

    # schedule the pushes
    num_pushes = schedule_pushes(push_min, push_max, prob, prob_we, start, stop)


    for push in range(num_pushes):
        push_to_github()
        print (push)
        sleep(2)
