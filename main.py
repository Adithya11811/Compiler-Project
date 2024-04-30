import re
import warnings
from tabulate import tabulate
import copy
import sys
warnings.filterwarnings("ignore")

# Token types
tokens = [
    'PRINT', 'INTEGER', 'REAL', 'STRING', 'EQUAL','END','BEGIN','KEYWORD',
    'REAL_VALUE', 'INTEGER_VALUE', 'STRING_VALUE',
    'FOR', 'TO', 'COLON', 'SEMICOLON', 'LEFT_BRACKET','IDENTIFIER',
    'RIGHT_BRACKET','COMMA'
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

def removeLeftRecursion (rulesDiction):
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
            lhs_ = lhs +"'"
            while (lhs in rulesDiction.keys()) \
                or (lhs_ in store.keys()):
                lhs_ +="'"
            # For each rule in betaRules, it appends the new non-terminal lhs_
            # to the end of the rule and updates the original non-terminal's rules with the modified betaRules.
            for b in range(0, len(betaRules)):
                betaRules [b].append(lhs_)
            rulesDiction [lhs] = betaRules
            for a in range(0, len(alphaRules)):
                alphaRules [a].append(lhs_)
            alphaRules.append(['#'])
            store[lhs_] = alphaRules
    for left in store:
        # Result of left recursion will be stored in temp storage store
        rulesDiction [left] = store[left]
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
    global rules,nonterm_userdef,\
        term_userdef,diction,firsts
    if len(rule) != 0 and (rule is not None):
        if rule[0] in term_userdef:
            return rule[0]
        elif rule[0] == '#': # For epsilon
            return '#'
    # If the first symbol is a non-terminal, recursively calculate the FIRST set for the corresponding 
    #right-hand side rules in the grammar.
    if len(rule) != 0:
            if rule[0] in list(diction.keys()):
                fres = []
                rhs_rules = diction[rule[0]]
                for itr in rhs_rules:
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
                        ansNew = first (rule[1:])
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

def follow(nt):
    global start_symbol, rules, nonterm_userdef, \
    term_userdef, diction, firsts, follows
    # The solset set will store the symbols in the FOLLOW set for the given non-terminal.
    solset = set()
    # Handling the Start Symbol:
    if nt == start_symbol:
        solset.add('$')
    # Iterating Over Non-terminals and Production Rules:
    for curNT in diction:
        rhs = diction[curNT]
        for subrule in rhs:
            # Finding the Occurrences of the Target Non-terminal in a Rule:
            if nt in subrule:
                while nt in subrule:
                    index_nt = subrule.index(nt)
                    subrule = subrule[index_nt + 1:]
                    # Handling Symbols Following the Target Non-terminal:
                    if len(subrule) != 0:
                        res = first(subrule)

                    # Handling Epsilon Transitions in FIRST set
                        if '#' in res:
                            newList = []
                            res.remove('#')
                            ansNew = follow(curNT)
                            if ansNew != None:
                                if type(ansNew) is list:
                                    newList = res + ansNew
                                else:
                                    newList = res + [ansNew]
                            else:
                                newList = res
                            res = newList
                    else:
                        if nt != curNT:
                             res = follow(curNT)
                    # Adding Symbols to solset
                    if res is not None:
                        if type(res) is list:
                            for g in res:
                                solset.add(g)
                        else:
                            solset.add(res)
    return list(solset)

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
    # Open a file named rules.txt in write mode 
    # with open('rules.txt', 'w') as file:
       # file.write("Rules: \n")
    #for y in diction:
           # file.write(f"{y} -> {diction [y]}\n")
    # Remove left recursion
    diction = removeLeftRecursion (diction)
    # Remove left factoring
    diction = LeftFactoring (diction)
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

    print("================================================================================================")
    print("\nCalculated firsts: ")
    key_list = list(firsts.keys())
    index = 0
    for gg in firsts:
        print(f"first({key_list [index]}) "f"=> {firsts.get(gg)}")
        index += 1

def computeAllFollows():
    global start_symbol, rules, nonterm_userdef, \
        term_userdef, diction, firsts, follows
    for NT in diction:
        solset = set()
        sol = follow (NT)
        if sol is not None:
            for g in sol:
                solset.add(g)
        follows[NT] = solset
    print("\nCalculated follows: ")
    key_list = list(follows.keys())
    index = 0
    for gg in follows:
        print(f"follow({key_list[index]})"f" => {follows[gg]}")
        index + 1


def createParseTable():
    import copy
    global diction, firsts, follows, term_userdef 
    print("\n")
    print("===================================================================")
    print("Firsts and Follow Result table")
    # Printing FIRST and FOLLOW Sets
    mx_len_first = 0
    mx_len_fol = 0
    for u in diction:
        k1 = len(str(firsts[u]))
        k2 = len(str(follows[u]))
        if k1 > mx_len_first:
            mx_len_first = k1
        if k2 > mx_len_fol:
            mx_len_fol = k2
   # print(tabulate([["Non-T", "FIRST", "FOLLOW"]] + [[u, str(firsts [u]),
                    #str(follows [u])] for u in diction], headers='first row', tablefmt='fancy_grid'))
   # print("\n")
    #print("================================================================================")
    print(f"{{:<{10}}} "
        f"{{:<{mx_len_first + 5}}} "
        f"{{:<{mx_len_fol + 5}}}"
        .format("Non-T", "FIRST", "FOLLOW"))
    for u in diction:
        print(f"{{:<{10}}} "
            f"{{:<{mx_len_first + 5}}} "
            f"{{:<{mx_len_fol + 5}}}"
            .format(u, str(firsts[u]), str(follows[u])))
    ntlist = list(diction.keys())
    terminals = copy.deepcopy(term_userdef)
    terminals.remove('(')
    terminals.remove(')')
    terminals.remove('+')
    terminals.remove('-')
    terminals.remove('=')
    terminals.remove('1')
    
    terminals.append('$')
    
    mat = []
    for x in diction:
        row = []
        for y in terminals:
            row.append('')
        mat.append(row)
        
    grammar_is_LL = True

    # Filling in the Parsing Table:
    # Filling in the Parsing Table:
    for lhs in diction:
        rhs = diction[lhs]
        for y in rhs:
            res = first(y)
        #if res is not None:  # Add this line to check if res is not None
            if '#' in res:
                if type(res) == str:
                    firstFollow = []
                    fol_op = follows[lhs]
                    if fol_op is str:
                        firstFollow.append(fol_op)
                    else:
                        for u in fol_op:
                            firstFollow.append(u)
                        res = firstFollow
                else:
                    res.remove('#')
                    res = list(res) + \
                        list(follows[lhs])
        #else:
            # Handle the case when res is None
           # res = list(follows[lhs]) if isinstance(follows[lhs], list) else [follows[lhs]]
            ttemp = []
            if type(res) is str:
                ttemp.append(res)
                res = copy.deepcopy(ttemp)
            for c in res:
                xnt = ntlist.index(lhs)
                yt = terminals.index(c)
                if mat[xnt][yt] == '':
                    mat[xnt][yt] = mat[xnt][yt] + f"{lhs}->{' '.join(y)}"
                else:
                    if f"{lhs}->{y}" in mat[xnt][yt]:
                        continue
                    else:
                        grammar_is_LL = False
                    mat[xnt][yt] = mat[xnt][yt] \
                        + f",{lhs}->{' '.join(y)}"

    print("\nGenerated parsing table:\n")
    frmt = "{:>15}" * len(terminals)
    print(frmt.format(*terminals))
    j = 0
    for y in mat:
        frmt1 = "{:>15}" * len(y)
        print(f"{ntlist[j]} {frmt1.format(*y)}")
        j += 1
    return (mat, grammar_is_LL, terminals)

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
    lexer.pos += 1;
    if lexer.pos >= len(lexer_input):
        break

# print(lexer.get_tokens())
for token in lexer.get_tokens():
    print(token)

print(code)

tokens = lexer.get_tokens()

#hege acess madudu helthirudu
# print(tokens[0][1])

token_dict = {}
for token_type, token_value in tokens:
    if token_type in token_dict:
        if token_value not in token_dict[token_type]:
            token_dict[token_type].append(token_value)
    else:
        token_dict[token_type] = [token_value]

# print(token_dict)


# print(token_dict['BEGIN'][0])


# print(token_dict['BEGIN'][0])

rules = [
    "S -> "+token_dict['BEGIN'][0]+" statement_list "+token_dict['END'][0]+" ",
    "statement_list -> statement_list statement | statement",
    "statement -> declaration | assignment | "+token_dict['PRINT'][0]+" LIT | loop",
    "declaration -> type ID_list",
    "type -> "+token_dict['INTEGER'][0]+" | "+token_dict['REAL'][0]+" | "+token_dict['STRING'][0]+"",
    "ID_list -> ID_list , ID | ID",
    "assignment -> ID "+token_dict['EQUAL'][0]+" expression",
    "expression ->  IDENTIFIER | NUM | REAL_DIG | LIT",
    "loop -> "+token_dict['FOR'][0]+" ID "+token_dict['EQUAL'][0]+" NUM "+token_dict['TO'][0]+" NUM  statement",
    "ID -> "+token_dict['IDENTIFIER'][0]+" | "+token_dict['IDENTIFIER'][1]+" |"+token_dict['IDENTIFIER'][2]+" |"+token_dict['IDENTIFIER'][3]+" |"+token_dict['IDENTIFIER'][4]+" |"+token_dict['IDENTIFIER'][5]+" |"+token_dict['IDENTIFIER'][6]+" |"+token_dict['IDENTIFIER'][7]+"  ",
    "LIT -> "+token_dict['STRING_VALUE'][0]+" | "+token_dict['STRING_VALUE'][1]+" | "+token_dict['STRING_VALUE'][2]+" | "+token_dict['STRING_VALUE'][3]+" ",
    "NUM -> "+token_dict['INTEGER_VALUE'][0]+" | "+token_dict['INTEGER_VALUE'][1]+"| "+token_dict['INTEGER_VALUE'][2]+" | "+token_dict['INTEGER_VALUE'][3]+" | "+token_dict['INTEGER_VALUE'][4]+" ",
    "REAL_DIG -> "+token_dict['REAL_VALUE'][0]+" | "+token_dict['REAL_VALUE'][1]+" ",
    
]

# nonterm_userdef = ['S','T','M','B','D','A','E','F','G','W','P','Q','R','X','C']

# # # List of terminals in our grammar
# term_userdef = [id,arr1,arr2,arr3,'n','int','main()','End','for','if','begin','do','i','to',
#                 '(',')','+','-','endif','endfor','return','>','=','1',',',';']
diction = {}
firsts = {}
follows = {}
computeAllFirsts()
start_symbol = list(diction.keys())[0]
print(start_symbol)
computeAllFollows()
(parsing_table, result, tabTerm) = createParseTable()
# if code != None:

