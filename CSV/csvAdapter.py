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