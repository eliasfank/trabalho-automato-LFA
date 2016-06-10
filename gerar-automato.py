from sys import argv
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-g", "--gramatica", required = False, help = "Path to the directory of grammar")
ap.add_argument("-t", "--tokens", required = False, help = "Path to the directory of tokens")
args = vars(ap.parse_args())

arqGramatica = args["gramatica"]
arqTokens = args["tokens"]

contEstado = 0
matriz = []
simbolos = []
estadosFinais = []

def calculaGramatica(gramatica):
	global contEstado
	global matriz
	global estadosFinais
	global simbolos
	tempDic={}

	##Percorrer todas as linhas de uma gramatica
	###salvando os estados da esquerda
	for line in gramatica:
		partes = line.split("=")
		estadoEsq = partes[0][partes[0].find("<")+1:partes[0].find(">")]
		tempDic[estadoEsq] = contEstado
		contEstado+=1
	contEstado-=1

	##Percorre todas as linhas de uma gramatica
	###fazendo a ligacao de cada simbolo com o respectivo estado
	for line in gramatica:
		partes = line.split("=")
		estadoEsq = partes[0][partes[0].find("<")+1:partes[0].find(">")]
		producoes = partes[1].split("|")
		estadosAdicionais = 0
		matriz.append({})
		terminal = ""
		for producao in producoes:
			if "<" in producao:
				terminal = producao[producao.find(" ")+1:producao.find("<")]
				estado = producao[producao.find("<")+1:producao.find(">")]
				matriz[tempDic[estadoEsq]][terminal]=[]
				matriz[tempDic[estadoEsq]][terminal].append(tempDic[estado])
			else:
				terminal = producao.strip()
				if(terminal.strip()=="&"):
					estadosFinais.append(tempDic[estadoEsq])
				else:
					matriz.append({})
					matriz[tempDic[estadoEsq]][terminal]=[]
					matriz[tempDic[estadoEsq]][terminal].append(contEstado)
					estadosFinais.append(contEstado)
					contEstado+=1
			if (terminal!="&"):
				if terminal not in simbolos:
					simbolos.append(terminal)

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

if arqGramatica is not None:					
	f = open(arqGramatica)
	lines = f.readlines()
	gramatica = []
	for line in lines:
		if line == "\n":
			calculaGramatica(gramatica)
			gramatica=[]
		else:
			gramatica.append(line)
	calculaGramatica(gramatica)
if arqTokens is not None:
	f = open(arqTokens)
	tokens = f.readlines()
	calculaTokens(tokens)

print "Automato"
for i in range(0,len(matriz)):
	for c, v in matriz[i].iteritems():
		print i, c,
		for x in range(0,len(v)):
			if x < len(v)-1:
				print v[x],",",
			else:
				print v[x],
		print
print "Estados Finais:"
print estadosFinais
print len(matriz), "estados no automato"
print simbolos
