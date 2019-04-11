import sys

if len(sys.argv) < 2:
	print('USE: python3 aceitos.py file.csv')
	exit(0)
else:
	index = sys.argv[1].index('.csv')
	package_name = sys.argv[1][:index]

fileInput = open(package_name + '.csv')
fileOutput = open(package_name + '_aceitos_ordenados.csv', 'w')

fileOutput.write(fileInput.readline())	# write the header
packages = []
# getting only the accept packages
for line in fileInput.readlines():
	line = line.split(', ')
	line[5] = line[5].rstrip()	# remove '\n' if contains

	if line[4].__eq__('True') and line[5].__eq__('True') and int(line[1]) > 0 and int(line[2]) > 0:
		packages.append(line)

# sort the packages by the releases
def get_value(package):
	return int(package[1])

for index in range(1, len(packages)):

	currentvalue = packages[index]
	position = index

	while position > 0 and get_value(packages[position-1]) > get_value(currentvalue):
		packages[position] = packages[position-1]
		position = position-1

	packages[position] = currentvalue

# just insert in fileOutput the result
def to_str(package, eol):
	return package[0] + ', ' + package[1] + ', ' + package[2] + ', ' + package[3] + ', ' + package[4] + ', ' + package[5] + eol

# end of line
eol = '\n'
for package in packages:
	if package.__eq__(packages[-1]):
		eol = ''

	fileOutput.write(to_str(package, eol))

fileOutput.close()
print('File saved in: ' + package_name + '_aceitos_ordenados.csv')