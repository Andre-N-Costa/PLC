import csv
import json
import re

filestr = input("Nome do ficheiro que pretende converter: ")

with open("C:\\Users\\letsd\\OneDrive\\Área de Trabalho\\uni\\PLCTP\\" + filestr, 'r') as file:
  csvreader = list(csv.reader(file))
  json_list = []
  nvezes = 0
  header = csvreader[0]
  del csvreader[0]
  item = 0

  while item < len(header):
    if re.search(r"{\d+",header[item]) and item < len(header)-1:
      header[item] = header[item] + "," + header[item+1]
      del header[item+1]
    item+=1

  for m,info in enumerate(csvreader):
    n = 0;i = 0
    json_list.append({})
    while i < len(info):
      func = ""
      if info[i] != "" or header[n] != "":
        nvezes = re.search(r"(?<={)\d+(?=})|(?<={)((\d+),(\d+))(?=})",header[n])
        if nvezes:
          func = re.search(r"(?<=::)[a-z]+",header[n])
          if func:
            func = func.group(0)
          if re.search(r"\d+,\d+",nvezes.group(0)):
            nmin = int(nvezes.group(2))
            nmax = int(nvezes.group(3))
            nvezes_int = nmax
            head = re.sub(r"{((\d+),(\d+))}","",header[n])
            head = re.sub(r"::[a-z]+","",head)
            n+=1
            list_aux = []
            while nvezes_int > 0:
              while nvezes_int > nmax - nmin:
                list_aux.append(int(info[i]))
                nvezes_int-=1;n+=1;i+=1
              if info[i] == "":
                break
              else:
                list_aux.append(int(info[i]))
                nvezes_int-=1;n+=1;i+=1
            if func == "sum":
              json_list[m][head + "_sum"] = sum(list_aux)
            elif func == "media":
              json_list[m][head + "_media"] = sum(list_aux)/len(list_aux)
            else:
              json_list[m][head] = list_aux  
          else:
            nvezes_int = int(nvezes.group(0))
            head = re.sub(r"{\d+}","",header[n])
            n+=1
            list_aux = []
            while nvezes_int > 0:
              list_aux.append(int(info[i]))
              nvezes_int-=1;n+=1;i+=1
            if func == "sum":
              json_list[m][head + "_sum"] = sum(list_aux)
            elif func == "media":
              json_list[m][head + "_media"] = sum(list_aux)/len(list_aux)
            else:
              json_list[m][head] = list_aux 
        else:
          json_list[m][header[n]] = info[i]
          n+=1;i+=1
      else:
        i+=1;n+=1
  output = json.dumps(json_list, indent=4,ensure_ascii=False)
  opf = open(filestr[:-3] + "json", "x")
  opf.write(output)
  opf.close()
  pesquisar = 1
  while pesquisar:
    pesquisar = int(input("0 - Sair do programa\n1 - Pesquisar no ficheiro JSON\n"))
    if pesquisar:
      pesquisastr = "Escolhe um elemento do header:\n"
      for n in range(len(header)-1):
        find = re.search(r"({\d+}|{\d+,\d+})(::[a-z]+)?",header[n])
        if find:
          del header[n]
      for n,i in enumerate(header): 
        if i != "":
          pesquisastr = pesquisastr + str(n) + " - " + i + "\n"
      elemheader = input(pesquisastr)
      eleminfo = input("Por o quê que se vai pesquisar?\n")
      encontros = []
      for i in json_list:
        if i[header[int(elemheader)]] == eleminfo:
          encontros.append(i)
      print(json.dumps(encontros,indent=4,ensure_ascii=False))
