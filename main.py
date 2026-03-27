import sys
import coursemaintenance
import questionmaintenance
import studentprofile
import scheduling
import testgeneration

def main_menu():
    while True:
        print("\n" + "="*50)
        print(" Test Centre Assessment Management System")
        print("="*50)
        print("1. Course Maintenance")
        print("2. Question Bank Maintenance")
        print("3. Student Profile Maintenance")
        print("4. Test Date Scheduling")
        print("5. Test Paper Generation")
        print("0. Exit")
        print("="*50)
        
        choice = input("Select an option: ").strip()
        
        if choice == '1':
            coursemaintenance.menu()
        elif choice == '2':
            questionmaintenance.menu()
        elif choice == '3':
            studentprofile.menu()
        elif choice == '4':
            scheduling.menu()
        elif choice == '5':
            testgeneration.menu()
        elif choice == '0':
            print("Exiting system... Goodbye!")
            sys.exit(0)
        else:
            print("Invalid option. Please input a number from 0 to 5.")

if __name__ == "__main__":
    main_menu()
