%{
#include <stdio.h>
#include <stdlib.h>

void yyerror(const char *s);
int yylex(void);

typedef struct {
    char *str;
    int num;
} YYSTYPE;

#define YYSTYPE YYSTYPE

%}

%union {
    char *str;
    int num;
}

%token <str> IDENTIFIER
%token <num> NUMBER
%token CLASS DEF SELF PASS RETURN
%token INDENT DEDENT NEWLINE

%left '='
%left '.'

%%

program:
    /* empty */
    | program class_def
    ;

class_def:
    CLASS IDENTIFIER inheritance_opt ':' NEWLINE INDENT class_suite DEDENT
    ;

inheritance_opt:
    /* empty */
    | '(' base_class_list ')'
    ;

base_class_list:
    IDENTIFIER
    | base_class_list ',' IDENTIFIER
    ;

class_suite:
    /* empty */
    | class_suite class_stmt
    ;

class_stmt:
    func_def
    | assignment
    | PASS NEWLINE
    ;

func_def:
    DEF IDENTIFIER '(' parameters_opt ')' ':' NEWLINE INDENT func_suite DEDENT
    ;

parameters_opt:
    /* empty */
    | parameters
    ;

parameters:
    IDENTIFIER
    | parameters ',' IDENTIFIER
    ;

func_suite:
    /* empty */
    | func_suite func_stmt
    ;

func_stmt:
    assignment
    | RETURN expression NEWLINE
    | PASS NEWLINE
    ;

assignment:
    IDENTIFIER '=' expression NEWLINE
    ;

expression:
    IDENTIFIER
    | NUMBER
    | expression '.' IDENTIFIER
    | IDENTIFIER '(' arguments_opt ')'
    ;

arguments_opt:
    /* empty */
    | arguments
    ;

arguments:
    expression
    | arguments ',' expression
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}

int main() {
    return yyparse();
}
