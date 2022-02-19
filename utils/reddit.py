from typing import Generator, TypedDict
import praw
from praw.reddit import Reddit, Subreddit, Submission, Comment, Redditor


def _get_submissions(subreddit: Subreddit, limit: int) -> Generator[Submission, None, None]:
    yield from subreddit.new(limit=limit)
    yield from subreddit.hot(limit=limit)
    yield from subreddit.rising(limit=limit)
    yield from subreddit.random_rising(limit=limit)
    yield from subreddit.controversial(limit=limit)


class RedditPost(TypedDict):
    author: str
    created_at: int | None
    id: str
    permalink: str
    score: int
    subreddit: str
    title: str | None
    url: str | None


def get_submissions(subreddit: Subreddit, limit: int = 10000) -> Generator[RedditPost, None, None]:
    processed: set[str] = set()
    for post in _get_submissions(subreddit, limit):
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
