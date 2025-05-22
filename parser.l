%{
#include "y.tab.h"  
#include <string.h>
#include <stdlib.h>

#undef yywrap


int indent_stack[100];
int indent_top = 0;
int last_indent = 0;

void push_indent(int indent) {
    indent_stack[indent_top++] = indent;
}

void pop_indent() {
    if (indent_top > 0) indent_top--;
}

int count_leading_spaces(char *text) {
    int count = 0;
    for (int i = 0; text[i] == ' '; i++) count++;
    return count;
}

int yywrap(){
  return 1;
}

%}

%option noyywrap

/* Define tokens */
CLASS       class
DEF         def
SELF        self
PASS        pass
RETURN      return
IDENTIFIER  [a-zA-Z_][a-zA-Z0-9_]*
NUMBER      [0-9]+
NEWLINE     \n
WS          [ \t]+

%%

"class"         { return CLASS; }
"def"           { return DEF; }
"self"          { return SELF; }
"pass"          { return PASS; }
"return"        { return RETURN; }

{IDENTIFIER}    { yylval.str = strdup(yytext); return IDENTIFIER; }
{NUMBER}        { yylval.num = atoi(yytext); return NUMBER; }

":"             { return ':'; }
"("             { return '('; }
")"             { return ')'; }
","             { return ','; }
"="             { return '='; }
"."             { return '.'; }

{NEWLINE} {
    /* Handle indentation on new lines */
    int spaces = count_leading_spaces(yytext + 1);
    if (spaces > last_indent) {
        push_indent(spaces);
        last_indent = spaces;
        return INDENT;
    }
    else if (spaces < last_indent) {
        while (indent_top > 0 && indent_stack[indent_top-1] > spaces) {
            pop_indent();
            yylval.num = 0;
            last_indent = indent_top > 0 ? indent_stack[indent_top-1] : 0;
            return DEDENT;
        }
    }
    return NEWLINE;
}

{WS}            { /* skip whitespace */ }

.               { /* ignore any other characters */ }

%%

