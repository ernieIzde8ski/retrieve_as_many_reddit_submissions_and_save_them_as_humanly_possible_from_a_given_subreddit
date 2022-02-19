from datetime import datetime
import json
import logging
from utils.reddit import Data, RedditPost


def get_keys(data: Data, subreddits: list[str]) -> list[str]:
    subreddits = [i.strip() for i in subreddits]
    subreddits = [i for i in subreddits if i]
    if not subreddits or subreddits == ["all"]:
        return list(data.keys())
    dkeys = {key.lower(): key for key in data.keys()}
    skeys = (i.lower() for i in subreddits)
    return [dkeys[s] for s in skeys if s in dkeys]


def print_vals(stream, vals: list[RedditPost]) -> None:
    for post in vals:
        logging.debug("")
        title = post["title"] or ""
        top = (
            post["author"].ljust(30),
            post["subreddit"].ljust(20),
            datetime.fromtimestamp(post["created_at"] or 0).strftime("%Y-%m-%d %H:%M:%S"),
        )
        mid = (title[:40] + (title[40:] and "...")).ljust(30), post["url"]
        bottom = f"https://reddit.com{post['permalink']}"

        print(*top, sep=" | ", file=stream)
        print(*mid, sep=" | ", file=stream)
        print(bottom, file=stream)
        print(file=stream)
        print(file=stream)


def output(data: Data, subreddits: list[str], path: str) -> None:
    keys = get_keys(data, subreddits)
    if not keys:
        logging.error("No valid subreddits were picked!")

    # I'll rewrite this eventually lmao
    for key in keys:
        for i in data[key]:
            data[key][i]["subreddit"] = key
    vals = [j[i] for j in (data[key] for key in keys) for i in j]

    vals.sort(key=lambda x: x["created_at"] or 0)

    with open(path, "w+", encoding="utf-8") as file:
        print_vals(file, vals)

    logging.info(f"Saved dump to {path}!")
