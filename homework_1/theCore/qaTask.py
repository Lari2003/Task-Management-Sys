from theCore.task import Task
from theCore.enums import Status

class QATask(Task):
    def __init__(self, id, name, description, priority, status, project_id, test_type):
        super().__init__(id, name, description, priority, status, project_id)
        self.test_type = test_type

    def to_dict(self):
        data = super().to_dict()
        data["_type"] = "QATask"
        data["test_type"] = self.test_type
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            priority=data.get("priority", 1),
            status=Status[data.get("status", "NOT_STARTED")],
            project_id=data.get("project_id"),  # Use project_id instead of project
            test_type=data.get("test_type", "Default Test"),
        )
