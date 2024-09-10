from dataclasses import dataclass


@dataclass
class ProcessedComment:
    fb_comment_id: str
    sentiment: str
    category: str
    sub_category: str