import re
import warnings
from tabulate import tabulate
import csv

warnings.filterwarnings("ignore")

# Token types
tokens = [
    'PRINT', 'INTEGER', 'REAL', 'STRING', 'EQUAL', 'END', 'BEGIN', 'KEYWORD',
    'REAL_VALUE', 'INTEGER_VALUE', 'STRING_VALUE',
    'FOR', 'TO', 'COLON', 'SEMICOLON', 'LEFT_BRACKET', 'IDENTIFIER',
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


def removeLeftRecursion(rulesDiction):
    print("rulesDiction: ", rulesDiction)
    store = {}
    for lhs in rulesDiction:
        # alphaRules will store the rules with left recursion.
        # betaRules will store the rules without left recursion.
        # allrhs is the list of right-hand sides for the current non-terminal lhs
        alphaRules = []
        betaRules = []
        allrhs = rulesDiction[lhs]
        # Separate into 2 groups those with left recursion and those without
        for subrhs in allrhs:
            if subrhs[0] == lhs:
                alphaRules.append(subrhs[1:])
            else:
                betaRules.append(subrhs)
        ''' If there are rules with left recursion (alphaRules is not empty), it creates a new non-terminal symbol (lhs_) to replace the left-recursive rules. The loop ensures that the new symbol doesn't already exist in the original grammar or in the temporary storage (store).'''

        if len(alphaRules) != 0:
            lhs_ = lhs + "'"
            while (lhs in rulesDiction.keys()) \
                    or (lhs_ in store.keys()):
                lhs_ += "'"
            # For each rule in betaRules, it appends the new non-terminal lhs_
            # to the end of the rule and updates the original non-terminal's rules with the modified betaRules.
            for b in range(0, len(betaRules)):
                betaRules[b].append(lhs_)
            rulesDiction[lhs] = betaRules
            for a in range(0, len(alphaRules)):
                alphaRules[a].append(lhs_)
            alphaRules.append(['#'])
            store[lhs_] = alphaRules
    for left in store:
        # Result of left recursion will be stored in temp storage store
        rulesDiction[left] = store[left]
    return rulesDiction


def LeftFactoring(rulesDiction):
    # This dictionary will store the left-factored grammar rules.
    newDict = {}
    for lhs in rulesDiction:
        # Group right-hand sides (rhs) based on the first terminal/non-terminal in each:
        allrhs = rulesDiction[lhs]
        temp = dict()
        for subrhs in allrhs:
            if subrhs[0] not in list(temp.keys()):
                temp[subrhs[0]] = [subrhs]
            else:
                temp[subrhs[0]].append(subrhs)
        # Process each group:
        new_rule = []
        tempo_dict = {}
        for term_key in temp:
            allStartingWithTermKey = temp[term_key]
            # If a group has more than one rule, perform left factoring:
            if len(allStartingWithTermKey) > 1:
                lhs_ = lhs + "'"
                while (lhs in rulesDiction.keys()) \
                        or (lhs_ in tempo_dict.keys()):
                    lhs_ += "'"
                new_rule.append([term_key, lhs_])
                ex_rules = []
                for g in temp[term_key]:
                    ex_rules.append(g[1:])
                tempo_dict[lhs_] = ex_rules
            # If a group has only one rule, keep it unchanged:
            else:
                new_rule.append(allStartingWithTermKey[0])
        # Update the newDict with the left-factored rules:
        newDict[lhs] = new_rule
        for key in tempo_dict:
            newDict[key] = tempo_dict[key]
    return newDict


def first(rule):
    global rules, nonterm_userdef, \
        term_userdef, diction, firsts
    if len(rule) != 0 and (rule is not None):
        if rule[0] in term_userdef:
            return rule[0]
        elif rule[0] == '#':  # For epsilon
            return '#'
    # If the first symbol is a non-terminal, recursively calculate the FIRST set for the corresponding
    # right-hand side rules in the grammar.

    if len(rule) != 0:
        if rule[0] in list(diction.keys()):
            fres = []
            rhs_rules = diction[rule[0]]
            for itr in rhs_rules:
                if [['HELLO'], ['text1'], ['hello', 'there'], ['Strings', 'are', '[X]', 'and', '[Y]']] == rhs_rules:
                    print("itr: ", itr)
                indivRes = first(itr)

                if type(indivRes) is list:
                    for i in indivRes:
                        fres.append(i)
                else:
                    fres.append(indivRes)

            '''
            If the FIRST set of the non-terminal contains epsilon ('#'), remove it from the set.
            If the remaining symbols in the rule can derive epsilon, add epsilon back to the set.
            '''

            if '#' not in fres:
                return fres
            else:
                newList = []
                fres.remove('#')
                if len(rule) > 1:
                    ansNew = first(rule[1:])
                    if ansNew != None:
                        if type(ansNew) is list:
                            newList = fres + ansNew
                        else:
                            newList = fres + [ansNew]
                    else:
                        newList = fres
                    return newList
                fres.append('#')
                return fres


def computeAllFirsts():
    global rules, nonterm_userdef, \
        term_userdef, diction, firsts
    for rule in rules:
        k = rule.split("->")
        k[0] = k[0].strip()
        k[1] = k[1].strip()
        rhs = k[1]
        multirhs = rhs.split('|')
        for i in range(len(multirhs)):
            multirhs[i] = multirhs[i].strip()
            multirhs[i] = multirhs[i].split()
        diction[k[0]] = multirhs
    print(f"\nRules: \n")
    for y in diction:
        print(f"{y}->{diction[y]}")
    # Remove left recursion
    diction = removeLeftRecursion(diction)
    # Remove left factoring
    diction = LeftFactoring(diction)
    for y in list(diction.keys()):
        t = set()
        for sub in diction.get(y):
            res = first(sub)
            if res != None:
                if type(res) is list:
                    for u in res:
                        t.add(u)
                else:
                    t.add(res)
        firsts[y] = t

def createParseTable():
    import copy
    global diction, firsts, follows, nonterm_userdef, term_userdef

    # Combine terminals and non-terminals
    all_symbols = nonterm_userdef + term_userdef + ['$']

    # Print FIRST and FOLLOW Sets
    mx_len_first = max(len(str(f)) for f in firsts.values())
    mx_len_fol = max(len(str(f)) for f in follows.values())

    print("Firsts and Follow Result table")
    print(f"{'Non-T':<10} {'FIRST':<{mx_len_first + 5}} {'FOLLOW':<{mx_len_fol + 5}}")
    for nt in nonterm_userdef:
        print(f"{nt:<10} {str(firsts[nt]):<{mx_len_first + 5}} {str(follows[nt]):<{mx_len_fol + 5}}")

    grammar_is_LL = True

    # Initialize parsing table
    parsing_table = {nt: {t: '' for t in term_userdef + ['$']} for nt in nonterm_userdef}

    # Filling in the Parsing Table
    for lhs, rhs_list in diction.items():
        for rhs in rhs_list:
            first_rhs = first(rhs)
            if first_rhs is not None:
                if not isinstance(first_rhs, list):
                    first_rhs = [first_rhs]
                for term in first_rhs:

                    if term != '#':
                        if parsing_table[lhs][term] == "":
                            parsing_table[lhs][term] += f"{lhs} -> {' '.join(rhs)}"
                        else:
                            if f"{lhs}->{rhs}" in parsing_table[lhs][term]:
                                continue
                            else:
                                grammar_is_LL = False
                                parsing_table[lhs][term] = parsing_table[lhs][term] \
                                                           + f",{lhs}->{' '.join(rhs)}"
                if '#' in first_rhs:

                    for follow_symbol in follows[lhs]:
                        if parsing_table[lhs][follow_symbol] == '':
                            parsing_table[lhs][follow_symbol] = f"{lhs} -> {' '.join(rhs)}"
                        else:
                            if f"{lhs}->{rhs}" in parsing_table[lhs][follow_symbol]:
                                continue
                            else:
                                grammar_is_LL = False
                                parsing_table[lhs][follow_symbol] += f"{lhs} -> {' '.join(rhs)}"

    # Print the generated parsing table
    table_headers = [''] + term_userdef + ['$']
    table_data = [[nt] + [parsing_table[nt][t] for t in term_userdef + ['$']] for nt in nonterm_userdef]
    print("\nGenerated parsing table:")
    print(tabulate(table_data, headers=table_headers))

    with open('parsing_table.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(table_headers)
        writer.writerows(table_data)

    # Check if grammar is LL(1)
    print("\nIs the grammar LL(1)? ", grammar_is_LL)

    return parsing_table, grammar_is_LL, term_userdef + ['$']


def computeAllFollows():
    global start_symbol, rules, nonterm_userdef, term_userdef, diction, firsts, follows
    for NT in diction:
        solset = set()
        sol = follow(NT, set())
        if sol is not None:
            solset |= sol
        follows[NT] = solset
    print("\nCalculated follows:")
    for NT, follow_set in follows.items():
        print(f"follow({NT}) => {follow_set}")

def follow(nT, visited):
    global firsts, diction, follows, term_userdef
    follow_ = set()
    if nT == start_symbol:
        follow_ = follow_ | {'$'}
    for nt, rhs in diction.items():
        for alt in rhs:
            if nT in alt:
                idx = alt.index(nT)
                if idx < len(alt) - 1:  # If nT is not the last symbol in alt
                    following_str = alt[idx + 1:]
                    for symbol in following_str:
                        if symbol in term_userdef:  # If symbol is a terminal
                            follow_ |= {symbol}
                            break
                        else:  # If symbol is a non-terminal
                            firsts_of_symbol = firsts.get(symbol, set())
                            follow_ |= firsts_of_symbol - {'#'}
                            if '#' not in firsts_of_symbol:
                                break
                else:  # If nT is the last symbol in alt
                    if nt != nT and nt not in visited:
                        visited.add(nt)
                        follow_ |= follow(nt, visited)
    return follow_


def validateStringUsingStackBuffer(parsing_table, grammarll1,
                                   table_term_list, input_string,
                                   term_userdef, start_symbol):
    print(f"Validate String:\n\n{input_string}\n")
    print("Look into the parsing.txt file for the parsing steps")
    print("\n")
    if not grammarll1:
        return f"Input String = \"{input_string}\"\nGrammar is not LL(1)\n"

    stack = [start_symbol, '$']
    input_string = input_string.split()
    input_string.reverse()
    buffer = ['$'] + input_string

    # Writing Header for Parsing Steps:
    print("{:>70} {:>10} {:>20}\n".format("Input\t\t\t\t\tt\t\t\t\t\t", "Stack\t\t", "Action"))
    print()

    while True:
        # Checking for Valid End Condition:
        if stack == ['$'] and buffer == ['$']:
            print("{:>100} | {:>25} | {:>30}\n".format(' '.join(buffer), ' '.join(stack), "Valid"))
            return "Valid String!"


        # Parsing Non-terminals:
        elif stack[0] not in term_userdef:
            non_terminal = stack[0]
            terminal = buffer[-1]
            if non_terminal in parsing_table and terminal in table_term_list:
                entry = parsing_table[non_terminal][terminal]
                if entry:
                    print("{:>100} | {:>25} | {:>30}\n".format(' '.join(buffer), ' '.join(stack),
                                                               f"T[{non_terminal}][{terminal}]={entry}"))
                    lhs_rhs = entry.split(" -> ")
                    rhs = lhs_rhs[1].replace('#', '').strip().split()
                    stack = rhs + stack[1:]
                else:
                    return f"Invalid String! No rule at Table[{non_terminal}][{terminal}]."
            else:
                return f"Invalid String! Non-terminal '{non_terminal}' or terminal '{terminal}' not found in parsing table."

        # Matching Terminals:
        else:
            if stack[0] == buffer[-1]:
                print("{:>100} | {:>25} | {:>30}\n".format(' '.join(buffer), ' '.join(stack),
                                                           f"Matched: {stack[0]}"))
                buffer.pop()
                stack.pop(0)
            else:
                return "Invalid String! Unmatched terminal symbols\n"


# Test the lexer
code = """
BEGIN 
PRINT "HELLO" 
INTEGER A , B , C 
REAL D , E 
STRING X , Y 
A := 2 
B := 5
C := 6 
D := -3.65E-8 
E := 4.567 
X := "text1" 
Y := "hello_there" 
FOR I := 1 TO 5 
PRINT "Strings_are_[X]_and_[Y]" 
END 
"""

lexer_input = code

lexer = Lexer()
lexer.input(lexer_input)

# Tokenize
while True:
    lexer.token()
    lexer.pos += 1;
    if lexer.pos >= len(lexer_input):
        break

for token in lexer.get_tokens():
    print(token)

print(code)

tokens = lexer.get_tokens()

token_dict = {}
for token_type, token_value in tokens:
    if token_type in token_dict:
        if token_value not in token_dict[token_type]:
            token_dict[token_type].append(token_value)
    else:
        token_dict[token_type] = [token_value]


rules = [
    "S -> "+token_dict['BEGIN'][0]+" statement_list "+token_dict['END'][0]+" ",
    "statement_list -> statement st_li",
    "st_li -> statement st_li | #",
    "statement -> declaration | assignment | PRINT LIT | loop",
    "declaration -> type ID_List",
    "type -> INTEGER | REAL | STRING",
    "ID_List -> ID idli",
    "idli -> , ID idli | #",
    "assignment -> ID := expression",
    "expression ->  ID | NUM | REAL_DIG | LIT",
    "loop -> FOR ID := NUM TO  NUM  statement",
    "ID -> "+token_dict["IDENTIFIER"][0]+" | "+token_dict["IDENTIFIER"][1]+"  | "+token_dict["IDENTIFIER"][2]+"   | "+token_dict["IDENTIFIER"][3]+"  | "+token_dict["IDENTIFIER"][4]+"  | "+token_dict["IDENTIFIER"][5]+"  | "+token_dict["IDENTIFIER"][6]+" | "+token_dict["IDENTIFIER"][7]+"",
    'LIT -> '+token_dict["STRING_VALUE"][0]+'  | '+token_dict["STRING_VALUE"][1]+' |  '+token_dict["STRING_VALUE"][2]+' | '+token_dict["STRING_VALUE"][3]+' ',
    "NUM -> "+token_dict["INTEGER_VALUE"][0]+" | "+token_dict["INTEGER_VALUE"][1]+" | "+token_dict["INTEGER_VALUE"][2]+" | "+token_dict["INTEGER_VALUE"][3]+"  ",
    "REAL_DIG -> "+token_dict["REAL_VALUE"][0]+" | "+token_dict["REAL_VALUE"][1]+" ",
]

# print(token_dict)
nonterm_userdef = ['S', 'statement_list', 'statement', 'declaration', 'type', 'ID_List', 'assignment', 'expression',
                   'loop', 'ID', 'LIT', 'NUM', 'REAL_DIG', 'st_li', 'idli']
term_userdef = ['BEGIN', 'END', 'PRINT', '2', '4', '6', '1', '5', '-3.65E-8', '4.567', ':=', 'FOR', 'TO', 'A', 'B', 'C',
                'D', 'E', 'X', 'Y', 'I', '"HELLO"', '"text1"', '"hello_there"', '"Strings_are_[X]_and_[Y]"', "#",
                "INTEGER",
                "REAL", "STRING", ","]

diction = {}
firsts = {}
follows = {}
computeAllFirsts()
print("================================================================================================")
print("\nCalculated firsts: ")
key_list = list(firsts.keys())
index = 0
for gg in firsts:
    print(f"first({key_list[index]}) "f"=> {firsts.get(gg)}")
    index += 1


start_symbol = list(diction.keys())[0]
computeAllFollows()
print("\n \n")
print("================================================================================================")
print("\n \n")
(parsing_table, result, tabTerm) = createParseTable()

if code != None:
    validity = validateStringUsingStackBuffer(parsing_table, result,
                                              tabTerm, code,
                                              term_userdef, start_symbol)
    print(validity)
else:
    print("No input String detected")