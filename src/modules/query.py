### Module: query ###
### SQL Query Classes ###
### Description: provides the interface to convert hold SQL queries ###
### and converts them into PyMongo-compatible notation when required ###
### Patterns Used: Abstract Factory to generate query of required type ###

from custom_exceptions import *
from helper import convertColumns, convertConditions, convertSet, convertOrder
from yacc import parser
from abc import ABCMeta, abstractmethod

# from SQL query string, parses, translates and executes on Mongo DB
# has an instance of DBOperations, and delegates execution to it as required
class QueryContainer():
    def __init__(self, queryString):
        self.queryString = queryString
        self.query = None
    
    def createQuery(self, factory, translatedQueryNotation):
        return factory.createQuery(translatedQueryNotation)

    def parse(self):
        x = parser.parse(self.queryString)
        # print("parsed: ", x)
        return x

    def getQueryType(self):
        return self.translatedQueryNotation["operation"]

    def getDB(self):
        return self.translatedQueryNotation["db"]

    def translate(self):
        self.translatedQueryNotation = self.parse()
        # print("Translated query: ", self.translatedQueryNotation)
        queryType = self.getQueryType()
        if queryType=="use":
            return self.getDB()
        else:
            if queryType=="insert":
                self.query = self.createQuery(InsertFactory(), self.translatedQueryNotation)
            elif queryType=="find":
                self.query = self.createQuery(FindFactory(), self.translatedQueryNotation)
            elif queryType=="update":
                self.query = self.createQuery(UpdateFactory(), self.translatedQueryNotation)
            elif queryType=="delete":
                self.query = self.createQuery(DeleteFactory(), self.translatedQueryNotation)
            else:
                raise QueryNotFoundError("[Unknown query type]")
            return self.query
    
    def execute(self, dbop, db):
        if self.query is not None:
            params = self.query.getQueryParams()
            queryType = self.getQueryType()
            if queryType=="insert":
                return dbop.insert(db, *params)
            elif queryType=="find":
                return dbop.find(db, *params)
            elif queryType=="update":
                return dbop.update(db, *params)
            elif queryType=="delete":
                return dbop.delete(db, *params)

class AbstractFactory:
    @abstractmethod
    def createQuery(self, translatedQueryNotation):
        pass
        
class InsertFactory(AbstractFactory):
    def createQuery(self, translatedQueryNotation):
        coll = translatedQueryNotation["collection"]
        cols = translatedQueryNotation["columns"]
        vals = translatedQueryNotation["values"]
        toSet = list(zip(cols,vals))
        obj = convertSet(toSet)
        return InsertQuery(coll, obj)

class FindFactory(AbstractFactory):
    def createQuery(self, translatedQueryNotation):
        coll = translatedQueryNotation["collection"]
        cols = convertColumns(translatedQueryNotation["columns"])
        cond = convertConditions(translatedQueryNotation["condition"])
        order = convertOrder(translatedQueryNotation["order"])
        return FindQuery(coll, cols, cond, order)

class UpdateFactory(AbstractFactory):
    def createQuery(self, translatedQueryNotation):
        coll = translatedQueryNotation["collection"]
        oldObj = convertConditions(translatedQueryNotation["condition"])
        newObj = convertSet(translatedQueryNotation["set"])
        return UpdateQuery(coll, newObj, oldObj)

class DeleteFactory(AbstractFactory):
    def createQuery(self, translatedQueryNotation):
        coll = translatedQueryNotation["collection"]
        obj = convertConditions(translatedQueryNotation["condition"])
        return DeleteQuery(coll, obj)

class AbstractQuery:
    @abstractmethod
    def getQueryParams(self):
        pass

class InsertQuery(AbstractQuery):
    def __init__(self, collection, obj):
        self.collection = collection
        self.obj = obj

    def getQueryParams(self):
        return (self.collection, self.obj)      

class FindQuery(AbstractQuery):
    def __init__(self, collection, columns, conditions, order):
        self.collection = collection
        self.columns = columns
        self.conditions = conditions
        self.order = order

    def getQueryParams(self):
        return (self.collection, self.columns, self.conditions, self.order)

class UpdateQuery(AbstractQuery):
    def __init__(self, collection, newObj, oldObj):
        self.collection = collection
        self.newObj = newObj
        self.oldObj = oldObj

    def getQueryParams(self):
        return (self.collection, self.newObj, self.oldObj)

class DeleteQuery(AbstractQuery):
    def __init__(self, collection, obj):
        self.collection = collection
        self.obj = obj

    def getQueryParams(self):
        return (self.collection, self.obj)
