%{
#include "parser.tab.h"
%}

%%
"class"                { return CLASS; }
"def"                  { return DEF; }
"self"                 { return SELF; }
[a-zA-Z_][a-zA-Z0-9_]* { yylval.str = strdup(yytext); return IDENTIFIER; }
":"                    { return COLON; }
"("                    { return LPAREN; }
")"                    { return RPAREN; }
[\r\n]+                { return NEWLINE; }
[ \t]+                 { /* skip spaces & tabs */ }
.+                     { /* any other single character */ return OTHER; }
%%
