### Module: dbop ###
### Database Operations ###
### Description: provides an interface to simplify interaction with the Mongo database ###
### Patterns Used: Singleton (Connector, DBOperator sub-classes) ###

"""
DB Operations Supported:
    Insert into database
    Find in database (all matches)
    Delete from database (all matches)
    Update database (all matches)
"""

from custom_exceptions import NotConnectedError
from helper import convertCursor, createSetObj
from pymongo import MongoClient

class DBOperations:
    # functionality for connecting to MongoDB using PyMongo: Singleton class 
    class __Connector:
        def __init__(self, host = None, port = None):
            if host is not None:
                self.host = host
            else:
                self.host = 'localhost'
            if port is not None:
                self.port = port
            else:
                self.port = 27017
            self.connection = None

        def getHost(self):
            return self.host

        def getPort(self):
            return self.port

        def connect(self):
            self.connection = MongoClient(self.host, self.port)

        def isConnected(self):
            if self.connection is None:
                return False
            else:
                return True

        def checkConnection(self):
            if self.connection is None:
                raise NotConnectedError("[Database connection not established]") 

        def changeConnection(self, host = None, port = None):
            if host is not None or port is not None:
                # close existing connection on resetting host or port
                if self.isConnected():
                    self.connection.close()
                    self.connection = None
                if host is not None:
                    self.host = host
                if port is not None:
                    self.port = port
                self.connect()
    
    # functionality for performing database operations: Singleton class, composes a connector object
    class __DBOperator:
        def __init__(self, connector):
            self.connector = connector

        def setConnector(self, connector):
            self.connector = connector

        def getCollections(self, db):
            pass

        def insert(self, db, collection, obj):
            self.connector.checkConnection()
            coll = self.connector.connection[db][collection]
            coll.insert_one(obj)

        def find(self, db, collection, projection = {}, obj = {}, order = {}):
            self.connector.checkConnection()
            coll = self.connector.connection[db][collection]
            if len(order)==0:
                found = coll.find(obj, projection)
            else:
                found = coll.find(obj, projection).sort(order)
            found = convertCursor(found)
            return found

        def update(self, db, collection, newObj, oldObj = {}):
            self.connector.checkConnection()
            setObj = createSetObj(newObj)
            # print("Collection: ", collection)
            coll = self.connector.connection[db][collection]
            # print("DBOp Update; coll: {}, oldObj: {}, setObj: {}".format(coll, oldObj, setObj))
            result = coll.update_many(oldObj, setObj)
            # print(result.matched_count)
            # print(result.modified_count)

        def delete(self, db, collection, obj = {}):
            self.connector.checkConnection()
            coll = self.connector.connection[db][collection]
            coll.delete_many(obj)

    connector = None
    operator = None

    def __init__(self):
        pass

    def getConnector(self, host = None, port = None):
        if not DBOperations.connector:
            DBOperations.connector = DBOperations.__Connector(host, port)
        elif (host is not None) or (port is not None):
            DBOperations.connector.changeConnection(host, port)
        return DBOperations.connector

    # returns Singleton __DBOperator object that has the Singleton __DBConnector object embedded
    def getOperator(self, host = None, port = None):   
        if not DBOperations.operator:
            conn = self.getConnector(host, port)
            if not conn.isConnected():
                conn.connect()
            DBOperations.operator = DBOperations.__DBOperator(conn)
        else:
            if host is not None or port is not None:
                conn = self.getConnector(host, port)
                if not conn.isConnected():
                    conn.connect()
        return DBOperations.operator
