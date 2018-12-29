import sys
import csv
from multiprocessing import Process

'''
	Script para recuperar do csv todas as ocorrências de um determinado pacote.
	Pode ser usado como 'python3 recuperaCSV.py pacotessorteados.csv' após ter usado o script de sortear
	Ou pode ser usado como 'python3 recuperaCSV.py --package package1 package2 ...'
'''

def toCSV(package, url_repo=''):
	print(package + ': ', end='', flush=True)
	csvReader = csv.reader(open('npmdep.csv', 'r'), delimiter=',', quotechar='\n')
	arquivo2 = open(package+'.csv', 'w')
	#                   0               2                   4                      10
	fieldnames = ['client_name', 'client_version', 'client_timestamp', 'client_previous_timestamp',
	#     14                    15                 18                               28
	'dependency_name', 'dependency_type', 'dependency_resolved_version', 'dependency_resolved_version_change', url_repo]# cabecalho do novo arquivo
	csvWriter = csv.DictWriter(arquivo2, fieldnames=fieldnames)										# abro como CSV
	csvWriter.writeheader()																			# escrevo o cabecalho
	encontrou = False

	try:
		while True:
			#qtdLinha += 1
			linha = csvReader.__next__()
			if linha[0].__eq__(package):
				encontrou = True
				csvWriter.writerow({'client_name': linha[0], 'client_version': linha[2], 'client_timestamp': linha[4], 
					'client_previous_timestamp': linha[10], 'dependency_name': linha[14], 'dependency_type': linha[15],
					'dependency_resolved_version': linha[18], 'dependency_resolved_version_change': linha[28]})

			if encontrou:
				raise StopIteration

	except StopIteration:
		print('OK')
		arquivo2.close()

if len(sys.argv) > 1:
	# se os pacotes forem passados direto do terminal
	if sys.argv.__contains__('--packages'):

		for i in range(2, len(sys.argv)):
			toCSV(sys.argv[i])

	else:	# senão, recupera de um arquivo
		print(sys.argv[1])

		listaPacotes = csv.reader(open(sys.argv[1]), delimiter=',', quotechar='\n')

		try:

			# pula o cabeçalho
			listaPacotes.__next__()
			# processos que irão executar: 6 processos paralelos
			NUM_PROCESS = 6
			process = list(range(0, NUM_PROCESS))
			while True:
				for i in range(0, NUM_PROCESS):
					# pacote, qtd_versoes, qtd_dependentes, url_repo
					linha = listaPacotes.__next__()
					process[i] = Process(target=toCSV, args=(linha[0], linha[3]))
					process[i].start()
					#toCSV(linha[0], linha[3])

				# aguarda todos os processos
				for i in range(0, NUM_PROCESS):
					process[i].join()

		except StopIteration:
			pass

		try:
			# aguarda todos os processos restantes
			for i in range(0, NUM_PROCESS):
				process[i].join()

		except AttributeError:
			pass
else:
	print('USE: python3 recuperaCSV.py pacotessorteados.csv')