from s3_queries import get_user
from flask_login import UserMixin

# used to keep track of the logged in user with flask_login module
class User(UserMixin):
    def __init__(self, email):
        self.id = email
        user_dict = get_user(email)
        self.name = user_dict['name']
        self.age = user_dict['age']
        self.gender = user_dict['gender']
        self.location = user_dict['location']