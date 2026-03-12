# Intelligent Payment Routing & Settlement Engine

A high-performance backend engine designed to validate, prioritize, and route financial transactions through a multi-node banking network. This project demonstrates the practical application of advanced Data Structures and Algorithms (DSA) in a mission-critical financial context.

## 🚀 Key Features & DSA Implementation

This engine is built on four core algorithmic pillars designed for speed, scalability, and security:

* **Optimal Routing (Graphs & Dijkstra's Algorithm):**
    Models the banking network as a weighted graph where nodes represent banks and edges represent transaction fees. It implements **Dijkstra’s Algorithm** to dynamically calculate the most cost-effective path for settlement in $O(V \log V + E)$ time.
* **Instant Validation (Trie / Prefix Tree):**
    Utilizes a custom **Trie** implementation to validate VPA (UPI ID) handles and routing suffixes. This ensures $O(m)$ lookup time, preventing invalid requests from consuming downstream system resources.
* **System Security (Sliding Window Rate Limiter):**
    Protects the engine against high-frequency API abuse. It uses a **Hash Map** combined with a **Deque** to implement a Sliding Window counter, accurately tracking and limiting requests per user.
* **Transaction Prioritization (Priority Queue / Max-Heap):**
    Ensures that mission-critical settlements and premium merchant transactions are processed first during high-load periods by using a **Max-Heap** based priority queue.

## 🛠️ Tech Stack

* **Backend:** Python 3.13, FastAPI (Asynchronous API Framework)
* **Server:** Uvicorn (ASGI Server)
* **Frontend:** HTML5, CSS3, Vanilla JavaScript (Fetch API)
* **Core Logic:** Pure Python implementations of Graph, Trie, Heap, and Deque structures.

## 📂 Project Structure

```text
payment-engine/
├── core/
│   ├── graph/       # Dijkstra's routing logic
│   ├── trie/        # VPA validation logic
│   ├── queue/       # Priority queue for transactions
│   └── security/    # Sliding window rate limiter
├── api/             # FastAPI route definitions
├── frontend/        # Web interface (HTML/JS)
└── main.py          # Application entry point & service integration


<img width="1440" height="900" alt="Screenshot 2026-03-12 at 14 32 01" src="https://github.com/user-attachments/assets/a4bcd80a-7e19-49d8-8eb6-de3390f840c6" />

<img width="1440" height="900" alt="Screenshot 2026-03-12 at 14 32 10" src="https://github.com/user-attachments/assets/b2bbbb81-6116-49c9-9ff7-f34bc4b0f1f1" />
