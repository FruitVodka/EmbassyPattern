import json
from pymongo import MongoClient

class ID:
    _id = 0
    def __init__(self):
        pass
    def getID(self):
        ID._id+=1
        return ID._id
        
def createClient():
    client = MongoClient('localhost', 27017)
    return client

def getDB(client):
    db = client['embassy']
    return db

def convertCursor(info):
    data = []
    for x in info:
        data.append(x)
    return data	

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

def endSession(session_id):
    client = createClient()
    db = getDB(client)
    x = db['session'].delete_many({'ID':session_id})
    client.close()
    if(x.deleted_count==1):
        return True
    else:
        return False

def authorize(session_id, operation_name):
    client = createClient()
    db = getDB(client)
    x = db['session'].find({'ID': session_id})
    x = convertCursor(x)
    print(x)
    if operation_name in x[0]['operations']:
        return True
    else:
        return False
#tests
# id = getSession('member', None, None)
# print(id)
# print(authorize(id['ID'], 'find'))
# print(authorize(id['ID'], 'update'))
# print(authorize(id['ID'], 'insert'))

# print(authorize(id['ID'], 'delete'))
# print(authorize(id['ID'], 'use'))
# print(endSession(id['ID']))