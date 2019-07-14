import csv

csvReader = csv.reader(open('npmdep.csv'), delimiter=',', quotechar='\n')
csvWriter = open('all_packages.csv', 'w')

try:
    last_package = ''
    while True:
        linha = csvReader.__next__()
        if linha[0].__eq__(last_package):
            continue

        last_package = linha[0]
        csvWriter.write(last_package + '\n')
except StopIteration:
    print('OK')
    csvWriter.close()