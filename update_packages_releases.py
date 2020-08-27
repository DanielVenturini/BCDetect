'''
This script aims to update all the 384 packages
'''

import re
import csv
import json
import requests
import datetime
from os import mkdir
import semantic_version
from lamp import worker
from copy import deepcopy
from os.path import join, isfile, isdir


PATH_OLDS  = join('.', 'CSV', 'packagejson', 'npm_packs_2017-06-01', '{}.json')
PATH_NEW   = join('.', 'CSV', 'packagejson', 'npm_packs_new', '{}.json')
PATH_DIFF  = join('.', 'CSV', 'packagejson', 'npm_packs_diff', '{}.json')
PATH_CSV   = join('.', 'CSV', 'packagejson', 'CSV', '{}.csv')
PATH_CSV_OLD  = join('.', 'CSV', '{}.csv')
PATH_PACKAGES = join('.', 'CSV', 'packagejson', 'sample.csv')
PATH_NEXT     = join('.', 'CSV', 'packagejson', 'sample_next.csv')
PATH_RESULTS  = join('.', 'workspace', '{}_results.csv')

PACKAGE_URL = 'http://registry.npmjs.org/{}'
CSV_HEADER = 'client_name,client_version,client_timestamp,client_previous_timestamp,dependency_name,dependency_type,dependency_resolved_version,dependency_resolved_version_change, {}\n'	# this last one is the repo url

# STATISTICAL
remain_packages = 0
remain_releases = 0
last_date = datetime.datetime(2017, 6, 1)
max_date = datetime.datetime(2020, 4, 1, 23, 59, 59)


'''
Return the all 384 package names
'''
def get_package_names(packages=PATH_PACKAGES):
	names = []
	for line in csv.reader(open(packages), delimiter=',', quotechar='\n'):
		if line[0].startswith('#'):
			continue

		names.append(line[0])

	return names


'''
Save the file in the specific location
'''
def save_package(package, filedir):
	if not package:
		return

	json.dump(package, open(filedir, 'w'))
	return package


'''
Get the package from npm and save it in the filedir=PATH_NEW
'''
def get_package_npm(package_name, filedir, attempt=0):

	try:
		response = requests.request('GET', PACKAGE_URL.format(package_name), timeout=3)

		if response.status_code == 404:
			print('PACKAGE {} not found'.format(package_name))
		else:
			save_package(response.json(), filedir)
	except requests.exceptions.ReadTimeout:
		return get_package_npm(package_name, filedir, attempt+1) if attempt < 3 else {}


'''
Return the metadata package from the package_name
If it is already in the PATH_NEW, it was downloaded and may be used
If not, the package will be downloaded from PACKAGE_URL and saved in PATH_NEW
'''
def get_package(package_name, PATH):
	FILE_CACHE = PATH.format(package_name)	# just a conveninet name
	if isfile(FILE_CACHE):
		print('    CACHE {}'.format(package_name))
		return json.load(open(FILE_CACHE))
	else:
		print('    NPM   {}'.format(package_name))
		return get_package_npm(package_name, FILE_CACHE)


'''
Return a datetime object from a string
'''
def get_datetime(datestr):
	date, time = datestr.split('T')
	year, month, day = date.split('-')
	hour, minutes, seconds = time.split(':')
	seconds, mili = seconds.split('.')

	return datetime.datetime(int(year), int(month), int(day), int(hour), int(minutes), int(seconds), int(mili[:-1]))


'''
Return the last time that a version was published
'''
def get_latest_time(package, greatest_date):
	return get_datetime(package['time'][list(package['time'])[-1]])


def delete(package, key, version):
	try:
		del(package[key][version])
	except KeyError:
		pass

'''
Create a new packagejson that does not have the versions that are in both packages
'''
def create_diff(package_ori, package_new):
	global remain_packages, remain_releases, last_date, max_date
	key_imp = 0 # modified and created keys
	last_time_ori = get_latest_time(package_ori, last_date)
	previous_timestamp = last_time_ori
	previous_version = '0.0.0'
	setted = False
	package_diff = deepcopy(package_new)

	# remove from the package_new all versions that are in the ori
	for version in package_new['time']:
		if version == 'modified' or version == 'created':
			key_imp += 1
			continue

		current_time = get_datetime(package_new['time'][version])
		# delete
		if current_time <= last_time_ori or current_time > max_date:
			delete(package_diff, 'time', version)
			delete(package_diff, 'versions', version)

		# for releases after the Apr. 2020
		if (not setted) and current_time > max_date:
			package_diff['time']['modified'] = str(previous_timestamp).replace(' ', 'T')
			package_diff['dist-tags']['latest'] = previous_version
			setted = True


		previous_timestamp = current_time
		previous_version = version

	remain = len(package_diff['time']) - key_imp
	if remain > 0:
		print('{0} {1}'.format(remain, package_ori['_id']))
		remain_packages += 1
		remain_releases += remain

		new_date = get_latest_time(package_diff, max_date)
		if last_date < new_date:
			last_date = new_date
	else:
		return None

	return package_diff


'''
Verify if there are new releases for each package in PATH_PACKAGES
and verify the the diff between that with the one in the PATH_OLDS
and update the new ones storing the new json file in PATH_NEW
'''
def verify_new_releases():
	packages = get_package_names()

	# verify the diff
	for package in packages:
		package_ori = get_package(package, PATH_OLDS)
		package_new = get_package(package, PATH_NEW)

		package_diff = create_diff(package_ori, package_new)
		save_package(package_diff, PATH_DIFF.format(package))

	print()
	print('=======================')
	print('Remain packages: {}'.format(remain_packages))
	print('Remain releases: {}'.format(remain_releases))
	print('Snapshot time  : {}'.format(last_date))


'''
Create the file writer and save it in PATH_DIFF
Also, insert the header
'''
def create_writer(package_name, package, PATH):
	writer = open(PATH.format(package_name), 'w')
	writer.write(CSV_HEADER.format(package['repository']['url']))

	return writer


'''
Use the vigilant-lamp to solve the providers version
'''
def resolve_version(prov_name, semverstr, timestamp, NPM_CACHE):
	prov_path = prov_name
	if prov_name.startswith('@'):
	 	prov_path = prov_name.split('/')[0]
	 	prov_path = PATH_NEW.format(prov_path).replace('.json', '')
	 	if not isdir(prov_path):
	 		mkdir(prov_path)

	return worker.worker(prov_name, semverstr, timestamp, get_package(prov_name, PATH_NEW), NPM_CACHE)


'''
Return the type of change from the previous client release:
steady
upgrade

'''
def get_version_change(client_version, prov_name, new_version, CHANGELOG):

	change = ''
	try:
		prev_version = CHANGELOG[CHANGELOG[client_version]['previous_version']][prov_name]
		change = 'steady' if prev_version == new_version else 'upgraded'	# I'll assume it
	except KeyError:
		pass

	CHANGELOG[client_version][prov_name] = new_version
	return change


'''
In each dev type, return the provider name and its version
'''
def get_providers(package, version, dep_type, timestamp, CHANGELOG, NPM_CACHE):
	provs = []
	try:
		for prov in package['versions'][version][dep_type]:
			# provider, its version, its change
			resolved_version = resolve_version(prov, package['versions'][version][dep_type][prov], timestamp, NPM_CACHE)
			provs.append((prov, resolved_version, get_version_change(version, prov, resolved_version, CHANGELOG)))
	except KeyError:
		pass

	return provs


'''
Resolve the dep type
Domain Type Server
'''
def DTS(dep_type):
	if dep_type == 'dependencies':
		return 'dependency'
	elif dep_type == 'devDependencies':
		return 'dev_dependency'
	elif dep_type == 'peerDependencies':
		return 'peer_dependency'
	elif dep_type == 'optionalDependencies':
		return 'optional_dependency'
	else:
		return 'global_dependency'


'''
Insert the value as a map of secondkey, that is a map of firstkey in the obj
'''
def insert_obj(obj, firstkey, secondkey, value):
	try:
		obj[firstkey][secondkey] = value
	except KeyError:
		obj[firstkey] = {}
		insert_obj(obj, firstkey, secondkey, value)


'''
Create the changelog, it means, open the old executed csv and get all version
'''
def create_changelog(package_name):
	CHANGELOG = {}
	reader = open(PATH_CSV_OLD.format(package_name))
	reader.readline()	# skip header
	prev_version = ''

	for line in reader.readlines():
		line = line.split(',')
		# client_version, provider_name, provider_resolved_version
		insert_obj(CHANGELOG, line[1], line[4], line[6])
		prev_version = line[1]

	return CHANGELOG, prev_version


'''
Create the rows of the file. For each dependency type, get each dependency
and get its information, such as resolved version
'''
def get_providers_by_type(package_name, package, version, prev_version, writer, timestamp, prev_timestamp, CHANGELOG, NPM_CACHE):

	for dep_type in ['dependencies', 'devDependencies', 'peerDependencies', 'optionalDependencies', 'globalDependencies']:
		for provinfo in get_providers(package, version, dep_type, timestamp, CHANGELOG, NPM_CACHE):

			writer.write('{0},{1},{2},{3},{4},{5},{6},{7},\n'.format(
				package_name,
				version,
				timestamp,
				prev_timestamp,
				provinfo[0],
				DTS(dep_type),
				provinfo[1],
				provinfo[2]
			))


'''
Generate the new csv files to each package resolving their ranges
c_name,c_version,c_timestamp,c_previous_timestamp,d_name,d_type,d_resolved_version,d_resolved_version_change,https://github.com/user/package
'''
def generate_new_csv():
	packages = get_package_names(PATH_NEXT)
	NPM_CACHE = {}

	for package_name in packages:
		print(package_name)
		if not isfile(PATH_DIFF.format(package_name)):
			continue

		package = get_package(package_name, PATH_DIFF)
		writer = create_writer(package_name, package, PATH_CSV)

		prev_timestamp = ''

		CHANGELOG, prev_version = create_changelog(package_name)

		for version in package['versions']:
			insert_obj(CHANGELOG, version, 'previous_version', prev_version)	# insert the previous version from csv at packagejson
			timestamp = package['time'][version]
			get_providers_by_type(package_name, package, version, prev_version, writer, timestamp, prev_timestamp, CHANGELOG, NPM_CACHE)

			prev_timestamp = timestamp
			prev_version = version

		writer.close()


def is_range(version):
    return version.__contains__('^') or \
           version.__contains__('~') or \
           version.__contains__('>') or \
           version.__contains__('<') or \
           version.__contains__('*') or \
           version.__contains__('.x') or \
           version.__contains__('latest') or \
           version.__contains__('||') or \
           version.__eq__('next') or \
           version.__eq__('')


def verify_executable():
	packages = get_package_names(PATH_NEXT)
	count_releases = 0
	count_packages = 0

	for package_name in packages:
		reader = csv.reader(open(PATH_CSV.format(package_name)), delimiter=',', quotechar='\n')

		count_releases_package = 0
		previous_version = 'x.y.z'
		stop = False
		for line in reader:
			line.append('')
			if is_range(line[6]):
				if not stop:
					print('{')
					print('  "date":"{}",'.format(line[2]))
					print('  "dependencies": {')

				print('    "{0}": "{1}",'.format(line[4], line[6]))
				stop = True

			if line[1] != previous_version and line[7] != 'steady':
				previous_version = line[1]
				count_releases_package += 1

		count_releases += count_releases_package
		if count_releases_package > 1:
			count_packages += 1
		else:
			print(package_name)

		if stop:
			print('  }\n}')
			print('{}'.format(line[0]))
			input()

	print('Releases remain: {}'.format(count_releases))
	print('Packages remain: {}'.format(count_packages))


def is_pre(version):
	if not version.__contains__('-') or version.startswith('git'):
		return False

	if version.lower().__contains__('-alpha') or \
		version.lower().__contains__('-beta') or \
		version.lower().__contains__('-rc') or \
		version.lower().__contains__('-dev') or \
		version.lower().__contains__('-patch') or \
		version.lower().__contains__('-git') or \
		version.lower().__contains__('-pre') or \
		version.lower().__contains__('beta'):
		return True

	if re.search('\d+\.\d+\.\d+\-[\d\w]', version):
		return True

	return False

def verify_order():
	packages = get_package_names(PATH_NEXT)

	for package_name in packages:
		reader = csv.reader(open(PATH_CSV.format(package_name)), delimiter=',', quotechar='\n')
		reader.__next__()	# skip header

		prev_version = reader.__next__()[1]
		for line in reader:
			cur_version = line[1]
			if semantic_version.Version(prev_version) > semantic_version.Version(cur_version):
				print(package_name)
				break
			prev_version = cur_version

def verify_results():
	packages = get_package_names(PATH_NEXT)

	packages_error = 0
	packages_success = 0
	releases_error = 0
	releases_success = 0

	for package_name in packages:
		reader = csv.reader(open(PATH_RESULTS.format(package_name)), delimiter=',', quotechar='\n')
		reader.__next__()	# skip header

		all_releases_success = True
		for line in reader:
			if line[2] == 'OK':
				release_executed = True

				if line[4] == 'OK':
					releases_success += 1
				else:
					releases_error += 1
					all_releases_success = False

		if all_releases_success:
			packages_success += 1
		else:
			packages_error += 1

	print('Packages success: {}'.format(packages_success))
	print('Packages error  : {}'.format(packages_error))
	print('releases success: {}'.format(releases_success))
	print('releases error  : {}'.format(releases_error))


if __name__ == '__main__':
	# verify_new_releases()
	# generate_new_csv()
	# verify_executable()
	# verify_order()
	verify_results()
	# to verify the pre-releases
	# for package_name in get_package_names(PATH_NEXT):
	# 	packages = json.load(open('./CSV/packagejson/npm_packs_new/{}.json'.format(package_name)))
	# 	for version in packages['versions']:
	# 		for types in ['dependencies', 'devDependencies', 'peerDependencies', 'globalDependencies', 'optionalDependencies']:
	# 			try:
	# 				for prov in packages['versions'][version][types]:
	# 					is_pre(packages['versions'][version][types][prov])
	# 			except KeyError:
	# 				pass
	## NOT IN THE ORDER
	# jeggy-mongoose
	# paypal-rest-sdk
	# kelper
	# nanocomponent
	# nexmo-cli
	# heroku-cli-util
	# ubk
	# angular2-jsonapi
	# contentful-import
	# assetgraph-builder
	# riot
	# testcafe
	# ut-test
	# primer-forms