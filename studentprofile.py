import os
import coursemaintenance

STUDENTINFOPATH = "students/studentInfo.txt"

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

def student_exists(student_id):
    lines = read_file_lines(STUDENTINFOPATH)
    for line in lines:
        parts = line.split("|")
        if len(parts) >= 1 and parts[0] == student_id:
            return True
    return False

def is_valid_student_id(std_id):
    return std_id.isdigit() and len(std_id) >= 5

def create_student():
    print("\n--- Create Student Profile ---")
    while True:
        std_id = input("Enter Student ID (numeric) (0 to exit): ").strip()
        if std_id == '0':
            return
        if not is_valid_student_id(std_id):
            print("Student ID must be numeric (min 5 digits).")
            continue
        if student_exists(std_id):
            print(f"Student with ID {std_id} already exists.")
            continue
        break
        
    while True:
        name = input("Enter Student Name (0 to exit): ").strip()
        if name == '0':
            return
        if not name:
            print("Name cannot be empty.")
            continue
        break
    
    courses = []
    print("Enter Course Codes the student is enrolled in (leave blank or type 0 to finish):")
    while True:
        code = input("Course Code: ").strip().upper()
        if code == '0' or not code:
            break
        if coursemaintenance.course_exists(code):
            if code not in courses:
                courses.append(code)
                print(f"Course {code} added to student.")
            else:
                print("Course already added.")
        else:
            print(f"Course {code} does not exist. Please create it first in Course Maintenance.")
            
    course_str = ",".join(courses)
    append_line(STUDENTINFOPATH, f"{std_id}|{name}|{course_str}")
    print("Student profile created successfully.")

def read_students():
    print("\n--- Student List ---")
    lines = read_file_lines(STUDENTINFOPATH)
    if not lines:
        print("No students found.")
        return
        
    for line in lines:
        parts = line.split("|")
        if len(parts) >= 2:
            std_id = parts[0]
            name = parts[1]
            courses = parts[2] if len(parts) > 2 else "None"
            print(f"ID: {std_id} | Name: {name} | Enrolled in: {courses}")

def update_student():
    print("\n--- Update Student Profile ---")
    while True:
        std_id = input("Enter Student ID to update (0 to exit): ").strip()
        if std_id == '0':
            return
        if not student_exists(std_id):
            print("Student not found.")
            continue
        break
        
    lines = read_file_lines(STUDENTINFOPATH)
    new_lines = []
    for line in lines:
        parts = line.split("|")
        if len(parts) >= 2 and parts[0] == std_id:
            current_name = parts[1]
            current_courses = parts[2] if len(parts) > 2 else ""
            print(f"Current Name: {current_name}")
            new_name = input("Enter new Name (leave blank to keep current, 0 to exit): ").strip()
            if new_name == '0': return
            name = new_name if new_name else current_name
            
            print(f"Current Courses: {current_courses}")
            
            while True:
                update_courses = input("Do you want to update courses? (Y/N) (0 to exit): ").strip().upper()
                if update_courses == '0': return
                if update_courses in ['Y', 'N']:
                    break
                print("Please enter Y or N.")
            
            courses = []
            if update_courses == 'Y':
                print("Enter new set of Course Codes (leave blank or type 0 to finish):")
                while True:
                    code = input("Course Code: ").strip().upper()
                    if code == '0' or not code:
                        break
                    if coursemaintenance.course_exists(code):
                        if code not in courses:
                            courses.append(code)
                            print(f"Course {code} added.")
                        else:
                            print("Course already added.")
                    else:
                        print(f"Course {code} does not exist.")
            else:
                courses = current_courses.split(",") if current_courses else []
                
            course_str = ",".join(c for c in courses if c)
            new_lines.append(f"{std_id}|{name}|{course_str}")
        else:
            new_lines.append(line)
            
    write_file_lines(STUDENTINFOPATH, new_lines)
    print("Student profile updated successfully.")

def delete_student():
    print("\n--- Delete Student Profile ---")
    while True:
        std_id = input("Enter Student ID to delete (0 to exit): ").strip()
        if std_id == '0':
            return
        if not student_exists(std_id):
            print("Student not found.")
            continue
        break
        
    lines = read_file_lines(STUDENTINFOPATH)
    new_lines = [line for line in lines if not line.startswith(std_id + "|")]
    
    write_file_lines(STUDENTINFOPATH, new_lines)
    print("Student profile deleted successfully.")

def menu():
    while True:
        print("\n--- Student Profile Maintenance ---")
        print("1. Create Student")
        print("2. Read Students")
        print("3. Update Student")
        print("4. Delete Student")
        print("0. Back to Main Menu")
        
        choice = input("Select an option: ").strip()
        if choice == '1':
            create_student()
        elif choice == '2':
            read_students()
        elif choice == '3':
            update_student()
        elif choice == '4':
            delete_student()
        elif choice == '0':
            break
        else:
            print("Invalid option.")
