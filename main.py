import re

# Token types
tokens = [
    'PRINT', 'INTEGER', 'REAL', 'STRING', 'EQUAL','END','BEGIN','KEYWORD'
    'IDENTIFIER', 'INTEGER_VALUE', 'REAL_VALUE', 'STRING_VALUE',
    'FOR', 'TO', 'COLON', 'SEMICOLON', 'LEFT_BRACKET',
    'RIGHT_BRACKET', 'COMMA'
]

# Lexical analyzer
class Lexer:
    def __init__(self):
        self.tokens = []
        self.pos = 0

    def input(self, code):
        self.code = code

    def token(self):
        if self.pos >= len(self.code):
            return None

        for token in tokens:
            pattern = None
            if token == 'PRINT':
                pattern = r'PRINT'
            elif token == 'BEGIN':
                pattern = r'BEGIN'
            elif token == 'END':
                pattern = r'END'
            elif token == 'INTEGER':
                pattern = r'INTEGER'
            elif token == 'REAL':
                pattern = r'REAL'
            elif token == 'STRING':
                pattern = r'STRING'
            elif token == 'EQUAL':
                pattern = r':='
            elif token == 'FOR':
                pattern = r'FOR'
            elif token == 'TO':
                pattern = r'TO'
            elif token == 'COLON':
                pattern = r':'
            elif token == 'SEMICOLON':
                pattern = r';'
            elif token == 'LEFT_BRACKET':
                pattern = r'\['
            elif token == 'RIGHT_BRACKET':
                pattern = r'\]'
            elif token == 'COMMA':
                pattern = r','
            elif token == 'IDENTIFIER':
                pattern = r'[A-Za-z][A-Za-z0-9_]*'
            elif token == 'REAL_VALUE':
                pattern = r'[-+]?[0-9]*\.[0-9]+([eE][-+]?[0-9]+)?'
            elif token == 'INTEGER_VALUE':
                pattern = r'\d+'
            elif token == 'STRING_VALUE':
                pattern = r'\"([^\\\n]|(\\.))*?\"'

            if pattern is not None:
                match = re.match(pattern, self.code[self.pos:])
                if match:
                    value = match.group(0)
                    self.pos += len(value)
                    if token not in ['COMMENT']:
                        self.tokens.append((token, value))
                    break

    def get_tokens(self):
        return self.tokens

# Test the lexer
code = """
BEGIN 
PRINT "HELLO" 
INTEGER A, B, C 
REAL D, E 
STRING X, Y 
A := 2 
B := 4 
C := 6 
D := -3.65E-8 
E := 4.567 
X := "text1" 
Y := "hello there" 
FOR I:=1 TO 5 
PRINT "Strings are [X] and [Y]" 
END 
"""

lexer_input = code

lexer = Lexer()
lexer.input(lexer_input)

# Tokenize
while True:
    lexer.token()
    lexer.pos += 1
    if lexer.pos >= len(lexer_input):
        break

# print(lexer.get_tokens())
for token in lexer.get_tokens():
    print(token)

print(code)

tokens = lexer.get_tokens()

#hege acess madudu helthirudu
print(tokens[0][1])

token_dict = {}
for token_type, token_value in tokens:
    if token_type in token_dict:
        token_dict[token_type].append(token_value)
    else:
        token_dict[token_type] = [token_value]

# print(token_dict)

print(token_dict['BEGIN'][0])