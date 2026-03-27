import os
import coursemaintenance

SCHEDULEINFOPATH = "schedules/scheduleInfo.txt"

def read_file_lines(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f.readlines()]

def write_file_lines(filepath, lines):
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    with open(filepath, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + "\n")

def append_line(filepath, line):
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write(line + "\n")

def is_valid_date(date_str):
    # simple formatting check YYYY-MM-DD
    parts = date_str.split("-")
    if len(parts) != 3: return False
    return len(parts[0]) == 4 and len(parts[1]) == 2 and len(parts[2]) == 2 and "".join(parts).isdigit()

def add_schedule():
    print("\n--- Add Test Schedule ---")
    
    coursemaintenance.read_courses()
    while True:
        course_code = input("Enter Course Code (0 to exit): ").strip().upper()
        if course_code == '0':
            return
        if not coursemaintenance.course_exists(course_code):
            print("Course does not exist. Please create it first.")
            continue
        break
        
    while True:
        date_str = input("Enter Date (YYYY-MM-DD) (0 to exit): ").strip()
        if date_str == '0':
            return
        if not is_valid_date(date_str):
            print("Invalid date format. Use YYYY-MM-DD.")
            continue
        break
        
    while True:
        time_slot = input("Enter Time Slot (e.g., 09:00-11:00) (0 to exit): ").strip()
        if time_slot == '0':
            return
        if not time_slot:
            print("Time slot cannot be empty.")
            continue
        break
        
    while True:
        capacity = input("Enter Capacity (numeric) (0 to exit): ").strip()
        if capacity == '0':
            return
        if not capacity.isdigit():
            print("Must be numeric.")
            continue
        break
    
    append_line(SCHEDULEINFOPATH, f"{course_code}|{date_str}|{time_slot}|{capacity}")
    print("Schedule added successfully.")

def list_schedules():
    print("\n--- Test Schedules ---")
    lines = read_file_lines(SCHEDULEINFOPATH)
    if not lines:
        print("No schedules found.")
        return
        
    for idx, line in enumerate(lines, 1):
        parts = line.split("|")
        if len(parts) >= 4:
            print(f"{idx}. Course: {parts[0]} | Date: {parts[1]} | Time: {parts[2]} | Capacity: {parts[3]}")

def delete_schedule():
    print("\n--- Delete Test Schedule ---")
    lines = read_file_lines(SCHEDULEINFOPATH)
    if not lines:
        print("No schedules found.")
        return
        
    list_schedules()
    
    while True:
        idx_str = input(f"Enter schedule number to delete (1-{len(lines)}) (0 to exit): ").strip()
        if idx_str == '0':
            return
        try:
            idx = int(idx_str) - 1
            if idx < 0 or idx >= len(lines):
                raise ValueError
            break
        except ValueError:
            print("Invalid schedule number.")
            continue
            
    deleted = lines.pop(idx)
    write_file_lines(SCHEDULEINFOPATH, lines)
    print("Schedule deleted successfully.")

def menu():
    while True:
        print("\n--- Test Date Scheduling ---")
        print("1. Add Test Schedule")
        print("2. List Test Schedules")
        print("3. Delete Test Schedule")
        print("0. Back to Main Menu")
        
        choice = input("Select an option: ").strip()
        if choice == '1':
            add_schedule()
        elif choice == '2':
            list_schedules()
        elif choice == '3':
            delete_schedule()
        elif choice == '0':
            break
        else:
            print("Invalid option.")
