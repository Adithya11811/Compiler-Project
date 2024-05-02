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

firsts = {'S': {'BEGIN'}, 'statement_list': {'REAL', 'E', 'D', 'I', 'FOR', 'X', 'STRING', 'Y', 'INTEGER', 'C', 'A', 'B', 'PRINT'}, 'st_li': {'REAL', 'E', 'D', 'I', 'FOR', 'X', 'STRING', 'Y', 'INTEGER', 'C', 'A', 'B', '#', 'PRINT'}, 'statement': {'REAL', 'E', 'D', 'I', 'FOR', 'X', 'STRING', 'Y', 'INTEGER', 'C', 'A', 'B', 'PRINT'}, 'declaration': {'REAL', 'STRING', 'INTEGER'}, 'type': {'REAL', 'STRING', 'INTEGER'}, 'ID_List': {'E', 'D', 'I', 'X', 'Y', 'C', 'A', 'B'}, 'idli': {',', '#'}, 'assignment': {'E', 'D', 'I', 'X', 'Y', 'C', 'A', 'B'}, 'expression': {'E', '6', 'D', '1', 'I', 'HELLO', '-3.65E-8', 'X', 'Y', '4.567', 'C', 'A', '2', 'text1', '5', 'B', '4', None}, 'loop': {'FOR'}, 'ID': {'E', 'D', 'I', 'X', 'Y', 'C', 'A', 'B'}, 'LIT': {'text1', 'HELLO'}, 'NUM': {'6', '1', '2', '5', '4'}, 'REAL_DIG': {'4.567', '-3.65E-8'}}


#idu corrected
diction = {'S': [['BEGIN', 'statement_list', 'END']], 'statement_list': [['statement', 'st_li']], 'st_li': [['statement', 'st_li'], ['#']], 'statement': [['declaration'], ['assignment'], ['PRINT', 'LIT'], ['loop']], 'declaration': [['type', 'ID_List']], 'type': [['INTEGER'], ['REAL'], ['STRING']], 'ID_List': [['ID', 'idli']], 'idli': [[',', 'ID', 'idli'], ['#']], 'assignment': [['ID', ':=', 'expression']], 'expression': [['ID'], ['NUM'], ['REAL_DIG'], ['LIT']], 'loop': [['FOR', 'ID', ':=', 'NUM', 'TO', 'NUM', 'statement']], 'ID': [['A'], ['B'], ['C'], ['D'], ['E'], ['X'], ['Y'], ['I']], 'LIT': [['HELLO'], ['text1'], ['hello', 'there'], ['Strings', 'are', '[X]', 'and', '[Y]']], 'NUM': [['2'], ['4'], ['6'], ['1'], ['5']], 'REAL_DIG': [['-3.65E-8'], ['4.567']]}

# diction1= {
#     'S': [['BEGIN', 'statement_list', 'END']],
#     'statement_list': [['statement', 'st_li']],
#     'st_li': [['statement', 'st_li'], ['#']],
#     'statement': [['declaration'], ['assignment'], ['PRINT', 'LIT'], ['loop']],
#     'declaration': [['type', 'ID_List']],
#     'type': [['INTEGER'], ['REAL'], ['STRING']],
#     'ID_List': [['ID', 'idli']],
#     'idli': [[',', 'ID', 'idli'], ['#']],
#     'assignment': [['ID', ':=', 'expression']],
#     'expression': [['ID'], ['NUM'], ['REAL_DIG'], ['LIT']],
#     'loop': [['FOR', 'ID', ':=', 'NUM', 'TO', 'NUM', 'statement']],
#     'ID': [['A'], ['B'], ['C'], ['D'], ['E'], ['X'], ['Y'], ['I']],
#     'LIT': [['HELLO'], ['text1'], ['hello', 'there'], ['Strings', 'are', '[X]', 'and', '[Y]']],
#     'NUM': [['2'], ['4'], ['6'], ['1'], ['5']],
#     'REAL_DIG': [['-3.65E-8'], ['4.567']]
# }
# print(diction1.items() == diction.items())
# print(diction1.items())
# print("\n")
# print(diction.items())


nonterm_userdef = ['S', 'statement_list', 'statement', 'declaration', 'type', 'ID_List', 'assignment', 'expression',
                   'loop', 'ID', 'LIT', 'NUM', 'REAL_DIG', 'st_li', 'idli']
term_userdef = ['BEGIN', 'END', 'PRINT', '2', '4', '6', '1', '5', '-3.65E-8', '4.567', ':=', 'FOR', 'TO', 'A', 'B', 'C',
                'D', 'E', 'X', 'Y', 'I', 'HELLO', 'text1', 'hello there', 'Strings are [X] and [Y]', "#", "INTEGER",
                "REAL", "STRING", ","]

start_symbol = 'S'
follows = {}

computeAllFollows()

def compare_dicts(dict1, dict2):
    if len(dict1) != len(dict2):
        return False
    for key in dict1:
        if key not in dict2:
            print(f"Key {key} not in dict2")
            return False
        if isinstance(dict1[key], list):
            if not isinstance(dict2[key], list):
                print(f"Value of key {key} in dict1 is a list, but not in dict2")
                return False
            if len(dict1[key]) != len(dict2[key]):
                print(f"Length of list of key {key} in dict1 is different from that in dict2")
                return False
            for i in range(len(dict1[key])):
                if dict1[key][i] != dict2[key][i]:
                    print(f"Value of key {key} in dict1 is different from that in dict2")
                    print("dict1[key]:", dict1[key])
                    print("dict2[key]:", dict2[key])
                    return False
        else:
            if dict1[key] != dict2[key]:
                print(f"Value of key {key} in dict1 is different from that in dict2")
                print("dict1[key]:", dict1[key])
                print("dict2[key]:", dict2[key])
                return False
    return True

print(compare_dicts(diction1, diction))
