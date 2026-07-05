from agent.circuit_breaker import CircuitBreaker
from agent.fallback_chains import execute_with_retry
from typing import Callable, Any

class GlobalErrorHandler:
    def __init__(self):
        """Registers distinct circuit breakers for core external financial tools."""
        self.breakers = {
            "financial_data_api": CircuitBreaker("Financial Data API"),
            "sec_filing_search": CircuitBreaker("SEC EDGAR Search")
        }

    def route_tool_execution(self, tool_name: str, primary_func: Callable, fallback_func: Callable, *args, **kwargs) -> Any:
        """
        Orchestrates tool routing by evaluating system health. 
        Applies primary execution, retries, and ultimate fallback strategies.
        """
        breaker = self.breakers.get(tool_name)
        
        # Fallback if no specific circuit breaker is configured
        if not breaker:
            try:
                return execute_with_retry(primary_func, *args, **kwargs)
            except Exception as e:
                return f"Execution Error: {str(e)}"

        # Check state: If OPEN, skip primary entirely and hit the fallback tool
        if not breaker.allow_request():
            return fallback_func(*args, **kwargs)

        try:
            # Attempt primary tool execution with retry logic
            result = execute_with_retry(primary_func, *args, **kwargs)
            breaker.record_success()
            return result
            
        except Exception:
            breaker.record_failure()
            
            # Graceful Degradation Strategy
            try:
                fallback_result = fallback_func(*args, **kwargs)
                return f"[DEGRADED OPERATION] Primary source failed. Data pulled via fallback: {fallback_result}"
            except Exception as fallback_error:
                # Absolute last line of protection to prevent system crashes
                return f"[CRITICAL API ERROR] Data unavailable across all channels: {str(fallback_error)}"