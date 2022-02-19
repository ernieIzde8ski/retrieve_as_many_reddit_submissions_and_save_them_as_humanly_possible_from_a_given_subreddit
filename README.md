# RMRSSTH~~P~~PGS: Retrieve as Many Reddit Submissions and Save Them as Humanly ~~(or Programmatically)~~ Possible from a Given Subreddit

## Prerequisites

- Python (3.10+)

## Setup

Using a venv is recommended.

```bash
pip install -r requirements.txt
python setup.py
python index.py
```

### Manual Setup

Install the required packages from `requirements.txt`.

Generate a personal use script from <https://www.reddit.com/prefs/app>, and then set the following variables either as environment variables or in a `.env` file (takes precedence). It should look something like this:

```bash
# Optional
platform="py310"
app_id="RMRSSTHPGS"
author="u/PepitoJuanitodeHuevo"
ver="1.0.0"

# Required
client_id="Cqf84t8YXh4A3ZTORpPA5A"
client_secret="TDLTC_BOYYKdk69iExMEHCx4w1-Wew"
user_agent="${platform}:${app_id}:${ver} (by ${author})"
```
