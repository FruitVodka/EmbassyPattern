import sqlparse 
from pprint import pprint

def get_table_name(tokens):
    fromSeen = 0
    tableName = None
    for i in range(0, len(tokens)):
        if 'Whitespace' not in str(tokens[i].ttype):
            tType = str(tokens[i].ttype)
            if fromSeen and 'Keyword' not in tType:
                fromSeen=0
                tableName = tokens[i].value
            if 'Keyword' in tType and tokens[i].value.upper() == 'FROM' or tokens[i].value.upper()=='UPDATE' or tokens[i].value.upper() == 'INTO':
                fromSeen=1
    return tableName

def get_where_clause(tokens):
    whereClause = None
    for i in range(0, len(tokens)):
        if 'Whitespace' not in str(tokens[i].ttype):
            if 'WHERE' in tokens[i].value.upper():
                whereClause = tokens[i].value[6:]
    operators=
    return whereClause

def get_operation(token):
    if token.value.upper()=='SELECT':
        return 'find'
    elif token.value.upper()=='UPDATE':
        return 'update'
    elif token.value.upper()=='DELETE':
        return 'delete'
    elif token.value.upper()=='INSERT':
        return 'insert'
    elif token.value.upper()=='USE':
        return 'use'
    else:
        return None

def convert(tokens):
    res = dict()
    tableName = get_table_name(tokens)
    whereClause = get_where_clause(tokens)
    operationName = get_operation(tokens[0])
    if not operationName: #invalid query
        return None
    if operationName=='use':
        res['operation'] = operationName
        res['db'] = tokens[2].value
        return res
    res['collection'] = tableName
    res['where'] = whereClause
    res['operation'] = operationName
    print(res)

# raw1 = 'select * from foo where x == 12 orderby y'
# raw1 = 'use foo'
# raw1 = 'update foo set y = 12 where x == 12 orderby y'
raw1 = 'INSERT INTO tab_name VALUES (value1, value2, value3, ...);'
print(raw1)
parsed = sqlparse.parse(raw1)[0]
print(parsed.tokens)
x = convert(parsed.tokens)
print(x)