import heapq

class PaymentRouter:
    def __init__(self):
        # Adjacency list to represent the network: { "BankA": { "BankB": fee, "BankC": fee } }
        self.network = {}

    def add_bank_connection(self, bank1: str, bank2: str, fee: float):
        """Adds a bidirectional connection between two nodes with a routing fee."""
        if bank1 not in self.network:
            self.network[bank1] = {}
        if bank2 not in self.network:
            self.network[bank2] = {}
        
        # Adding the connection both ways (undirected graph)
        self.network[bank1][bank2] = fee
        self.network[bank2][bank1] = fee 

    def find_cheapest_route(self, start_bank: str, end_bank: str):
        """
        Implementation of Dijkstra's Algorithm.
        Returns a tuple: (total_fee, path_taken)
        """
        if start_bank not in self.network or end_bank not in self.network:
            return float('inf'), []

        # Priority Queue stores tuples of (cumulative_fee, current_bank, path_taken)
        pq = [(0, start_bank, [start_bank])]
        
        # Dictionary to track the minimum fee to reach each bank
        min_fees = {bank: float('inf') for bank in self.network}
        min_fees[start_bank] = 0

        while pq:
            # Always explore the path with the lowest cumulative fee first
            current_fee, current_bank, path = heapq.heappop(pq)

            # If we reached our destination, we are done
            if current_bank == end_bank:
                return current_fee, path

            # If we pulled out a path that is worse than one we already found, skip it
            if current_fee > min_fees[current_bank]:
                continue

            # Explore all connected neighbors
            for neighbor, edge_fee in self.network[current_bank].items():
                new_fee = current_fee + edge_fee

                # If this new route is cheaper, record it and push to the queue
                if new_fee < min_fees[neighbor]:
                    min_fees[neighbor] = new_fee
                    heapq.heappush(pq, (new_fee, neighbor, path + [neighbor]))

        return float('inf'), [] # No path exists

# --- Quick Local Test ---
if __name__ == "__main__":
    router = PaymentRouter()
    
    # Build the network (Edges represent transaction fees in Rupees ₹)
    router.add_bank_connection("HDFC", "UPI_SWITCH", 1.5)
    router.add_bank_connection("HDFC", "AXIS", 2.0)
    router.add_bank_connection("UPI_SWITCH", "SBI", 1.0)
    router.add_bank_connection("AXIS", "SBI", 3.0)
    router.add_bank_connection("SBI", "ICICI", 1.2)
    router.add_bank_connection("UPI_SWITCH", "ICICI", 2.5)

    print("Banking Network Graph Initialized.\n")

    # Test 1: Find the cheapest route from HDFC to SBI
    start, end = "HDFC", "SBI"
    cost, path = router.find_cheapest_route(start, end)
    print(f"Cheapest route from {start} to {end}:")
    print(f"Path: {' -> '.join(path)}")
    print(f"Total Fee: ₹{cost}\n")

    # Test 2: Find the cheapest route from HDFC to ICICI
    start, end = "HDFC", "ICICI"
    cost, path = router.find_cheapest_route(start, end)
    print(f"Cheapest route from {start} to {end}:")
    print(f"Path: {' -> '.join(path)}")
    print(f"Total Fee: ₹{cost}\n")