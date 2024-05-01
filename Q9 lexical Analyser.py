import re
from tabulate import tabulate

delimiters = [" ", "+", "-", "*", "/", "=", ";", "(", ")", "[", "]", "{", "}", "<", ">", "!", "&", "|", "^", "%", "~", "?", ".", ",", "'", "\""]
keywords = ['int', 'main', 'begin', 'end', 'do', 'while', 'return']

kwd_dict ={
    "int": "t",
    "main": "m",
    "begin": "b",
    "end": "e",
    "do": "d",
    "while": "w",
    "return": "r",
    "+": "o",
    "-": "o",
    "*": "o",
    "/": "o",
    "=": "a",
    "expr": "v",
    "exp": "v",
    "n": "v"
}

def isKeyword(token):
    return token in keywords

def isDelimiter(ch):
    return ch in delimiters

print("------------------------ LEXICAL ANALYZER - TOKENIZER -----------------------")

tokentable_global = []
tokentable_global.append(["Token No","Lexeme","Token","Line No"])

txt = open("input.txt","r")
tokens = txt.read()
count = 0
tkncount = 0
program = tokens.split("\n")

for line in program:
    err = 0
    prevct = tkncount
    count = count + 1
    tokentable_local = []
    print(f"At line {count}\nContent: {line}\n")
    tokens = line
    tokens = re.findall(r"[A-Za-z0-9_]+|[0-9]+|[(){}]|\S",tokens)
    print("Tokens found: ")
    tokentable = []
    tokentable.append(["Lexeme","Token"])

    for token in tokens:
        if isDelimiter(token):
            if token in ["{", "}", "(", ")", ";", ","]:
                tkncount +=1
                tokentable.append([token, "Delimiter"])
                tokentable_local.append([tkncount,token,"Delimiter", count])
            elif token in ["+", "-", "*", "/", "="]:
                if token in ["+", "-", "*", "/"]:
                    tkncount +=1
                    tokentable.append([token, "Arithmetic Operators"])
                    tokentable_local.append([tkncount,token, "Assignment Operator", count])
                elif token == "=":
                    tkncount +=1
                    tokentable.append([token, "Arithmetic Operators"])
                    tokentable_local.append([tkncount,token, "Assignment Operator", count])
            else: 
                tokentable.append([token,"Invalid Character [Error]"])
                print("Error Recovery: Line Ignored")
                err = 1
                break
            continue 
            
        else:
            if isKeyword(token):
                tkncount += 1
                tokentable.append([token, "Keyword"])
                tokentable_local.append([tkncount, token, "Keyword", count])
            else:
                if token.isnumeric():
                    tkncount += 1
                    tokentable.append([token, "Number"])
                    tokentable_local.append([tkncount,token, "Number", count])
                else:
                    if re.match("^[a-zA-Z][a-zA-Z0-9_]*",token) is not None:
                        tkncount +=1
                        tokentable.append([token, "Identifier"])
                        tokentable_local.append([tkncount,token, "Identifier", count])
                    else:
                        tokentable.append([token, "Invalid Character [Error]"])
                        print("Error Recovery: Line Ignored")
                        err = 1
                        break
    if err != 1:
        for entry in tokentable_local:
            tokentable_global.append(entry)
    else:
        tkncount = prevct

    print(tabulate(tokentable, headers="firstrow", tablefmt="grid"))
    print("\n-----------------------------------------------------")

print("\nGlobal Token Table: ")
print(tabulate(tokentable_global, headers="firstrow", tablefmt="grid"))

# For the parser tool
mth_flag = 0

with open('tokens1.txt','w') as f:
    str_to_load = ""

    for token in tokentable_global[1:]:
        if mth_flag > 0:
            mth_flag -=1
            continue

        sym = kwd_dict.get(token[1]) if kwd_dict.get(token[1]) is not None else token[1]
        str_to_load += str(sym) + ""
    
    f.write(f"{str_to_load}")
    print({str_to_load})