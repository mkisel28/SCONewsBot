from typing import Literal

from pydantic import AnyHttpUrl, BaseModel


class FeedSchema(BaseModel):
    id: int
    feed_url: AnyHttpUrl
    feed_type: Literal["rss", "sitemap"] = "rss"
