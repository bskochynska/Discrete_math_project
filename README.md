Optimal Delivery Routing (TSP Variant with Weight Constraints)
📘 Project Overview

This project solves a constrained version of the Travelling Salesman Problem (TSP) applied to a real-world logistics scenario.

A delivery truck must transport packages from a warehouse to several clients. Each order has a delivery location and a package weight. The truck has a maximum load capacity, so the goal is to determine:

Which orders can be delivered together without exceeding capacity,

What is the optimal route that visits all selected clients exactly once and returns to the warehouse,

How to minimize the total travel distance.

This task combines graph processing, optimization, and TSP algorithms.

🧩 Problem Definition
Input

You are given:

A connected undirected weighted graph, where each edge has a distance (cost).

A list of delivery orders, each containing:

client_id — destination (graph vertex),

weight — package weight.

A truck capacity limit (maximum weight).

A starting node — the warehouse (typically vertex 1).

Goal

Find the optimal delivery route that:

starts at the warehouse,

visits all selected clients exactly once,

respects the total weight limit,

returns to the warehouse,

and has the minimal possible distance.

If some orders cannot fit in a single trip, the algorithm must choose the largest possible feasible subset.

🛠 Features
✔ Graph Input

Reads a graph from a file where each line is:

u v w


u, v — connected vertices,

w — distance (edge weight).

✔ Order Input

Reads delivery requests from a file, e.g.:

3 12
5 20
2 7


Meaning:

deliver 12 kg to vertex 3,

deliver 20 kg to 5,

deliver 7 kg to 2.

✔ Order Selection

Determine which orders can fit within the truck’s load capacity.

Select the maximum feasible subset of clients.

Optional: apply priority rules if required.

✔ Route Optimization

For the selected clients:

Use the Exact TSP algorithm (Held–Karp) for small sets,

Or use a Greedy TSP heuristic (Nearest Neighbor) for larger inputs.

Return the route and its total distance.

✔ Error Handling

If nodes are unreachable, show a warning.

If no order fits within the capacity, return a clear message.

📂 Recommended Structure
project/
│
├─ src/
│   ├─ graph_reader.py
│   ├─ order_reader.py
│   ├─ order_selector.py
│   ├─ tsp_exact.py
│   ├─ tsp_greedy.py
│   └─ delivery_solver.py
│
├─ data/
│   ├─ graph.txt
│   ├─ orders.txt
│
├─ tests/
│   ├─ test_orders.py
│   ├─ test_selection.py
│   ├─ test_route_exact.py
│   ├─ test_route_greedy.py
│
└─ README.md

▶ Usage
1️⃣ Install dependencies
pip install -r requirements.txt

2️⃣ Run delivery solver
python src/delivery_solver.py --graph data/graph.txt --orders data/orders.txt --capacity 300

3️⃣ Example Output
Selected orders: [2, 3, 5]
Total weight: 39 / 50
Optimal route: 1 → 3 → 5 → 2 → 1
Distance: 41

📊 Expected Results

Your solution should:

correctly parse graph and order files,

select the maximal valid subset of orders,

compute an optimal or near-optimal delivery route,

compare exact and greedy algorithms (if implemented),

handle errors such as disconnected nodes or exceeding capacity.

📚 References

Held–Karp Dynamic Programming Algorithm for TSP

Nearest Neighbor Heuristic

Weighted Graph Representation

Knapsack-like order selection
