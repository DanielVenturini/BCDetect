import json

def open_file(file_name, is_json=False, header=False):
	try:
		file = open(file_name, 'w' if is_json else 'r')

		if is_json:
			file = json.load(file)
			header = False
	except FileNotFoundError:
		print('File {} not found'.format(file_name))
	else:
		if header:
			file.readline()

		return file

def close_file(file, file_name='results.json', is_json=False):
	try:
		if is_json:
			json.dump(file, open(file_name, 'w'), indent=2)
		else:
			file.close()
	except FileNotFoundError:
		print('File {} couldn\'t be saved'.format(file_name))

def get_providers(providers):
	return providers.split('->')

def generate_json(file_csv_name='results.csv', file_json_name='results.json'):
	file_csv  = open_file(file_csv_name, header=True)
	file_json = {}

	try:
		for line in file_csv.readlines():
			'''
				[0]  client
				[1]  provider
				[2]  affected_clients_releases
				[3]  category
				[4]  description
				[5]  documentation
				[6]  fixed_by
				[7]  fixed_after_days
				[8]  fixed_after_releases
				[9]  introduced_in
				[10] fixed_in
				[11] provider_was
				[12] client_affected_by
			'''
			fields = line.split(',')
			bc = {
				'providers': get_providers(fields[1]),
				'affected_clients_releases': int(fields[2]),
				'category': fields[3].lower(),
				'description': fields[4],
				'documentation': fields[5].lower(),
				'fixed_by': fields[6].lower(),
				'fixed_after_days': int(fields[7].replace('--', '-1')),
				'fixed_after_releases': int(fields[8].replace('--', '-1')),
				'introduced_in': fields[9],#.lower(),
				'fixed_in': fields[10],#.lower(),
				'provider_was': fields[11].lower(),
				'client_affected_by': fields[12].lower(),
				'time_until_introduction': int(fields[13]),
				'introduced_after_releases': int(fields[14].strip())
			}

			# file_json[client] = breaking change
			try:
				file_json[fields[0]].append(bc)
			except KeyError:
				file_json[fields[0]] = [bc]

	except Exception as ex:
		print(ex)
		print(fields[7])
		print(fields[8])
		# do nothing, because the csv.__next__ raise
		# an Exception when it arrives at file end
		pass

	close_file(file_csv, file_csv_name)
	close_file(file_json, file_json_name, is_json=True)






generate_json()