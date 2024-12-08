from theCore.project import Project
from tools.json_handler import load_data, save_data

class ProjectService:
    def __init__(self, user_service, filepath="data/users.json"):
        self.user_service = user_service
        self.filepath = filepath
        self.users = load_data(filepath)

    def add_project(self, user_id, name, description, deadline):
        try:
            user_id = int(user_id)  # Ensure the input is numeric
            print(f"TEST the received user ID: {user_id}")  # Debugging line
        except ValueError:
            print("Invalid input. Please enter a valid numeric user ID.")
            return None

        user = self.user_service.find_user_by_id(user_id)
        if not user:
            print(f"No user found with ID {user_id}")
            return None

        # Ensure the user has a 'projects' attribute
        if not hasattr(user, "projects") or user.projects is None:
            user.projects = []

        project_id = len(user.projects) + 1
        project = Project(id=project_id, name=name, description=description, deadline=deadline)

        user.projects.append(project)
        self.save()
        print(f"Project '{name}' created successfully for User(ID: {user_id}).")
        return project



    def delete_project(self, user_id, project_id):
        user = self.user_service.find_user_by_id(user_id)
        if not user:
            print(f"No user found with ID {user_id}")
            return False

        project = self.find_project_by_id(user, project_id)
        if project:
            user.projects.remove(project)
            self.save()
            print(f"Project(ID: {project_id}) deleted successfully for User(ID: {user_id}).")
            return True

        print(f"Project(ID: {project_id}) not found for User(ID: {user_id}).")
        return False


    def modify_project(self, user_id, project_id, name=None, description=None, deadline=None):
        user = self.user_service.find_user_by_id(user_id)
        if not user:
            print(f"No user found with ID {user_id}")
            return False

        # Find the project by ID for the user
        project = self.find_project_by_id(user, project_id)
        if project:
            # Update project attributes
            if name:
                project.name = name
            if description:
                project.description = description
            if deadline:
                project.deadline = deadline
            self.save()
            print(f"Project(ID: {project_id}) modified successfully.")
            return True

        print(f"Project(ID: {project_id}) not found.")
        return False


    def find_project_by_id(self, user_id, project_id):
        """Find a project by its ID for a specific user."""
        user = self.user_service.find_user_by_id(user_id)
        if not user:
            print(f"No user found with ID {user_id}")
            return None

        project = next((p for p in user.projects if p.id == project_id), None)
        if not project:
            print(f"No project found with ID {project_id} for User(ID: {user_id})")
        return project


    def list_projects(self):
        for user in self.user_service.list_users():
            print(f"User(ID: {user.id}, Name: {user.name}, Email: {user.email})")
            if hasattr(user, "projects") and user.projects:
                for project in user.projects:
                    print(f"  Project(ID: {project.id}, Name: {project.name}, Description: {project.description}, Deadline: {project.deadline})")
            else:
                print("  No projects found.")


    def save(self):
        """Save all user data (including projects) back to JSON."""
        save_data(self.filepath, [user.to_dict() for user in self.user_service.list_users()])

