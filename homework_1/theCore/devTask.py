from theCore.task import Task
from theCore.enums import Status

class DevTask(Task):
    def __init__(self, id, name, description, priority, status, project_id, language):
        super().__init__(id, name, description, priority, status, project_id)
        self.language = language

    def to_dict(self):
        data = super().to_dict()
        data["_type"] = "DevTask"
        data["language"] = self.language
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            priority=data.get("priority", 1),
            status=Status[data.get("status", "NOT_STARTED")],
            project_id=data.get("project_id"),
            language=data.get("language", "Unknown"),
        )
