"""
Rate Limiter using Token Bucket Algorithm
Prevents API abuse and manages request rates
"""
import time
from threading import Lock
from typing import Dict, Optional
from collections import defaultdict


class TokenBucket:
    """
    Token Bucket implementation for rate limiting
    """
    
    def __init__(self, capacity: int, refill_rate: float):
        """
        Initialize Token Bucket
        
        Args:
            capacity: Maximum number of tokens (requests)
            refill_rate: Tokens refilled per second
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.time()
        self.lock = Lock()
    
    def _refill(self):
        """Refill tokens based on elapsed time"""
        now = time.time()
        elapsed = now - self.last_refill
        
        # Calculate tokens to add
        tokens_to_add = elapsed * self.refill_rate
        
        # Add tokens (up to capacity)
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill = now
    
    def consume(self, tokens: int = 1) -> bool:
        """
        Try to consume tokens
        
        Args:
            tokens: Number of tokens to consume
            
        Returns:
            True if tokens consumed successfully, False if not enough tokens
        """
        with self.lock:
            self._refill()
            
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False
    
    def get_available_tokens(self) -> float:
        """
        Get current available tokens
        
        Returns:
            Number of available tokens
        """
        with self.lock:
            self._refill()
            return self.tokens
    
    def get_wait_time(self, tokens: int = 1) -> float:
        """
        Calculate time to wait until tokens available
        
        Args:
            tokens: Number of tokens needed
            
        Returns:
            Time to wait in seconds (0 if tokens available)
        """
        with self.lock:
            self._refill()
            
            if self.tokens >= tokens:
                return 0.0
            
            tokens_needed = tokens - self.tokens
            wait_time = tokens_needed / self.refill_rate
            return wait_time


class RateLimiter:
    """
    Rate Limiter with support for multiple limits (per-user, global)
    """
    
    def __init__(
        self,
        global_requests_per_minute: int = 60,
        user_requests_per_minute: int = 10,
        user_requests_per_hour: int = 100
    ):
        """
        Initialize Rate Limiter
        
        Args:
            global_requests_per_minute: Global rate limit (all users)
            user_requests_per_minute: Per-user requests per minute
            user_requests_per_hour: Per-user requests per hour
        """
        # Global bucket
        self.global_bucket = TokenBucket(
            capacity=global_requests_per_minute,
            refill_rate=global_requests_per_minute / 60.0
        )
        
        # Per-user buckets (minute)
        self.user_buckets_minute: Dict[str, TokenBucket] = defaultdict(
            lambda: TokenBucket(
                capacity=user_requests_per_minute,
                refill_rate=user_requests_per_minute / 60.0
            )
        )
        
        # Per-user buckets (hour)
        self.user_buckets_hour: Dict[str, TokenBucket] = defaultdict(
            lambda: TokenBucket(
                capacity=user_requests_per_hour,
                refill_rate=user_requests_per_hour / 3600.0
            )
        )
        
        self.limits = {
            "global_per_minute": global_requests_per_minute,
            "user_per_minute": user_requests_per_minute,
            "user_per_hour": user_requests_per_hour
        }
    
    def check_limit(self, user_id: str = "anonymous") -> Dict[str, any]:
        """
        Check if request is allowed
        
        Args:
            user_id: Unique identifier for the user
            
        Returns:
            Dict with 'allowed' (bool), 'reason' (str), 'wait_time' (float)
        """
        # Check global limit
        if not self.global_bucket.consume():
            wait_time = self.global_bucket.get_wait_time()
            return {
                "allowed": False,
                "reason": "Global rate limit exceeded",
                "wait_time": wait_time,
                "limit_type": "global"
            }
        
        # Check user per-minute limit
        if not self.user_buckets_minute[user_id].consume():
            wait_time = self.user_buckets_minute[user_id].get_wait_time()
            # Refund global token since we didn't use it
            self.global_bucket.tokens = min(
                self.global_bucket.capacity,
                self.global_bucket.tokens + 1
            )
            return {
                "allowed": False,
                "reason": "User per-minute rate limit exceeded",
                "wait_time": wait_time,
                "limit_type": "user_minute"
            }
        
        # Check user per-hour limit
        if not self.user_buckets_hour[user_id].consume():
            wait_time = self.user_buckets_hour[user_id].get_wait_time()
            # Refund previous tokens
            self.global_bucket.tokens = min(
                self.global_bucket.capacity,
                self.global_bucket.tokens + 1
            )
            self.user_buckets_minute[user_id].tokens = min(
                self.user_buckets_minute[user_id].capacity,
                self.user_buckets_minute[user_id].tokens + 1
            )
            return {
                "allowed": False,
                "reason": "User per-hour rate limit exceeded",
                "wait_time": wait_time,
                "limit_type": "user_hour"
            }
        
        # All checks passed
        return {
            "allowed": True,
            "reason": None,
            "wait_time": 0.0,
            "limit_type": None
        }
    
    def get_user_status(self, user_id: str = "anonymous") -> Dict[str, any]:
        """
        Get current rate limit status for a user
        
        Args:
            user_id: Unique identifier for the user
            
        Returns:
            Dict with available tokens for each limit type
        """
        return {
            "global_available": self.global_bucket.get_available_tokens(),
            "user_minute_available": self.user_buckets_minute[user_id].get_available_tokens(),
            "user_hour_available": self.user_buckets_hour[user_id].get_available_tokens(),
            "limits": self.limits
        }
    
    def reset_user(self, user_id: str):
        """
        Reset rate limits for a specific user
        
        Args:
            user_id: User to reset
        """
        if user_id in self.user_buckets_minute:
            del self.user_buckets_minute[user_id]
        if user_id in self.user_buckets_hour:
            del self.user_buckets_hour[user_id]
    
    @staticmethod
    def from_env() -> "RateLimiter":
        """
        Create RateLimiter from environment variables
        
        Environment variables:
            - RATE_LIMIT_PER_MINUTE: Requests per minute (default: 10)
            - RATE_LIMIT_PER_HOUR: Requests per hour (default: 100)
            - GLOBAL_RATE_LIMIT: Global requests per minute (default: 60)
            
        Returns:
            Configured RateLimiter instance
        """
        import os
        from dotenv import load_dotenv
        
        load_dotenv()
        
        return RateLimiter(
            global_requests_per_minute=int(os.getenv("GLOBAL_RATE_LIMIT", "60")),
            user_requests_per_minute=int(os.getenv("RATE_LIMIT_PER_MINUTE", "10")),
            user_requests_per_hour=int(os.getenv("RATE_LIMIT_PER_HOUR", "100"))
        )
