import os
import coursemaintenance

def get_course_file(course_code):
    return f"course/{course_code}.txt"

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

def parse_question(line):
    parts = line.split("|")
    if len(parts) == 6:
        return {
            "text": parts[0],
            "options": parts[1:5],
            "answer": int(parts[5])
        }
    return None

def format_question(question_dict):
    opts = "|".join(question_dict["options"])
    return f"{question_dict['text']}|{opts}|{question_dict['answer']}"

def create_question(course_code):
    print("\n--- Create Question ---")
    while True:
        text = input("Enter Question text (0 to exit): ").strip()
        if text == '0':
            return
        if not text:
            print("Question text cannot be empty.")
            continue
        break
        
    options = []
    for i in range(1, 5):
        while True:
            opt = input(f"Enter Option {i} (0 to exit): ").strip()
            if opt == '0':
                return
            if not opt:
                print("Option cannot be empty.")
                continue
            options.append(opt)
            break
            
    while True:
        ansStr = input("Enter correct option number (1-4) (0 to exit): ").strip()
        if ansStr == '0':
            return
        if ansStr not in ['1', '2', '3', '4']:
            print("Must be 1, 2, 3, or 4.")
            continue
        ans = int(ansStr)
        break
        
    q_dict = {"text": text, "options": options, "answer": ans}
    line = format_question(q_dict)
    
    append_line(get_course_file(course_code), line)
    print("Question added successfully.")

def read_questions(course_code):
    print(f"\n--- Questions for {course_code} ---")
    lines = read_file_lines(get_course_file(course_code))
    if not lines:
        print("No questions found for this course.")
        return
    
    for i, line in enumerate(lines):
        q = parse_question(line)
        if q:
            print(f"\nQ{i+1}: {q['text']}")
            for j, opt in enumerate(q['options']):
                prefix = "*" if j + 1 == q['answer'] else " "
                print(f"  {prefix}{j+1}. {opt}")

def update_question(course_code):
    print("\n--- Update Question ---")
    lines = read_file_lines(get_course_file(course_code))
    if not lines:
        print("No questions found for this course.")
        return
    
    read_questions(course_code)
    
    while True:
        idx_str = input(f"Enter question number to update (1-{len(lines)}) (0 to exit): ").strip()
        if idx_str == '0':
            return
        try:
            idx = int(idx_str) - 1
            if idx < 0 or idx >= len(lines):
                raise ValueError
            break
        except ValueError:
            print("Invalid question number.")
            continue
            
    print("\nEditing Question Data (Leave blank to keep current value, type 0 to exit)")
    q = parse_question(lines[idx])
    
    new_text = input(f"Question text [{q['text']}]: ").strip()
    if new_text == '0': return
    if new_text:
        q['text'] = new_text
        
    for i in range(4):
        new_opt = input(f"Option {i+1} [{q['options'][i]}]: ").strip()
        if new_opt == '0': return
        if new_opt:
            q['options'][i] = new_opt
            
    while True:
        new_ans = input(f"Correct option (1-4) [{q['answer']}]: ").strip()
        if new_ans == '0': return
        if not new_ans:
            break
        if new_ans in ['1', '2', '3', '4']:
            q['answer'] = int(new_ans)
            break
        print("Must be 1, 2, 3, or 4.")
        
    lines[idx] = format_question(q)
    write_file_lines(get_course_file(course_code), lines)
    print("Question updated successfully.")

def delete_question(course_code):
    print("\n--- Delete Question ---")
    lines = read_file_lines(get_course_file(course_code))
    if not lines:
        print("No questions found for this course.")
        return
    
    read_questions(course_code)
    
    while True:
        idx_str = input(f"Enter question number to delete (1-{len(lines)}) (0 to exit): ").strip()
        if idx_str == '0':
            return
        try:
            idx = int(idx_str) - 1
            if idx < 0 or idx >= len(lines):
                raise ValueError
            break
        except ValueError:
            print("Invalid question number.")
            
    while True:
        confirm = input(f"Are you sure you want to delete Question {idx+1}? (Y/N) (0 to exit): ").strip().upper()
        if confirm == '0':
            return
        if confirm == 'Y':
            deleted = lines.pop(idx)
            write_file_lines(get_course_file(course_code), lines)
            print("Question deleted successfully.")
            break
        elif confirm == 'N':
            print("Deletion cancelled.")
            break
        else:
            print("Please enter Y or N.")

def course_menu(course_code):
    while True:
        print(f"\n--- Question Bank: {course_code} ---")
        print("1. Add Question")
        print("2. List Questions")
        print("3. Update Question")
        print("4. Delete Question")
        print("0. Back to Course Selection")
        
        choice = input("Select an option: ").strip()
        if choice == '1':
            create_question(course_code)
        elif choice == '2':
            read_questions(course_code)
        elif choice == '3':
            update_question(course_code)
        elif choice == '4':
            delete_question(course_code)
        elif choice == '0':
            break
        else:
            print("Invalid option.")

def menu():
    while True:
        print("\n--- Question Bank Maintenance ---")
        print("1. Select Course to Manage Questions")
        print("0. Back to Main Menu")
        
        choice = input("Select an option: ").strip()
        if choice == '1':
            coursemaintenance.read_courses()
            while True:
                code = input("Enter Course Code (0 to exit): ").strip().upper()
                if code == '0':
                    break
                if coursemaintenance.course_exists(code):
                    course_menu(code)
                    break
                else:
                    print("Course not found.")
        elif choice == '0':
            break
        else:
            print("Invalid option.")
