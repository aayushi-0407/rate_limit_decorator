from abc import ABC, abstractmethod

class RateLimitStrategy(ABC):
    @abstractmethod
    def allow_request(self, user_id: str, endpoint: str, timestamp: float):
        """
        Returns:
            (allowed: bool, retry_after: int | None)
        """
        pass
