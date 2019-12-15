'''
to execute in other file:

from yacc1 import parser 

query = "select a, b, c from table1 where a=b groupby b orderby a"
result = parser.parse(query)
print(result) 
'''

from ply import yacc 
from lex1 import tokens
from ast_node import Node

tokens = tokens
res = dict()
res['columns'] = list()
res['condition'] = None
res['order'] = list()
res['set'] = list()
res['values'] = list()

root = Node('root')
start = 'start'

def p_start(p):
    r"""start : SELECT select_statement
    | UPDATE update_statement
    | DELETE delete_statement
    | INSERT insert_statement
    | USE use_statement"""
    p[0] = res

def p_use_statement(p):
    r"""use_statement : IDENTIFIER"""
    res['operation'] = 'use'
    res['db'] = p[1]
    
def p_select_statement(p):
    r"""select_statement : args FROM IDENTIFIER 
    | args FROM IDENTIFIER WHERE where_clause
    | args FROM IDENTIFIER WHERE where_clause GROUPBY IDENTIFIER ORDERBY order_list
    | args FROM IDENTIFIER WHERE where_clause GROUPBY IDENTIFIER
    | args FROM IDENTIFIER WHERE where_clause ORDERBY order_list
    | args FROM IDENTIFIER GROUPBY IDENTIFIER ORDERBY order_list
    | args FROM IDENTIFIER ORDERBY order_list"""
    res['operation'] = 'find'
    res['collection'] = p[3]
    if(len(p)>4):
        if(p[4]=='groupby'):
            res['group'] = p[5]
        if(len(p)>6):
            if(p[6]=='groupby'):
                res['group'] = p[7]

def p_update_statement(p):
    r"""update_statement : IDENTIFIER SET update_list WHERE where_clause"""
    res['operation'] = 'update'
    res['collection'] = p[2]

def p_delete_statement(p):
    r"""delete_statement : FROM IDENTIFIER WHERE where_clause"""
    res['operation'] = 'delete'
    res['collection'] = p[2]

def p_insert_statement(p):
    r"""insert_statement : INTO IDENTIFIER LPAREN column_list RPAREN VALUES LPAREN value_list RPAREN"""
    res['operation'] = 'insert'
    res['collection'] = p[2]

def p_args(p):
    r"""args : STAR
    | arg_list"""
    pass

def p_where_clause(p):
    r"""where_clause : term 
    | term OR term"""
    if(len(p)>2):
        p[0] = Node('OR')
        p[0].set([p[1], p[3]])
    else:
        p[0] = p[1]
    root = p[0]
    res['condition'] = root

def p_term(p):
    r"""term : factor 
    | factor AND factor"""
    if(len(p)>2):
        p[0] = Node('AND')
        p[0].set([p[1],p[3]])
    else:
        p[0] = p[1]

def p_factor(p):
    r"""factor : condition
    | NOT factor
    | LPAREN where_clause RPAREN"""
    if(len(p)==4):
        p[0] = p[2]
    elif(len(p)==3):
        p[0] = Node('NOT')
        p[0].set([p[2]])
    else:
        p[0] = p[1]

def p_condition(p):
    r"""condition : IDENTIFIER operators IDENTIFIER
    | IDENTIFIER operators NUMBER"""
    p[0] = Node(p[2])
    p[0].set([Node(p[1]), Node(p[3])])


def p_update_list(p):
    r"""update_list : update_list COMMA update_expression
    | update_expression"""
    pass

def p_column_list(p):
    r"""column_list : column_list COMMA IDENTIFIER
    | IDENTIFIER"""
    if(len(p)==2):
        res['columns'].append(p[1])
    else:
        res['columns'].append(p[3])

def p_value_list(p):
    r"""value_list : value_list COMMA NUMBER
    | value_list COMMA IDENTIFIER
    | NUMBER
    | IDENTIFIER"""
    if(len(p)==2):
        res['values'].append(p[1])
    else:
        res['values'].append(p[3])

def p_update_expression(p):
    r"""update_expression : IDENTIFIER EQ NUMBER
    | IDENTIFIER EQ IDENTIFIER"""
    x = list()
    x.append(p[1])
    x.append(p[3])
    res['set'].append(x)

def p_arg_list(p):
    r"""arg_list : arg_list COMMA IDENTIFIER
    | IDENTIFIER"""
    if(len(p)==2):
        res['columns'].append(p[1])
    else:
        res['columns'].append(p[3])

def p_order_list(p):
    r"""order_list : order_list COMMA IDENTIFIER
    | IDENTIFIER"""
    if(len(p)>3):
        res['order'].append(p[3])
    else:
        res['order'].append(p[1])

def p_operators(p):
    r"""operators : EE
    | EQ
    | NE
    | LT
    | LE
    | GT
    | GE"""
    p[0] = p[1]

parser = yacc.yacc(debug=True)
