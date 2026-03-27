import os

COURSEINFOPATH = "course/courseInfo.txt"

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

def is_valid_code(code):
    if len(code) != 8:
        return False
    if not code[:4].isalpha() or not code[4:].isdigit():
        return False
    return True

def course_exists(code):
    lines = read_file_lines(COURSEINFOPATH)
    for line in lines:
        parts = line.split("|")
        if len(parts) >= 2 and parts[0] == code:
            return True
    return False

def create_course():
    print("\n--- Create Course ---")
    while True:
        name = input("Enter Course Name (0 to exit): ").strip()
        if name == '0':
            return
        if not name:
            print("Course name cannot be empty.")
            continue
        break
        
    while True:
        code = input("Enter Course Code (e.g. FHCT1024) (0 to exit): ").strip().upper()
        if code == '0':
            return
        if not is_valid_code(code):
            print("Invalid format. Course code must be 4 letters followed by 4 digits.")
            continue
        if course_exists(code):
            print(f"Course with code {code} already exists.")
            continue
        break
    
    append_line(COURSEINFOPATH, f"{code}|{name}")
    print("Course created successfully.")

def read_courses():
    print("\n--- Course List ---")
    lines = read_file_lines(COURSEINFOPATH)
    if not lines:
        print("No courses available.")
        return
    for line in lines:
        parts = line.split("|")
        if len(parts) >= 2:
            print(f"Code: {parts[0]} - Name: {parts[1]}")

def update_course():
    print("\n--- Update Course ---")
    while True:
        code = input("Enter Course Code to update (0 to exit): ").strip().upper()
        if code == '0':
            return
        if not course_exists(code):
            print(f"Course {code} not found.")
            continue
        break
    
    while True:
        new_name = input("Enter new Course Name (0 to exit): ").strip()
        if new_name == '0':
            return
        if not new_name:
            print("Course name cannot be empty.")
            continue
        break
    
    lines = read_file_lines(COURSEINFOPATH)
    new_lines = []
    for line in lines:
        parts = line.split("|")
        if len(parts) >= 2:
            if parts[0] == code:
                new_lines.append(f"{code}|{new_name}")
            else:
                new_lines.append(line)
    
    write_file_lines(COURSEINFOPATH, new_lines)
    print("Course updated successfully.")

def delete_course():
    print("\n--- Delete Course ---")
    while True:
        code = input("Enter Course Code to delete (0 to exit): ").strip().upper()
        if code == '0':
            return
        if not course_exists(code):
            print(f"Course {code} not found.")
            continue
        break
    
    lines = read_file_lines(COURSEINFOPATH)
    new_lines = [line for line in lines if not line.startswith(code + "|")]
    write_file_lines(COURSEINFOPATH, new_lines)
    
    # Delete associated question file
    q_file = f"course/{code}.txt"
    if os.path.exists(q_file):
        os.remove(q_file)
        
    print("Course deleted successfully.")

def menu():
    while True:
        read_courses()
        print("\n--- Course Maintenance ---")
        print("1. Create Course")
        print("2. Update Course")
        print("3. Delete Course")
        print("0. Back to Main Menu")
        choice = input("Select an option: ").strip()
        
        if choice == '1':
            create_course()
        elif choice == '2':
            update_course()
        elif choice == '3':
            delete_course()
        elif choice == '0':
            break
        else:
            print("Invalid option. Please enter a number between 0 and 4.")
