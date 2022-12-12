from pathlib import Path
from scanner import Lexer

code = file = Path("teste.txt").read_text()

lexer = Lexer()

tabelaDeSimbolos, erros = lexer.tokenize(code)

print ("\n","erro léxico na linha: ", erros)

