# GitHuber

GitHuber is an automated tool that scrapes a book from a given URL and pushes it line by line to a GitHub repository every day. The pushes have random possibility and random number each day.  It's written in Python and runs in a Docker container. The execution of the script is governed by a scheduled job in Google Cloud Run.

Why does on do that?
Well ... it´s just an exercise on how to schedule a container in the cloud to do a simple job on a regular bases.
Other than that it´s a nice way to make sure, my activity on Github looks "busy" no mather if a push things or not 😉

## Tools and Techniques Used
1. **Python**: The primary language in which the script is written.
2. **Docker**: Used to run the script in an isolated container.
3. **Google Cloud Run**: Used to host and manage the Docker container.
4. **Google Cloud Scheduler**: Used to schedule the daily run of the script.

## Reproduction Instructions
### Step 1: Setup
Firstly, you need to clone this repository to your local machine. You can do this by running the following command:

 `git clone https://github.com/d-gilles/githuber.git`

Navigate into the directory: `cd githuber`.
Then push it to your own github account in a new repo.

### Step 2: Create GitHub Token
In order to interact with your GitHub repository, the script requires a GitHub token. Here's how to generate one:

1. Go to your GitHub account settings.
2. Click on `Developer settings` at the bottom of the left sidebar.
3. Click on `Personal access tokens` in the left sidebar.
4. Click on the `Generate new token` button.
5. Give your token a descriptive name and check the boxes for the permissions your token needs.
6. Click on the `Generate token` button at the bottom.
7. Copy the token and save it somewhere safe. You won't be able to see it again!

### Step 3: Configure Environment Variables
You will need to update the `.env` file in the cloned repository with your own values:
```
# URL of th book - Le petit prince á Antoine de Saint-Exupéry
URL=http://gutenberg.net.au/ebooks03/0300771h.html

# github
GITHUB_TOKEN=<Your GitHub Token>
REPO_NAME=<Your Repository Name>
GCP_PROJECT=<Your GCP Project>
CONTAINER_REGISTRY=eu.gcr.io
REGION=europe-west3

# variables
PROB=12  # If the random number of the day is below, no work will be done
PROB_WE=85 # If the random number on a weekend is above, work will be done although it is weekend
PUSH_MIN=3
PUSH_MAX=15
```

### Step 4: Build, Run and Deploy
To build the Docker image, run the following command:

3. Build the Docker image: `make build`.
4. Run the Docker image: `make run`.
5. Push the Docker image to Container Registry: `make push`.
7. Create a Google Cloud Scheduler job to trigger the Cloud Run job daily at 9 AM.

### Step 5: Schedule the Job
Create a Google Cloud Scheduler job that triggers the Cloud Run job daily at 9 AM.

## Notes
* Make sure you have the appropriate access rights to the GitHub repository and the Google Cloud Project.
