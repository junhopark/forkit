# forkit

Forks the current repo and adds it to the logged-in GitHub account. Will initiate the login process if the person is logged out of GitHub.

## Installation, Usage, Tests

This was set up as a GitHub OAuth app. The following steps were followed:
* Log in to github.com
* Click on the profile avatar (upper right corner) > `Settings` > `Developer settings` > `OAuth Apps` > `New OAuth App`.
    * Set `Application name` to: `forkit`
    * Set `Homepage URL` to: `http://127.0.0.1:5000`
    * Set `Authorization callback URL` to: `http://127.0.0.1:5000/oauth-callback`
    * Click on the `Register application` button
* Clone the repo locally. In the project root, create a `secrets.json` file and include the necessary info.
* Open up Terminal > Go to the project root > Execute `flask run` to run the application locally
* To run unit tests, open up Terminal > Go to the project root > execute `python3 -m pytest` to run all unit tests

## Usage

* Log out of your GitHub account online.
* Run the app locally > Open up a web browser > Go to: `http://127.0.0.1:5000`
* Clicking the hyperlink on the webpage should prompt you to log into GitHub. Once the forking attempt has been submitted successfully, you will see a success message. An error message will be shown otherwise.

## Design considerations & things to note

* Created this as a GitHub OAuth app as that seemed to be a good way to facilitate and ensure that the user is logged into their GitHub account before attempting to fork the repo.
* Decided to use Flask for its simplicity and light weight-ness.
* A limitation of the [GitHub Forking API](https://docs.github.com/en/rest/repos/forks?apiVersion=2022-11-28#create-a-fork) is that the response indicates whether or not a successful forking _attempt_ occurred, which isn't the same thing as indicating that a new fork of the repo was actually created in the logged-in user's GitHub account. I chose not to handle this in this project but if we wanted to handle it, I could've first checked to see if a current fork of the repo already exists > Fork the repo (if one doesn't already exist) > Confirm whether or not the fork was created successfully.