"""Retry utility with exponential backoff and jitter for Docker operations"""

import asyncio
import logging
import random
from typing import Any, Callable, Optional, Type, Union
from functools import wraps

logger = logging.getLogger(__name__)


class RetryConfig:
    """Configuration for retry behavior"""
    def __init__(
        self,
        max_attempts: int = 3,
        base_delay: float = 0.1,
        max_delay: float = 2.0,
        backoff_factor: float = 2.0,
        jitter: bool = True,
        retryable_exceptions: tuple[Type[Exception], ...] = (
            ConnectionError,
            TimeoutError,
            OSError,
        )
    ):
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.backoff_factor = backoff_factor
        self.jitter = jitter
        self.retryable_exceptions = retryable_exceptions


# Default retry configs for different operation types
READ_RETRY_CONFIG = RetryConfig(
    max_attempts=3,
    base_delay=0.1,
    max_delay=1.0,
    backoff_factor=2.0,
    jitter=True
)

WRITE_RETRY_CONFIG = RetryConfig(
    max_attempts=2,
    base_delay=0.2,
    max_delay=1.5,
    backoff_factor=2.0,
    jitter=True
)

NO_RETRY_CONFIG = RetryConfig(
    max_attempts=1,
    base_delay=0.0,
    max_delay=0.0,
    backoff_factor=1.0,
    jitter=False
)


async def retry_with_backoff(
    func: Callable,
    *args,
    config: RetryConfig = READ_RETRY_CONFIG,
    operation_name: str = "docker_operation",
    **kwargs
) -> Any:
    """
    Execute a function with exponential backoff retry logic
    
    Args:
        func: Function to execute
        *args: Function arguments
        config: Retry configuration
        operation_name: Name for logging purposes
        **kwargs: Function keyword arguments
        
    Returns:
        Result of the function execution
        
    Raises:
        The last exception if all retries are exhausted
    """
    last_exception = None
    
    for attempt in range(config.max_attempts):
        try:
            if attempt > 0:
                delay = min(
                    config.base_delay * (config.backoff_factor ** (attempt - 1)),
                    config.max_delay
                )
                
                if config.jitter:
                    # Add ±25% jitter to avoid thundering herd
                    jitter_factor = 0.75 + (random.random() * 0.5)
                    delay *= jitter_factor
                
                logger.debug(
                    f"Retrying {operation_name} (attempt {attempt + 1}/{config.max_attempts}) "
                    f"after {delay:.2f}s delay",
                    extra={
                        "operation": operation_name,
                        "attempt": attempt + 1,
                        "max_attempts": config.max_attempts,
                        "delay": delay,
                        "retry": True
                    }
                )
                
                await asyncio.sleep(delay)
            
            result = await func(*args, **kwargs)
            
            if attempt > 0:
                logger.info(
                    f"{operation_name} succeeded on attempt {attempt + 1}",
                    extra={
                        "operation": operation_name,
                        "attempt": attempt + 1,
                        "retry": True
                    }
                )
            
            return result
            
        except config.retryable_exceptions as e:
            last_exception = e
            logger.warning(
                f"{operation_name} failed on attempt {attempt + 1}: {str(e)}",
                extra={
                    "operation": operation_name,
                    "attempt": attempt + 1,
                    "max_attempts": config.max_attempts,
                    "error_code": type(e).__name__,
                    "retry": True,
                    "error": str(e)
                }
            )
            
            # If this is the last attempt, don't sleep again
            if attempt == config.max_attempts - 1:
                break
                
        except Exception as e:
            # Non-retryable exception, fail immediately
            logger.error(
                f"{operation_name} failed with non-retryable error: {str(e)}",
                extra={
                    "operation": operation_name,
                    "attempt": attempt + 1,
                    "error_code": type(e).__name__,
                    "retry": False,
                    "error": str(e)
                }
            )
            raise
    
    # All retries exhausted
    logger.error(
        f"{operation_name} failed after {config.max_attempts} attempts",
        extra={
            "operation": operation_name,
            "max_attempts": config.max_attempts,
            "error_code": type(last_exception).__name__ if last_exception else "Unknown",
            "retry": True,
            "error": str(last_exception) if last_exception else "No error recorded"
        }
    )
    
    raise last_exception


def retry_async(
    config: RetryConfig = READ_RETRY_CONFIG,
    operation_name: Optional[str] = None
):
    """
    Decorator for adding retry logic to async functions
    
    Args:
        config: Retry configuration
        operation_name: Optional operation name for logging
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            op_name = operation_name or f"{func.__module__}.{func.__name__}"
            return await retry_with_backoff(
                func, *args, config=config, operation_name=op_name, **kwargs
            )
        return wrapper
    return decorator


# Operation-specific retry decorators
def retry_read(operation_name: Optional[str] = None):
    return retry_async(READ_RETRY_CONFIG, operation_name)

def retry_write(operation_name: Optional[str] = None):
    return retry_async(WRITE_RETRY_CONFIG, operation_name)

def retry_none(operation_name: Optional[str] = None):
    return retry_async(NO_RETRY_CONFIG, operation_name)