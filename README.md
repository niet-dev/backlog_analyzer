# Backlog Analyzer

Learn what games you like using Infinite Backlog and IGDB.

## Instructions

### Installation
Create a virtual environment. These instructions vary slightly depending on your platform. 

```
$ python -m venv .venv
$ .venv/scripts/Activate.bat
```

With your virtual environment enabled, navigate to the root project directory and run:

`$ pip install requirements.txt`

### Client ID and Secret
To obtain game data from IGDB, you need a Twitch account and a registered application in the Twitch Developer Portal. 

Follow the instructions [here](https://api-docs.igdb.com/#getting-started), taking note of the Client ID and Client Secret when prompted.

Open `.env.sample`. Here you will see `CLIENT_ID` and `CLIENT_SECRET`. 

Replace the sample values with your own Client ID and Secret, then rename the file from `.env.sample` to `.env`.

### Run
With your virtual environment enabled, navigate to the root project directory and run:

`$ streamlit run Home.py`

A new page will open in your default web browser.
