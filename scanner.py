import nltk as nl
import re
import numpy as np

class Lexer:
   def __init__(self):
      self.tokens = [
            ('<TKwhile>','MAIS_UMA?'),
            ('<TKif>','CERVEJINHA_HOJE?'),
            ('<TKelse>','VOU_NAO'),
            ('<TKfunc>',''),
            ('<TKint>','GARRAFA'),
            ('<TKstring>','LATAO'),
            ('<TKchar>','LATA'),
            ('<TKfloat>','LITRAO'),
            ('<TKsoma>','+'),
            ('<TKsub>','-'),
            ('<TKmult>','*'),
            ('<TKdiv>','/'),
            ('<TKatr>','='),
            ('<TKnewline>','~'),
            ('<TKidentificador>',''),
            ('<TKconstante>',''),
            ('<TKreturn>','ZEROU_POR_HOJE'),
            ('<TKpareop>','('),
            ('<TKparecl>',')'),
            ('<TKpt>','.'),
            ('<TKcomma>',','),
            ('<TKdoblept>',':'),
            ('<TKbraceop>','{'),
            ('<TKbracecl>','}'),
            ('<TKbracketop>','['),
            ('<TKbracketcl>',']'),
            ('<TKsemicolon>',';'),
            ('<TKprint>','DESCE_REDONDO'),
            ('<TKscan>','BEBER'),
            ('<TKmain>','BAR')
            ] 

      self.regex_Keywords = "MAIS_UMA?|CERVEJINHA_HOJE?|VOU_NAO|TRAZ_OUTRA|GARRAFA|LATAO|LATA|LITRAO|ZEROU_POR_HOJE|DESCE_REDONDO|BEBER|BAR"
      self.regex_Identificadores = "^[a-zA-Z_]+[a-zA-Z0-9_]*"
      self.regex_Numeros = "^(\d+)$"
      self.regex_Float = "[+-]?[0-9]+\.[0-9]+"
      self.regex_StringsConstantes = "\".*\""
      self.regex_CaracteresEspeciais = "[\[{}\]:;,']|\(\)|\(|\)|{}|\[\]|\""
      self.regex_Operadores = "(\++)|(-)|(=)|(\*)|(/)|(%)|(--).|(<=)|(>=)|and|or|not|(<)|(>)"


   def tokenize (self, file):
      
      file = file.replace('\n','~')
      file = file.replace(' ','¨')
      file = self.RemoverComentarios(file)

      code_tokens = self.AjustarTokensDeCaracteresEspeciais(nl.wordpunct_tokenize(file))
      code_tokens = self.AjustaTokensDeLiterais(code_tokens)
      code_tokens = self.AjustaTokensDeFloat(code_tokens)

      tokenLine = self.ControleLinhas(code_tokens)

      cont = 1
      lasterror = 0
      error = []
      tabelaDeSimbolos = dict()

      index = 0
      idCount = 0

      for tk in code_tokens:
         token = tk

         if tk == "~": cont+=1    
         
         if(tk == "~" or tk == "¨"):
            continue

         line = tokenLine[1][index]

         if(re.findall(self.regex_Keywords,token)):
            tabelaDeSimbolos[index] = {'Lexema': token, 'Classe': "Keyword", 'Valor': 0, 'Posicao': line}
         elif(re.findall(self.regex_StringsConstantes,token,)):
            tabelaDeSimbolos[index] = {'Lexema': token, 'Classe': "Literal", 'Valor': token.replace('\"',''), 'Posicao': line}
         elif(re.findall(self.regex_Identificadores,token)):
            tabelaDeSimbolos[index] = {'Lexema': token, 'Classe': "Identificador", 'Valor': idCount, 'Posicao': line}
            idCount+=1
         elif(re.findall(self.regex_Numeros,token)):
            tabelaDeSimbolos[index] = {'Lexema': token, 'Classe': "Inteiro", 'Valor': int(token), 'Posicao': line}
         elif(re.findall(self.regex_Float,token)):
            tabelaDeSimbolos[index] = {'Lexema': token, 'Classe': "Float", 'Valor': float(token), 'Posicao': line}
         elif(re.findall(self.regex_Operadores,token)):
            tabelaDeSimbolos[index] = {'Lexema': token, 'Classe': "Operador", 'Valor': 0, 'Posicao': line}
         elif(re.findall(self.regex_CaracteresEspeciais,token)):
            tabelaDeSimbolos[index] = {'Lexema': token, 'Classe': "Caractere Especial", 'Valor': 0, 'Posicao': line}
         else:
            if lasterror != cont : 
               error.append(cont)
               lasterror = cont

         index += 1
               
      return tabelaDeSimbolos, error
      

   def ContemCaractereEspecial(self, token):
         for char in token:
            if re.findall(self.regex_CaracteresEspeciais,char):
               return True

         return False

   def AjustarTokensDeCaracteresEspeciais(self, tokens):
      tokens_corretos = []

      for tk in tokens:
         if self.ContemCaractereEspecial(tk) and len(tk) > 1:
            for char in tk: tokens_corretos.append(char)
         else:
            tokens_corretos.append(tk)

      return tokens_corretos

   def RemoverComentarios(self, file):
      fileSemComentarios = ""
      isComentario = False

      for char in file:
         if char == '#':
            isComentario = True
         elif char == '~':
            isComentario = False
         if not isComentario:
            fileSemComentarios+=char

      return fileSemComentarios

   def  ControleLinhas(self, tokens):
      x = len(tokens)
      A = np.empty((2,x), dtype=np.object)
      cont = 1 
      for i in range(x):
         A[0][i] = tokens[i]
         A[1][i] = cont
         if tokens[i] == '~': cont += 1

      return A

   def AjustaTokensDeLiterais(self, tokens):
      tokens_corretos = []
      literal = False
      palavra=""
      for tk in tokens:
         token = tk

         if "¨" in token and len(token) > 1:
            token = token.replace('¨','')

         if literal:
            if token == "¨":
               token = " "
            palavra += token
            if tk == "\"" or tk == "~": 
               literal = False
               token = palavra
               tokens_corretos.append(token)
               palavra = ""
         elif tk == "\"":
            literal = True
            palavra += tk
         else:
            tokens_corretos.append(token)
      
      return tokens_corretos

   def AjustaTokensDeFloat(self, tokens):
      tokens_corretos = []
      float = False
      tokenFloat = ""
      index = 0

      for tk in tokens:

         if float:
            if tk == ' ' or re.findall(self.regex_CaracteresEspeciais,tk):
               float = False
               tokens_corretos.append(tokenFloat)
               tokens_corretos.append(tk)
               tokenFloat = ""
            else:
               tokenFloat += tk
         elif re.findall(self.regex_Numeros,tk) and tokens[index+1] == ".":
            float = True
            tokenFloat += tk
         else: 
            tokens_corretos.append(tk)

         index += 1 

      return tokens_corretos


