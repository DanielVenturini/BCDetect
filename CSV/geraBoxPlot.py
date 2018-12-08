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
        return json.load(open('./packagejson/npm_packs_2017-06-01/{0}.json'.format(packageName)))
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

def salvaInformacoes(dependencias, releases):
    file = open('dataBoxPlot.js', 'w')

    file.write('var data = echarts.dataTool.prepareBoxplotData([\n    [')
    virgula = ','
    for i, value in enumerate(dependencias):
        if i == dependencias.__len__()-1:
            virgula = ''

        file.write('{0}{1}'.format(str(value), virgula))

    file.write('],\n    [')
    virgula = ','
    for i, value in enumerate(releases):
        if i == releases.__len__()-1:
            virgula = ''

        file.write('{0}{1}'.format(str(value), virgula))

    file.write(']\n]);')


def geraBoxPlot(arquivo):
    csvReader = csv.reader(open(arquivo), delimiter=',', quotechar='\n')
    dependencias = []
    releases = []

    try:
        while True:
            pacote = csvReader.__next__()[0]
            package = getPackage(pacote)

            qtdDepende = getDependencias(package)
            qtdVersoes = getVersoes(package)
            test = getTest(package)
            url_repo = getUrl(package)
            repo_exists = verifyExistsRepo(url_repo)

            print('package: {0}; dependecies: {1}; versions: {2}; test: {3}; url: {4}; exists: {5}'.format(pacote, qtdDepende, qtdVersoes, test, url_repo, repo_exists), end=' - ', flush=True)
            if url_repo and test and repo_exists:
                dependencias.append(qtdDepende)
                releases.append(qtdVersoes)
                print('OK')
            else:
                print('ERR')

    except Exception as ex:
        print('Err: ' + str(ex))

    salvaInformacoes(dependencias, releases)

try:
    if len(sys.argv) > 1 and len(sys.argv) < 3:
        geraBoxPlot(sys.argv[1])
    else:
        print("USE: python3 sorteador.py todos_pacotes.csv")
except Exception as ex:
    print("USE: python3 sorteador.py todos_pacotes.csv: " + str(ex))