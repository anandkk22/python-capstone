import os
import time
import csv;

EMPLOYEE_CSV_FILE = "employee_details.csv"
view_heading = ""

def load_csvFile(file_name=EMPLOYEE_CSV_FILE):
    try:
        with open(file_name, mode="r", newline="", encoding="utf-8") as file:            
            data = list(csv.DictReader(file))
            numeric_fields = {"ID", "Experience", "Salary"}
            for row in data:
                for field in numeric_fields:
                    if row.get(field):
                        row[field] = int(row[field])
            return data
    except FileNotFoundError:
        return [];

def clear_screen():
    time.sleep(0.5)
    os.system("clear")

def is_file_open(filename):
    try:
        with open(filename, "a"):
            return False
    except PermissionError:
        return True

def view_emp_details(data, view_heading="Employee Details", is_export=False):
    clear_screen()
    print(f"\n\n{view_heading}\n")
    columns = ("ID", "Name", "Department", "Location", "Experience", "Salary")
    column_widths = {
    "ID": 10,
    "Name": 25,
    "Department": 20,
    "Location": 25,
    "Experience": 15,
    "Salary": 15
    }
    width = 25
    print("\t" + "_" * 140 + "\n")
    print("\t" + "".join(f"{column:<{column_widths.get(column, width)}}" for column in columns))
    print("\t" + "_" * 140 + "\n")
    if not data:
        print("\tNo records found\n")
        return
    for emp in data:
        print("\t" + "".join(f"{str(emp.get(column, '')):<{column_widths.get(column, width)}}" for column in columns) + "\n")
    if is_export:
        export_choice = input("\t\t\nDo you want to export to .csv file? (y/n): ").lower()
        print("\n")
        if export_choice == "y":
            exportData(data)
        elif export_choice == "n":
            return
        else:
            print("\tInvalid choice. Please enter 'y' or 'n'.\n")
            return
    data.sort(key=lambda x: int(x["ID"])) if data else []

def search(data):
    emp_id = input("Enter Employee ID: ")
    if emp_id == "" or not emp_id.isdigit():
        clear_screen()
        print(f"\n\n{view_heading}\n")
        print("Invalid Employee ID. Please enter a valid numeric ID.")
        return
    found = [e for e in data if e["ID"] == int(emp_id)]
    if found:
        view_emp_details(found, view_heading=f"Employee Details for ID {emp_id}", is_export=True)
    else:
        clear_screen()
        print(f"\n\n{view_heading}\n")
        print(f"\tNo employee found with ID {emp_id}\n")
        print("\t" + "_" * 140 + "\n")

def update(data):
    view_emp_details(data, view_heading="Update Employee Details")
    emp_id = input("\nEnter Employee ID: ")
    if emp_id == "" or not emp_id.isdigit():
            clear_screen()
            print(f"\n\n{view_heading}\n")
            print("\t\tInvalid Employee ID. Please enter a valid numeric ID.")
            return
    if not any(obj["ID"] == int(emp_id) for obj in data):
        clear_screen()
        print(f"\n\n{view_heading}\n")
        print(f"Employee with ID {emp_id} not found.")
        return
    index = -1
    for i, obj in enumerate(data):
        if obj["ID"] == int(emp_id):
            index = i
            break
    new_emp_id = input("Employee ID: ").strip()
    name = input("Name: ").strip()
    department = input("Department: ").strip()
    location = input("Location: ").strip()
    experience = input("Experience: ").strip()
    salary = input("Salary: ").strip()

    if not name or not department or not location:
        print("Name, department, and location cannot be empty.")
        return
    if any(not value.isdigit() or int(value) <= 0 for value in (new_emp_id, experience, salary)):
        print("Employee ID, experience, and salary must be positive numbers.")
        return

    employee = {
        "ID": int(new_emp_id),
        "Name": name.lower(),
        "Department": department.lower(),
        "Location": location.lower(),
        "Experience": int(experience),
        "Salary": int(salary),
    }
    if index != -1:
        data[index] = employee
        save_data(data)
        clear_screen()
        print(f"\n\n{view_heading}\n")
        print(f"\tEmployee with ID {emp_id} updated successfully.")


def deleteEmp(data):
    emp_id = input("Enter Employee ID: ")
    if emp_id == "" or not emp_id.isdigit():
        clear_screen()
        print(f"\n\n{view_heading}\n")
        print("Invalid Employee ID. Please enter a valid numeric ID.")
        return
    if not any(obj["ID"] == int(emp_id) for obj in data):
        clear_screen()
        print(f"\n\n{view_heading}\n")
        print(f"Employee with ID {emp_id} not found.")
        return
    index = next((i for i, e in enumerate(data) if e["ID"] == int(emp_id)), None)
    if index is not None:
        clear_screen()
        del data[index]
        save_data(data)
        print(f"\nEmployee with ID {emp_id} deleted successfully.")

def filterEmp(data):
    print("Filter by:\n\n1 -  Name, 2 - Department, 3 - Location, 4 - Experience, 5 - Salary")
    filter_by = input()
    match filter_by:
        case "1":
            filter_by = "Name"
        case "2":
            filter_by = "Department"
        case "3":
            filter_by = "Location"
        case "4":
            filter_by = "Experience"
        case "5":
            filter_by = "Salary"
        case _:
            print("Invalid filter option.")
            return

    print(f"Filter by: {filter_by}\n\n")
    filter_value = input(f"Enter {filter_by}: ").lower()
    print("\n")
    if filter_by in ["Experience", "Salary"]:
        filter_value = int(filter_value)
    filtered_data = [emp for emp in data if emp.get(filter_by) == filter_value]
    view_emp_details(filtered_data, view_heading=f"Filtered by {filter_by}: {filter_value}", is_export=True)

def sortData(data):
    print("Sort by:\n1 - ID, 2 - Name, 3 - Department, 4 - Location, 5 - Experience, 6 - Salary")
    sort_by = input()

    match sort_by:
        case "1":
            sort_by = "ID"
        case "2":
            sort_by = "Name"
        case "3":
            sort_by = "Department"
        case "4":
            sort_by = "Location"
        case "5":
            sort_by = "Experience"
        case "6":
            sort_by = "Salary"
        case _:
            print("Invalid sort by option.")
            return

    order_by = input(
        "Sort order (Type 'a' for ascending, 'd' for descending): "
    ).lower()

    if order_by == "a":
        reverse = False
    elif order_by == "d":
        reverse = True
    else:
        print("Invalid sort order option.")
        return

    if sort_by == "Salary":
        try:
            min_salary = float(input("\nEnter minimum salary: "))
            max_salary = float(input("\nEnter maximum salary: "))

            filtered_data = [
                emp for emp in data
                if min_salary <= float(emp["Salary"]) <= max_salary
            ]

            if not filtered_data:
                print("No employees found in the given salary range.")
                return

            filtered_data.sort(
                key=lambda x: float(x["Salary"]),
                reverse=reverse
            )

            view_emp_details(
                filtered_data,
                view_heading=(
                    f"Employees with Salary between {min_salary} and {max_salary} "
                    f"sorted in {'descending' if reverse else 'ascending'} order."
                ),
                is_export=True
            )

        except ValueError:
            print("Please enter valid salary values.")
            return

    else:
        data.sort(
            key=lambda x: str(x.get(sort_by, "")).lower(),
            reverse=reverse
        )

        view_emp_details(
            data,
            view_heading=(
                f"Data sorted by {sort_by} in "
                f"{'descending' if reverse else 'ascending'} order."
            ),
            is_export=True
        )

def generalStat(data, filename="export.csv"):
    total_emp = len(data)
    average_salary = sum(emp["Salary"] for emp in data) / total_emp if total_emp > 0 else 0
    average_experience = sum(emp["Experience"] for emp in data) / total_emp if total_emp > 0 else 0
    unique_dept = list({item["Department"] for item in data})
    average_salary = sum(emp["Salary"] for emp in data) / total_emp if total_emp > 0 else 0
    average_experience = sum(emp["Experience"] for emp in data) / total_emp if total_emp > 0 else 0
    highest_salary = max(emp['Salary'] for emp in data) if data else 0
    lowest_salary = min(emp['Salary'] for emp in data) if data else 0
    
    print(f"\tAverage Salary: {average_salary:.2f}\n")
    print(f"\tAverage Experience: {average_experience:.2f}\n")
    print(f"\tHighest Salary: {highest_salary}\n")
    print(f"\tLowest Salary: {lowest_salary}\n")

    print("\tDepartment-wise employee count\n")
    for item in unique_dept:
        dept_employees = [emp for emp in data if emp["Department"] == item]
        print(f"\t\t{item}: {len(dept_employees)}\n")
    print(f"\tTotal Employees: {total_emp}\n")

    is_export = input("\tDo you want to export the statistics to a CSV file? (y/n): ").lower()
    if is_export == "y":
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Description", "Value"])
            writer.writerow(["Total Employees", total_emp])
            writer.writerow(["Average Salary", f"{average_salary:.2f}"])
            writer.writerow(["Average Experience", f"{average_experience:.2f}"])
            writer.writerow(["Highest Salary", highest_salary])
            writer.writerow(["Lowest Salary", lowest_salary])
            writer.writerow([])
            writer.writerow(["Department", "Employee Count"])
            for dept in unique_dept:
                dept_count = sum(
                    1 for emp in data
                    if emp["Department"] == dept
                )
                writer.writerow([dept, dept_count])

    print(f"\t\t\t\t\nStatistics exported successfully to '{filename}'")

def exportData(data):
    if not data:
        print("No employee data to export.")
        return
    fieldnames = data[0].keys()
    with open("export.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print("Employee data exported successfully to export.csv.")    
    data = data.sort(key=lambda x: int(x["ID"])) if data else []

def quitApp():
    clear_screen()
    print("\n")
    print("Thanks for using the Employee Details Information application\n")
    

def save_data(data, file_name=EMPLOYEE_CSV_FILE):
    with open(file_name, mode="w", newline="", encoding="utf-8") as file:
        fieldnames = data[0].keys() if data else [
            "ID", "Name", "Department", "Location", "Experience", "Salary"
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def add_new_emp(data):
    emp_id = input("Employee ID: ").strip()
    if not emp_id or not emp_id.isdigit() or int(emp_id) < 0:
        print("\nInvalid input. Please provide a valid Employee ID (non-empty, numeric, and greater than or equal to 0).\n")
        return

    name = input("Name: ").strip().lower()
    department = input("Department: ").strip().lower()
    location = input("Location: ").strip().lower()
    experience = input("Experience: ").strip()
    salary = input("Salary: ").strip()

    if (
        not name
        or not department
        or not location
        or not experience.isdigit()
        or int(experience) <= 0
        or not salary.isdigit()
        or int(salary) <= 0
    ):
        print("\nInvalid input. Please provide non-empty values for name, department, and location, and positive numeric values for experience and salary.\n")
        return

    employee = {
        "ID": int(emp_id),
        "Name": name,
        "Department": department,
        "Location": location,
        "Experience": int(experience),
        "Salary": int(salary)
    }

    data.append(employee)
    save_data(data)
    print("\nEmployee added successfully\n")
    view_emp_details(data, view_heading="View All Employees Details", is_export=True)

def getMenu():
    data = load_csvFile()

    while True:
        width = os.get_terminal_size().columns
        print("\n")
        print("=" * width + "\n")
        welcome_message = "-------- Welcome to Employee Details Information --------"
        print("\n\t\t\t\t" + welcome_message.center(100, "-") + "\n")
        print("\t" + "_" * 140 + "\n")
        columns = (
            "\t\t\t\t1 - View All Employees Details",
            "\t\t\t\t2 - Search Employee\n",
            "\t\t\t\t3 - Add New Employee",
            "\t\t\t\t4 - Update Employees Details\n",
            "\t\t\t\t5 - Delete Employee",
            "\t\t\t\t6 - Filter Employee\n",
            "\t\t\t\t7 - Sort Employee",
            "\t\t\t\t8 - General Statistics\n",
            "\t\t\t\t9 - Export Data",
            "\t\t\t\t0 - Exit"
        )
        col_width = max(len(item) for item in columns)
        for i in range(0, len(columns), 2):
            left = columns[i]
            right = columns[i + 1] if i + 1 < len(columns) else ""            
            print(f" {left:<{col_width}} {right:<{col_width}}")
        

        user_choice = input("\nChoose an option: ")
        if user_choice not in [str(i) for i in range(10)]:
            print("\nInvalid option selected. Please select 0 - 9.\n")
            continue
        print("\n")
        match user_choice:
            case "1": 
                selected_option = "View All Employees Details"
            case "2":
                selected_option = "Search Employee"
            case "3":
                selected_option = "Add New Employee"
            case "4":
                selected_option = "Update Employees Details"
            case "5":
                selected_option = "Delete Employee"
            case "6":
                selected_option = "Filter Employee"
            case "7":
                selected_option = "Sort Employee"
            case "8":
                selected_option = "General Statistics"
            case "9":
                selected_option = "Export Data"
            case "0":
                selected_option = "Exit"

        print("You selected option: " + selected_option + "\n\n")

        match user_choice:
            case "1":
                view_emp_details(data, view_heading="View All Employees Details", is_export=True)
            case "2":
                search(data)
            case "3":
                add_new_emp(data) 
            case "4":
                update(data)
            case "5":
                deleteEmp(data)
            case "6":
                filterEmp(data)
            case "7":
                sortData(data)
            case "8":
                generalStat(data)
            case "9":
                exportData(data)
            case "0":
                quitApp()
                break
            case _:
                print("Invalid option selected. Please select 0 - 9.\n")                


if __name__ == "__main__":
    getMenu()    
