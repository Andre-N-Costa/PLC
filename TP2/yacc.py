import ply.yacc as yacc
import re
import sys

from lex import tokens


"""
Script  : Decls SubPs Corpo
         | Decls Corpo
         | SubPs Corpo
         | Corpo
Decls   : Decl
         | Decls Decl
Decl    : MATRIZ NOME SA Exp SF SA Exp SF
         | ARRAY NOME SA Exp SF
         | INT NOME
         | INT NOME ART Exp
Atr     : NOME SA Exp SF SA Exp SF ATR Exp
         | NOME SA Exp SF ATR Exp
         | NOME ATR Exp
         | NOME SA Exp SF ATR INPUT
         | NOME SA Exp SF SA Exp SF ATR INPUT
         | NOME ATR INPUT
SubPs   : SubP
         | SubPs SubP
SubP    : SUBP NOME PA PF DELIM Decls Corpo DELIM
         | SUBP NOME PA PF DELIM Corpo DELIM
Corpo   : Proc
         | Corpo Proc
Proc    : Exp
         | Atr
         | Output
         | Se
         | Enquanto
Exp     : PA Exp PF
         | Var
         | NUM
         | Cond
         | Call
         | Exp SOMA Exp
         | Exp MULT Exp
         | Exp SUB Exp
         | Exp DIV Exp
         | Exp MOD Exp
Output  : OUTPUT PA Exp PF
         | OUTPUTAM PA NOME PF
Se      : SE Cond ENTAO Corpo DELIM
         | SE Cond ENTAO Corpo SENAO ENTAO Corpo DELIM
Enquanto: ENQUANTO Cond FAZ Corpo DELIM
Var     : NOME SA Exp SF SA Exp SF
         | NOME SA Exp SF
         | NOME
Cond    : PA Cond PF
         | Exp MAIOR Exp
         | Exp MENOR Exp
         | Exp IGUAL Exp
         | Exp MENORIG Exp
         | Exp MAIORIG Exp
         | Exp DIF Exp
         | Exp E Exp
         | Exp OU Exp
         | NO Exp
Call    : CALL PA NOME PF
"""

def p_Script(p):
    "Script : Corpo"
    parser.assembly = f'start\n{p[1]}stop'
  
def p_Script_Decls_SubPs(p):
    "Script : Decls SubPs Corpo"
    parser.assembly = f'{p[1]}\nstart\n{p[3]}stop'

def p_Script_Decls(p):
    "Script : Decls Corpo"
    parser.assembly = f'{p[1]}\nstart\n{p[2]}stop'

def p_Script_SubPs(p):
    "Script : SubPs Corpo"
    parser.assembly = f'start\n{p[2]}stop'

def p_Decls(p):
    "Decls : Decl"
    p[0] = f'{p[1]}'

def p_Decls_Varias(p):
    "Decls : Decls Decl"
    p[0] = f'{p[1]}{p[2]}'

def p_Decl_Matriz(p):
    "Decl : MATRIZ NOME SA NUM SF SA NUM SF"
    if p[2] not in p.parser.log:
        p.parser.log.update({p[2] : (p.parser.gp, int(p[4]), int(p[7]))})
        tam = int(p[4])*int(p[7])
        p[0] = f'PUSHN {str(tam)}\n'
        p.parser.gp += tam
    else:
        print("Erro! Variável já existe.")
        parser.success = False


def p_Decl_Array(p):
    "Decl : ARRAY NOME SA NUM SF"
    if p[2] not in p.parser.log:
        p.parser.log.update({p[2] : (p.parser.gp, int(p[4]))})
        p[0] = f'PUSHN {p[4]}\n'
        p.parser.gp += int(p[4])
    else:
        print("Erro! Variável {p[2]} já existe.")
        parser.success = False


def p_Decl_Int(p):
    "Decl : INT NOME"
    if p[2] not in p.parser.log:
        p.parser.log.update({p[2] : p.parser.gp})
        p[0] = 'PUSHI 0\n'
        p.parser.vars.append(p[2])
        p.parser.gp += 1
    else:
        print(f"ERRO! Variável {p[2]} já existe.")
        parser.success = False

def p_Decl_Int_Atr(p):
    "Decl : INT NOME ATR Exp"
    if p[2] not in p.parser.log:
        p.parser.log.update({p[2] : p.parser.gp})
        p[0] = p[4]
        p.parser.vars.append(p[2])
        p.parser.gp += 1
    else:
        print(f"ERRO! Variável {p[2]} já existe.")
        parser.success = False

def p_Matriz_Atr(p):
    "Atr : NOME SA Exp SF SA Exp SF ATR Exp"
    if p[1] in p.parser.log:
        if p[1] not in p.parser.vars and len(p.parser.log.get(p[1])) == 3:
            c = p.parser.log.get(p[1])[2]
            p[0] = f'PUSHGP\nPUSHI {p.parser.log.get(p[1])[0]}\nPADD\n{p[3]}PUSHI {c}\nMUL\n{p[6]}ADD\n{p[9]}STOREN\n'
        else:
            print(f"Erro: Variável {p[1]} não é uma matriz.")
            parser.success = False
    else:
        print("Erro: Variável ainda não existe.")
        parser.success = False

def p_Array_Atr(p):
    "Atr : NOME SA Exp SF ATR Exp"
    if p[1] in p.parser.log:
        if p[1] not in p.parser.vars and len(p.parser.log.get(p[1])) == 2:
            p[0] = f'PUSHGP\nPUSHI {p.parser.log.get(p[1])[0]}\nPADD\n{p[3]}{p[6]}STOREN\n'
        else:
            print(f"Erro: Variável {p[1]} não é um array.")
            parser.success = False
    else:
        print("Erro: Variável ainda não existe.")
        parser.success = False

def p_Atr_Exp(p):
    "Atr : NOME ATR Exp"
    if p[2] not in p.parser.log:
        p[0] = f"{p[3]}\nSTOREG {p.parser.log.get(p[1])}\n"
        p.parser.vars.append(p[1])
        p.parser.gp += 1
    else:
        print(f"ERRO! Variável {p[1]} já existe.")
        parser.success = False

def p_Atr_Array_I(p):
    "Atr : NOME SA Exp SF ATR INPUT"
    if p[1] in p.parser.log:
        if p[1] not in p.parser.vars and len(p.parser.log.get(p[1])) == 2:
            p[0] = f'PUSHGP\nPUSHI {p.parser.log.get(p[1])[0]}\nPADD\n{p[3]}READ\nATOI\nSTOREN\n'
        else:
            print(f"Erro: Variável {p[1]} não é um array.")
            parser.success = False
    else:
        print("Erro: Variável ainda não existe.")
        parser.success = False


def p_Atr_Matriz_I(p):
    "Atr : NOME SA Exp SF SA Exp SF ATR INPUT"
    if p[1] in p.parser.log:
        if p[1] not in p.parser.vars and len(p.parser.log.get(p[1])) == 3:
            c = p.parser.log.get(p[1])[2]
            p[0] = f'PUSHGP\nPUSHI {p.parser.log.get(p[1])[0]}\nPADD\n{p[3]}PUSHI {c}\nMUL\n{p[6]}ADD\nREAD\nATOI\nSTOREN\n'
        else:
            print(f"Erro: Variável {p[1]} não é uma matriz.")
            parser.success = False
    else:
        print("Erro: Variável ainda não existe.")
        parser.success = False


def p_Atr_Input(p):
    "Atr : NOME ATR INPUT"
    if p[1] in p.parser.log:
        p[0] = f'READ\nATOI\nSTOREG {p.parser.log.get(p[1])}\n'
    else:
        print("Erro: Variável não definida.")
        parser.success = False

def p_SubPs(p):
    "SubPs : SubP"
    p[0] = f'{p[1]}'

def p_SubPs_Varias(p):
    "SubPs : SubPs SubP"
    p[0] = f'{p[1]}{p[2]}'

def p_SubP_C(p):
    "SubP : SUBP NOME PA PF DELIM Corpo DELIM"
    if p[2] not in p.parser.subP:
        p.parser.subP.update({p[2] : f'{p[6]}'})
    else:
        print(f"ERRO! SubPrograma com o nome {p[2]} já existe.")
        parser.success = False

def p_SubP_DC(p):
    "SubP : SUBP NOME PA PF DELIM Decls Corpo DELIM"
    if p[2] not in p.parser.subP:
        p.parser.subP.update({p[2] : f'{p[6]}{p[7]}'})
    else:
        print(f"ERRO! SubPrograma com o nome {p[2]} já existe.")
        parser.success = False

def p_Corpo(p):
    "Corpo : Proc"
    p[0] = p[1]

def p_Corpo_Varias(p):
    "Corpo : Corpo Proc"
    p[0] = f'{p[1]}{p[2]}'

def p_Proc_Exp(p):
    "Proc : Exp"
    p[0] = p[1]

def p_Proc_Atr(p):
    "Proc : Atr"
    p[0] = p[1]

def p_Proc_Output(p):
    "Proc : Output"
    p[0] = p[1]

def p_Proc_Se(p):
    "Proc : Se"
    p[0] = p[1]

def p_Proc_Enquanto(p):
    "Proc : Enquanto"
    p[0] = p[1]

def p_Se(p):
    "Se : SE Cond ENTAO Corpo DELIM"
    p[0] = f'{p[2]}JZ l{p.parser.labels}\n{p[4]}l{p.parser.labels}: NOP\n'
    p.parser.labels += 1

def p_Se_Senao(p):
     "Se : SE Cond ENTAO Corpo SENAO ENTAO Corpo DELIM"
     p[0] = f'{p[2]}JZ l{p.parser.labels}\n{p[4]}JUMP l{p.parser.labels}e\nl{p.parser.labels}: NOP\n{p[7]}l{p.parser.labels}e: NOP\n'
     p.parser.labels += 1

def p_Enquanto(p):
    "Enquanto : ENQUANTO Cond FAZ Corpo DELIM"
    p[0] = f'l{p.parser.labels}w: NOP\n{p[2]}JZ l{p.parser.labels}e\n{p[4]}JUMP l{p.parser.labels}w\nl{p.parser.labels}e: NOP\n'
    p.parser.labels += 1

def p_Output_Exp(p):
    "Output : OUTPUT PA Exp PF"
    p[0] = f'{p[3]}WRITEI\nPUSHS "\\n"\nWRITES\n'

def p_Output_AM(p):
    "Output : OUTPUTAM PA NOME PF"
    if p[3] in p.parser.log:
        if p[3] not in p.parser.vars:
            if len(p.parser.log.get(p[3])) == 2:
                array = ""
                for i in range(p.parser.log.get(p[3])[1]):
                    array += f'PUSHGP\nPUSHI {p.parser.log.get(p[3])[0]}\nPADD\nPUSHI {i}\nLOADN\nWRITEI\nPUSHS " "\nWRITES\n'
                p[0] = array + 'PUSHS "\\n"\nWRITES\n'
            else:
                matriz = ""
                for l in range(p.parser.log.get(p[3])[1]):
                    for c in range(p.parser.log.get(p[3])[2]):
                        matriz += f'PUSHGP\nPUSHI {p.parser.log.get(p[3])[0]}\nPADD\nPUSHI {p.parser.log.get(p[3])[2] * l + c}\nLOADN\nWRITEI\nPUSHS " "\nWRITES\n'
                    matriz += 'PUSHS "\\n"\nWRITES\n'
                p[0] = matriz

        else:
            print("Erro! Variável não é um array.")
            parser.success = False
    else:
        print("Erro! Variável não definida.")
        parser.success = False

def p_Exp_Var(p):
    "Exp : Var"
    p[0] = p[1]

def p_Exp_P(p):
    "Exp : PA Exp PF"
    p[0] = p[2]

def p_Exp_NUM(p):
    "Exp : NUM"
    p[0] = f'PUSHI {p[1]}\n'

def p_Exp_SOMA(p):
    "Exp : Exp SOMA Exp" 
    p[0] = f'{p[1]}{p[3]}ADD\n'

def p_Exp_MULT(p):
    "Exp : Exp MULT Exp" 
    p[0] = f'{p[1]}{p[3]}MUL\n'
  
def p_Exp_DIV(p):
    "Exp : Exp DIV Exp" 
    p[0] = f'{p[1]}{p[3]}DIV\n'

def p_Exp_SUB(p):
    "Exp : Exp SUB Exp" 
    p[0] = f'{p[1]}{p[3]}SUB\n'

def p_Exp_MOD(p):
    "Exp : Exp MOD Exp" 
    p[0] = f'{p[1]}{p[3]}MOD\n'

def p_Exp_Cond(p):
    "Exp : Cond"
    p[0] = p[1]

def p_Exp_Call(p):
    "Exp : Call"
    p[0] = p[1]

def p_Call(p):
    "Call : CALL PA NOME PF"
    if p[3] in p.parser.subP:
        p[0] = p.parser.subP[p[3]]
    else:
        print(f"Erro! SubPrograma com o nome {p[3]} não existe.")

def p_Var_Matriz(p):
    "Var : NOME SA Exp SF SA Exp SF"
    if p[1] in p.parser.log:
        if p[1] not in p.parser.vars and len(p.parser.log.get(p[1])) == 3:
            c = p.parser.log.get(p[1])[2]
            p[0] = f'PUSHGP\nPUSHI {p.parser.log.get(p[1])[0]}\nPADD\n{p[3]}PUSHI {c}\nMUL\n{p[6]}ADD\nLOADN\n'
        else:
            print(f"Erro! Variável {p[1]} não é uma matriz.")
            parser.success = False
    else:
        print("Erro! Variável não definida.")
        parser.success = False

def p_Var_Array(p):
    "Var : NOME SA Exp SF"
    if p[1] in p.parser.log:
        if p[1] not in p.parser.vars and len(p.parser.log.get(p[1])) == 2:
            p[0] = f'PUSHGP\nPUSHI {p.parser.log.get(p[1])[0]}\nPADD\n{p[3]}LOADN\n'
        else:
            print(f"Erro! Variável {p[1]} não é um array.")
            parser.success = False
    else:
        print("Erro! Variável não definida.")
        parser.success = False

def p_Var_Int(p):
    "Var : NOME"
    if p[1] in p.parser.log:
        p[0] = f'PUSHG {p.parser.log.get(p[1])}\n'
    else:
        print("ERRO! Variável não definida.")
        parser.success = False

def p_Cond_P(p):
    "Cond : PA Cond PF"
    p[0] = p[2]

def p_Cond_Maior(p):
    "Cond : Exp MAIOR Exp"
    p[0] = f'{p[1]}{p[3]}SUP\n'

def p_Cond_Menor(p):
    "Cond : Exp MENOR Exp"
    p[0] = f'{p[1]}{p[3]}INF\n'

def p_Cond_Igual(p):
    "Cond : Exp IGUAL Exp"
    p[0] = f'{p[1]}{p[3]}EQUAL\n'

def p_Cond_Menori(p):
    "Cond : Exp MENORIG Exp"
    p[0] = f'{p[1]}{p[3]}INFEQ\n'

def p_Cond_Maiori(p):
    "Cond : Exp MAIORIG Exp"
    p[0] = f'{p[1]}{p[3]}SUPEQ\n'

def p_Cond_Dif(p):
    "Cond : Exp DIF Exp"
    p[0] = f'{p[1]}{p[3]}EQUAL\nNOT\n'

def p_Cond_E(p):
    "Cond : Exp E Exp"
    p[0] = f'{p[1]}{p[3]}ADD\nPUSHI 2\nEQUAL\n'

def p_Cond_Ou(p):
    "Cond : Exp OU Exp"
    p[0] = f'{p[1]}{p[3]}ADD\nPUSHI 1\nSUPEQ\n'

def p_Cond_Nao(p):
    "Cond : NO Exp"
    p[0] = f'{p[2]}NOT\n'

def p_error(p):
    print('Syntax error: ', p)
    parser.success = False

parser = yacc.yacc()

parser.success = True
parser.assembly = ""
parser.log = {}
parser.labels = 0
parser.gp = 0
parser.vars = []
parser.subP = {}

f = open('script.txt')
content = f.read()

parser.parse(content)

if parser.success:
  print(parser.assembly)
