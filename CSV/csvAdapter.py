Baixar todas as versões de um pacote cliente.
Baixar todas as dependencias de cada cliente na release espécífica
Rodar o npm teste para ver se quebra
Rodar o npm mutante teste para ver se quebra
Se não , testar a próxima versão
Se quebrar, 


import csv
import os
import subprocess

def getRepositoryURL(packageName):
    resp = subprocess.getstatusoutput('npm view {0} repository.url'.format(packageName))    # get the repository url
    if resp[1].find('npm ERR!') == -1:                                                      # if dosent have err
        return resp[1]
    else:
        return ''

def csvAdapter(fileName):
    print(os.getppid()+1)
    fieldnames = ['client_name', 'client_timestamp', 'client_previous_timestamp', 'client_git_head', 'repository_link']    # fields in the new csv

    csvReader = csv.reader(open(fileName), delimiter=',', quotechar='\n')
    fileToWrite = open('npmreleases_reduzide.csv', 'w')
    csvWriter = csv.DictWriter(fileToWrite, fieldnames=fieldnames)
    csvWriter.writeheader()

    last_client = ''
    csvReader.__next__()            # ignore first line with fields
    qtdFail = 0						# qtd of fail repo
    try:
        while True:
            line = csvReader.__next__()
            if last_client.__eq__(line[0]):
                csvWriter.writerow({'client_name': line[0], 'client_timestamp': line[4], 'client_previous_timestamp': line[10], 'client_git_head': line[6], 'repository_link': ''})
            else:
                url = getRepositoryURL(line[0])
                csvWriter.writerow({'client_name': line[0], 'client_timestamp': line[4], 'client_previous_timestamp': line[10], 'client_git_head': line[6], 'repository_link': url})
                last_client = line[0]
                if url.__eq__(''):
                    qtdFail += 1

    except (StopIteration):
        novo = open('failqtd', 'w')
        novo.write('From 461640 package, ' + str(qtdFail) + ' havent repo')
        novo.close()
        fileToWrite.close()

pid = os.fork()	# criando um processo filho
if pid == 0:	# filho
    csvAdapter('npmreleases.csv')


import csv
csvReader = csv.reader(open('npmreleases_reduzide.csv'), delimiter=',', quotechar='\n')
def vaiate(linha):
	csvReader = csv.reader(open('npmreleases_reduzide.csv'), delimiter=',', quotechar='\n')
	last_client = ''
	qtdinteriorGit = 0
	for i in range(0, linha):
		linhaAlvo = csvReader.__next__()
		try:
			if last_client.__eq__(linhaAlvo[0]):
				continue
			last_client = linhaAlvo[0]
			if(linhaAlvo[4].find('/tree/') != -1):
				#print("Linha {0}: ".format(csvReader.line_num+1), linhaAlvo[0], " - ", linhaAlvo[4])
				#b = input()
				qtdinteriorGit += 1
		except IndexError:
			continue
	print("Quantidade dentro dos repositorios: ", qtdinteriorGit)

vaiate(3065789)
# 461640
# 3065789

# 361102
# 2654494

import csv
def operacoes():
	csvReader = csv.reader(open('npmreleases_reduzide_v2.csv'), delimiter=',', quotechar='\n')		# abro arquivo para leitura
	fileToWrite = open('npmreleases_limpo.csv', 'w')												# abro arquivo para escrita
	fieldnames = ['client_name', 'client_timestamp', 'client_previous_timestamp', 'repository_link']# cabecalho do novo arquivo
	csvWriter = csv.DictWriter(fileToWrite, fieldnames=fieldnames)									# abro como CSV
	csvWriter.writeheader()																			# escrevo o cabecalho
	last_client = ''
	escrever = False
	linha = csvReader.__next__()																	# le o cabecalho
	csvWriter.writerow({'client_name': linha[0], 'client_timestamp': linha[1], 'client_previous_timestamp': linha[2], 'repository_link': linha[4]})
	try:
		while True:
			linha = csvReader.__next__()		# le a linha
			if linha[0].__eq__(last_client):	# se estiver nas linhas do mesmo cliente
				if escrever:					# se for para escrever
					csvWriter.writerow({'client_name': linha[0], 'client_timestamp': linha[1], 'client_previous_timestamp': linha[2], 'repository_link': linha[4]})
					continue					# volta para o comeco
				else:							# senao
					continue					# ignora a linha
			last_client = linha[0]				# eh um cliente diferente, entao atualiza
			escrever = False					# a priori nao pode escrever
			if linha[4].startswith('\"'):		# se a linha comecar com '"'
				linha = csvReader.__next__()	# le a proxima linha que so tem o '"' e ignora ela
				continue						# volta para o comeco
			if len(linha[4]) > 21:				# se for um repositorio valido
				csvWriter.writerow({'client_name': linha[0], 'client_timestamp': linha[1], 'client_previous_timestamp': linha[2], 'repository_link': linha[4]})
				escrever = True					# marca que as demais linhas deste cliente deverao ser escritas
	except StopIteration:
		fileToWrite.close()


import csv
def operacoes():
	csvReader = csv.reader(open('npmreleases_reduzide_v2.csv'), delimiter=',', quotechar='\n')		# abro arquivo para leitura
	last_client = ''
	escrever = False
	linha = csvReader.__next__()																	# le o cabecalho
	qtdLinhasRemovidas = 0
	qtdReposRemovidos = 0
	try:
		while True:
			linha = csvReader.__next__()		# le a linha
			if linha[0].__eq__(last_client):	# se estiver nas linhas do mesmo cliente
				if escrever:					# se for para escrever
					continue					# volta para o comeco
				else:							# senao
					qtdLinhasRemovidas += 1
					continue					# ignora a linha
			last_client = linha[0]				# eh um cliente diferente, entao atualiza
			escrever = False					# a priori nao pode escrever
			if linha[4].startswith('\"'):		# se a linha comecar com '"'
				linha = csvReader.__next__()	# le a proxima linha que so tem o '"' e ignora ela
				qtdLinhasRemovidas += 1
				continue						# volta para o comeco
			if len(linha[4]) > 21:				# se for um repositorio valido
				escrever = True					# marca que as demais linhas deste cliente deverao ser escritas
			else:
				qtdReposRemovidos += 1
	except StopIteration:
		print("Repos : ", qtdReposRemovidos)
		print("Linhas: ", qtdLinhasRemovidas)

request

import csv
def operacoes(pacote):
	csvReader = csv.reader(open('npmreleases_limpo.csv'), delimiter=',', quotechar='\n')
	linha = csvReader.__next__()	# le o cabecalho
	qtdLine = 0
	try:
		while True:
			linha = csvReader.__next__()	# le o cabecalho
			if linha[0].__eq__(pacote):
				print(linha)
				qtdLine += 1
	except StopIteration:
		print("Linhas:", qtdLine)

operacoes('request')



import re
def toRegex():
	exp = re.compile('\[[\d|\w|_|\-|\.|@|\/]+]')
	arquivo = open('toregex')
	arquivo2 = open('tonpm', 'w')
	for line in arquivo.readlines():
		encontrado = exp.search(line)
		arquivo2.write(encontrado.group(0)[1:-1] + '\n')
	arquivo2.close()

import subprocess
def toNpm():
	arquivo = open('tonpm')
	arquivo2 = open('toplanilhas.csv', 'w')
	num_line = 1
	for line in arquivo.readlines():
		resp = subprocess.getstatusoutput('npm view {0} dependencies'.format(line[:-1]))[1]
		qtdDependencias = resp.count(',')+1
		resp = subprocess.getstatusoutput('npm view {0} versions'.format(line[:-1]))[1]
		qtdVersions = resp.count(',')+1
		if qtdDependencias < 4 or qtdVersions < 4:
			continue
		if(num_line == 3):
			break
		num_line += 1
		print(num_line, '\"' + line[:-1] + '\",\"' + str(qtdDependencias) + '\",\"' + str(qtdVersions) + '\"')
		arquivo2.write('\"' + line[:-1] + '\",\"' + str(qtdDependencias) + '\",\"' + str(qtdVersions) + '\",\n')	# "pacote", "qtd_dependencia", "qtdVersions"
	arquivo2.close()

import csv
import threading

def toCSV(package):
	print("executando para o pacote " + package)
	csvReader = csv.reader(open('npmdep.csv', 'r'), delimiter=',', quotechar='\n')
	arquivo2 = open(package+'.csv', 'w')
	#                   0               2                   4                      5                      10                
	fieldnames = ['client_name', 'client_version', 'client_timestamp', 'client_version_branch', 'client_previous_timestamp',
	#     14                    15                 16                               18               
	'dependency_name', 'dependency_type', 'dependency_version_range', 'dependency_resolved_version']# cabecalho do novo arquivo
	csvWriter = csv.DictWriter(arquivo2, fieldnames=fieldnames)										# abro como CSV
	csvWriter.writeheader()																			# escrevo o cabecalho
	#qtdLinha = 0
	try:
		while True:
			#qtdLinha += 1
			linha = csvReader.__next__()
			if linha[0].__eq__(package):
				csvWriter.writerow({'client_name': linha[0], 'client_version': linha[2], 'client_timestamp': linha[4],
					'client_version_branch': linha[5], 'client_previous_timestamp': linha[10], 'dependency_name': linha[14],
					'dependency_type': linha[15], 'dependency_version_range': linha[16], 'dependency_resolved_version': linha[18]})
	except StopIteration:
		#print('Quantidade de linhas:', qtdLinha)
		print('terminou para o pacote ' + pacote)
		arquivo2.close()

for package in ['inert','gulp-shell','csv','restler','chai','nunjucks','gulp-notify','mocha','grunt','restify','handlebars']:
	threading.Thread(target=toCSV,args=(package,)).start()

print('foi todas')