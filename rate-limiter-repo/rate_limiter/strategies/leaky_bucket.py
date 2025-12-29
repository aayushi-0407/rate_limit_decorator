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
        """
Checks whether the incoming request can be served using the Leaky Bucket algorithm.

Args:
    user_id (str): Identifier of the user
    endpoint (str): API endpoint
    timestamp (float): Current request time (epoch seconds)
    rule (dict):
        capacity (int): Maximum size of the request queue
        leak_rate (int): Number of requests processed per second

Returns:
    Tuple[bool, Optional[int]]:
        - True if request is allowed
        - False if rate limit exceeded
"""

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