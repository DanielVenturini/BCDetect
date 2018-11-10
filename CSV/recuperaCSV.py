import sys
import csv

def toCSV(package):
	print(package + ': ', end='', flush=True)
	csvReader = csv.reader(open('npmdep.csv', 'r'), delimiter=',', quotechar='\n')
	arquivo2 = open(package+'.csv', 'w')
	#                   0               2                   4                      10
	fieldnames = ['client_name', 'client_version', 'client_timestamp', 'client_previous_timestamp',
	#     14                    15                 18
	'dependency_name', 'dependency_type', 'dependency_resolved_version']# cabecalho do novo arquivo
	csvWriter = csv.DictWriter(arquivo2, fieldnames=fieldnames)										# abro como CSV
	csvWriter.writeheader()																			# escrevo o cabecalho
	try:
		while True:
			#qtdLinha += 1
			linha = csvReader.__next__()
			if linha[0].__eq__(package):
				csvWriter.writerow({'client_name': linha[0], 'client_version': linha[2], 'client_timestamp': linha[4], 
					'client_previous_timestamp': linha[10], 'dependency_name': linha[14], 'dependency_type': linha[15],
					'dependency_resolved_version': linha[18]})
	except StopIteration:
		print('OK')
		arquivo2.close()


if len(sys.argv) > 1:
	print(sys.argv[1])
	listaPacotes = csv.reader(open(sys.argv[1]), delimiter=',', quotechar='\n')

	try:

		# pula o cabeçalho
		listaPacotes.__next__()
		while True:
			# pacote, qtd_versoes, qtd_dependentes
			linha = listaPacotes.__next__()
			toCSV(linha[0])

	except StopIteration:
		pass

else:
	print('USE: python3 recuperaCSV.py listaPacotes.csv')