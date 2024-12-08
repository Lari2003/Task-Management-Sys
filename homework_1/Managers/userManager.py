import json
from theCore.user import User
from tools.json_handler import load_data, save_data


class UserService:
    def __init__(self, filepath="data/users.json"):
        self.filepath = filepath
        self.users = [User.from_dict(data) for data in load_data(filepath)]

    def add_user(self, name, surname, email):
        user_id = len(self.users) + 1
        user = User(id=user_id, name=name, surname=surname, email=email)
        self.users.append(user)
        self.save()
        return user

    def delete_user(self, user_id):
        user = self.find_user_by_id(user_id)
        if user:
            self.users.remove(user)
            self.save()
            return True
        return False

    def modify_user(self, user_id, name=None, surname=None, email=None):
        user = self.find_user_by_id(user_id)
        if user:
            user.name = name or user.name
            user.surname = surname or user.surname
            user.email = email or user.email
            self.save()
            return True
        return False

    def find_user_by_id(self, user_id):
        return next((u for u in self.users if u.id == user_id), None)

    def list_users(self):
        return self.users

    def save(self):
        save_data(self.filepath, [user.to_dict() for user in self.users])