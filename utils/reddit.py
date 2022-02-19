from typing import Generator, TypedDict
import praw
from praw.reddit import Reddit, Subreddit, Submission, Comment, Redditor
import logging
import sys

class RedditPost(TypedDict):
    author: str
    created_at: int | None
    id: str
    permalink: str
    score: int
    subreddit: str
    title: str | None
    url: str | None


SubredditData = dict[str, RedditPost]
Data = dict[str, SubredditData]

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


def _get_submissions(subreddit: Subreddit, limit: int, search_even_more: bool = False) -> Generator[Submission, None, None]:
    yield from subreddit.new(limit=limit)
    yield from subreddit.hot(limit=limit)
    yield from subreddit.rising(limit=limit)
    yield from subreddit.random_rising(limit=limit)
    yield from subreddit.controversial(limit=limit)
    
    if search_even_more:
        yield from subreddit.search(query="site:youtube OR youtu.be")


def get_submissions(subreddit: Subreddit, limit: int = 10000) -> Generator[RedditPost, None, None]:
    processed: set[str] = set()
    for post in _get_submissions(subreddit, limit, "--SEARCH_MORE" in sys.argv or "-S" in sys.argv):
        if post.id in processed:
            continue
        author: Redditor | None = getattr(post, "author", None)
        yield RedditPost(
            author="[deleted/removed]" if author is None else author.name,
            created_at=int(getattr(post, "created_utc", 0)) or None,
            id=post.id,
            permalink=getattr(post, "permalink", None) or getattr(post, "url", ""),
            score=getattr(post, "score", -1),
            subreddit=getattr(post, "subreddit", subreddit).display_name,
            title=getattr(post, "title", None),
            url=getattr(post, "url", None),
        )
        processed.add(post.id)


def parse_submissions(reddit: Reddit, data: Data, default_sub: str = DEFAULT_SUBS) -> Data:
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
