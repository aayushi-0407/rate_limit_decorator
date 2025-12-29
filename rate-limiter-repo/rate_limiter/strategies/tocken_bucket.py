from rate_limiter.strategies.base import RateLimitStrategy
from collections import defaultdict

class Token_bucket(RateLimitStrategy):

    def __init__(self):
        self.buckets=defaultdict(lambda: {'tokens': 0, 'last_refill': None})

    def allow_request(self, user_id: str, endpoint: str, current_time: float, rule: dict):
        """
        Checks whether the incoming request can be served.

        Args:
            user_id (str): Identifier of the user
            endpoint (str): API endpoint
            timestamp (float): Current request time
            rule (dict):
                capacity (int): Maximum tokens allowed
                refill_rate (int): Tokens added per second

        Returns:
            Tuple[bool, Optional[int]]:
                - True if request is allowed
                - False if rate limit exceeded
        """
        key=f"{user_id}:{endpoint}"
        capacity=rule["capacity"]
        refill_rate=rule["refill_rate"]

        bucket=self.buckets[key]

        if bucket['last_refill'] is None:
            bucket['last_refill']=current_time

        elapsed=current_time - bucket['last_refill']
        tokens_to_add=int(elapsed * refill_rate)

        if tokens_to_add > 0:
            bucket['tokens']=min(capacity, bucket['tokens'] + tokens_to_add)
            bucket['last_refill']=current_time

        if bucket['tokens'] > 0:
            bucket['tokens'] -= 1
            return True, None
        else:
            return False, "Rate limit exceeded. Try again later."

    
    