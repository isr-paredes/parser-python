import ply.lex as lex
import ply.yacc as yacc

# --- Lexer ---

tokens = (
    'CLASS', 'DEF', 'IMPORT', 'FROM', 'RETURN', 'PASS',
    'IDENTIFIER', 'NUMBER', 'STRING_LITERAL',
    'COLON', 'LPAREN', 'RPAREN', 'COMMA', 'DOT', 'ASSIGN',
)

# Keywords
reserved = {
    'class': 'CLASS',
    'def': 'DEF',
    'import': 'IMPORT',
    'from': 'FROM',
    'return': 'RETURN',
    'pass': 'PASS',
}

t_COLON = r':'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','
t_DOT = r'\.'
t_ASSIGN = r'='

t_ignore = ' \t'

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING_LITERAL(t):
    r'(\"([^\\\n]|(\\.))*?\")|(\'([^\\\n]|(\\.))*?\')'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character {t.value[0]!r}")
    t.lexer.skip(1)

lexer = lex.lex()

# --- Parser ---

def p_program(p):
    '''program : segment_list'''
    p[0] = p[1]

def p_segment_list(p):
    '''segment_list : segment_list segment
                    | empty'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []

def p_segment(p):
    '''segment : misc_list class_def misc_list'''
    p[0] = ('segment', p[1], p[2], p[3])

def p_misc_list(p):
    '''misc_list : misc_list misc
                 | empty'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []

def p_class_def(p):
    '''class_def : CLASS IDENTIFIER inheritance_opt COLON suite'''
    p[0] = ('class_def', p[2], p[3], p[5])

def p_inheritance_opt(p):
    '''inheritance_opt : LPAREN base_classes RPAREN
                       | empty'''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = []

def p_base_classes(p):
    '''base_classes : IDENTIFIER
                    | base_classes COMMA IDENTIFIER'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_misc(p):
    '''misc : import_stmt
            | function_def
            | statement'''
    p[0] = p[1]

def p_import_stmt(p):
    '''import_stmt : IMPORT IDENTIFIER import_dots_opt
                   | FROM IDENTIFIER import_dots_opt IMPORT IDENTIFIER import_id_list_opt'''
    if p[1] == 'import':
        p[0] = ('import', p[2], p[3])
    else:
        p[0] = ('from_import', p[2], p[3], p[5], p[6])

def p_import_dots_opt(p):
    '''import_dots_opt : import_dots
                       | empty'''
    p[0] = p[1] if len(p) > 1 else []

def p_import_dots(p):
    '''import_dots : import_dots DOT IDENTIFIER
                   | DOT IDENTIFIER'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[2]]

def p_import_id_list_opt(p):
    '''import_id_list_opt : COMMA import_id_list
                          | empty'''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = []

def p_import_id_list(p):
    '''import_id_list : IDENTIFIER
                      | import_id_list COMMA IDENTIFIER'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_function_def(p):
    '''function_def : DEF IDENTIFIER LPAREN parameters_opt RPAREN COLON suite'''
    p[0] = ('function_def', p[2], p[4], p[7])

def p_parameters_opt(p):
    '''parameters_opt : parameters
                      | empty'''
    p[0] = p[1] if len(p) > 1 else []

def p_parameters(p):
    '''parameters : IDENTIFIER
                  | parameters COMMA IDENTIFIER'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_statement(p):
    '''statement : attribute_as
                 | simple_stmt
                 | function_def
                 | class_def'''
    p[0] = p[1]

def p_attribute_as(p):
    '''attribute_as : IDENTIFIER ASSIGN expression'''
    p[0] = ('assign', p[1], p[3])

def p_simple_stmt(p):
    '''simple_stmt : RETURN expression
                   | expression
                   | PASS'''
    if len(p) == 3:
        p[0] = ('return', p[2])
    else:
        p[0] = p[1]

def p_expression(p):
    '''expression : IDENTIFIER
                  | literal'''
    p[0] = p[1]

def p_literal(p):
    '''literal : NUMBER
               | STRING_LITERAL'''
    p[0] = p[1]

def p_suite(p):
    '''suite : suite statement
             | statement
    '''
    p[0] = p[1:]

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print(f"Syntax error at token {p.type}({p.value!r})")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()
