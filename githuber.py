## This is a script, that pushes changes to a github repo <REPO> on a daily basis.
## The Idea is to connect to the repo, take one line of a book and append it to a file for every push.
## Pushes should be done from <STRARTDAY> to <ENDDAY> and <STARTTIME> to <ENDTIME> every day.
## For every day there should be a random number of pushes between <MINPUSHES> and <MAXPUSHES>.
## The script should be run in a container on Google Cloud Run, and should be triggered by a cron job.
## In addition, the container should be able to run locally, for testing purposes.
## The book should be stored in a file called <BOOKNAME> in a gst bucket called <BUCKETNAME>.
## The file should be called <FILENAME> and should be stored in the github repo <REPO>.
## A second container should run a frontend, that displays the content of the file <FILENAME>, the <REPO> and a graph of the pushes.
## The frontend should be build with streamlit and should be deployed on Streamlit cloud.
## All the parameters should be stored in a config file called <CONFIGFILE> in the <REPO>

# Step by step:


from package.scrape import scrape

def githuber():
    # get the book
    book = scrape()
    with open('the_book.txt', 'r+') as f:
    lob = f.readlines()
    l1 = len(lob)
    lob += book.split('\n')[l1:l1+1]+['\n']
    f.seek(0)
    f.writelines(lob)

    # push the book to github
    # push the book to streamlit cloud
    # push the book to google cloud run


if __name__ == '__main__':
    githuber()
