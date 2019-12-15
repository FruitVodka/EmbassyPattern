### Module: query ###
### SQL Query Translation ###
### Description: provides the interface to convert SQL queries into PyMongo-compatible notation ###
### Patterns Used: Abstract Factory to generate query of required type ###

from custom_exceptions import *
from yacc1 import parser
from helper import convertColumns, convertConditions, convertSet
from abc import ABCMeta, abstractmethod

class QueryContainer():
    def __init__(self, queryString):
        self.queryString = queryString
        self.query = None
    
    def createQuery(self, factory, translatedQueryNotation):
        return factory.createQuery(translatedQueryNotation)

    def parse(self):
        return parser.parse(self.queryString)

    def getQueryType(self):
        return self.translatedQueryNotation["operation"]

    def getDB(self):
        return self.translatedQueryNotation["db"]

    def translate(self):
        self.translatedQueryNotation = self.parse()
        print("Translated query: ", self.translatedQueryNotation)
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
        return FindQuery(coll, cols, cond)

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
    def __init__(self, collection, columns, conditions):
        self.collection = collection
        self.columns = columns
        self.conditions = conditions

    def getQueryParams(self):
        return (self.collection, self.columns, self.conditions)

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