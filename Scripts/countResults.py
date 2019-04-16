import csv
import json

def get_line(package, qtd_versions, qtd_depends, qtd_sucess, qtd_err, link):
	return package + ',' + str(qtd_versions) + ',' + str(qtd_depends) + ',' + str(qtd_sucess) + ',' + qtd_err + ',' + link

def count_results(packageName):
	try:
		file = csv.reader(open('../workspace/{}_results.csv'.format(packageName)), delimiter=',', quotechar='\n')
		npm_package = json.load(open('../CSV/packagejson/npm_packs_2017-06-01/{}.json'.format(packageName)))
		fileOutput = open('result.csv', 'a+')
	except Exception as ex:
		print('File: ' + packageName + ' not exists: ' + ex)

	try:
		file.__next__() # jump the header
		versions = npm_package['versions']
		latest_version = npm_package['dist-tags']['latest']
		latest_release = versions[latest_version]
		qtd_versions = len(versions.keys())
		qtd_depends = len(latest_release['dependencies']) + len(latest_release['devDependencies'])
		print(get_line(packageName, qtd_versions, qtd_depends, 'anyvalue', 'anyvalue', 'anyvalue'))
	except StopIteration:
		print('OK')
		fileOutput.close()

count_results('phoenix-cypto')