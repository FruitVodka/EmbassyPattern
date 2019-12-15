### Module: embassy ###
### Embassy ###
### Description: provides an interface to allow SQL agents to interact with a Mongo database ###
### Patterns: Embassy: Adapter with Access Control, implemented as a Singleton ###

from custom_exceptions import *
from dbop import DBOperations
from query import QueryContainer
from access_control import authenticate, getSession, endSession, authorize
from tabulate import tabulate
"""
Supports:
    Access Control: Role-Based
    Querying:
        Translation: SQL Query -> Mongo Query, along with query execution
        Back-translation of query results
"""

# Adapter: Embassy, Adaptee: DBOperations
class Embassy:
    class __Embassy:
        currentDBs = {}
        def __init__(self):
            pass

        # access control: authenticate, authorize, create session
        def seekEntry(self, username, password, host = None, port = None):
            role = authenticate(username, password)
            if role=="invalid":
                raise NotAuthenticatedError("Invalid credentials")
            print("authentication done")
            session = getSession(role, host, port)
            print("creating session done")
            return session

        def seekExit(self, sessionID):
            endSession(sessionID)

        def queryMongoDB(self, session, querystring):
            # translates the query string -> Mongo-compatible query object that can be executed
            qc = QueryContainer(querystring)
            query = qc.translate()
            queryType = qc.getQueryType()
            sessionID = session["ID"]
            if queryType=="use":
                Embassy.__Embassy.currentDBs[sessionID] = query
                return(["Changed DB"])
            else:
                # access control
                isAuthorized = authorize(sessionID, queryType)
                isAuthorized = True
                if isAuthorized:
                    host = None
                    port = None
                    if "host" in session:
                        host = session["host"]
                    elif "port" in session:
                        port = session["port"]
                    dbop = DBOperations().getOperator(host, port)
                    if sessionID not in Embassy.__Embassy.currentDBs:
                        return "Set DB first: 'use db-name'"
                        # raise DBNotSpecifiedError("Specify database: 'use db-name'")   
                    db = Embassy.__Embassy.currentDBs[sessionID]
                    results = qc.execute(dbop, db)
                    if queryType=="find":
                        return self.backTranslate(results)
                    elif results is None:
                        return "Successful"
                    else:
                        return results

        def backTranslate(self, results):
            return tabulate(results, headers="keys")

    embassy = None
    def getEmbassy(self):
        if Embassy.embassy is None:
            Embassy.embassy = Embassy.__Embassy()
        return Embassy.embassy