import csv
import json

def get_line(package, qtd_versions, qtd_depends, qtd_sucess, qtd_err, link):
	return package + ',' + qtd_version + ',' + qtd_depends + ',' + qtd_sucess + ',' + qtd_err + ',' + link

def count_results(packageName):
	try:
		file = csv.reader(open('../workspace/{}_results.csv'.format(packageName)), delimiter=',', quotechar='\n')
		npm_package = json.load(open('../CSV/packagejson/npm_packs_2017-06-01/{}.json'.format(packageName)))
		fileOutput = open('result.csv', 'a+')
	except Exception as ex:
		print('File: ' + packageName + ' not exists: ' + ex)

	try:
		file.__next__() # jump the header
		qtd_versions = 0
		qtd_depends = 0
		'''while True:
			linha = csvReader.__next__()
			if linha[0].__eq__(package):
				encontrou = True
				csvWriter.writerow({'client_name': linha[0], 'client_version': linha[2], 'client_timestamp': linha[4], 
					'client_previous_timestamp': linha[10], 'dependency_name': linha[14], 'dependency_type': linha[15],
					'dependency_resolved_version': linha[18], 'dependency_resolved_version_change': linha[28]})
				continue

			if encontrou:
				raise StopIteration
		'''

	except StopIteration:
		print('OK')
		arquivo2.close()

count_results('phoenix-cypto')