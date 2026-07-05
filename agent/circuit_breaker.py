import time

class CircuitBreaker:
    def __init__(self, name: str, failure_threshold: int = 3, recovery_timeout: float = 15.0):
        """
        Initializes a stateful circuit breaker for a specific tool endpoint.
        States: CLOSED (Normal execution), OPEN (Blocked), HALF-OPEN (Testing recovery).
        """
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.state = "CLOSED"
        self.last_failure_time = 0.0

    def allow_request(self) -> bool:
        """Determines if the system should allow a tool call or route to fallback immediately."""
        if self.state == "OPEN":
            # Check if the recovery timeout window has expired
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "HALF-OPEN"
                return True
            return False
        return True

    def record_success(self):
        """Resets the failure counter upon a successful execution."""
        self.failure_count = 0
        self.state = "CLOSED"

    def record_failure(self):
        """Increments failures and trips the circuit breaker if the threshold is crossed."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"