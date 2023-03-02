import ply.lex as lex

tokens = (
  'PA',
  'PF',
  'NUM',
  'NOME',
  'INT',
  'SOMA',
  'SUB',
  'MULT',
  'DIV',
  'MOD',
  'ATR',
  'SA',
  'SF',
  'OUTPUT',
  'INPUT',
  'MENOR',
  'MENORIG',
  'MAIOR',
  'MAIORIG',
  'IGUAL',
  'DIF',
  'SE',
  'ENTAO',
  'SENAO',
  'ENQUANTO',
  'FAZ',
  'OU',
  'E',
  'NO',
  'ARRAY',
  'MATRIZ',
  'OUTPUTAM',
  'SUBP',
  'DELIM',
  'CALL',
)

t_PA = r'\('
t_PF = r'\)'
t_ENTAO = r'\|'
t_SA = r'\['
t_SF = r'\]'
t_DELIM = r'\$'

def t_NUM(t):
  r"\d+"
  return t

def t_SUBP(t):
  r"def"
  return t

def t_FAZ(t):
  r"->"
  return t

def t_CALL(t):
  r"call"
  return t

def t_MATRIZ(t):
  r"Mat"
  return t

def t_INT(t):
  r"Int"
  return t

def t_OUTPUTAM(t):
  r"outputAM"
  return t

def t_OUTPUT(t):
  r"output"
  return t

def t_INPUT(t):
  r"input"
  return t

def t_ATR(t):
  r"is"
  return t

def t_SOMA(t):
  r"\+"
  return t

def t_SUB(t):
  r"-"
  return t

def t_MOD(t):
  r"%"
  return t

def t_MULT(t):
  r"><"
  return t

def t_DIV(t):
  r"/"
  return t

def t_MENORIG(t):
  r"\_i"
  return t

def t_MAIORIG(t):
  r"\^i"
  return t

def t_MENOR(t):
  r"\_"
  return t

def t_MAIOR(t):
  r"\^"
  return t

def t_DIF(t):
  r"\#"
  return t

def t_IGUAL(t):
  r"<->"
  return t


def t_OU(t):
  r"u\s"
  return t

def t_E(t):
  r"n\s "
  return t

def t_NO(t):
  r"\~"
  return t

def t_SENAO (t):
  r"se!"
  return t

def t_SE (t):
  r"se"
  return t

def t_ENQUANTO (t):
  r"eqnt"
  return t

def t_ARRAY(t):
  r"Arr"
  return t

def t_NOME(t):
  r"\w+"
  return t

t_ignore = ' \r\t\n'

def t_error(t):
  print("Illegal character '%s'" % t.value[0])
  t.lexer.skip(1)

lexer = lex.lex()
