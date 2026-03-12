from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # <-- This is the missing piece!
from pydantic import BaseModel
import uvicorn

# Import our custom data structures
from core.trie.vpa_trie import VPATrie
from core.security.rate_limiter import SlidingWindowRateLimiter
from core.graph.router import PaymentRouter
from core.queue.transaction_queue import TransactionQueue

app = FastAPI(title="Intelligent Payment Routing Engine")

# CORS Middleware to allow web browser connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ... (The rest of your code below stays exactly the same) ...

# --- 1. Initialize Core Systems in Memory ---
trie = VPATrie()
for suffix in ["@okicici", "@sbi", "@hdfcbank", "@ybl"]:
    trie.insert_valid_suffix(suffix)

rate_limiter = SlidingWindowRateLimiter(window_size_seconds=10, max_requests=3)

router = PaymentRouter()
router.add_bank_connection("HDFC", "UPI_SWITCH", 1.5)
router.add_bank_connection("HDFC", "AXIS", 2.0)
router.add_bank_connection("UPI_SWITCH", "SBI", 1.0)
router.add_bank_connection("AXIS", "SBI", 3.0)
router.add_bank_connection("SBI", "ICICI", 1.2)
router.add_bank_connection("UPI_SWITCH", "ICICI", 2.5)

tx_queue = TransactionQueue()

# --- 2. Define the Request Payload ---
class PaymentRequest(BaseModel):
    user_id: str
    receiver_vpa: str
    amount: float
    sender_bank: str
    receiver_bank: str
    priority: int = 1 

# --- 3. The Core API Endpoint ---
@app.post("/process-payment")
async def process_payment(payment: PaymentRequest):
    
    # Step 1: Security - Check Rate Limiter (O(1) amortized)
    if not rate_limiter.is_allowed(payment.user_id):
        raise HTTPException(status_code=429, detail="Too Many Requests. Slow down.")

    # Step 2: Validation - Check VPA via Trie (O(m))
    if not trie.validate_vpa(payment.receiver_vpa):
        raise HTTPException(status_code=400, detail="Invalid UPI ID routing suffix.")

    # Step 3: Ingestion - Push to Priority Queue (O(log n))
    tx_data = payment.dict()
    tx_queue.add_transaction(tx_data, payment.priority)

    # Step 4: Processing - Pop highest priority from Heap (O(log n))
    current_tx = tx_queue.process_next()

    # Step 5: Routing - Find cheapest path via Dijkstra's (O(V log V + E))
    cost, path = router.find_cheapest_route(current_tx["sender_bank"], current_tx["receiver_bank"])
    
    if cost == float('inf'):
        raise HTTPException(status_code=503, detail="No routing path available.")

    # Step 6: Settlement
    return {
        "status": "SUCCESS",
        "routing_info": {
            "optimal_path": " -> ".join(path),
            "network_fee": f"₹{cost}"
        },
        "transaction_details": current_tx
    }

if __name__ == "__main__":
    # Runs the server on localhost port 8000
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)