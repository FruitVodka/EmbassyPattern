### SQL Application ###
### Description: interacts with the Mongo database using SQL queries that go through the Embassy ###
### Menu-Driven ###

import sys
sys.path.insert(1, '../../modules/')

from query import QueryContainer
from embassy import Embassy

def logIn(username, password, host = None, port = None):
    embassy = Embassy().getEmbassy()
    session = embassy.seekEntry(username, password, host, port)
    return session

def logOut(sessionID):
    embassy = Embassy().getEmbassy()
    embassy.seekExit(sessionID)

def query(session, querystring):
    embassy = Embassy().getEmbassy()
    result = embassy.queryMongoDB(session, querystring)
    if result is None:
        result = []
    return result

details = ("Alice", "alice123")
logOut(1)
qs1 = "use themes"
qs2 = "select * from colors"
qs3 = "select * from colors where color='antiquewhite'"
qs4 = "select * from colors where color='antiquewhite' or hexCode='#00ced1'"

session = None
quitEntered = False

while True:
    print("\nMenu\n(1) Log In\n(2) Query Console\n(3) Log Out\n(4) Quit")
    choice = input(">>> ").lower().rstrip()
    if choice=="1":
        print("Enter username: ")
        un = input()
        print("Enter password: ")
        pw = input()
        print("Enter host (Optional, press Return for default):")
        host = input()
        if host=="" or host=="\n":
            host = None
        print("Enter port (Optional, press Return for default):")
        port = input()
        if port=="" or port=="\n":
            port = None
        # nonlocal session
        session = logIn(un, pw, host, port)
        if session=="invalid":
            print("Invalid credentials.")
            continue
        else:
            print("Logged in! You can now execute queries on the query console.")
    elif choice=="2":
        # nonlocal session
        if session is None:
            print("Please log in first.")
            continue
        else:
            quitEntered = False
            while True:
                print("Query Console\nTo exit, type 'quit' as the query string.")
                print("Enter query string:")
                qs = input(">>> ").rstrip()
                if qs.lower()=="quit":
                    quitEntered = True
                    break
                else:
                    res = query(session, qs)
                    if res=="auth invalid":
                        print("Not authorized to perform this query.")
                        print()
                    elif res=="query invalid":
                        print("Invalid query. Check format.")
                        print()
                    else:
                        print()
                        print(res)
                        print()
            if quitEntered:
                continue
    elif choice=="3":
        # nonlocal session
        session = None
        print("Logged out.")
        print()
        continue
    elif choice=="4":
        break
    else:
        print("Invalid choice, please choose again.")

print("\nbye")




