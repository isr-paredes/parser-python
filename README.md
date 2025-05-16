# How to run the parser flex parser.l
## 

flex parser.l && bison -d -t -v parser.y && g++ -o oop_parser lex.yy.c parser.tab.c

## Step by step to compile
flex parser.l
bison -d -t -v parser.y
gcc lex.yy.c parser.tab.c


