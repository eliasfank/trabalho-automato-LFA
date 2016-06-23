from sys import argv
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-g", "--gramatica", required = False, help = "Path to the directory of grammar")
ap.add_argument("-t", "--tokens", required = False, help = "Path to the directory of tokens")
args = vars(ap.parse_args())

arqGramatica = args["gramatica"]
arqTokens = args["tokens"]

contEstado = 0
matriz = []					   ###Lista de dicionarios
simbolos = []				   ###Lista com todos os simbolos do automato
vivos = set()                  ###Lista com o estados vivos
alcansaveis = set()			   ###Lista com estados alcansaveis
estadosFinais = []			   ###Lista com os estados finais

def calculaGramatica(gramatica, contGramatica):
	print contGramatica
	global contEstado
	global matriz
	global estadosFinais
	global simbolos
	tempDic={}

	first = 0
	##Percorrer todas as linhas de uma gramatica
	###salvando os estados da esquerda
	for line in gramatica:
		partes = line.split("=")
		estadoEsq = partes[0][partes[0].find("<")+1:partes[0].find(">")]
		#Se for a primeira gramatica comecamos pelo indice 0
		if contGramatica > 0:
			contEstado+=1
		tempDic[estadoEsq] = contEstado
		if contGramatica > 0 and first == 0:
			first = 1
			tempDic[estadoEsq] = 0
			contEstado-=1
		else:
			matriz.append({})
		print estadoEsq, "--", tempDic[estadoEsq]
		#Se nao for a primeira gramatica precisamos incrementar
		if contGramatica == 0:
			contEstado+=1
	contEstado-=1

	first = 0
	##Percorre todas as linhas de uma gramatica
	###fazendo a ligacao de cada simbolo com o respectivo estado
	for line in gramatica:
		partes = line.split("=")
		estadoEsq = partes[0][partes[0].find("<")+1:partes[0].find(">")]
		producoes = partes[1].split("|")
		estadosAdicionais = 0
		terminal = ""
		
		for producao in producoes:
			if "<" in producao:  ##Se tiver estado e terminal
				terminal = producao[producao.find(" ")+1:producao.find("<")]
				estado = producao[producao.find("<")+1:producao.find(">")]
				if verificaSeExiste(terminal) == False or first != 0:
					matriz[tempDic[estadoEsq]][terminal]=[]
				matriz[tempDic[estadoEsq]][terminal].append(tempDic[estado])
			else:                ##Se nao tiver estado
				terminal = producao.strip()
				if(terminal.strip()=="&"): ##Se o simbolo for epsilon
					estadosFinais.append(tempDic[estadoEsq])
				else:            ##Se for um simbolo diferente de epsilon
					matriz.append({})
					matriz[tempDic[estadoEsq]][terminal]=[]
					matriz[tempDic[estadoEsq]][terminal].append(contEstado)
					estadosFinais.append(contEstado)
					contEstado+=1
			if (terminal!="&"):
				if terminal not in simbolos:
					simbolos.append(terminal)
		if first == 0:
			first = 1

def verificaSeExiste(carac):
	if not matriz:
		return False
	for c, v in matriz[0].iteritems():
		if c is carac:
			return True
	return False

def calculaTokens(tokens):
	global contEstado
	global matriz
	global estadosFinais
	global simbolos
	for t in tokens:
		flagFirst = 0
		for c in t:
			if c != "\n" and c != "\r":
				if flagFirst == 0:
					flagFirst = 1
					if verificaSeExiste(c) == True:	
						matriz[0][c].append(contEstado+1)
					else: 
						if not matriz:
							matriz.append({})
						matriz[0][c]=[]	
						matriz[0][c].append(contEstado+1)
				else:
					matriz.append({})
					contEstado+=1
					matriz[contEstado][c]=[]
					matriz[contEstado][c].append(contEstado+1)
				if c not in simbolos:
					simbolos.append(c)
		contEstado+=1
		estadosFinais.append(contEstado)
		matriz.append({})

def imprime():
	global matriz
	a = ""#usado na impressao de valores 
	print
	print "Automato:"
	print
	print ('regra inicial = 0:')
	print
	print (' '*11+'|'),
	for simbolo in simbolos:#mostrou as ligacoes
		print '%10s' % (simbolo),"|",
		
	print
	print ('_ _'*(len(simbolos)*5))
	#verifique se o estado e final e imprima o *
	for i in range(0,len(matriz)):
		if i in estadosFinais:
			print "*",
		else:
			print " ",
		print '%8s' % (i),"|",
		#imprime os simbilos que sao nomes das regras
			
		for simbolo in simbolos:
			try:
				print '%10s' % (matriz[i][simbolo]),
			except:
				print '%8s' % (a),"x",
				
			print ('|'),
		print
		print


def gerarGrafo(grafo):
	global matriz
	grafo = {}
	for i in range(0,len(matriz)):
		#print i,":",
		grafo[i]=set()
		for simbolo in simbolos:
			try:
				x = matriz[i][simbolo]
				for j in x:
					#print j,
					grafo[i].add(j)
			except:
				pass
		#print
	return grafo


def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    for next in graph[start] - visited:
        dfs(graph, next, visited)
    return visited

################################################################################################

contGramatica = 0
if arqGramatica is not None:					
	f = open(arqGramatica)
	lines = f.readlines()
	gramatica = []
	for line in lines:
		if line == "\n":
			calculaGramatica(gramatica, contGramatica)
			gramatica=[]
			contGramatica+=1
		else:
			gramatica.append(line)
	calculaGramatica(gramatica, contGramatica)
if arqTokens is not None:
	f = open(arqTokens)
	tokens = f.readlines()
	calculaTokens(tokens)

#print "Automato"
#for i in range(0,len(matriz)):
#	for c, v in matriz[i].iteritems():
#		print i, c,
#		for x in range(0,len(v)):
#			if x < len(v)-1:
#				print v[x],",",
#			else:
#				print v[x],
#		print
#print "Estados Finais:"
#print estadosFinais
#print len(matriz), "estados no automato"
#print simbolos

imprime()

grafo = gerarGrafo(None)

alcansaveis = dfs(grafo, 0, None)
print "Estados Alcancaveis"
print alcansaveis
print
for i in range(0,len(matriz)):
	vis=dfs(grafo, i, None)
	if not vis.isdisjoint(estadosFinais):
		vivos.update(vis)
print "Estados Vivos"
print vivos
print
print "Estados Finais:"
print estadosFinais
print
