# Mystry Delivery System

A Python-based delivery simulation system developed for a fictional delivery company called
**FastBox** to assign packages to the nearest delivery agent, simulate package deliveries, calculate travel distances, and produce a report showing which packages were delivered, total distance traveled by each agent, and the most efficient agent.

The system uses **Euclidean distance** to assign packages to agents based on the distance between the agent's starting location and the package's warehouse.


## Project Overview

FastBox operates a delivery network with multiple warehouses, delivery agents, and packages.

The objective of this project is to build a system that can:

- Read delivery data from a JSON file.
- Assign each package to the nearest delivery agent.
- Simulate the delivery journey.
- Calculate the total distance traveled by each agent.
- Calculate agent efficiency.
- Identify the best-performing agent.
- Generate a structured JSON report.

This project demonstrates practical applications of Python programming, data validation, distance calculation, algorithmic assignment, and simulation.


## Features

### 1. JSON Data Processing

- Reads input data from a JSON file.
- Supports custom input files through command-line arguments.
- Validates the structure of the input data.
- Checks warehouse references and location coordinates.

### 2. Nearest Agent Assignment

Each package is assigned to the nearest agent based on the Euclidean distance between:
- Agent's starting location → Package warehouse

If two agents have the same distance, a deterministic tie-breaking rule is used based on the agent ID.

### 3. Delivery Simulation

The system simulates the delivery journey for every assigned package:\
 Agent's Current Location -> Package Warehouse -> Destination


After delivering a package, the agent's current location is updated to the destination of that package.

### 4. Route Tracking

The system records the route for every package, including:

- Package ID
- Agent ID
- Starting location
- Warehouse ID
- Warehouse location
- Destination
- Distance from agent to warehouse
- Distance from warehouse to destination
- Total distance for the package

### 5. Performance Report

The generated report contains:
- Number of packages delivered by each agent
- Ids of delivered packages by each agent
- Total distance traveled
- Average distance per delivered package
- Best-performing agent based on delivery efficiency

### 6. Data Validation

The system validates:

- Required JSON keys
- Data types
- Agent locations
- Warehouse locations
- Package destinations
- Warehouse references
- Total number of delivered packages

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| JSON | Input and output data format |
| math | Euclidean distance calculations |
| sys | Command-line argument handling |
| pathlib | File path management |

## Input Data Format

The system accepts JSON data containing warehouses, agents, and packages.

### Input Components
#### Warehouses

Each warehouse contains a unique ID and its two-dimensional coordinates.\
"W1": [0, 0]

#### Agents

Each agent contains:
- A unique agent ID
- An initial location

```json
{
    "id": "A1",
    "location": [5, 5]
}
```

#### Packages
Each package contains:

- A unique package ID
- The warehouse from which it is collected
- Its destination coordinates

```json
{
    "id": "P1",
    "warehouse": "W1",
    "destination": [30, 40]
}
```


## Output
The system generates a JSON report containing delivery performance and route information.

##  Performance Metrics

### Packages Delivered

The total number of packages successfully delivered by an agent.

### Total Distance

The sum of all distances traveled by the agent while collecting and delivering packages.\
Total Distance = Sum of all package delivery distances


### Efficiency

The average distance traveled per delivered package.\
Efficiency = Total Distance / Number of Packages Delivered 

A lower efficiency value indicates a lower average travel distance per delivered package. The report uses this metric when identifying the best-performing agent.

### Validation Check

The system verifies that:\
Total Delivered Packages = Total Input Packages 

This helps ensure that no package is lost during assignment or simulation.


## Assumptions

The simulation follows these assumptions:

1. All agents begin from their initial locations.
2. Each package is assigned to exactly one agent.
3. Assignment is based on the distance from the agent's original location to the package warehouse.
4. Agents collect and deliver their assigned packages sequentially.
5. After delivery, an agent's current location becomes the package destination.
6. Euclidean distance is used.
7. If two agents have equal distances, the agent with the smaller ID is selected.
8. Package delivery order follows the order in which packages are assigned.
9. Agents with zero packages have null efficiency and are excluded from best-agent selection.
10. Travel time, traffic, and delivery delays are not included.

## Possible Future Improvements

The current project focuses on the core delivery assignment and simulation requirements.

Possible future improvements include:

- Interactive route visualization using a map.
- Real-world road distance and travel time.
- Delivery time estimation.
- Traffic-aware route planning.
- Package priority handling.
- Route optimization.
- CSV export for performance reports.
- A web dashboard for delivery monitoring.



##  Learning Outcomes

Through this project, I practiced:

- Reading and processing JSON data.
- Designing reusable Python functions.
- Validating structured input.
- Implementing Euclidean distance calculations.
- Applying nearest-agent assignment logic.
- Simulating sequential delivery operations.
- Generating structured reports.
- Handling errors and command-line inputs.

---
