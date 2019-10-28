import re
import sys
import csv
import time
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

def getGenericDependencies(package, depType):
    try:
        return len(list(package['latest'][depType].keys()))
    except:
        return 0

def getDependencias(package):
    return \
        getGenericDependencies(package, 'dependencies') + \
        getGenericDependencies(package, 'devDependencies') + \
        getGenericDependencies(package, 'peerDependencies') + \
        getGenericDependencies(package, 'optionalDependencies')

def getTest(package):
    try:
        stringTest = getScriptTest(package)

        if stringTest.lower().__contains__('no test specified'):
            return False
        elif len(stringTest) < 2:
            return False
        else:
            return True
    except:
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
        versoes = list(package['versions'].keys())
        versoes.sort()
        url = package['versions'][versoes[-1]]['repository']['url']
        return resolvUrl(url)
    except:
        return 'https://github.com/danielventurini/false'

def verifyExistsRepo(url_repo):
    # avoid request in false repository
    if url_repo.__eq__('https://github.com/danielventurini/false'):
        return False

    # avoid DoS in github
    time.sleep(1)
    return requests.head(url_repo).ok

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
    csvReader.__next__()    # ignorando a primeira linha
    dependencias = []
    releases = []
    count  = 0
    limit = 0

    try:
        while True:
            pacote = csvReader.__next__()[0]
            package = getPackage(pacote)

            qtdDepende = getDependencias(package)
            qtdVersoes = getVersoes(package)
            test = getTest(package)
            url_repo = getUrl(package)

            if qtdDepende >= 1 and url_repo and test:
                if verifyExistsRepo(url_repo):
                    dependencias.append(qtdDepende)
                    releases.append(qtdVersoes)

            if count == limit:
                print(count)
                limit += 1000

    except Exception as ex:
        print('Err: ' + str(ex))

    salvaInformacoes(dependencias, releases)

try:
    if len(sys.argv) > 1 and len(sys.argv) < 3:
        geraBoxPlot(sys.argv[1])
    else:
        print("USE: python3 geraBoxPlot.py todos_pacotes.csv")
except Exception as ex:
    pass