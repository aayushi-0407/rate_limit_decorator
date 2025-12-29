import time
from collections import defaultdict
from rate_limiter.strategies.base import RateLimitStrategy

class LeakyBucketLimiter(RateLimitStrategy):

    def __init__(self):
        self.buckets=defaultdict(lambda:{
            "queue_size":0,
            "last_leak_time"
            :time.time()
        })
    
    def allow_request(self, user_id: str, endpoint: str, current_time: float, rule: dict):

        key=f"{user_id}:{endpoint}"
        capacity=rule["queue_size"]
        leak_rate=rule["leak_rate"]

        bucket=self.buckets[key]

        elapsed=current_time - bucket["last_leak_time"]
        leaked_requests=int(elapsed * leak_rate)

        if leaked_requests > 0:
            bucket["queue_size"]=max(0, bucket["queue_size"] - leaked_requests)
            bucket["last_leak_time"]=current_time

        if bucket["queue_size"] < capacity:
            bucket["queue_size"] += 1
            return True, None
        else:
            return False, "Rate limit exceeded. Try again later."