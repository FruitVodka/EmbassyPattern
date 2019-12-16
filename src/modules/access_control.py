### Module: access_control ###
### Access Control ###
### Description: provides role-based access control: authentication, session creation, authorization ###

from helper import ID, convertCursor
import json
from pymongo import MongoClient
        
def createClient():
    client = MongoClient('localhost', 27017)
    return client

def getDB(client):
    db = client['embassy']
    return db

# checks username and password for authentication
def authenticate(username, password):
    client = createClient()
    db = getDB(client)
    x = db['users'].find({'username':username})
    client.close()
    x = convertCursor(x)
    if(len(x)==0):
        return 'invalid'
    else:
        if(password==x[0]['password']):
            return x[0]['role']
        else:
            return 'invalid'

# creates authenticated session for user
def getSession(role, host, port):
    res = dict()
    client = createClient()
    db = getDB(client)
    x = ID()
    sess_id = x.getID()
    x = db['role_auth'].find({'role':role})
    x = convertCursor(x)
    operations = x[0]['operations']
    db['session'].insert({'_id': sess_id, 'ID': sess_id, 'operations': operations, 'role':role})
    res['ID'] = sess_id
    if host:
        res['host'] = host
    if port:
        res['port'] = port
    client.close()
    return res

# ends session
def endSession(session_id):
    client = createClient()
    db = getDB(client)
    x = db['session'].delete_many({'ID':session_id})
    client.close()
    if(x.deleted_count==1):
        return True
    else:
        return False

# authorize DB operation based on role
def authorize(session_id, operation_name):
    # print(operation_name)
    client = createClient()
    db = getDB(client)
    x = db['session'].find({'ID': session_id})
    x = convertCursor(x)
    if operation_name in x[0]['operations']:
        return True
    else:
        return False