import requests

USER_API_URL = "http://127.0.0.1:8081/v1"
BOARD_API_URL = "http://127.0.0.1:8083/v1"


def register():
    login = input("Login: ")
    password = input("Password: ")
    email = input("Email: ")
    response = requests.post(f"{USER_API_URL}/users", json={"login": login, "password": password, "email": email})
    if response.status_code == 200:
        print("Registration successful!")
        return response.json()
    print("Registration failed.")
    return None


def login():
    login = input("Login: ")
    password = input("Password: ")
    response = requests.post(f"{USER_API_URL}/login", json={"login": login, "password": password})
    if response.status_code == 200:
        print("Login successful!")
        return response.json()
    print("Login failed.")
    return None


def create_user():
    login = input("Login: ")
    password = input("Password: ")
    email = input("Email: ")
    response = requests.post(f"{USER_API_URL}/users", json={"login": login, "password": password, "email": email})
    if response.status_code == 200:
        print("User created successfully!")
    else:
        print("Failed to create user.")


def update_user(user_id):
    login = input("New Login: ")
    password = input("New Password: ")
    response = requests.put(f"{USER_API_URL}/users/{user_id}", json={"login": login, "password": password})
    if response.status_code == 200:
        print("User updated successfully!")
    else:
        print("Failed to update user.")


def delete_user(user_id):
    response = requests.delete(f"{USER_API_URL}/users/{user_id}")
    if response.status_code == 200:
        print("User deleted successfully!")
    else:
        print("Failed to delete user.")


def list_users():
    response = requests.get(f"{USER_API_URL}/users")
    if response.status_code == 200:
        users = response.json()
        for user in users:
            print(f"ID: {user['id']} | Login: {user['login']} | Email: {user['email']}")
    else:
        print("Failed to retrieve users.")


def create_ticket(user_id):
    name = input("Ticket name: ")
    description = input("Description: ")
    response = requests.post(f"{BOARD_API_URL}/tickets",
                             json={"name": name, "description": description, "user_id": user_id})
    if response.status_code == 200:
        print("Ticket created successfully!")
        return response.json()
    print("Ticket creation failed.")
    return None


def update_ticket(ticket_id, new_status):
    data = {"status": new_status}
    response = requests.put(f"{BOARD_API_URL}/tickets/{ticket_id}", json=data)
    if response.status_code == 200:
        print("Ticket updated successfully!")
    else:
        print("Failed to update ticket.")


def delete_ticket(ticket_id):
    response = requests.delete(f"{BOARD_API_URL}/tickets/{ticket_id}")
    if response.status_code == 200:
        print("Ticket deleted successfully!")
    else:
        print("Failed to delete ticket.")


def list_tickets():
    response = requests.get(f"{BOARD_API_URL}/tickets")
    if response.status_code == 200:
        tickets = response.json()
        for ticket in tickets:
            print(f"ID: {ticket['id']} | Name: {ticket['name']} | Status: {ticket['status']}")
    else:
        print("Failed to retrieve tickets.")


def main():
    user = None
    while True:
        print("\n1. Register\n2. Login\n3. Create User\n4. Update User\n5. Delete User\n6. List Users\n7. Create Ticket\n8. Update Ticket\n9. Delete Ticket\n10. List Tickets\n11. Exit")
        choice = input("Choose an action: ")

        if choice == "1":
            user = register()
        elif choice == "2":
            user = login()
        elif choice == "3":
            create_user()
        elif choice == "4" and user:
            user_id = user["id"]
            update_user(user_id)
        elif choice == "5" and user:
            user_id = user["id"]
            delete_user(user_id)
        elif choice == "6":
            list_users()
        elif choice == "7" and user:
            user_id = user["id"]
            create_ticket(user_id)
        elif choice == "8":
            ticket_id = input("Enter the ticket ID to update: ")
            new_status = input("Enter the new status (e.g., 'IN_PROGRESS', 'DONE'): ")
            update_ticket(ticket_id, new_status)
        elif choice == "9":
            ticket_id = input("Enter the ticket ID to delete: ")
            delete_ticket(ticket_id)
        elif choice == "10":
            list_tickets()
        elif choice == "11":
            print("Goodbye!")
            break
        else:
            print("Invalid option or action not available. You must be logged in to continue.")


if __name__ == "__main__":
    main()
