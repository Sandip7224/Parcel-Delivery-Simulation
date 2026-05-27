# Parcel Delivery Simulation

A Python-based simulation system that intelligently assigns delivery packages to agents using a greedy scoring algorithm. The system minimizes total travel distance, balances workload across agents, and identifies the most efficient performer at the end of each run.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
  - [Assignment Algorithm](#assignment-algorithm)
  - [Scoring Formula](#scoring-formula)
  - [Tie-Breaking Logic](#tie-breaking-logic)
  - [Efficiency Metric](#efficiency-metric)
- [Input Format](#input-format)
- [Output](#output)
  - [output.json](#outputjson)
  - [package_log.csv (Added Feature)](#package_logcsv--added-feature)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Running the Simulation](#running-the-simulation)
- [File Descriptions](#file-descriptions)
- [Example](#example)

---

## Project Overview

This project simulates a real-world parcel delivery system where multiple delivery agents operate across a 2D coordinate grid. Packages need to be picked up from warehouses and dropped off at their respective destinations.

The simulation processes packages **one at a time**, in the order they are given, and for each package, it selects the most suitable agent based on how far they'd need to travel and how busy they already are. Once all deliveries are done, the system reports each agent's performance and crowns the most efficient one.

---

## Project Structure

```
PARCEL_DELIVERY_SIMULATION/
│
├── Python Assignment(Delivery System Test Cases)/   # Folder containing input JSON test cases
│
├── assignment.py        # Core assignment engine — greedy algorithm lives here
├── csv_exporter.py      # Handles CSV report generation
├── distance.py          # Euclidean distance utility function
├── main.py              # Entry point — reads input, runs simulation, writes outputs
│
├── output.json          # Generated: per-agent summary results
└── package_log.csv      # Generated: detailed per-package delivery log (added feature)
```

---

## How It Works

### Assignment Algorithm

The simulation uses a **greedy, real-time dispatch strategy**:

1. Packages are processed strictly in the order they appear in the input.
2. For each package, **every available agent is scored**.
3. The agent with the **lowest score** gets assigned that package.
4. The assigned agent's position is then **updated to the delivery destination** — their next assignment starts from there.

This means each decision is made with full knowledge of the current state of all agents, but without looking ahead at future packages. It's fast, practical, and mirrors how many real-world dispatch systems operate.

### Scoring Formula

For each agent evaluated against a package:

```
score = (distance: agent → warehouse) + (distance: warehouse → destination) + (agent's current load × PENALTY)
```

- **Travel distance** is calculated using standard **Euclidean distance** on a 2D grid.
- **PENALTY = 2** — each package an agent is already carrying adds 2 to their score.
  This discourages the system from overloading a single fast agent and promotes balanced distribution.

### Tie-Breaking Logic

When two agents have the same score, the following rules apply in order:

1. **Fewer packages carried** — prefer the less loaded agent
2. **Alphabetical agent ID** — if still tied, pick the agent whose ID comes first alphabetically (ensures deterministic, reproducible results)

### Efficiency Metric

At the end of the simulation, each agent's **efficiency** is calculated as:

```
efficiency = total_distance_traveled / packages_delivered
```

Lower efficiency = better performance (less distance per package). The agent with the lowest efficiency score is declared the **best agent**.

Agents who delivered zero packages are excluded from this ranking.

---

## Input Format

The simulation expects a `.json` file with the following structure:

```json
{
    "agents": {
        "A1": [0, 0],
        "A2": [10, 10]
    },
    "warehouses": {
        "W1": [5, 5],
        "W2": [8, 2]
    },
    "packages": [
        {
            "warehouse": "W1",
            "destination": [3, 7]
        },
        {
            "warehouse": "W2",
            "destination": [12, 1]
        }
    ]
}
```

| Field        | Type             | Description                                           |
|--------------|------------------|-------------------------------------------------------|
| `agents`     | dict             | Agent IDs mapped to their starting `[x, y]` positions |
| `warehouses` | dict             | Warehouse IDs mapped to their `[x, y]` positions      |
| `packages`   | list of objects  | Each package has a warehouse to pick up from and a destination to deliver to |

---

## Output

### output.json

A summary of how each agent performed across the entire simulation run.

```json
{
    "A1": {
        "packages_delivered": 3,
        "total_distance": 24.5,
        "efficiency": 8.17
    },
    "A2": {
        "packages_delivered": 2,
        "total_distance": 14.2,
        "efficiency": 7.1
    },
    "best_agent": "A2"
}
```

| Field                | Description                                        |
|----------------------|----------------------------------------------------|
| `packages_delivered` | Total number of packages this agent handled        |
| `total_distance`     | Total Euclidean distance traveled (rounded to 2dp) |
| `efficiency`         | Average distance per package (lower is better)     |
| `best_agent`         | The agent ID with the lowest efficiency score      |

---

### package_log.csv — Added Feature

> **This CSV export is an added feature built on top of the core simulation.**
> While the base assignment engine outputs a JSON summary, this feature generates a detailed,
> human-readable log of every single package delivery — making it easy to audit, debug,
> or analyze individual trips in a spreadsheet.

Each row in the CSV represents one package delivery and includes the full trip breakdown:

| Column                              | Description                                              |
|-------------------------------------|----------------------------------------------------------|
| `Package Index`                     | Sequential number (1-based) of the package in the run    |
| `Assigned Agent`                    | Which agent was selected for this delivery               |
| `Warehouse ID`                      | The warehouse the agent had to visit for pickup          |
| `Warehouse Location (x, y)`         | Coordinates of the pickup warehouse                      |
| `Destination Location (x, y)`       | Coordinates of the drop-off point                       |
| `Distance: Agent to Warehouse`      | How far the agent traveled to reach the warehouse        |
| `Distance: Warehouse to Destination`| The warehouse-to-delivery leg of the trip               |
| `Trip Distance`                     | Total distance for this delivery (both legs combined)    |

This file is automatically generated every time the simulation runs — no extra steps needed.

---

## Getting Started

### Prerequisites

- Python 3.7 or higher
- No third-party libraries required — uses only Python's standard library (`math`, `csv`, `json`)

### Running the Simulation

**Step 1** — Clone or download the project files into a folder.

**Step 2** — Open `main.py` and update the `input_path` variable to point to your test case JSON file:

```python
input_path = r'path\to\your\test_case.json'
```

**Step 3** — Run the simulation from your terminal:

```bash
python main.py
```

**Step 4** — Check the output files generated in the same directory:

```
output.json       → agent performance summary
package_log.csv   → per-package delivery details
```

---

## File Descriptions

| File               | Role                                                                                      |
|--------------------|-------------------------------------------------------------------------------------------|
| `main.py`          | Entry point. Loads input JSON, runs the simulation, and saves both output files.          |
| `assignment.py`    | Core logic. Implements the greedy assignment algorithm and builds the per-package log.    |
| `distance.py`      | Utility. Contains the Euclidean distance function used throughout the assignment engine.  |
| `csv_exporter.py`  | Export module. Takes the package log from the assignment engine and writes it to CSV.     |

---

## Example

Given a test case with 2 agents and 3 packages:

```
Agent A1 starts at (0, 0)
Agent A2 starts at (10, 10)

Package 1 → pickup from W1 (5,5), deliver to (3,7)
Package 2 → pickup from W2 (8,2), deliver to (12,1)
Package 3 → pickup from W1 (5,5), deliver to (1,1)
```

The algorithm will:
1. Score both agents for Package 1 → assign to whoever has the lower travel cost
2. Update the winning agent's position to `(3,7)`
3. Repeat for Package 2 and 3 with updated positions and load penalties

Final output will show each agent's total distance, how many packages they delivered, and who came out most efficient.

---

## Notes

- All coordinates are on a flat 2D Euclidean plane — no real-world map data is used.
- The simulation is **deterministic** — same input always produces the same output.
- The `PENALTY` constant in `assignment.py` can be adjusted to control how aggressively the system balances load across agents.
