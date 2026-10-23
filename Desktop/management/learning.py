
# Dictionary of users (lecturer and student)
from dotenv import load_dotenv
import jwt
import os

users_ = [
    {
        "name": "Ouma Arera",
        "username": "ouma",
        "password": "123456789",
        "role": "student"
    },
    {
        "name": "Hillary Oswago",
        "username": "hill",
        "password": "Hil12345",
        "role": "lecturer"
    }
]

load_dotenv()

IS_STUDENT = False
IS_LECTURER = False
IS_LOGIN = False
ROLE = None

SECRET_KEY = os.getenv("SECRET")

# Check whether the secret key exists
if not SECRET_KEY:
    raise ValueError("SECRET is missing from the .env file")


# Data structures for LMS activities
units = {
    "csc101": {
        "name": "python programming",
        "lecturer": "hill",
        "students": ["ouma"]
    }
}

learning_materials = []

assignments = []

students_mark = {
    "ouma": {}
}

submissions = {}

fee_records = {
    "ouma": {
        "total_fees": 35000,
        "paid": 0
    }
}


# Login function
def login(users):
    global IS_LOGIN, IS_STUDENT, IS_LECTURER, ROLE

    username = input("Enter your username: ").lower()
    password = input("Enter your password: ")

    for user in users:
        if user["username"] == username and user["password"] == password:

            IS_LOGIN = True
            ROLE = user["role"]

            if ROLE == "student":
                IS_STUDENT = True
                IS_LECTURER = False

            elif ROLE == "lecturer":
                IS_LECTURER = True
                IS_STUDENT = False

            payload = {
                "username": user["username"],
                "fullname": user["name"],
                "role": user["role"]
            }

            token = jwt.encode(
                payload,
                SECRET_KEY,
                algorithm="HS256"
            )

            print(f"Welcome, {user['name']}!")
            return token

    print("Invalid username or password.")
    return None


# 1. View lecturer's unit
def view_unit():
    found = False

    for code, unit in units.items():
        if unit["lecturer"] == "hill":
            print(f"\nUnit code: {code}")
            print(f"Unit name: {unit['name']}")
            found = True

    if not found:
        print("No units assigned to this lecturer.")


# 2. Upload learning materials
def upload_material():
    unit_code = input("Enter unit code: ").strip().lower()

    if unit_code not in units:
        print("Unit not found.")
        return

    title = input("Enter material title: ").strip()
    description = input(
        "Enter material description or file path: "
    ).strip()

    if not title or not description:
        print("Title and description are required.")
        return

    learning_materials.append({
        "unit_code": unit_code,
        "title": title,
        "description": description,
        "uploaded_by": "hill"
    })

    print("Learning material uploaded successfully.")


# 3. Manage assignments
def manage_assignments():
    print("\n1. Create assignment")
    print("2. View assignments")

    choice = input("Choose an activity: ").strip()

    if choice == "1":
        unit_code = input("Enter unit code: ").strip().lower()

        if unit_code not in units:
            print("Unit not found.")
            return

        title = input("Enter assignment title: ").strip()
        instructions = input(
            "Enter assignment instructions: "
        ).strip()
        due_date = input("Enter due date: ").strip()

        if not title or not instructions or not due_date:
            print("All assignment details are required.")
            return

        assignments.append({
            "id": len(assignments) + 1,
            "unit_code": unit_code,
            "title": title,
            "instructions": instructions,
            "due_date": due_date
        })

        print("Assignment created successfully.")

    elif choice == "2":
        view_assignments()

    else:
        print("Invalid choice.")


# 4. Enter student marks
def enter_student_marks():
    username = input(
        "Enter student username: "
    ).strip().lower()

    if username not in students_mark:
        students_mark[username] = {}

    unit_code = input("Enter unit code: ").strip().lower()

    if unit_code not in units:
        print("Unit not found.")
        return

    try:
        marks = float(input("Enter marks (0-100): "))

        if not 0 <= marks <= 100:
            print("Marks must be between 0 and 100.")
            return

    except ValueError:
        print("Please enter a valid number.")
        return

    students_mark[username][unit_code] = marks
    print("Student marks recorded successfully.")


# Lecturer menu
def lecturer_menu():
    global IS_LOGIN, IS_LECTURER, ROLE

    while IS_LOGIN and IS_LECTURER:
        print("LECTURER MENU")
        print("1. View unit")
        print("2. Upload learning materials")
        print("3. Manage assignments")
        print("4. Enter student marks")
        print("5. Logout")

        choice = input("Choose an activity: ").strip()

        if choice == "1":
            view_unit()

        elif choice == "2":
            upload_material()

        elif choice == "3":
            manage_assignments()

        elif choice == "4":
            enter_student_marks()

        elif choice == "5":
            print("Logging out...")
            IS_LOGIN = False
            IS_LECTURER = False
            ROLE = None

        else:
            print("Invalid choice. Try again.")


# 1. View units
def student_view_units():
    username = "ouma"
    found = False

    for code, unit in units.items():
        if username in unit["students"]:
            print(f"Unit code: {code}")
            print(f"Unit name: {unit['name']}")
            found = True

    if not found:
        print("You are not enrolled in any units.")


# 2. Pay fees
def pay_fees():
    username = "ouma"
    record = fee_records[username]

    balance = record["total_fees"] - record["paid"]

    print(f"Total fees: KSh {record['total_fees']}")
    print(f"Amount paid: KSh {record['paid']}")
    print(f"Outstanding balance: KSh {balance}")

    if balance <= 0:
        print("Your fees are fully paid.")
        return

    try:
        amount = float(input("Enter payment amount (KSh): "))

        if amount <= 0:
            print("Payment must be greater than zero.")

        elif amount > balance:
            print("Payment exceeds the outstanding balance.")

        else:
            record["paid"] += amount
            print(f"Payment of KSh {amount:.2f} recorded.")

    except ValueError:
        print("Please enter a valid amount.")


# 3. View assignments
def view_assignments():
    if not assignments:
        print("No assignments have been created.")
        return

    for assignment in assignments:
        print(f"ID: {assignment['id']}")
        print(f"Unit: {assignment['unit_code']}")
        print(f"Title: {assignment['title']}")
        print(f"Instructions: {assignment['instructions']}")
        print(f"Due date: {assignment['due_date']}")


# 4. View learning materials
def view_learning_materials():
    if not learning_materials:
        print("No learning materials have been uploaded.")
        return

    for material in learning_materials:
        print(f"Unit: {material['unit_code']}")
        print(f"Title: {material['title']}")
        print(
            f"Description/file path: {material['description']}"
        )


# 5. View results
def view_results():
    username = "ouma"
    marks = students_mark.get(username, {})

    if not marks:
        print("No results have been entered yet.")
        return

    print("YOUR RESULTS:")

    for unit_code, score in marks.items():
        print(f"Unit: {units[unit_code]['name']}")
        print(f"Marks: {score}/100")


# 6. Submit or resubmit an assignment
def resubmit_assignment():
    username = "ouma"

    if not assignments:
        print("There are no assignments to submit.")
        return

    view_assignments()

    try:
        assignment_id = int(input("Enter assignment ID: "))
    except ValueError:
        print("Enter a valid assignment ID.")
        return

    selected = None

    for assignment in assignments:
        if assignment["id"] == assignment_id:
            selected = assignment
            break

    if selected is None:
        print("Assignment not found.")
        return

    answer = input(
        "Enter your submission text or file path: "
    ).strip()

    if not answer:
        print("Submission cannot be empty.")
        return

    key = (username, assignment_id)
    is_resubmission = key in submissions

    submissions[key] = {
        "answer": answer,
        "unit_code": selected["unit_code"]
    }

    if is_resubmission:
        print("Assignment resubmitted successfully.")
    else:
        print("Assignment submitted successfully.")


# 7. View fee statement
def view_fee_statement():
    username = "ouma"
    record = fee_records[username]

    balance = record["total_fees"] - record["paid"]

    print("FEE STATEMENT:")
    print(f"Student: {username}")
    print(f"Total fees: KSh {record['total_fees']:.2f}")
    print(f"Total paid: KSh {record['paid']:.2f}")
    print(f"Outstanding balance: KSh {balance:.2f}")


# Student menu
def student_menu():
    global IS_LOGIN, IS_STUDENT, ROLE

    while IS_LOGIN and IS_STUDENT:
        print("STUDENTS MENU:")
        print("1. View units")
        print("2. Pay fees")
        print("3. Assignments")
        print("4. View learning materials")
        print("5. View results")
        print("6. Resubmit assignment")
        print("7. View fee statement")
        print("8. Logout")

        choice = input(
            "Choose activity (1-8): "
        ).strip()

        if choice == "1":
            student_view_units()

        elif choice == "2":
            pay_fees()

        elif choice == "3":
            view_assignments()

        elif choice == "4":
            view_learning_materials()

        elif choice == "5":
            view_results()

        elif choice == "6":
            resubmit_assignment()

        elif choice == "7":
            view_fee_statement()

        elif choice == "8":
            print("Logging out...")
            IS_LOGIN = False
            IS_STUDENT = False
            ROLE = None

        else:
            print("Invalid choice. Try again.")


# Main program - keep this at the bottom
token = login(users_)

if token is not None:
    print("Login successful. You can proceed.")

    if ROLE == "lecturer":
        lecturer_menu()

    elif ROLE == "student":
        student_menu()

else:
    print("Access denied.")
