%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// OOP detection flags
int found_class  = 0;
int found_method = 0;
int uses_self    = 0;

void yyerror(const char *s);
int yylex(void);
%}

%union {
    char* str;
}

%token <str> IDENTIFIER OTHER
%token CLASS DEF SELF COLON LPAREN RPAREN NEWLINE

%start program

%%

program:
    statements {
        printf("\n--- Analysis Result ---\n");
        if (found_class && found_method && uses_self) {
            printf("✅ OOP code detected.\n");
        } else {
            printf("❌ Not object-oriented.\n");
            if (!found_class)  printf("No class found.\n");
            if (!found_method) printf("No method with self found.\n");
            if (!uses_self)    printf("Self not used in method definitions.\n");
        }
    }
;

statements:
      /* empty input OK */
    | statements statement
;

statement:
      class_def NEWLINE
    | method_def NEWLINE
    | other_line NEWLINE   /* swallow anything else */
    | NEWLINE              /* blank line */
;

class_def:
    CLASS IDENTIFIER COLON {
        found_class = 1;
    }
    | CLASS IDENTIFIER LPAREN IDENTIFIER RPAREN COLON {
        found_class = 1;
    }
;

method_def:
    DEF IDENTIFIER LPAREN SELF RPAREN COLON {
        found_method = 1;
        uses_self    = 1;
    }
;

other_line:
      other_line other_line_token
    | other_line_token
;

other_line_token:
      OTHER
    | IDENTIFIER
    | COLON
    | LPAREN
    | RPAREN
;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Syntax error: %s\n", s);
}

int main(void) {
    return yyparse();
}
