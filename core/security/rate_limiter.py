import time
from collections import deque

class SlidingWindowRateLimiter:
    def __init__(self, window_size_seconds: int, max_requests: int):
        self.window_size = window_size_seconds
        self.max_requests = max_requests
        # Hash Map: { "user_id": deque([timestamp1, timestamp2, ...]) }
        self.user_requests = {}

    def is_allowed(self, user_id: str) -> bool:
        """
        Determines if a user is allowed to make a request based on the sliding window.
        """
        current_time = time.time()

        # If it's a new user, initialize their deque and allow the request
        if user_id not in self.user_requests:
            self.user_requests[user_id] = deque([current_time])
            return True

        user_deque = self.user_requests[user_id]

        # 1. Remove outdated timestamps from the left of the deque
        # If the timestamp is older than (current_time - window_size), it's outside our window
        while user_deque and user_deque[0] < current_time - self.window_size:
            user_deque.popleft()

        # 2. Check if the user has exceeded the maximum allowed requests in the current window
        if len(user_deque) >= self.max_requests:
            return False  # Rate limited (Too Many Requests)

        # 3. If they are within the limit, log the new request and allow it
        user_deque.append(current_time)
        return True

# --- Quick Local Test ---
if __name__ == "__main__":
    # Allow max 3 requests per 5 seconds
    limiter = SlidingWindowRateLimiter(window_size_seconds=5, max_requests=3)
    test_user = "user_jayanth_99"

    print("Simulating incoming payment requests...\n")

    # Send 5 rapid requests
    for i in range(1, 6):
        allowed = limiter.is_allowed(test_user)
        status = "✅ PROCESSED" if allowed else "🛑 BLOCKED (Rate Limited)"
        print(f"Request {i}: {status}")
    
    print("\nWaiting for 6 seconds for the window to clear...")
    time.sleep(6)
    
    # Try one more request after the window clears
    allowed = limiter.is_allowed(test_user)
    status = "✅ PROCESSED" if allowed else "🛑 BLOCKED (Rate Limited)"
    print(f"Request 6 (After delay): {status}")