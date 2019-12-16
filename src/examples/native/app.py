### Native Example Appplication ##
### Description: uses PyMongo to interact with the Mongo database ###

"""
Functionality:
    Create a user
    Delete a user
    Find a user's details
    Update user's theme color
    Add color
    Delete color
    Find color details
"""

import sys
sys.path.insert(1, '../../modules/')

import dbop

colorObj = {'color': 'onyx', 'hexCode': '#353839'}
newColorObj = {'color': 'blackbeauty'}
details = ('themes', 'colors', colorObj)

def createColor():
    # insert onyx and search for it
    op = dbop.DBOperations().getOperator()
    op.insert(*details)
    print(op.find(*details))

def updateColor():
    # update color name onyx to blackbeauty, search for blackbeauty
    op = dbop.DBOperations().getOperator()
    op.update(*(details[:2]), newColorObj, colorObj)
    print(op.find(*(details[:2]), newColorObj))

def deleteColor():
    # delete blackbeauty
    op = dbop.DBOperations().getOperator()
    op.delete(*(details[:2]), newColorObj)
    print(op.find(*details))   

createColor()
updateColor()
deleteColor()
