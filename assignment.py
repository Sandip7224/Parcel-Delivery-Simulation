# assignment.py

from distance import calculate_distance

#user for load penalty in scoring function
PENALTY = 2

# Main function to assign packages to agents
def assign_packages(data):

    # Extract the agnet, warehouse and packeage data and save as dictionaries
    agents = data["agents"]
    warehouses = data["warehouses"]
    packages = data["packages"]

    # Initialize agent state
    agent_state = {}

    # set the initial state for each agent
    for agent_id, location in agents.items():
        agent_state[agent_id] = {
            "location": location,
            "load": 0,
            "total_distance": 0.0,
            "packages_delivered": 0
        }

    # Package log for CSV export
    package_log = []

    # Process packages in given order
    for pkg_index, pkg in enumerate(packages):

        best_agent_id = None
        best_score = float("inf")

        warehouse_loc = warehouses[pkg["warehouse"]]
        delivery_loc = pkg["destination"]

        # Check all agents distcance to warehouse and delivery location and calculate score based on distance and load, then apply tie-breaking.
        for agent_id, state in agent_state.items():

            dist1 = calculate_distance(state["location"], warehouse_loc)
            dist2 = calculate_distance(warehouse_loc, delivery_loc)

            total_distance = dist1 + dist2
            score = total_distance + (state["load"] * PENALTY)

            # Tie-breaking logic
            if (best_agent_id is None or
                score < best_score or
                (score == best_score and state["load"] < agent_state[best_agent_id]["load"]) or
                (score == best_score and state["load"] == agent_state[best_agent_id]["load"] and agent_id < best_agent_id)):

                best_score = score
                best_agent_id = agent_id

        # Assign package to the best agent with least score
        chosen = agent_state[best_agent_id]

        dist1 = calculate_distance(chosen["location"], warehouse_loc)
        dist2 = calculate_distance(warehouse_loc, delivery_loc)

        trip_distance = dist1 + dist2

        chosen["total_distance"] += trip_distance
        chosen["packages_delivered"] += 1
        chosen["load"] += 1

        # Log this package's details
        package_log.append({
            "package_index": pkg_index + 1,
            "assigned_agent_id": best_agent_id,
            "warehouse_id": pkg["warehouse"],
            "warehouse_x": warehouse_loc[0],
            "warehouse_y": warehouse_loc[1],
            "destination_x": delivery_loc[0],
            "destination_y": delivery_loc[1],
            "dist_agent_to_warehouse": round(dist1, 2),
            "dist_warehouse_to_destination": round(dist2, 2),
            "trip_distance": round(trip_distance, 2)
        })

        # update location
        chosen["location"] = delivery_loc


    # Prepare output
    output = {}
    best_agent = None
    best_efficiency = float("inf")

    for agent_id, state in agent_state.items():

        if state["packages_delivered"] == 0:
            efficiency = 0
        else:
            efficiency = state["total_distance"] / state["packages_delivered"]

        efficiency = round(efficiency, 2)
        total_distance = round(state["total_distance"], 2)

        output[agent_id] = {
            "packages_delivered": state["packages_delivered"],
            "total_distance": total_distance,
            "efficiency": efficiency
        }

        if state["packages_delivered"] > 0 and efficiency < best_efficiency:
            best_efficiency = efficiency
            best_agent = agent_id

    output["best_agent"] = best_agent

    return output, package_log