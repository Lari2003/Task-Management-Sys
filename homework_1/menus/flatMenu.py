from theCore.enums import Status, Priority
from theCore.devTask import DevTask
from theCore.qaTask import QATask
from theCore.docTask import DocTask

def f_menu(user_service, project_service, task_service):
    def create_user():
        name = input("Enter user name: ")
        surname = input("Enter user surname: ")
        email = input("Enter user email: ")
        user = user_service.add_user(name, surname, email)
        print(f"User '{user.name} {user.surname}' created successfully with ID {user.id}.")

    def delete_user():
        user_id = int(input("Enter user ID to delete: "))
        if user_service.delete_user(user_id):
            print(f"User with ID {user_id} deleted successfully.")
        else:
            print(f"User with ID {user_id} not found.")

    def modify_user():
        user_id = int(input("Enter user ID to modify: "))
        user = user_service.find_user_by_id(user_id)
        if not user:
            print(f"User with ID {user_id} not found.")
            return
        name = input(f"Enter new name (leave empty to keep '{user.name}'): ") or user.name
        surname = input(f"Enter new surname (leave empty to keep '{user.surname}'): ") or user.surname
        email = input(f"Enter new email (leave empty to keep '{user.email}'): ") or user.email
        if user_service.modify_user(user_id, name, surname, email):
            print(f"User with ID {user_id} updated successfully.")
        else:
            print(f"Failed to update User with ID {user_id}.")

    def list_users():
        users = user_service.list_users()
        if not users:
            print("No users available.")
        else:
            print("\nList of Users:")
            for user in users:
                print(f"User(ID: {user.id}, Name: {user.name}, Surname: {user.surname}, Email: {user.email})")

    def create_project():
        user_id = int(input("Enter user ID to assign project to: "))
        user = user_service.find_user_by_id(user_id)
        if not user:
            print(f"User with ID {user_id} not found.")
            return
        name = input("Enter project name: ")
        description = input("Enter project description: ")
        deadline = input("Enter project deadline (YYYY-MM-DD, optional): ") or None
        project = project_service.add_project(user_id, name, description, deadline)
        if project:
            print(f"Project '{project.name}' created successfully with ID {project.id}.")
        else:
            print("Failed to create project.")

    def delete_project():
        user_id = int(input("Enter user ID: "))
        project_id = int(input("Enter project ID to delete: "))
        if project_service.delete_project(user_id, project_id):
            print(f"Project with ID {project_id} deleted successfully.")
        else:
            print("Error deleting project.")

    def modify_project():
        user_id = int(input("Enter user ID: "))
        project_id = int(input("Enter project ID to modify: "))
        project = project_service.find_project_by_id(user_id, project_id)
        if not project:
            print(f"Project with ID {project_id} not found for User(ID: {user_id}).")
            return

        name = input(f"Enter new name (leave empty to keep '{project.name}'): ") or project.name
        description = input(f"Enter new description (leave empty to keep '{project.description}'): ") or project.description
        deadline = input(f"Enter new deadline (leave empty to keep '{project.deadline}'): ") or project.deadline

        if project_service.modify_project(user_id, project_id, name, description, deadline):
            print(f"Project with ID {project_id} updated successfully.")
        else:
            print("Error modifying project.")

    def list_projects():
        projects = project_service.list_projects()  # Expecting a list of project objects
        if not projects:
            print("No projects available.")
        else:
            print("\nList of Projects:")
            for project in projects:
                print(f"Project(ID: {project.id}, Name: {project.name}, Description: {project.description}, Deadline: {project.deadline})")

    def create_task():
        user_id = int(input("Enter user ID to assign task to: "))
        user = user_service.find_user_by_id(user_id)
        if not user:
            print(f"User with ID {user_id} not found.")
            return

        project_id = int(input("Enter project ID to assign task to: "))
        project = next((p for p in user.projects if p.id == project_id), None)
        if not project:
            print(f"Project with ID {project_id} not found for User(ID: {user_id}).")
            return

        name = input("Enter task name: ")
        description = input("Enter task description: ")

        # Select Task Priority
        print("\nSelect Task Priority:")
        for priority_enum in Priority:
            print(f"{priority_enum.value}: {priority_enum.name.capitalize()}")
        priority_val = int(input("Enter priority: "))
        if priority_val not in [p.value for p in Priority]:
            print("Invalid priority selected.")
            return
        priority = priority_val

        # Select Task Status
        print("\nSelect Task Status:")
        status_mapping = {
            1: Status.NOT_STARTED,
            2: Status.IN_PROGRESS,
            3: Status.COMPLETED,
        }
        for key, val in status_mapping.items():
            print(f"{key}: {val.value}")
        status_input = int(input("Enter status: "))
        if status_input not in status_mapping:
            print("Invalid status selected.")
            return
        status = status_mapping[status_input]

        # Task Type and additional arguments
        task_type = input("Enter task type (DevTask, QATask, DocTask): ")
        kwargs = {}
        if task_type == "DocTask":
            kwargs["document"] = input("Enter document name or path: ")
        elif task_type == "DevTask":
            kwargs["language"] = input("Enter programming language: ")
        elif task_type == "QATask":
            kwargs["test_type"] = input("Enter type of QA test: ")
        else:
            print("Invalid task type.")
            return

        try:
            task = task_service.add_task(task_type, user_id, project_id, name, description, priority, status, **kwargs)
            print(f"Task '{task.name}' created successfully.")
        except Exception as e:
            print(f"Error creating task: {e}")

    def modify_task():
        task_id = int(input("Enter task ID to modify: "))
        task = task_service.find_task_by_id(task_id)
        if not task:
            print(f"Task with ID {task_id} not found.")
            return

        print(f"Modifying Task(ID: {task.id}, Name: {task.name})")

        name = input(f"Enter new name (leave empty to keep '{task.name}'): ") or task.name
        description = input(f"Enter new description (leave empty to keep '{task.description}'): ") or task.description

        # Update Priority
        print("\nSelect Task Priority:")
        for priority_enum in Priority:
            print(f"{priority_enum.value}: {priority_enum.name.capitalize()}")
        priority_input = input(f"Enter priority (leave empty to keep '{task.priority}'): ")
        priority = int(priority_input) if priority_input.strip() else task.priority

        # Update Status
        print("\nSelect Task Status:")
        status_mapping = {
            1: Status.NOT_STARTED,
            2: Status.IN_PROGRESS,
            3: Status.COMPLETED,
        }
        for key, val in status_mapping.items():
            print(f"{key}: {val.value}")
        status_input = input(f"Enter status (leave empty to keep '{task.status.name}'): ")
        status = task.status
        if status_input.strip():
            status_choice = int(status_input)
            if status_choice in status_mapping:
                status = status_mapping[status_choice]
            else:
                print("Invalid status chosen. Keeping current status.")

        # Handle task-type-specific attributes
        kwargs = {}
        if isinstance(task, DocTask):
            doc = input(f"Enter document (leave empty to keep '{task.document}'): ") or task.document
            kwargs["document"] = doc
        elif isinstance(task, DevTask):
            lang = input(f"Enter language (leave empty to keep '{task.language}'): ") or task.language
            kwargs["language"] = lang
        elif isinstance(task, QATask):
            test_type = input(f"Enter test type (leave empty to keep '{task.test_type}'): ") or task.test_type
            kwargs["test_type"] = test_type

        if task_service.modify_task(task_id, name, description, priority, status, **kwargs):
            print(f"Task with ID {task_id} updated successfully.")
        else:
            print(f"Failed to update Task with ID {task_id}.")

    def delete_task():
        task_id = int(input("Enter task ID to delete: "))
        if task_service.delete_task(task_id):
            print(f"Task with ID {task_id} deleted successfully.")
        else:
            print(f"Task with ID {task_id} not found.")

    def list_tasks():
        user_id_input = input("Enter user ID (leave empty for all users): ").strip()
        project_id_input = input("Enter project ID (leave empty for all projects): ").strip()

        user_id = int(user_id_input) if user_id_input.isdigit() else None
        project_id = int(project_id_input) if project_id_input.isdigit() else None

        tasks = task_service.list_tasks(user_id=user_id, project_id=project_id)
        if not tasks:
            print("No tasks available.")
        else:
            print("\nList of Tasks:")
            for task in tasks:
                print(f"Task(ID: {task.id}, Name: {task.name}, Priority: {task.priority}, Status: {task.status.name})")

    menu_options = {
        1: create_user,
        2: delete_user,
        3: modify_user,
        4: list_users,
        5: create_project,
        6: delete_project,
        7: modify_project,
        8: list_projects,
        9: create_task,
        10: modify_task,
        11: delete_task,
        12: list_tasks,
        13: exit
    }

    while True:
        print("\nFlat Menu:")
        print("1. Create User")
        print("2. Delete User")
        print("3. Modify User")
        print("4. List Users")
        print("5. Create Project")
        print("6. Delete Project")
        print("7. Modify Project")
        print("8. List Projects")
        print("9. Create Task")
        print("10. Modify Task")
        print("11. Delete Task")
        print("12. List Tasks")
        print("13. Exit")

        try:
            choice = int(input("Enter your choice: "))
            action = menu_options.get(choice, lambda: print("Invalid option!"))
            action()
        except ValueError:
            print("Please enter a valid number.")
