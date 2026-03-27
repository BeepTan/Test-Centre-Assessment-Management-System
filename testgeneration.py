import os
import random
import coursemaintenance
import studentprofile
import questionmaintenance

TESTOUTDIR = "tests"

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def read_file_lines(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f.readlines()]

def write_file_lines(filepath, lines):
    directory = os.path.dirname(filepath)
    if directory:
        ensure_dir(directory)
    with open(filepath, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + "\n")

def get_student_courses(std_id):
    lines = read_file_lines(studentprofile.STUDENTINFOPATH)
    for line in lines:
        parts = line.split("|")
        if len(parts) >= 3 and parts[0] == std_id:
            return parts[2].split(",")
    return []

def generate_test():
    print("\n--- Generate Test Paper ---")
    
    # 1. Get and validate Student ID
    while True:
        std_id = input("Enter Student ID (0 to exit): ").strip()
        if std_id == '0':
            return
        if not studentprofile.student_exists(std_id):
            print(f"Student ID {std_id} not found.")
            continue
        break
        
    # 2. Get and validate Course Code
    while True:
        course_code = input("Enter Course Code (0 to exit): ").strip().upper()
        if course_code == '0':
            return
        if not coursemaintenance.course_exists(course_code):
            print(f"Course {course_code} not found.")
            continue
        break
        
    enrolled_courses = get_student_courses(std_id)
    if course_code not in enrolled_courses:
        print(f"Student {std_id} is not enrolled in {course_code}.")
        return
        
    # 3. Get Date of Test
    while True:
        date_str = input("Enter Date of Test (YYYY-MM-DD) (0 to exit): ").strip()
        if date_str == '0':
            return
        if not date_str:
            print("Date cannot be empty.")
            continue
        break
    
    # 4. Get Number of Questions
    q_file = questionmaintenance.get_course_file(course_code)
    lines = read_file_lines(q_file)
    total_q = len(lines)
    
    if total_q == 0:
        print(f"No questions available in the question bank for {course_code}.")
        return
        
    while True:
        num_q_str = input(f"Enter number of questions to generate (Max {total_q}) (0 to exit): ").strip()
        if num_q_str == '0':
            return
        if not num_q_str.isdigit():
            print(f"Must be a number between 1 and {total_q}.")
            continue
        num_q = int(num_q_str)
        if 1 <= num_q <= total_q:
            break
        print(f"Must be a number between 1 and {total_q}.")
    
    # Select random questions
    selected_lines = random.sample(lines, num_q)
    
    # Prepare test paper content
    test_content = []
    test_content.append(f"TEST PAPER: {course_code}")
    test_content.append(f"STUDENT ID: {std_id}")
    test_content.append(f"DATE: {date_str}")
    test_content.append("="*40)
    test_content.append("")
    
    answer_key = []
    
    for i, line in enumerate(selected_lines, 1):
        q = questionmaintenance.parse_question(line)
        if not q: continue
        
        test_content.append(f"Q{i}. {q['text']}")
        
        # Original options and answer
        orig_options = q['options']
        correct_idx = q['answer'] - 1
        correct_opt_text = orig_options[correct_idx]
        
        # Shuffle options
        shuffled_options = orig_options[:]
        random.shuffle(shuffled_options)
        
        new_correct_idx = shuffled_options.index(correct_opt_text)
        new_correct_letter = chr(65 + new_correct_idx) # A, B, C, D
        
        for j, opt in enumerate(shuffled_options):
            letter = chr(65 + j)
            test_content.append(f"   {letter}. {opt}")
            
        test_content.append("")
        answer_key.append(f"Q{i}: {new_correct_letter}")
        
    test_content.append("="*40)
    test_content.append("END OF PAPER")
    test_content.append("\n\n--- FOR EXAMINER USE ONLY ---")
    test_content.append("ANSWER KEY:")
    test_content.extend(answer_key)
    
    ensure_dir(TESTOUTDIR)
    outfile = os.path.join(TESTOUTDIR, f"{course_code}{std_id}.txt")
    write_file_lines(outfile, test_content)
    
    print(f"\nTest paper generated successfully:")
    print(f"File saved to: {outfile}")

def menu():
    while True:
        print("\n--- Test Paper Generation ---")
        print("1. Generate New Test Paper")
        print("0. Back to Main Menu")
        
        choice = input("Select an option: ").strip()
        if choice == '1':
            generate_test()
        elif choice == '0':
            break
        else:
            print("Invalid option.")
