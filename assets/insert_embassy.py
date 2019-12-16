import json
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['embassy']
users = db['users']

with open('passwords.json') as f:
    file_data = json.load(f)

users.insert_many(file_data)

roles = db['role_auth']

with open('role_auth.json') as f:
    file_data = json.load(f)

roles.insert_many(file_data)

client.close()

client = MongoClient('localhost', 27017)
db = client['themes']
users = db['colors']

with open('colors.json') as f:
    file_data = json.load(f)

users.insert_many(file_data)

client.close()