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
        package = json.load(open('./packagejson/npm_packs_2017-06-01/{0}.json'.format(packageName)))
        setLatest(package)
        return package
    except FileNotFoundError:
        return {'error': "Not found"}

def setLatest(package):

    try:
        versions = list(package['versions'].keys())
        versions.sort()
        latest = package['dist-tags']['latest']

        for version in versions:
            specifyPackage = package['versions'][version]
            if specifyPackage['version'].__eq__(latest):
                package['latest'] = specifyPackage
                return

        package['latest'] = package['versions'][versions[-1]]
    except:
        versoes = list(package['versions'].keys())
        package['latest'] = package['versions'][versoes[-1]]


def getVersoes(package):
    try:
        versoes = list(package['versions'].keys())
        return len(versoes)
    except:
        return 0

def getScriptTest(package):
    try:
        return package['latest']['scripts']['test']
    except:
        return 'no test specified'

def getDependencias(package):
    try:
        return len(list(package['latest']['dependencies'].keys()))
    except:
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
            return 'https://github.com/danielventurini/false'
    except:
        return 'https://github.com/danielventurini/false'

def getUrl(package):
    try:
        url = package['latest']['repository']['url']
        return resolvUrl(url)
    except:
        return 'https://github.com/danielventurini/false'

def verifyExistsRepo(url_repo):
    return requests.head(url_repo).ok

def sorteador(quantidade):
    qtd = 0
    pacotesSorteados = []
    file = open('pacotessorteados.csv', 'w')
    csvWriter = file
    csvWriter.write('pacote, qtd_versoes, qtd_dependentes, url_repo, had_test, repo_exist\n')

    try:
        while qtd < quantidade:							# recupera 30 pacotes

            csvReader = csv.reader(open('all_packages.csv', 'r'), delimiter=',', quotechar='\n')
            packageLine = random.randint(0, 366629)	    # sorteia uma linha 31608634 ou 366629

            print('linha sorteada:', packageLine)
            if pacotesSorteados.__contains__(packageLine):  # se o pacote já foi sorteado
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
            csvWriter.write('{0}, {1}, {2}, {3}, {4}, {5}\n'.format(pacote, qtdVersoes, qtdDepende, url_repo, test, repo_exists))
            if qtdDepende >= 1 and url_repo and test and repo_exists:
                qtd += 1
                print('OK')
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