from ply import lex 

reserved = {
    'select' : 'SELECT',
    'from' : 'FROM',
    'where' : 'WHERE',
    'update' : 'UPDATE',
    'delete' : 'DELETE',
    'insert' : 'INSERT',
    'values' : 'VALUES',
    'use' : 'USE',
    'set' : 'SET', 
    'into' : 'INTO',
    'and' : 'AND',
    'not' : 'NOT',
    'or' : 'OR',
    'groupby' : 'GROUPBY',
    'orderby' : 'ORDERBY'
 }

tokens = ['NUMBER', 'IDENTIFIER', 'LPAREN', 'RPAREN', 'GT', 'GE', 'LT', 'LE', 'EQ', 'NE', 'EE', 'NEWLINE','QUOTED_IDENTIFIER', 'COMMA', 'STAR']+list(reserved.values())

reserved = list(reserved.values())

print(tokens)

t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_EQ = r'='
t_EE = r'=='
t_NE = r'<>|!='
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_COMMA = r','
t_STAR = r'\*'

def t_IDENTIFIER(t):
    r"""[#a-zA-Z_][a-zA-Z0-9]*"""
    val = t.value
    if val.upper() in reserved:
        t.type = val.upper()
    return t

def t_QUOTED_IDENTIFIER(t):
    r'"([^"]|"")*"'
    t.val = t.value.lower()
    if t.val.upper() in reserved:
        print("what")
        t.type = reserved[val]
    return t


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

def t_NEWLINE(t):
    r'[\r\n]+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

t_ignore = ' \t'
lexer = lex.lex()