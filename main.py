# main.py

import json
from assignment import assign_packages
from csv_exporter import export_package_log


def main():

    # Here we read the input json file. you can change the path to test different input files.
    with open(r'C:\Users\Dell\Desktop\projects\Parcel_delivery_simulation\Python Assignment(Delivery System Test Cases)\test_case_5.json', "r") as file:
        data = json.load(file)

    #call the main function to assign packages and get the result and package log
    result, package_log = assign_packages(data)

    # Save output JSON
    with open("output.json", "w") as file:
        json.dump(result, file, indent=4)

    # Save package log CSV
    export_package_log(package_log, filepath="package_log.csv")

    

if __name__ == "__main__":
    main()