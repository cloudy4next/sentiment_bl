from dataclasses import dataclass


@dataclass(frozen=True)
class Comment():
    user_name : str
    user_id : str
    comment : str
    time : str
    fb_comment_id : str
    
    
    def __str__(self):
        return f'{self.user_name} commented "{self.comment}" at {self.time}'