import ply.lex as lex
import ply.yacc as yacc

# --- Lexer ---

tokens = (
    'EQ',  # ==
    'CLASS', 'DEF', 'IMPORT', 'FROM', 'RETURN', 'PASS', 'IF',
    'IDENTIFIER', 'NUMBER', 'STRING_LITERAL',
    'COLON', 'LPAREN', 'RPAREN', 'COMMA', 'DOT', 'ASSIGN',
    'OTHER',
)

reserved = {
    'class': 'CLASS',
    'def': 'DEF',
    'import': 'IMPORT',
    'from': 'FROM',
    'return': 'RETURN',
    'pass': 'PASS',
    'if': 'IF',
}

t_EQ = r'=='
t_ASSIGN = r'='  # Must come after t_EQ

t_COLON = r':'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','
t_DOT = r'\.'

t_ignore = ' \t'

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    print(f"Token: {t.type}({t.value}) at line {t.lineno}")
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    print(f"Token: NUMBER({t.value}) at line {t.lineno}")
    return t

def t_STRING_LITERAL(t):
    r'(\"([^\\\n]|(\\.))*?\")|(\'([^\\\n]|(\\.))*?\')'
    print(f"Token: STRING_LITERAL({t.value}) at line {t.lineno}")
    return t

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    # Return newline token if needed
    # return t

def t_OTHER(t):
    r'.'
    # For any other single character not matched above
    # print(f"Token: OTHER({t.value}) at line {t.lineno}")
    return t

def t_error(t):
    print(f"Illegal character {t.value[0]!r} at line {t.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()

# --- Precedence ---

precedence = (
    ('left', 'COMMA'),
    ('right', 'ASSIGN'),
    ('left', 'EQ'),
    ('left', 'DOT'),
)

# --- Parser ---

def p_program(p):
    '''program : segment_list'''
    p[0] = p[1]

def p_segment_list(p):
    '''segment_list : segment_list segment
                    | segment'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_segment(p):
    '''segment : misc_list class_def misc_list
               | misc_list'''
    if len(p) == 4:
        p[0] = ('segment', p[1], p[2], p[3])
    else:
        p[0] = ('segment', p[1])

def p_misc_list(p):
    '''misc_list : misc_list misc
                 | misc'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_class_def(p):
    '''class_def : CLASS IDENTIFIER inheritance_opt COLON suite_opt'''
    p[0] = ('class_def', p[2], p[3], p[5])

def p_inheritance_opt(p):
    '''inheritance_opt : LPAREN base_classes RPAREN
                       | empty'''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = []

def p_base_classes(p):
    '''base_classes : IDENTIFIER base_class_tail'''
    p[0] = [p[1]] + p[2]

def p_base_class_tail(p):
    '''base_class_tail : COMMA IDENTIFIER base_class_tail
                       | empty'''
    if len(p) == 4:
        p[0] = [p[2]] + p[3]
    else:
        p[0] = []

def p_suite_opt(p):
    '''suite_opt : suite
                 | empty'''
    p[0] = p[1] if len(p) > 1 else []

def p_suite(p):
    '''suite : statement
             | suite statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_statement(p):
    '''statement : misc
                 | function_def
                 | class_def'''
    p[0] = p[1]

def p_function_def(p):
    '''function_def : DEF IDENTIFIER LPAREN parameters_opt RPAREN COLON suite_opt'''
    p[0] = ('function_def', p[2], p[4], p[7])

def p_parameters_opt(p):
    '''parameters_opt : parameters
                      | empty'''
    p[0] = p[1] if len(p) > 1 else []

def p_parameters(p):
    '''parameters : IDENTIFIER parameter_tail'''
    p[0] = [p[1]] + p[2]

def p_parameter_tail(p):
    '''parameter_tail : COMMA IDENTIFIER parameter_tail
                      | empty'''
    if len(p) == 4:
        p[0] = [p[2]] + p[3]
    else:
        p[0] = []

def p_misc(p):
    '''misc : IDENTIFIER
            | NUMBER
            | STRING_LITERAL
            | COLON
            | LPAREN
            | RPAREN
            | COMMA
            | DOT
            | ASSIGN
            | EQ
            | OTHER'''
    p[0] = ('misc', p[1])

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print(f"Syntax error at token {p.type}({p.value!r}) at line {p.lineno}")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc(debug=True)
