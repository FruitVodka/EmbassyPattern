### Module: helper ###
### Helper Functions ###

from ast_node import Node

class ID:
    _id = 0
    def __init__(self):
        pass
    def getID(self):
        ID._id+=1
        return ID._id

def convertCursor(cursor):
    results = []
    for c in cursor:
        results.append(c)
    return results

def createSetObj(obj):
    setobj = {"$set": obj}
    return setobj

def convertColumns(cols):
    colObj = {}
    for col in cols:
        colObj[col] = 1
    colObj["_id"] = 0
    return colObj

def getOpDetails(op):
    if op=="==" or op=="=":
        return "$eq", "ar"
    elif op==">":
        return "$gt", "ar"
    elif op==">=":
        return "$gte", "ar"
    elif op=="<":
        return "$lt", "ar"
    elif op=="<=":
        return "$lte", "ar"
    elif op=="<>":
        return "$ne", "ar"
    elif op=="AND":
        return "$and", "lo"
    elif op=="OR":
        return "$or", "lo"
    else:
        return "", "operand"

def convertConditions(cond):
    if cond is None:
        return {}
    stack = []
    condList = cond.preorder()
    condList.reverse()
    for cond in condList:
        condObj = {}
        d = getOpDetails(cond)
        if d[1]=="operand":
            stack.append(cond)
        else:
            operator, otype = getOpDetails(cond)
            if otype=="ar":
                field = stack.pop()
                val = stack.pop()
                condObj[field] = {operator: val}
                stack.append(condObj)
            elif otype=="lo":
                val1 = stack.pop()
                val2 = stack.pop()
                condObj[operator] = [val1, val2]
                stack.append(condObj)
    finalObj = stack.pop()
    return finalObj

def convertSet(toSet):
    updateObj = {}
    for s in toSet:
        updateObj[s[0]] = s[1]
    return updateObj

def convertOrder(order):
    orderObj = []
    for o in order:
        orderObj.append((o, 1))
    return orderObj
