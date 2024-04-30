rules = [
    "S -> BEGIN ",
    "T -> int",
    "M -> main()",
    "B -> begin",
    "D -> End",
    "A -> E F G W X",
    "E -> T " +arr1+ " ; ",
    "F -> T " +id+ " = " +arr2+ " ; ",
    "G -> for C do ",
    "C -> i = 1 to n - 1",
    "W -> if "+arr3+" > "+id+" P Q R ",
    "P -> "+id+ " = "+arr3+" ; ",
    "Q -> endif",
    "R -> endfor",
    "X -> return ( "+id+ " )"
]
tokens = [
    'PRINT', 'INTEGER', 'REAL', 'STRING', 'EQUAL','END','BEGIN','KEYWORD'
    'IDENTIFIER', 'INTEGER_VALUE', 'REAL_VALUE', 'STRING_VALUE',
    'FOR', 'TO', 'COLON', 'SEMICOLON', 'LEFT_BRACKET',
    'RIGHT_BRACKET', 'COMMA'
]