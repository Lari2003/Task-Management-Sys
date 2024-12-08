from theCore.enums import  Status

class Task:
    def __init__(self, id, name, description, priority, status, project_id):
        self.id = id
        self.name = name
        self.description = description
        self.priority = priority
        self.status = status
        self.project_id = project_id 

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "priority": self.priority,
            "status": self.status.name if self.status else None,  # Serialize Status enum
            "project_id": self.project_id,  # Store project ID only
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            priority=data.get("priority", 1),
            status=Status[data.get("status", "NOT_STARTED")],  # Convert to Status enum
            project_id=data.get("project_id"),  # Store project ID
        )
