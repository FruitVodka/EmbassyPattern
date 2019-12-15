import lex1
from ply import lex
lexer = lex.lex(module=lex1)
lexer.input("select a, b from table1 where a=b orderby a")
r = lexer.token()
while(r):
    print(r)
    # print(dir(r))
    r = lexer.token()
    