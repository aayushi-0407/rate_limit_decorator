from collections import defaultdict, deque
from rate_limiter.strategies.base import RateLimitStrategy


class SlidingWindowLimiter(RateLimitStrategy):
    def __init__(self):
        """
        For each (user_id + endpoint), store timestamps of requests.
        """
        self.requests = defaultdict(deque)

    def allow_request(self, user_id: str, endpoint: str, current_time: float, rule: dict):
        """
        rule contains:
        - limit: max requests allowed
        - window_seconds: sliding window size
        """

        key = f"{user_id}:{endpoint}"
        window_size = rule["window_seconds"]
        limit = rule["limit"]

        request_times = self.requests[key]

        # 1️⃣ Remove requests that are outside the sliding window
        while request_times and request_times[0] <= current_time - window_size:
            request_times.popleft()

        # 2️⃣ Check if we can allow the request
        if len(request_times) < limit:
            request_times.append(current_time)
            return True, None

        # 3️⃣ Reject request → calculate retry time
        retry_after = int(
            window_size - (current_time - request_times[0])
        )
        return False, max(retry_after, 1)
