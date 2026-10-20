
# Dictionary of users (lecturer and student)
users = {
    "lecturer": {
        "name": "John ouma",
        "username": "ouma",
        "password": "doc123",
        "unit": "python programming"
    },

    "student": {
        "name": "Hillary oswago",
        "username": "shadow",
        "password": "doc123",
        "course": "computer science"
    }
}


# Login function
def login(users):
    username = input("Enter your username: ").lower()
    password = input("Enter your password: ")

    token = None

    for role in users:
        details = users[role]

        if (details["username"] == username
                and details["password"] == password):
            token = role
            print(f"Welcome, {details['name']}!")
            print(f"Role: {role}")
            break

    if token is None:
        print("Invalid username or password.")
        return None

    return token


# Call the login function
token = login(users)

if token is not None:
    print("Login successful. You can proceed.")
else:
    print("Access denied.")
