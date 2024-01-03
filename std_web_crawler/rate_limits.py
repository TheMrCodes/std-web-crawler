import threading
import asyncio
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from std_web_crawler.error import error, value_error



URL = str


@dataclass
class RateLimit:
    """
    Data class that represents a rate limit for a specific URL.
    """

    # Fields
    rpm: Optional[int]                          = field(default=None, metadata={"unit": "requests per minute"})
    min_time_between_crawls: Optional[float]    = field(default=None, metadata={"unit": "seconds"})
    retries: int                                = field(default=0)

    # Constructor
    def __post_init__(self):
        if self.rpm is None and self.min_time_between_crawls is None:
            raise ValueError("Either rpm or min_time_between_crawls must be set!")
        if self.rpm is not None and self.min_time_between_crawls is not None:
            raise ValueError("Only one of rpm or min_time_between_crawls can be set!")
        
    
    def get_rpm(self) -> int:
        return self.rpm or int(60 / self.min_time_between_crawls)
    
    def get_min_time_between_crawls(self) -> float:
        return self.min_time_between_crawls or 60 / self.rpm



class RateLimitManager:
    """
    Class that combines multiple rate limits for different URLs and provides methods to check if a URL is avaliable and to get the rate limit for a URL.
    It also handles the backoff logic, retries and access to the services.
    """

    # Fields
    _services: Dict[URL, RateLimit]
    _access_times: Dict[URL, float]
    _access_locks: Dict[URL, asyncio.Lock]


    def __init__(self, services: Dict[URL, RateLimit]) -> None:
        self._services = services
        self._access_times = { url: 0.0 for url in services.keys() }
        self._access_locks = { url: asyncio.Lock() for url in services.keys() }


    # Methods
    # - Rate limit management
    async def wait_for_access(self, url: URL, timeout: float = None, waiting_time: float = 0.01) -> None:
        """
        Waits until the url can be accessed according to the rate limit.
        """
        # Check the arguments
        if not self.is_avaliable(url): value_error(f"Url {url} is not avaliable!")
        if timeout is not None and timeout < 0: value_error(f"Timeout must be positive!")

        # Wait until the url can be accessed
        with await self._access_locks[url]:

            # Get the min time between crawls
            min_time_between_crawls = self._services[url].get_min_time_between_crawls()
            async def check_access() -> bool:
                last_access_time = self._access_times.get(url, 0.0)
                return last_access_time + min_time_between_crawls < time.time()

            # Wait until the url can be accessed
            if timeout is not None:
                end_time = time.time() + timeout if timeout is not None else None
                while not await check_access() and time.time() < end_time:
                    await asyncio.sleep(waiting_time)
            else:
                while not await check_access():
                    await asyncio.sleep(waiting_time)

            # Update the last access time
            self._access_times[url] = time.time()
        

    # - Information retrieval methods
    def is_avaliable(self, url: URL) -> bool:
        return url in self._services
    
    def get_services(self) -> Dict[URL, RateLimit]:
        return self._services

    def get_rate_limit(self, url: URL) -> RateLimit:
        url: RateLimit = self._services.get(url, None) or value_error(f"No rate limit for url {url}")
        return url.get_rpm()
    
    def get_min_time_between_crawls(self, url: URL) -> float:
        url: RateLimit = self._services.get(url, None) or value_error(f"No rate limit for url {url}")
        return url.get_min_time_between_crawls()
    
    def get_retries(self, url: URL) -> int:
        url: RateLimit = self._services.get(url, None) or value_error(f"No rate limit for url {url}")
        return url.retries
    
    def get_last_access_time(self, url: URL) -> Optional[float]:
        return self._access_times.get(url, None)
    
    