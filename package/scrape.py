from bs4 import BeautifulSoup as bs4
import requests
import os

# variables
URL = os.environ.get('URL')

# scrape function
def scrape():
    # get the url
    if URL is not None:
        page = requests.get(URL)
        # parse the html
        soup = bs4(page.text, 'html.parser')
        # find the elements
        elements = soup.find_all(['h2','p'])
        # return the text
        lines = [element.text for element in elements]
        book = '\n'.join(lines[0:2] + lines[3:9])
        return book
    else:
        return []
