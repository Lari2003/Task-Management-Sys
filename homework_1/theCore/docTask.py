from theCore.task import Task
from theCore.enums import Status

class DocTask(Task):
    def __init__(self, id, name, description, priority, status, project_id, document):
        super().__init__(id, name, description, priority, status, project_id)
        self.document = document

    def to_dict(self):
        data = super().to_dict()
        data["_type"] = "DocTask"
        data["document"] = self.document
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
            document=data.get("document", "Unknown"),
        )
