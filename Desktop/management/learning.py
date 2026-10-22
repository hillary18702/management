
# Dictionary of users (lecturer and student)
from dotenv import load_dotenv
import jwt
import os

users_=[
    {
        "name":"Ouma Arera",
        "username": "ouma",
        "password": "123456789",
        "role": "student"
    },
    {
        "name":"Hillary Oswago",
        "username": "hill",
        "password": "Hil12345",
        "role": "lecturer"
    }
]

load_dotenv()

IS_STUDENT=False
IS_LECTURER=False
IS_LOGIN=False
ROLE=None
SECRET_KEY=os.getenv("SECRET")
print(f'Secret Key: {SECRET_KEY}')

# Login function
def login(users):
    global IS_LOGIN, IS_STUDENT, IS_LECTURER, ROLE
    username = input("Enter your username: ").lower()
    password = input("Enter your password: ")

    token = None
    for user in users:
        if user['username']==username and user['password']==password:
            IS_LOGIN=True
            if user['role'] == "student":
                IS_STUDENT =True 
                ROLE=user['role']
            elif user['role'] == 'lecturer':
                IS_LECTURER=True
                ROLE=user['role']
            payload={
                "username": user["username"],
                "fullname": user['name'],
                "role": user['role']
            }
            token=jwt.encode(payload, SECRET_KEY, algorithm="HS256")
            print(token)

        print("invalid username or password")

   

    if token is None:
        print("Invalid username or password.")
        return None

    return token


# Call the login function
token = login(users_)

if token is not None:
    print("Login successful. You can proceed.")
else:
    print("Access denied.")


#lecturer menu

def lecturer_menu():
    while IS_LOGIN and IS_LECTURER:
        print("LECTURER MENU")
        print("1. View unit")
        print("2. Upload learning materials")
        print("3. Manage assignments")
        print("4. Enter student marks")
        print("5. Logout")

        choice = input("Choose an activity: ")

        if choice == "1":
            print("Viewing lecturer's unit...")
        elif choice == "2":
            print("Learning materials section selected.")
        elif choice == "3":
            print("Assignment management selected.")
        elif choice == "4":
            print("Student marks section selected.")
        elif choice == "5":

            print("Logging out...")
            break
        else:
            print("Invalid choice. Try again.")
            break




#students menu
def student_menu():
    while IS_LOGIN and IS_STUDENT:
        print("STUDENTS MENU: ")
        print(1,"view units")
        print(2,"pay fees")
        print(3, "assignments")
        print(4, "view learning materials")
        print(5, "view results")
        print(6, "resubmitt assignment")
        print(7, "view fee statement")

        choice = input("choose activity, (1-7): ")

        if choice==1:
            print("view units: ")

        elif choice==2:
            print("pay fees: ")

        elif choice==3:
            print("assignments: ")

        elif choice==4:
            print("view learning materials: ")

        elif choice==5:
            print("view results: ")

        elif choice==6:
            print("resubmit assignments: ")

        elif choice== 7:
            print("view fee statement: ")

        else:
            print("invalid choice. try again: ")



lecturer_menu() if ROLE == "lecturer" else student_menu()