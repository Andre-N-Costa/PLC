import re, os

# Abrir ficheiros --------------------
try:
  fhtml = open("index.html","x")
except FileExistsError:
  os.remove("index.html")
  fhtml = open("index.html","x")

f = open("C:\\Users\\letsd\\OneDrive\\Área de Trabalho\\uni\\PLCTP\\emd.csv", 'r')


# Separar as linhas de emd em lista de strings
csvreader = f.readlines()

# message vai guardar todo o código html de index.html
message = "<html><head><style>a{font-size: 18px;color: black;}h1{font-size: 32px;}h2{font-size: 24px;}li{margin-bottom: 15px;}</style></head><body><h1>Registos de Exames M&eacute;dicos Desportivos</h1><ul>"
 
# Datas extremas dos registos no dataset -----------------------------

anos = set()
for line in csvreader:
  n = re.search(r"\d{4}(?=(-\d{2}-\d{2}))",line)
  if n:
    anos.add(n.group(0))
anos = sorted(list(anos))

message += "<h2>Dados registados entre " + anos[0] + " e " + anos[-1] + "</h2>"

#  Distribuição por modalidade em cada ano e no total ---------------------------------------------------

try:
  fdmod = open("DistribModalidade.html","x")
except FileExistsError:
  os.remove("DistribModalidade.html")
  fdmod = open("DistribModalidade.html","x")

messagemodalidade = "<html><head></head><body><h1>Distribui&ccedil;&atilde;o por modalidade</h1><ol>"

message+= "<li><a href = \"DistribModalidade.html\">Distribui&ccedil;&atilde;o por modalidade em cada ano</a></li>"

modalidades = set()
for line in csvreader[1:]:
  n = re.search(r"(?<=,[MF],)([A-Z][a-z]+),([A-Z][^,]+)",line)
  if n:
    modalidades.add(n.group(2))
 
modalidades = sorted(list(modalidades))

messagemodalidade+="<div class=\"container\">"

messagemodalidade += "<div class=\"sub-container\">"
for ano in anos:
  messagemodalidade+= "<p><strong>" + ano + ":</strong>" + "</p>"
messagemodalidade+= "<p><strong>Total:</strong></p></div>"


for i in modalidades:
  messagemodalidade += "<div class=\"sub-container\"><head><strong>" + i + "</strong></head>"
  total = 0
  for ano in anos:
    counter = 0
    messagemodalidade+="<p>"
    for line in csvreader:
      nanos = re.search(r"\d{4}(?=(-\d{2}-\d{2}))",line)
      nmodalidade = re.search(r"(?<=,[MF],)([A-Z][a-z]+),([A-Z][^,]+)",line)
      if nanos and nmodalidade and nanos.group(0) == ano and nmodalidade.group(2) == i:
        counter+=1
    total+=counter
    messagemodalidade+= str(counter) + "</p>"
  messagemodalidade+= "<p>" + str(total) + "</p></div>"
messagemodalidade+="</div>"

messagemodalidade = messagemodalidade[:60] + "<style>h1{font-size: 32px;}.container {display:flex;gap: 10px;align-items: flex-end;}</style>" + messagemodalidade[60:]

messagemodalidade+="<p>----------------------------------------------</p>"

# Guarda-se os dados sobre modalidades num dicionário, (modalidade, ano) : nome

nmod = {} 

for line in csvreader:
  moradaemodal_dm = re.search(r"(?<=,[MF],)([A-Z][a-z]+),([A-Z][^,]+)",line)
  anos_dm = re.search(r"\d{4}(?=(-\d{2}-\d{2}))",line)
  nomes_dm = re.search(r"(?<=\d{4}-\d{2}-\d{2},)([A-Z][a-z]+),([A-Z][a-z]+),",line)

  if moradaemodal_dm and nomes_dm and anos_dm:
    if (moradaemodal_dm.group(2),anos_dm.group(0)) not in nmod:
      nmod[(moradaemodal_dm.group(2),anos_dm.group(0))] = [nomes_dm.group(1) + " " + nomes_dm.group(2)]
    else:
      nmod[(moradaemodal_dm.group(2),anos_dm.group(0))].append(nomes_dm.group(1) + " " + nomes_dm.group(2))

# modalidades já definida
modalidadesord = sorted(modalidades)
# anos já definida nas datas extremas

# a partir do dicionário escreve-se o código html em que listamos os atleta por modalidade e ano

for ano in anos:
  messagemodalidade += "<p><strong>" + ano + "</strong></p><ul>"
  for mod in modalidadesord:
    messagemodalidade += "<li><strong>" + mod + "</strong><ol>" 
    for atletas in list(nmod.items()):
      if atletas[0][1] == ano and atletas[0][0] == mod:
        atlord = sorted(atletas[1])
        for atleta in atlord:
          messagemodalidade += "<li>" + atleta + "</li>"
    messagemodalidade+= "</ol></li>"
  messagemodalidade+="</ul>"


fdmod.write(messagemodalidade)

#  Distribuição por idade e género ------------------------------------------------------------

try:
  fdig = open("DistribIG.html","x")
except FileExistsError:
  os.remove("DistribIG.html")
  fdig = open("DistribIG.html","x")

messageig = "<html><head></head><body><h1>Distribui&ccedil;&atilde;o por idade e g&eacute;nero</h1><ol>"

message+= "<li><a href = \"DistribIG.html\">Distribui&ccedil;&atilde;o por idade e g&eacute;nero</a></li>"
messageig+= "<div class=\"container\"><div class=\"sub-container\"><p><strong>Menos de 35 anos:</strong></p>"
messageig+="<p><strong>Mais ou com 35 anos:</strong></p></div>"


# Construção da tabela com a distribuição

for i in ['M','F']:
  countmenor=0
  countmaior=0
  messageig+= "<div class=\"sub-container\"><p>"
  for line in csvreader:
    genero = re.search(r"(?<=,)"+i+r"(?=,)",line)
    idade = re.search(r"(?<=,)\d{2}(?=,[MF])",line)
    if genero and idade and genero.group(0) == i and int(idade.group(0)) < 35:
      countmenor +=1
    elif genero and idade and genero.group(0) == i and int(idade.group(0)) >= 35:
      countmaior +=1
  messageig+= "<strong>" + i + "</strong>" + "</p><p>" + str(countmenor) + "</p><p>" + str(countmaior) + "</p></div>" 

messageig+="</div>"

messageig = messageig[:60] + "<style>h1{font-size: 32px;}.container{display:flex;gap: 10px;align-items: flex-end;}</style>" + messageig[60:]

messageig+="<p>---------------------------------------------------------</p>"

# Guarda-se os dados sobre idade e género num dicionário, (genero, idade) : nome

dictig = {}

for line in csvreader:
  generos_ig = re.search(r"(?<=,)[MF](?=,)",line)
  idades = re.search(r"(?<=,)\d{2}(?=,[MF])",line)
  nomes_ig = re.search(r"(?<=\d{4}-\d{2}-\d{2},)([A-Z][a-z]+),([A-Z][a-z]+),",line)

  if generos_ig and nomes_ig and idades:
    if (generos_ig.group(0),idades.group(0)) not in dictig:
      dictig[(generos_ig.group(0),idades.group(0))] = [nomes_ig.group(1) + " " + nomes_ig.group(2)]
    else:
      dictig[(generos_ig.group(0),idades.group(0))].append(nomes_ig.group(1) + " " + nomes_ig.group(2))

# a partir do dicionário escreve-se o código html em que listamos os atleta por idade e género

messageig+="<p><strong>Mais ou com 35 anos</strong></p><ul>"
for gen in ['M','F']:
  messageig+= "<li><strong>" + gen + "</strong><ol>"
  for atleta in list(dictig.items()):
    if atleta[0][0] == gen and int(atleta[0][1]) >= 35:
      atlord=sorted(atleta[1])
      for atl in atlord:
        messageig+= "<li>" + atl + "</li>"
  messageig+="</ol></li>"

messageig+="</ul><p><strong>Menos de 35 anos</strong></p><ul>"
for gen in ['M','F']:
  messageig+= "<li><strong>" + gen + "</strong><ol>"
  for atleta in list(dictig.items()):
    if atleta[0][0] == gen and int(atleta[0][1]) < 35:
      atlord=sorted(atleta[1])
      for atl in atlord:
        messageig+= "<li>" + atl + "</li>"
  messageig+="</ol></li>"


fdig.write(messageig)

# Distribuição por morada ----------------------------------------------------------------

message+="<li><a href=\"DistribMorada.html\">Distribui&ccedil;&atilde;o por morada</a></li>"
try:
  fdm = open("DistribMorada.html","x")
except FileExistsError:
  os.remove("DistribMorada.html")
  fdm = open("DistribMorada.html","x")

messagemorada = "<html><head><style>h1{font-size: 32px;}</style></head><body><h1>Distribui&ccedil;&atilde;o por morada</h1><ol>"

# faz-se uma lista de moradas com repetições e outra sem repetições

moradas = []
moradasnrep = []
for line in csvreader[1:]:
  n = re.search(r"(?<=,[MF],)[A-Z][a-z]+(?=,)",line)
  if n and n.group(0) not in moradas:
    moradasnrep.append(n.group(0))
  if n:
    moradas.append(n.group(0))


# Guarda-se os dados sobre moradas num dicionário, morada : (nome,modalidade)

nresidentes = {}

for line in csvreader:
  moradaemodal = re.search(r"(?<=,[MF],)([A-Z][a-z]+),([A-Z][^,]+)",line)
  nomes = re.search(r"(?<=\d{4}-\d{2}-\d{2},)([A-Z][a-z]+),([A-Z][a-z]+),",line)

  if moradaemodal and nomes:
    if moradaemodal.group(1) not in nresidentes:
      nresidentes[moradaemodal.group(1)] = []
    nresidentes[moradaemodal.group(1)].append((nomes.group(1) + " " + nomes.group(2),moradaemodal.group(2)))

nresidentes = sorted(list(nresidentes.items()), key= lambda x : x[0])

# a partir do dicionário escreve-se o código html em que listamos os atleta por morada

for localidade in nresidentes:
  messagemorada+="<li><p><strong>" + localidade[0] + "</strong></p><ul>"
  for residente in localidade[1]:
    messagemorada+="<li>Nome:&nbsp;" + residente[0] + ", Modalidade:&nbsp;" + residente[1] + "</li>"
  messagemorada+="</ul>"
messagemorada+="</ol>"

fdm.write(messagemorada)

# Percentagem de aptos e não aptos por ano ----------------------------------------------------------

message+="<li><a href=\"Aptidao.html\">Percentagem de aptos e n&atilde;o aptos</a></li>"
try:
  fapt = open("Aptidao.html","x")
except FileExistsError:
  os.remove("Aptidao.html")
  fapt = open("Aptidao.html","x")

messageapt = "<html><head><style>h1{font-size: 32px;}</style></head><body><h1>Percentagem de aptos e n&atilde;o aptos</h1><ol>"

for ano in anos:
  messageapt+= "<p><strong>" + ano + "</strong></p><ul>"
  laux = []
  for line in csvreader:
    n = re.search(r"\d{4}(?=(-\d{2}-\d{2}))",line)
    n1 = re.search(r"(false|true),(false|true)",line)
    if n and n1 and n.group(0) == ano:
      laux.append(n1.group(2))
  if len(laux) > 0: 
    messageapt += "<li><p>" + "<strong>aptos</strong> = " + str(round(laux.count("true")/len(laux)*100,1)) + "%</p></li>"
    messageapt += "<li><p>" + "<strong>n&atilde;o aptos</strong> = " + str(round(laux.count("false")/len(laux)*100,1)) + "%</p></li></ul>"
  

fapt.write(messageapt)



message+="</ul>"

fhtml.write(message)
fhtml.close()
fdmod.close()
fapt.close()
fdm.close()
f.close()
