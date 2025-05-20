from database import db
from bson import ObjectId

class User:
    collection = db.users
    
    def __init__(self, email, password, name, role='nurse'):
        self.email = email
        self.password = password
        self.name = name
        self.role = role
    
    def save(self):
        user_data = {
            'email': self.email,
            'password': self.password,
            'name': self.name,
            'role': self.role
        }
        result = self.collection.insert_one(user_data)
        return result.inserted_id
    
    @staticmethod
    def find_by_email(email):
        return User.collection.find_one({'email': email})
    
    @staticmethod
    def find_by_id(user_id):
        try:
            return User.collection.find_one({'_id': ObjectId(user_id)})
        except:
            return None
    
    @staticmethod
    def get_all():
        return list(User.collection.find())
    
    def to_dict(self):
        return {
            'email': self.email,
            'name': self.name,
            'role': self.role
        } 