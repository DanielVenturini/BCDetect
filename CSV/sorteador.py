import re
import csv
import random
import requests

def getPackage(packageName):
    return requests.get('https://registry.npmjs.org/'+packageName).json()

def getVersoes(package):
    try:
        versoes = list(package['versions'].keys())
        return len(versoes)
    except KeyError:
        return 0

def getScriptTest(package):
    try:
        versoes = list(package['versions'].keys())
        return package['versions'][versoes[-1]]['scripts']['test']
    except KeyError:
        return 'no test specified'

def getDependencias(package):
    try:
        versoes = list(package['versions'].keys())
        dependencies = package['versions'][versoes[-1]]['dependencies']
        return len(list(dependencies.keys()))
    except KeyError:
        return 0

def getTest(package):
    stringTest = getScriptTest(package)

    if stringTest.lower().__contains__('no test specified'):
        return False
    elif len(stringTest) < 2:
        return False
    else:
        return True

def resolvUrl(url):
    try:
        if url.__contains__('github'):
            return 'https://github.com/' + re.search('[\/|:][\w]+\/[\w]+', url).group(0)[1:]
        else:
            return url
    except:
        return url

def getUrl(package):
    try:
        versoes = list(package['versions'].keys())
        url = package['versions'][versoes[-1]]['repository']['url']
        return resolvUrl(url)
    except KeyError:
        return False

def sorteador(quantidade):
    qtd = 0
    linhasSorteadas = []
    file = open('pacotessorteados.csv', 'w')
    csvWriter = file
    csvWriter.write('pacote, qtd_versoes, qtd_dependentes, url_repo\n')

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
        package = getPackage(pacote)

        qtdDepende = getDependencias(package)
        qtdVersoes = getVersoes(package)
        test = getTest(package)
        url_repo = getUrl(package)

        print('package: {0}; dependecies: {1}; versions: {2}; test: {3}; url: {4}'.format(pacote, qtdDepende, qtdVersoes, test, url_repo), end=' - ', flush=True)
        if url_repo and test and qtdVersoes > 4 and qtdDepende > 4:
            qtd += 1
            print('OK -', qtd)
            csvWriter.write('{0}, {1}, {2}, {3}\n'.format(pacote, qtdVersoes, qtdDepende, url_repo))
        else:
            print('ERR')

    file.close()

sorteador(1)