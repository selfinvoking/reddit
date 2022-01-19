# Config

You'll need to create a [Reddit app](https://www.reddit.com/prefs/apps/) to get the `CLIENT_ID` and `CLIENT_SECRET` values. When creating your app you can use anything for the "about url" and "redirect uri" fields as this code doesn't use the OAuth flow. 

You'll need to enter your reddit username and password to use this tool, this is only used to authenticate on the reddit api. They are placed in the `.env` file, which isn't watched by git so it won't be exposed if you commit to the project. If you don't feel comfortable entering your password you won't be able to use this project yet, I'll be adding OAuth support soon to eliminate this requirement.

# Quick Start

You'll need `python` installed to begin.

Ensure you have `virtualenv` installed by running `pip install virtualenv` (alternatively `pip3`).

```bash
# Clone the repo and change directory
git clone https://github.com/selfinvoking/reddit-tools
cd reddit-tools

# setup .env
# NOTE: Edit the .env file and fill in your config values
mv .env.example .env 

# create a virtaulenv
virtualenv venv

# activate the virtualenv
source venv/bin/activate

# install dependencies
pip install -r requirements.txt

# run the script
python response-rate-by-hour.py
```