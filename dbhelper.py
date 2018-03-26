import datetime
import pymongo
import bson
from bson import ObjectId

DATABASE = "candyvault"

class DBHelper:

    def __init__(self):
        client = pymongo.MongoClient()
        self.db = client[DATABASE]

    def get_user(self, email):
        return self.db.users.find_one({"email": email})

    def add_user(self, email, salt, hashed, is_admin):
        self.db.users.insert({"email": email, "salt": salt, "hashed": hashed, "is_admin": is_admin})

    def add_candy_to(self, email):
        self.db.candyowners.insert({"email": email})

    def remove_candy_to(self, lom_id, email):
        self.db.candyowners.remove({"email": email})

    def consume_candy_for(self, user_mail):
        candyowner = self.db.candyowners.find({"email": user_mail})
        if not candyowner:
            return False

        self.db.candyowners.remove(user_mail)
        return True
        