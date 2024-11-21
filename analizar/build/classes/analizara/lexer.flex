package analizara;
import static analizara.Token.*;
%%
%class Lexer
%type Token

L = [a-zA-Z_]
D = [0-9]

WHITE = [ \t\r\n]

%{
public String tipo;
%}

%%
{WHITE} {/*Ingore*/}
"//".* {/*Ignore*/}
"==" {return OPERADORCOMPARACION;}
"+" {return SUMA;}
"-" {return RESTA;}
"*" {return MULTIPLICACION;}
"/" {return DIVICION;}
"^" {return POTENCIA;}
"<=" {return MENORIGUAL;}
"=" {return Igual;}
"%" {return Modulo;}
"++"       {return Incremento;}
"--"       {return Decremento;}
"<"        {return MenorQue;}
">"        {return MayorQue;}
">="       {return MayorOIgual;}
"!="       {return Diferente;}
"&&"       {return And;}
"||"       {return Or;}
"."        {return Punto;}
""""       {return ComillasDobles;}
"//".*     {/* Ignore single-line comment */}
"/*"       {return ComentarioParrafoAbre;}
"*/"       {return ComentarioParrafoCierra;}
";" {return FINALLINEA;}

importar     {tipo=yytext(); return IMPORT;}
paquete     {tipo=yytext(); return PACK;}
if         {tipo=yytext(); return Reservadas;}
else       {tipo=yytext(); return Reservadas;}
while      {tipo=yytext(); return Reservadas;}

publico      {tipo=yytext(); return PUBLIC;}



{L}({L}|{D})* {tipo=yytext();
return ID;}

("(-"{D}+")") |{D} + {tipo=yytext();
return INT;}

. {return ERROR;}
