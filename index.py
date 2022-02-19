import json
import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from utils.logger import get_logger
from utils.reddit import *


def set_logger_from_sysargs(path: Path | str = "./log.txt") -> logging.Logger:
    """Sets the default Logging logger from sys.argv arguments."""
    file = Path(path).absolute()
    file.touch()
    return get_logger(file, sys.argv[1].upper() if len(sys.argv) > 1 else None)


def get_env_vars(*required: str) -> dict[str, str]:
    load_dotenv(override=True)
    resp: dict[str, str] = {}
    for key in required:
        val = os.getenv(key)
        if not val:
            raise KeyError("Key '{key}' does not have a value associated with it")
        resp[key] = val
    return resp


SubredditData = dict[str, RedditPost]


def load_data(path: str = "data.json") -> dict[str, SubredditData]:
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        logging.info("Creating missing data file")
        resp = {}
        with open(path, "w+", encoding="utf-8") as file:
            json.dump(resp, file)
        return resp


def save_data(data: dict[str, SubredditData], path: str = "data.json") -> None:
    with open(path, "w+", encoding="utf-8") as file:
        json.dump(data, file)
    logging.info(f"Saved data to {path}!")


DEFAULT_SUBS = "+".join(
    [
        "ClassicMetal",
        "DankAlbums",
        "DankBlackMetal",
        "DankDoomMetal",
        "DankPowerMetal",
        "DankHipHop",
        "DankPunk",
        "DankBrutalDeathMetal",
        "DankIDM",
    ]
)


def parse_submissions(
    reddit: Reddit, data: dict[str, SubredditData], default_sub: str = DEFAULT_SUBS
) -> dict[str, SubredditData]:
    source_sr = reddit.subreddit(input("Subreddit? ").strip() or default_sub)
    total_changed = 0
    for submission in get_submissions(source_sr):
        sr = submission.pop("subreddit")
        id = submission.pop("id")

        if sr not in data:
            logging.debug(f"Creating object for subreddit {sr} for the first time!")
            data[sr] = {}
        elif id in data[sr]:
            logging.debug(f"Submission with id '{id}' already logged; skipping")
            continue
        else:
            logging.info(f"Dumping submission with id {id} from subreddit {sr}")
            data[sr][id] = submission
        total_changed += 1
    logging.info(f"Total number of new submissions: {total_changed}")
    return data


def main():
    set_logger_from_sysargs()

    data = load_data()
    reddit = Reddit(**get_env_vars("client_id", "client_secret", "user_agent"))
    data = parse_submissions(reddit, data)
    save_data(data)


if __name__ == "__main__":
    main()
