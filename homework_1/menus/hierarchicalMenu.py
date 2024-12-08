from theCore.devTask import DevTask
from theCore.docTask import DocTask
from theCore.qaTask import QATask
from theCore.enums import Status


def h_menu(user_service, project_service, task_service):
    while True:
        print("\nHierarchical Menu:")
        print("1. Users")
        print("2. Projects")
        print("3. Tasks")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            user_menu(user_service)
        elif choice == "2":
            project_menu(user_service, project_service)
        elif choice == "3":
            task_menu(project_service, task_service)
        elif choice == "4":
            print("Exiting the system.")
            break
        else:
            print("Invalid choice. Please try again.")

def user_menu(user_service):
    while True:
        print("\nUser Menu:")
        print("1. Create User")
        print("2. Delete User")
        print("3. Modify User")
        print("4. List Users")
        print("5. Back")
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter user name: ")
            surname = input("Enter user surname: ")
            email = input("Enter user email: ")
            user = user_service.add_user(name, surname, email)
            print(f"User '{user.name} {user.surname}' created successfully.")

        elif choice == "2":
            user_id = int(input("Enter user ID to delete: "))
            if user_service.delete_user(user_id):
                print("User deleted successfully.")
            else:
                print("User not found.")

        elif choice == "3":
            user_id = int(input("Enter user ID to modify: "))
            name = input("Enter new name (leave empty to keep current): ")
            surname = input("Enter new surname (leave empty to keep current): ")
            email = input("Enter new email (leave empty to keep current): ")
            if user_service.modify_user(user_id, name, surname, email):
                print("User modified successfully.")
            else:
                print("User not found.")

        elif choice == "4":
            users = user_service.list_users()
            if users:
                print("\nList of Users:")
                for user in users:
                    print(f"User(ID: {user.id}, Name: {user.name}, Email: {user.email})")
            else:
                print("No users found.")

        elif choice == "5":
            break

        else:
            print("Invalid choice. Please try again.")

def project_menu(user_service, project_service):
    while True:
        print("\nProject Menu:")
        print("1. Create Project")
        print("2. Delete Project")
        print("3. Modify Project")
        print("4. List Projects")
        print("5. Back")
        choice = input("Enter your choice: ")

        if choice == "1":  # Create Project
            user_id = input("Enter user ID to assign project to: ").strip()
            if not user_id.isdigit():
                print("Invalid input. Please enter a valid numeric user ID.")
                continue  # Retry the menu option
                
            name = input("Enter project name: ")
            description = input("Enter project description: ")
            deadline = input("Enter project deadline (YYYY-MM-DD, optional): ") or None
            project_service.add_project(user_id, name, description, deadline)
        
        elif choice == "2":  # Delete Project
            user_id = int(input("Enter user ID to delete project from: "))
            project_id = int(input("Enter project ID to delete: "))
            if project_service.delete_project(user_id, project_id):
                print("Project deleted successfully.")
            else:
                print("Error deleting project.")

        elif choice == "3":  # Modify Project
            user_id = int(input("Enter user ID to modify project for: "))
            project_id = int(input("Enter project ID to modify: "))
            print(f"Modifying Project(ID: {project_id})")
            name = input(f"Enter new name (leave empty to keep current): ")
            description = input(f"Enter new description (leave empty to keep current): ")
            deadline = input(f"Enter new deadline (leave empty to keep current): ")

            if project_service.modify_project(user_id, project_id, name, description, deadline):
                print("Project modified successfully.")
            else:
                print("Error modifying project.")

        elif choice == "4":  # List Projects
            print("\nListing all projects grouped by users:")
            project_service.list_projects()

                
        elif choice == "5":  # Back to Main Menu
                break
                
        else:
                print("Invalid choice. Please select a valid option.")


def task_menu(project_service, task_service):
    while True:
        print("\nTask Menu:")
        print("1. Create Task")
        print("2. Modify Task")
        print("3. Delete Task")
        print("4. List Tasks")
        print("5. Back")
        choice = input("Enter your choice: ")

        if choice == "1":  # Create Task
            try:
                user_id = int(input("Enter user ID: "))
                project_id = int(input("Enter project ID to assign task to: "))
                name = input("Enter task name: ")
                description = input("Enter task description: ")
                print("\nSelect Task Priority:")
                print("1: Low")
                print("2: Medium")
                print("3: High")
                print("4: Critical")
                priority = int(input("Enter priority: "))

                print("\nSelect Task Status:")
                print("1: Not Started")
                print("2: In Progress")
                print("3: Completed")
                status_input = int(input("Enter status: "))
                status_mapping = {
                    1: Status.NOT_STARTED,
                    2: Status.IN_PROGRESS,
                    3: Status.COMPLETED,
                }
                status = status_mapping.get(status_input)
                if not status:
                    print("Invalid status selected.")
                    continue

                task_type = input("Enter task type (DevTask, QATask, DocTask): ")
                kwargs = {}

                if task_type == "DocTask":
                    kwargs["document"] = input("Enter document name or path: ")
                elif task_type == "DevTask":
                    kwargs["language"] = input("Enter programming language: ")
                elif task_type == "QATask":
                    kwargs["test_type"] = input("Enter type of QA test: ")

                task = task_service.add_task(task_type, user_id, project_id, name, description, priority, status, **kwargs)
                print(f"Task '{task.name}' created successfully.")

            except Exception as e:
                print(f"Error creating task: {e}")

        elif choice == "2":  # Modify Task
            try:
                task_id = int(input("Enter task ID to modify: "))
                task = task_service.find_task_by_id(task_id)
                if not task:
                    print(f"Task with ID {task_id} not found.")
                    continue

                print(f"Modifying Task(ID: {task.id}, Name: {task.name})")
                name = input(f"Enter new name (leave empty to keep '{task.name}'): ")
                description = input(f"Enter new description (leave empty to keep '{task.description}'): ")
                print("\nSelect Task Priority:")
                print("1: Low")
                print("2: Medium")
                print("3: High")
                print("4: Critical")
                priority_input = input(f"Enter priority (leave empty to keep '{task.priority}'): ")
                priority = int(priority_input) if priority_input else task.priority
                print("\nSelect Task Status:")
                print("1: Not Started")
                print("2: In Progress")
                print("3: Completed")
                status_input = input(f"Enter status (leave empty to keep '{task.status.name}'): ")
                status = task.status  # Default to current
                if status_input:
                    status = {1: Status.NOT_STARTED, 2: Status.IN_PROGRESS, 3: Status.COMPLETED}.get(int(status_input))

                if task_service.modify_task(task.id, name, description, priority, status):
                    print(f"Task(ID: {task.id}) modified successfully.")
                else:
                    print(f"Error modifying task with ID {task.id}.")
            except Exception as e:
                print(f"Error modifying task: {e}")

        elif choice == "3":  # Delete Task
            try:
                user_id = int(input("Enter user ID: "))
                project_id = int(input("Enter project ID: "))
                task_id = int(input("Enter task ID to delete: "))
                if task_service.delete_task(user_id, project_id, task_id):
                    print(f"Task(ID: {task_id}) deleted successfully.")
                else:
                    print(f"Error deleting task with ID {task_id}.")
            except Exception as e:
                print(f"Error deleting task: {e}")

        elif choice == "4":  # List Tasks
            try:
                user_id = input("Enter user ID (leave empty for all users): ").strip()
                project_id = input("Enter project ID (leave empty for all projects): ").strip()

                tasks = task_service.list_tasks(
                    user_id=int(user_id) if user_id.isdigit() else None,
                    project_id=int(project_id) if project_id.isdigit() else None,
                )
                if not tasks:
                    print("No tasks found.")
                else:
                    for task in tasks:
                        print(f"Task(ID: {task.id}, Name: {task.name}, Priority: {task.priority}, Status: {task.status.name})")
            except Exception as e:
                print(f"Error listing tasks: {e}")

        elif choice == "5":  # Back to Main Menu
            break

        else:
            print("Invalid choice. Please select a valid option.")
