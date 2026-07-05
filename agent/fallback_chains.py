import time
import random
from typing import Callable, Any

def execute_with_retry(func: Callable, *args, **kwargs) -> Any:
    """
    Executes a function with an exponential backoff retry mechanism and random jitter.
    Protects against transient network issues and brief API rate limits.
    """
    max_retries = 3
    base_delay = 2.0
    
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            
            # Calculate exponential delay with randomized jitter
            delay = (base_delay ** attempt) + random.uniform(0, 0.5)
            time.sleep(delay)