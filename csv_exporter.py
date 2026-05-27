# csv_exporter.py

import csv

def export_package_log(package_log, filepath="package_log.csv"):
    """
    Exports the package log to a CSV file.

    Columns:
    - Package Index
    - Assigned Agent ID
    - Warehouse ID
    - Warehouse Location (x, y)
    - Destination Location (x, y)
    - Distance: Agent → Warehouse
    - Distance: Warehouse → Destination
    - Trip Distance
    """

    fieldnames = [
        "Package Index",
        "Assigned Agent ID",
        "Warehouse ID",
        "Warehouse X",
        "Warehouse Y",
        "Destination X",
        "Destination Y",
        "Distance: Agent to Warehouse",
        "Distance: Warehouse to Destination",
        "Trip Distance"
    ]

    with open(filepath, mode="w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for entry in package_log:
            writer.writerow({
                "Package Index": entry["package_index"],
                "Assigned Agent ID": entry["assigned_agent_id"],
                "Warehouse ID": entry["warehouse_id"],
                "Warehouse X": entry["warehouse_x"],
                "Warehouse Y": entry["warehouse_y"],
                "Destination X": entry["destination_x"],
                "Destination Y": entry["destination_y"],
                "Distance: Agent to Warehouse": entry["dist_agent_to_warehouse"],
                "Distance: Warehouse to Destination": entry["dist_warehouse_to_destination"],
                "Trip Distance": entry["trip_distance"]
            })

    print(f"package_log.csv saved to: {filepath}")
