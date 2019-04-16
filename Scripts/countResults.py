import re
import csv
import json

def get_line(package, qtd_versions, qtd_depends, qtd_sucess, qtd_err, link):
	return package + ',' + str(qtd_versions) + ',' + str(qtd_depends) + ',' + str(qtd_sucess) + ',' + str(qtd_err) + ',,,' + link + '\n'

def resolvUrl(package):
	try:
		url = package['repository']['url']
		if url.__contains__('github'):
			return 'https://github.com/' + re.search('[\/|:](\w|-|_|@|:)+\/(\w|-|_|@)+', url).group(0)[1:]
		else:
			return 'https://github.com/danielventurini/false'
	except Exception as ex:
		print(ex)
		return 'https://github.com/danielventurini/false'

def get_mapped(package, key):
	try:
		return package[key]
	except KeyError:
		return ''

def get_dependencies(package):
	result = 0
	result += len(get_mapped(package, 'dependencies'))
	result += len(get_mapped(package, 'devDependencies'))

	return result

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
		qtd_depends = get_dependencies(latest_release)
		qtd_sucess = 0
		qtd_err = 0
		link = resolvUrl(latest_release)

		while True:
			line = file.__next__()
			if line[3].__eq__('OK') and line[4].__eq__('OK'):
				qtd_sucess += 1
			else:
				qtd_err += 1

	except StopIteration:
		fileOutput.write(get_line(packageName, qtd_versions, qtd_depends, qtd_sucess, qtd_err, link))
		print('.')
		fileOutput.close()

# write a header
fileOutput = open('result.csv', 'w')
fileOutput.write('pacote,qtd_versoes,qtd_dependentes,qtd_sucess,qtd_err,erros_encontrados,cores,url_repo\n')
fileOutput.close()

count_results('phoenix-cypto')
count_results('svg-sprite_l')
count_results('xbee-stream')
count_results('sparkbar')
count_results('retrial')
count_results('nextprot')
count_results('deskbookers-react-intl')
count_results('snap-points-2d')
count_results('simply-build')
count_results('gulp-inject-html')
count_results('virtual-scroll')
count_results('keydir')
count_results('oddity')
count_results('sails-hook-seed')
count_results('postcss-inrule')
count_results('indeed-api-client')
count_results('light-swift')
count_results('primer-forms')
count_results('redux-async-load')