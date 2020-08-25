'''
This script aims to update all the 384 packages
'''

import csv
import json
import requests
import datetime
from os.path import join
from copy import deepcopy
from os.path import isfile


PATH_OLDS  = join('.', 'CSV', 'packagejson', 'npm_packs_2017-06-01', '{}.json')
PATH_NEW   = join('.', 'CSV', 'packagejson', 'npm_packs_new', '{}.json')
PATH_DIFF  = join('.', 'CSV', 'packagejson', 'npm_packs_diff', '{}.json')
PATH_CSV   = join('.', 'CSV', 'packagejson', 'CSV', '{}.csv')
PATH_PACKAGES = join('.', 'CSV', 'packagejson', 'sample.csv')

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
		# print('CACHE {}'.format(package_name))
		return json.load(open(FILE_CACHE))
	else:
		# print('NPM   {}'.format(package_name))
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
def get_latest_time(package):
	try:
		return get_datetime(package['time'][package['dist-tags']['latest']])
	except KeyError as ex:
		print('{0} -> {1}'.format(ex, package['_id']))
		return get_datetime(package['time']['modified'])


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
	last_time_ori = get_latest_time(package_ori)
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

		new_date = get_latest_time(package_diff)
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
In each dev type, return the provider name and its version
'''
def get_providers(package, version, dep_type):
	provs = []
	try:
		for prov in package['versions'][version][dep_type]:
			# provider, its version, its change
			provs.append((prov, package['versions'][version][dep_type][prov], ''))
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
	else:
		return 'notdependency'


'''
Create the rows of the file. For each dependency type, get each dependency
and get its information, such as resolved version
'''
def get_providers_by_type(package_name, package, version, writer, timestamp, prev_timestamp):
	for dep_type in ['dependencies', 'devDependencies', 'peerDependencies', 'optionalDependencies', 'globalDependencies']:
		for provinfo in get_providers(package, version, dep_type):

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
	packages = get_package_names()

	for package_name in packages:
		if not isfile(PATH_DIFF.format(package_name)):
			continue

		package = get_package(package_name, PATH_DIFF)
		writer = create_writer(package_name, package, PATH_CSV)

		prev_timestamp = ''
		for version in package['versions']:
			timestamp = package['time'][version]
			get_providers_by_type(package_name, package, version, writer, timestamp, prev_timestamp)

			prev_timestamp = timestamp

		writer.close()


if __name__ == '__main__':
	# verify_new_releases()
	generate_new_csv()