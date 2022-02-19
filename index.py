import json
import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from utils.logger import get_logger
from utils.reddit import *
import utils.list_submissions as ls


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


def load_data(path: str = "data.json") -> Data:
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        logging.info("Creating missing data file")
        resp = {}
        with open(path, "w+", encoding="utf-8") as file:
            json.dump(resp, file)
        return resp


def save_data(data: Data, path: str = "data.json") -> None:
    with open(path, "w+", encoding="utf-8") as file:
        json.dump(data, file)
    logging.info(f"Saved data to {path}!")


def retrieve(data: Data) -> None:
    reddit = Reddit(**get_env_vars("client_id", "client_secret", "user_agent"))
    data = parse_submissions(reddit, data)
    save_data(data)


def _list(data: Data) -> None:
    subreddits = input("Subreddits to dump? ").strip().split("+")
    path = input("Filepath? (optional) ").strip() or "dump.txt"
    ls.output(data, subreddits, path)


def main():
    set_logger_from_sysargs()

    data = load_data()
    do_retrieval = input("[0] Retrieve or [1] List? ") != "1"

    retrieve(data) if do_retrieval else _list(data)


if __name__ == "__main__":
    main()
