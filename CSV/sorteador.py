import re
import sys
import csv
import json
import random
import requests

def getPackage(packageName, current=False):
    if current:
        return requests.get('https://registry.npmjs.org/'+packageName).json()

    try:
        return json.load(open('./package.json/npm_packs_2017-06-01/{0}.json'.format(packageName)))
    except FileNotFoundError:
        return {error: "Not found"}

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
            return 'https://github.com/' + re.search('[\/|:](\w|-|_|@|:)+\/(\w|-|_|@)+', url).group(0)[1:]
        else:
            return url
    except:
        return url

def getUrl(package):
    try:
        versoes = list(package['versions'].keys())
        versoes.sort()
        url = package['versions'][versoes[-1]]['repository']['url']
        return resolvUrl(url)
    except KeyError:
        return 'https://github.com/danielventurini/false'

def verifyExistsRepo(url_repo):
    return requests.get(url_repo).ok

def sorteador(quantidade):
    qtd = 0
    pacotesSorteados = []
    file = open('pacotessorteados.csv', 'a')
    csvWriter = file
    #csvWriter.write('pacote, qtd_versoes, qtd_dependentes, url_repo\n')

    try:
        while qtd < quantidade:							# recupera 30 pacotes

            csvReader = csv.reader(open('npmdep.csv', 'r'), delimiter=',', quotechar='\n')
            packageLine = random.randint(0, 366629)	    # sorteia uma linha 31608634 ou 366629

            print('linha sorteada:', packageLine)
            if pacotesSorteados.__contains__(packageLine):  # se o pacote já foi sorteado
                print('já sorteador')
                continue								    # volta ao começo e sorteia novamente

            pacotesSorteados.append(packageLine)		# adiciona como pacote já sorteado
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
            repo_exists = verifyExistsRepo(url_repo)

            print('{5} - {6} - package: {0}; dependecies: {1}; versions: {2}; test: {3}; url: {4}; exists: {7}'.format(pacote, qtdDepende, qtdVersoes, test, url_repo, qtd+1, quantidade, repo_exists), end=' - ', flush=True)
            if url_repo and test and qtdVersoes > 4 and qtdDepende > 4:
                qtd += 1
                print('OK')
                csvWriter.write('{0}, {1}, {2}, {3}\n'.format(pacote, qtdVersoes, qtdDepende, url_repo))
            else:
                print('ERR')

    except Exception as ex:
        print('Err: ' + str(ex))
    finally:
        csvWriter.close()

try:
    if len(sys.argv) > 1 and len(sys.argv) < 3:
        sorteador(int(sys.argv[1]))
    else:
        print("USE: python3 sorteador.py qtd_para_sortear")
except Exception as ex:
    print("USE: python3 sorteador.py qtd_para_sortear: " + str(ex))