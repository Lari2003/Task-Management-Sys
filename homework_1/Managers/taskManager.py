from tools.json_handler import load_data, save_data
from theCore.devTask import DevTask
from theCore.docTask import DocTask
from theCore.qaTask import QATask
from theCore.enums import Status

TASK_MAPPING = {
    "DevTask": DevTask,
    "QATask": QATask,
    "DocTask": DocTask
}

class TaskService:
    def __init__(self, project_service, filepath="data/users.json"):
        self.project_service = project_service 
        self.filepath = filepath
        self.tasks = []  # This will hold Task objects

        user_data = load_data(filepath)
        self.tasks = self.extract_tasks_from_users(user_data)

    def generate_task_id(self):
        existing_ids = [task.id for task in self.tasks]
        return max(existing_ids, default=0) + 1
    
    def extract_tasks_from_users(self, user_data):
        """Extract tasks from all users and their projects and return a list of Task objects."""
        tasks = []
        for user in user_data:
            for project in user.get("projects", []):
                for task_data in project.get("tasks", []):
                    task_type = task_data.get("_type")
                    if task_type in TASK_MAPPING:
                        task_class = TASK_MAPPING[task_type]
                        task = task_class.from_dict(task_data)
                        # Store user_id so we know which user the task belongs to
                        task.user_id = user["id"]
                        tasks.append(task)
        return tasks

    def find_task_by_id(self, task_id):
        """Find a task by its ID within self.tasks."""
        return next((task for task in self.tasks if task.id == task_id), None)

    def add_task(self, task_type, user_id, project_id, name, description, priority, status, **kwargs):
        """Add a new task to a specific project."""
        user = self.project_service.user_service.find_user_by_id(user_id)
        if not user:
            raise ValueError(f"User(ID: {user_id}) not found.")

        project = next((p for p in user.projects if p.id == project_id), None)
        if not project:
            raise ValueError(f"Project(ID: {project_id}) not found for User(ID: {user_id}).")

        # Generate a unique task ID
        new_task_id = self.generate_task_id()

        task_class = TASK_MAPPING.get(task_type)
        if not task_class:
            raise ValueError(f"Invalid task type: {task_type}")

        # Instantiate the task object
        task = task_class(
            id=new_task_id,
            name=name,
            description=description,
            priority=priority,
            status=status,
            project_id=project_id,
            **kwargs,
        )
        task.user_id = user_id  # Assign the user_id to the task

        # Check for duplicates based on task name in the current project
        # Note: project.tasks are still dicts at this point (loaded from JSON)
        if any(t["name"] == task.name for t in project.tasks):
            print(f"Task '{name}' already exists in Project(ID: {project_id}).")
            return task

        # Add the task to the in-memory task list
        self.tasks.append(task)

        # Save changes back to file
        self.save()
        print(f"Task '{name}' created and added to Project(ID: {project_id}).")
        return task

    def delete_task(self, task_id):
        """Delete a task by its ID."""
        task = self.find_task_by_id(task_id)
        if not task:
            raise ValueError(f"Task with ID {task_id} not found.")

        self.tasks.remove(task)

        self.save()

    def modify_task(self, task_id, name=None, description=None, priority=None, status=None, **kwargs):
        """Modify an existing task."""
        task = self.find_task_by_id(task_id)
        if not task:
            return False  # Task not found

        if name: task.name = name
        if description: task.description = description
        if priority is not None: task.priority = priority
        if status is not None: task.status = status

        for key, value in kwargs.items():
            if hasattr(task, key):
                setattr(task, key, value)

        self.save()
        return True

    def list_tasks(self, user_id=None, project_id=None):
        """Return a list of Task objects filtered by user_id and/or project_id."""
        filtered_tasks = self.tasks

        if user_id is not None:
            filtered_tasks = [t for t in filtered_tasks if getattr(t, 'user_id', None) == user_id]

        if project_id is not None:
            filtered_tasks = [t for t in filtered_tasks if t.project_id == project_id]

        if not filtered_tasks:
            print("No tasks found.")
        return filtered_tasks

    def save(self):
        """Save the current state of self.tasks back to users.json."""
        print("Saving tasks...")
        user_data = load_data(self.filepath)

        for user in user_data:
            user_id = user["id"]
            for project in user.get("projects", []):
                project_id = project["id"]
                project_tasks = [
                    task.to_dict()
                    for task in self.tasks
                    if task.project_id == project_id and getattr(task, "user_id", None) == user_id
                ]
                project["tasks"] = project_tasks

        save_data(self.filepath, user_data)
        print(f"Data saved successfully to {self.filepath}.")
