import csv
import subprocess
import random

def sorteador(quantidade):
	qtd = 0
	linhasSorteadas = []
	csvWriter = open('pacotessorteados.csv', 'w')
	csvWriter.write('pacote, qtd_versoes, qtd_dependentes\n')

	while qtd < quantidade:							# recupera 30 pacotes

		csvReader = csv.reader(open('npmdep.csv', 'r'), delimiter=',', quotechar='\n')
		packageLine = random.randint(0, 31608634)	# sorteia uma linha

		print('linha sorteada:', packageLine)
		if linhasSorteadas.count(packageLine):		# se esta linha já foi sorteada
			continue								# volta ao começo e sorteia novamente

		linhasSorteadas.append(packageLine)			# adiciona como linha já sorteada
		line = 1

		while line < packageLine:					# avança até a linha sorteada
			csvReader.__next__()
			line += 1

		pacote = csvReader.__next__()[0]
		qtdVersoes = subprocess.getstatusoutput('npm view {0} versions'.format(pacote))[1].count(',')+1
		qtdDepende = subprocess.getstatusoutput('npm view {0} dependencies'.format(pacote))[1].count(',')+1

		print('package: {0}; versions: {1}; dependecies: {2}'.format(pacote, qtdVersoes, qtdDepende), end=' - ', flush=True)
		if qtdVersoes > 4 and qtdDepende > 4:
			qtd += 1
			print('OK -', qtd)
			csvWriter.write('{0}, {1}, {2}\n'.format(pacote, qtdVersoes, qtdDepende))
		else:
			print('ERR')

sorteador(12)