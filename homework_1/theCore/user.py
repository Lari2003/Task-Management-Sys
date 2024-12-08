from theCore.project import Project

class User:
    def __init__(self, id, name, surname, email):
        self.id = id
        self.name = name
        self.surname = surname
        self.email = email
        self.projects = [] 

    def add_project(self, project):
        self.projects.append(project)

    def remove_project(self, project_id):
        self.projects = [p for p in self.projects if p.id != project_id]

    def __str__(self):
        return f"User(ID: {self.id}, Name: {self.name} {self.surname}, Email: {self.email})"

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
            "projects": [project.to_dict() for project in self.projects],
        }

    @classmethod
    def from_dict(cls, data):
        user = cls(data["id"], data["name"], data["surname"], data["email"])
        user.projects = [Project.from_dict(p) for p in data.get("projects", [])]
        return user
