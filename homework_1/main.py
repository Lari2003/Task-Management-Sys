from Managers.userManager import UserService
from Managers.projectManager import ProjectService
from Managers.taskManager import TaskService
from menus.hierarchicalMenu import h_menu
from menus.flatMenu import f_menu

def main():
    user_service = UserService(filepath="data/users.json")
    project_service = ProjectService(user_service=user_service, filepath="data/users.json")
    task_service = TaskService(project_service=project_service, filepath="data/users.json")
    
    print("Welcome to the Task Management System!")
    print("Choose Menu Type:")
    print("1. Flat Menu")
    print("2. Hierarchical Menu")
    choice = input("Enter your choice: ")

    if choice == "1":
        f_menu(user_service, project_service, task_service)
    elif choice == "2":
        h_menu(user_service, project_service, task_service)
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
