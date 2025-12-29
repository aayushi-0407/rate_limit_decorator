import time
from collections import defaultdict
from rate_limiter.strategies.base import RateLimitStrategy

class FixedWindowLimiter(RateLimitStrategy):

    def __init__(self):

        self.requests= defaultdict(lambda:{"count":0,"window_start":0})

    def allow_request(self, user_id: str, endpoint: str, current_time: float, rule: dict):

        key=f"{user_id}:{endpoint}"
        window_size=rule["window_seconds"]
        limit=rule["limit"]

        record=self.requests[key]

        if current_time - record["window_start"] >= window_size:
            record["window_start"]=current_time
            record["count"]=0
        
        if record["count"] < limit:
            record["count"] += 1
            return True, None
        else:
            retry_after=record["window_start"] + window_size - current_time
            return False, f"Rate limit exceeded. Try again in {int(retry_after)} seconds."
    