import heapq
import time
from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class PrioritizedTransaction:
    # Priority comes first so the heap sorts by it
    priority: int
    # Timestamp ensures FIFO order for transactions with the SAME priority
    timestamp: float
    # We tell the dataclass NOT to compare the actual transaction payload
    transaction_data: Any = field(compare=False)

class TransactionQueue:
    def __init__(self):
        self._queue = []

    def add_transaction(self, transaction: dict, priority_score: int):
        """
        Pushes a transaction into the heap. 
        We use negative priority_score because heapq is a min-heap by default.
        A score of 100 becomes -100, which sits at the top of the heap.
        """
        item = PrioritizedTransaction(
            priority=-priority_score, 
            timestamp=time.time(), 
            transaction_data=transaction
        )
        heapq.heappush(self._queue, item)

    def process_next(self):
        """Pops and returns the highest priority transaction in O(log n) time."""
        if self.is_empty():
            return None
        # Return the actual transaction dictionary
        return heapq.heappop(self._queue).transaction_data

    def is_empty(self) -> bool:
        return len(self._queue) == 0

# --- Quick Local Test ---
if __name__ == "__main__":
    queue = TransactionQueue()

    print("Receiving concurrent transactions...\n")

    # Simulating incoming transactions out of order
    # Priority 1: Standard User, Priority 50: Premium User, Priority 100: Critical Settlement
    queue.add_transaction({"id": "TXN-001", "user": "standard_user_1"}, priority_score=1)
    queue.add_transaction({"id": "TXN-002", "user": "standard_user_2"}, priority_score=1)
    queue.add_transaction({"id": "TXN-003", "user": "amazon_merchant"}, priority_score=50)
    queue.add_transaction({"id": "TXN-004", "user": "system_settlement"}, priority_score=100)

    print("Processing queue based on priority:\n")

    # Process all transactions
    while not queue.is_empty():
        txn = queue.process_next()
        print(f"Processing: {txn['id']} for {txn['user'].ljust(20)}")