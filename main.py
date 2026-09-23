
import json
import math
import sys
from pathlib import Path


def load_data(file_path):
    """
    Read and parse the JSON input file.
    """

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data


def validate_data(data):
    """
    Validate the main input structure and required fields.
    """

    required_keys = {"warehouses", "agents", "packages"}

    missing_keys = required_keys - data.keys()

    if missing_keys:
        raise ValueError(
            f"Missing required keys: {sorted(missing_keys)}"
        )

    if not isinstance(data["warehouses"], dict):
        raise ValueError("Warehouses must be a dictionary.")

    if not isinstance(data["agents"], dict):
        raise ValueError("Agents must be a dictionary.")

    if not isinstance(data["packages"], list):
        raise ValueError("Packages must be a list.")

    for warehouse_id, location in data["warehouses"].items():
        if not is_valid_location(location):
            raise ValueError(
                f"Invalid location for warehouse: {warehouse_id}"
            )

    for agent_id, location in data["agents"].items():
        if not is_valid_location(location):
            raise ValueError(
                f"Invalid location for agent: {agent_id}"
            )

    for package in data["packages"]:
        required_package_keys = {
            "id",
            "warehouse",
            "destination"
        }

        if not required_package_keys.issubset(package):
            raise ValueError(
                f"Package is missing required fields: {package}"
            )

        warehouse_id = package["warehouse"]

        if warehouse_id not in data["warehouses"]:
            raise ValueError(
                f"Unknown warehouse: {warehouse_id}"
            )

        if not is_valid_location(package["destination"]):
            raise ValueError(
                f"Invalid destination for package: {package['id']}"
            )


def is_valid_location(location):
    
    # Check whether a location contains two numeric coordinates.
    

    if not isinstance(location, (list, tuple)):
        return False

    if len(location) != 2:
        return False

    return all(
        isinstance(value, (int, float)) and not isinstance(value, bool)
        for value in location
    )


def squared_distance(point_a, point_b):
    """
    Return squared Euclidean distance.

    We do not calculate square root here because it is unnecessary
    when only comparing distances.
    """

    delta_x = point_a[0] - point_b[0]
    delta_y = point_a[1] - point_b[1]

    return delta_x * delta_x + delta_y * delta_y


def euclidean_distance(point_a, point_b):
    """Return the actual Euclidean distance."""
    dx = point_a[0] - point_b[0]
    dy = point_a[1] - point_b[1]
    return math.hypot(dx,dy)
   
    


def assign_packages(warehouses, agents, packages):
    """
    Assign each package to the nearest agent.

    Distance is measured from the agent's original location
    to the package's warehouse.

    Returns:
        Dictionary containing agent IDs and their assigned packages.
    """

    assignments = {
        agent_id: []
        for agent_id in agents
    }

    for package in packages:
        package_id = package["id"]
        warehouse_id = package["warehouse"]

        warehouse_location = warehouses[warehouse_id]

        nearest_agent_id = None
        nearest_distance = float("inf")

        for agent_id, agent_location in agents.items():

            current_distance = squared_distance(
                agent_location,
                warehouse_location
            )

            if (
                current_distance < nearest_distance
                or (
                    current_distance == nearest_distance
                    and (
                        nearest_agent_id is None
                        or agent_id < nearest_agent_id
                    )
                )
            ):
                nearest_distance = current_distance
                nearest_agent_id = agent_id

        assignments[nearest_agent_id].append(package)

    return assignments


def simulate_deliveries(warehouses, agents, assignments):
    """
    Simulate package pickup and delivery.

    Each agent follows this route for every assigned package:

        Current location -> Warehouse -> Destination

    The agent's current location is updated after each delivery.
    """

    report = {}

    for agent_id, agent_location in agents.items():

        current_location = agent_location
        total_distance = 0.0
        packages_delivered = 0
        delivered_package_ids = [] # Store IDs of packages delivered by this agent

        assigned_packages = assignments[agent_id]
        
        # for each package which is assigend to agent
        for package in assigned_packages:

            warehouse_location = warehouses[
                package["warehouse"]
            ]

            destination = package["destination"]
           
            # from  agent currect location to warehouse
            distance_to_warehouse = euclidean_distance(
                current_location,
                warehouse_location
            )
             
            # from warehouse to customer destination
            distance_to_destination = euclidean_distance(
                warehouse_location,
                destination
            )

            total_distance += (
                distance_to_warehouse
                + distance_to_destination
            )

            current_location = destination
            packages_delivered += 1
            delivered_package_ids.append(package["id"]) # append the current package id


        if packages_delivered > 0:
            efficiency = total_distance / packages_delivered
        else:
            efficiency = 0.0

        report[agent_id] = {
            "packages_delivered": packages_delivered,
            "delivered_package_ids": delivered_package_ids,
            "total_distance": round(total_distance, 2),
            "efficiency": round(efficiency, 2)
        }

    return report


def find_best_agent(report):
    """
    Find the agent with the lowest average distance per package.

    Agents with zero delivered packages are excluded.
    """

    eligible_agents = [
        agent_id
        for agent_id, details in report.items()
        if details["packages_delivered"] > 0
    ]

    if not eligible_agents:
        return None

    return min(
        eligible_agents,
        key=lambda agent_id: (
            report[agent_id]["efficiency"],
            agent_id
        )
    )


def build_final_report(report):
    
    # Add the best agent to the report.
    

    final_report = dict(report)

    final_report["best_agent"] = find_best_agent(report)

    return final_report


def save_report(report, output_path):

    # Save the final report as formatted JSON.
    

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)


def main():
    # Main execution flow.
    

    if len(sys.argv) > 1:
        input_path = Path(sys.argv[1])
    else:
        input_path = Path("data.json")

    output_path = Path("report.json")

    try:
        data = load_data(input_path)
        
        validate_data(data)
        # print(data)

        warehouses = data["warehouses"]
        agents = data["agents"]
        packages = data["packages"]

        assignments = assign_packages(
            warehouses,
            agents,
            packages
        )
        # print(assignments)

        report = simulate_deliveries(
            warehouses,
            agents,
            assignments
        )

        final_report = build_final_report(report)

        delivered_count = sum(
            details["packages_delivered"]
            for details in report.values()
        )

        if delivered_count != len(packages):
            raise RuntimeError(
                "The number of delivered packages does not "
                "match the input package count."
            )

        save_report(final_report, output_path)

        print("Delivery simulation completed successfully.")
        print(f"Report saved to: {output_path}")
        print(
            f"Total packages delivered: "
            f"{delivered_count}"
        )
        print(
            f"Best agent: "
            f"{final_report['best_agent']}"
        )

    except (FileNotFoundError, json.JSONDecodeError, ValueError) as error:
        print(f"Input error: {error}")
        sys.exit(1)

    except RuntimeError as error:
        print(f"Simulation error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()