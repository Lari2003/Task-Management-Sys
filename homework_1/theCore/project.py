from theCore.devTask import DevTask
from theCore.qaTask import QATask
from theCore.docTask import DocTask

TASK_MAPPING = {
    "DevTask": DevTask,
    "QATask": QATask,
    "DocTask": DocTask,
}

class Project:
    def __init__(self, id, name, description, deadline=None, user_id=None):
        self.id = id
        self.name = name
        self.description = description
        self.deadline = deadline
        self.user_id = user_id  # Associate project with a user
        self.tasks = []

    def __str__(self):
        return f"Project(ID: {self.id}, Name: {self.name}, Description: {self.description}, Deadline: {self.deadline})"
    
    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, task_id):
        self.tasks = [t for t in self.tasks if t.id != task_id]

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "deadline": self.deadline,
            "tasks": [task.to_dict() for task in self.tasks],
        }

    @classmethod
    def from_dict(cls, data):
        project = cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            deadline=data.get("deadline"),
        )
        project.tasks = [
            TASK_MAPPING.get(t["_type"], lambda x: None).from_dict(t)
            for t in data.get("tasks", [])
            if t.get("_type") in TASK_MAPPING
        ]
        return project