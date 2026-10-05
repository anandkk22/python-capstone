# Employee Details Information Application

A simple Python-based employee management system for viewing, searching, adding, updating, deleting, filtering, sorting, and exporting employee records stored in a CSV file.

## Project Description

This application helps manage employee records efficiently using a command-line interface. It reads employee data from `employee_details.csv`, displays it in a tabular format, and lets the user perform common operations such as:

- viewing all employees
- searching by employee ID
- adding new employees
- updating details
- deleting records
- filtering by field
- sorting records
- viewing summary statistics
- exporting data to CSV

## Features

- CSV-based data storage
- Employee lookup by ID
- Add new employee records
- Update existing employee information
- Delete employee records
- Filter by name, department, location, experience, or salary
- Sort records in ascending or descending order
- View average salary, average experience, and department-wise counts
- Export current employee data to `export.csv`
- Menu-driven terminal interface

## Project Structure

- `python-capstone.py` - main application script
- `employee_details.csv` - source employee database
- `export.csv` - exported employee data (created when exporting)
- `README.md` - project documentation

## Setup Instructions

1. Open a terminal in the project folder.
2. Ensure Python 3 is installed on your system.
3. Make sure the CSV file exists in the project directory:
   - `employee_details.csv`
4. Run the application:

```bash
python python-capstone.py
```

## Usage Examples

### 1. View all employees
From the main menu, select:

```text
1
```

This displays all employee records in a table.

### 2. Search for an employee
Select:

```text
2
```

Then enter an employee ID such as:

```text
101
```

### 3. Add a new employee
Select:

```text
3
```

Then provide values for:

```text
Employee ID: 105
Name: Alice
Department: HR
Location: Chennai
Experience: 4
Salary: 55000
```

### 4. Update employee details
Select:

```text
4
```

Then enter the employee ID to update and provide the new values.

### 5. Delete an employee
Select:

```text
5
```

Then enter the employee ID to remove.

### 6. Filter employees
Select:

```text
6
```

Choose a filter field and enter the value you want to match.

### 7. Sort employees
Select:

```text
7
```

Choose a field and whether to sort in ascending or descending order.

### 8. View statistics
Select:

```text
8
```

This shows:
- average salary
- average experience
- department-wise employee counts
- total number of employees

### 9. Export employee data
Select:

```text
9
```

This writes the current employee list to:

```text
export.csv
```

### 10. Exit the application
Select:

```text
0
```

## Notes

- The application stores employee data in CSV format for easy editing outside the script.
- It expects the `employee_details.csv` file to follow the same structure as the fields shown in the menu.
- The script uses a terminal-based interface and is intended for local use on a command line.

## Requirements

- Python 3.x
- Standard library modules only (`csv`, `os`, `time`)
