import json

# ===========
# FIRST GRAPH
# ===========
levels = ['Minor','Minor','Patch','Minor','Patch','Major','Minor','Minor','Patch','Patch','Minor','Minor','Minor','Patch','Minor','Patch','Minor','Patch','Pre','Minor','Patch','Minor','Minor','Minor','Minor','Patch','Minor','Patch','Minor','Patch','Minor','Major','Minor','Patch','Minor','Minor','Patch','Minor','Minor','Patch','Minor','Patch','Minor','Patch','Minor']
for pos, level in enumerate(levels):
	levels[pos] = level.lower()

# =============
# SECOND GRAPH
# =============
result   = json.load(open('results.json'))
minor_bc = []
for client_name in list(result.keys()):
	for case in result[client_name]:
		if case['introduced_in'].__eq__('Minor'):
			minor_bc.append({
				'category': case['category'],
				'fixed_in': case['fixed_in'],
				'fixed_by': case['fixed_by']}
			)

# [{'category': 'wrong code', 'fixed_in': 'patch', 'fixed_by': 'provider'}, {'category': 'renamed function', 'fixed_in': 'patch', 'fixed_by': 'provider'}, {'category': 'incompatible providers versions', 'fixed_in': 'patch', 'fixed_by': 'provider'}, {'category': 'change one rule', 'fixed_in': 'Anyone', 'fixed_by': 'Anyone'}, {'category': 'change type of object', 'fixed_in': 'patch', 'fixed_by': 'client'}, {'category': 'incompatible providers versions', 'fixed_in': 'patch', 'fixed_by': 'provider'}, {'category': 'change one rule', 'fixed_in': 'minor', 'fixed_by': 'client'}, {'category': 'incompatible providers versions', 'fixed_in': 'patch', 'fixed_by': 'provider'}, {'category': 'incompatible providers versions', 'fixed_in': 'patch', 'fixed_by': 'provider'}, {'category': 'change type of object', 'fixed_in': 'patch', 'fixed_by': 'client'}, {'category': 'file not found', 'fixed_in': 'minor', 'fixed_by': 'client'}, {'category': 'change one rule', 'fixed_in': 'patch', 'fixed_by': 'provider'}, {'category': 'incompatible providers versions', 'fixed_in': 'patch', 'fixed_by': 'provider'}, {'category': 'change type of object', 'fixed_in': 'minor', 'fixed_by': 'client'}, {'category': 'change one rule', 'fixed_in': 'patch', 'fixed_by': 'client'}, {'category': 'change one rule', 'fixed_in': 'patch', 'fixed_by': 'client'}, {'category': 'change type of object', 'fixed_in': 'Anyone', 'fixed_by': 'client'}, {'category': 'wrong code', 'fixed_in': 'patch', 'fixed_by': 'client'}, {'category': 'incompatible providers versions', 'fixed_in': 'patch', 'fixed_by': 'provider'}, {'category': 'incompatible providers versions', 'fixed_in': 'patch', 'fixed_by': 'client'}, {'category': 'incompatible providers versions', 'fixed_in': 'patch', 'fixed_by': 'provider'}, {'category': 'incompatible providers versions', 'fixed_in': 'minor', 'fixed_by': 'client'}, {'category': 'change one rule', 'fixed_in': 'patch', 'fixed_by': 'client'}, {'category': 'change one rule', 'fixed_in': 'patch', 'fixed_by': 'client'}, {'category': 'just update provider', 'fixed_in': 'Anyone', 'fixed_by': 'Anyone'}, {'category': 'change one rule', 'fixed_in': 'patch', 'fixed_by': 'client'}]

def put_fixed_in(case, p_c_fix):
	try:
		p_c_fix[case['fixed_in']] += 1
	except KeyError:
		p_c_fix[case['fixed_in']] = 1

	# just for fun
	return 1

def appends(p_c_fix, field, source, target, value):
	for fix in list(p_c_fix.keys()):
		source.append(field)
		target.append(fix)
		value.append(p_c_fix[fix])


patch_provider = 0
patch_client   = 0
patch_none     = 0
provider_fix   = {}
client_fix     = {}
for case in minor_bc:
	if case['fixed_by'].__eq__('provider'):
		patch_provider += put_fixed_in(case, provider_fix)
	elif case['fixed_by'].__eq__('client'):
		patch_client += put_fixed_in(case, client_fix)
	else:
		patch_none += 1

source = ['Minor', 'Minor', 'Minor']
target = ['Provedor', 'Cliente', 'Não consertada']
value  = [patch_provider, patch_client, patch_none]

appends(provider_fix, 'Provedor', source, target, value)
appends(client_fix,   'Cliente',  source, target, value)

# https://www.r-graph-gallery.com/321-introduction-to-interactive-sankey-diagram-2.html
print('source -> {}'.format(source))
print('target -> {}'.format(target))
print('value  -> {}'.format(value))

# ===========
# THIRD GRAPH
# ===========
result = json.load(open('results.json'))
data   = []
source = []
target = []
# [{'category': 'wrong code', 'fixed_in': 'Patch', 'introduced_in': 'Minor', 'fixed_by': 'provider'}, {'category': 'renamed function', 'fixed_in': 'Patch', 'introduced_in': 'Minor', 'fixed_by': 'provider'}, {'category': 'undefined object', 'fixed_in': 'Major', 'introduced_in': 'Patch', 'fixed_by': 'provider'}, {'category': 'incompatible providers versions', 'fixed_in': 'Patch', 'introduced_in': 'Minor', 'fixed_by': 'provider'}, {'category': 'incompatible providers versions', 'fixed_in': 'Patch', 'introduced_in': 'Patch', 'fixed_by': 'client'}, {'category': 'just update provider', 'fixed_in': 'Patch', 'introduced_in': 'Major', 'fixed_by': 'client'}, {'category': 'change one rule', 'fixed_in': '--', 'introduced_in': 'Minor', 'fixed_by': '--'}, {'category': 'change type of object', 'fixed_in': 'Patch', 'introduced_in': 'Minor', 'fixed_by': 'client'}, {'category': 'undefined object', 'fixed_in': 'Minor', 'introduced_in': 'Patch', 'fixed_by': 'provider'}, {'category': 'change type of object', 'fixed_in': 'Patch', 'introduced_in': 'Patch', 'fixed_by': 'client'}, {'category': 'incompatible providers versions', 'fixed_in': 'Patch', 'introduced_in': 'Minor', 'fixed_by': 'provider'}, {'category': 'change one rule', 'fixed_in': 'Minor', 'introduced_in': 'Minor', 'fixed_by': 'client'}, {'category': 'incompatible providers versions', 'fixed_in': 'Patch', 'introduced_in': 'Minor', 'fixed_by': 'provider'}, {'category': 'wrong code', 'fixed_in': 'Patch', 'introduced_in': 'Patch', 'fixed_by': 'provider'}, {'category': 'incompatible providers versions', 'fixed_in': 'Patch', 'introduced_in': 'Minor', 'fixed_by': 'provider'}, {'category': 'change type of object', 'fixed_in': 'Patch', 'introduced_in': 'Patch', 'fixed_by': 'provider'}, {'category': 'change type of object', 'fixed_in': 'Patch', 'introduced_in': 'Minor', 'fixed_by': 'client'}, {'category': 'undefined object', 'fixed_in': 'Major', 'introduced_in': 'Patch', 'fixed_by': 'provider'}, {'category': 'renamed function', 'fixed_in': 'Patch', 'introduced_in': 'Pre', 'fixed_by': 'client'}, {'category': 'file not found', 'fixed_in': 'Minor', 'introduced_in': 'Minor', 'fixed_by': 'client'}, {'category': 'just update provider', 'fixed_in': 'Major', 'introduced_in': 'Patch', 'fixed_by': 'client'}, {'category': 'change one rule', 'fixed_in': 'Patch', 'introduced_in': 'Minor', 'fixed_by': 'provider'}, {'category': 'incompatible providers versions', 'fixed_in': 'Patch', 'introduced_in': 'Minor', 'fixed_by': 'provider'}, {'category': 'change type of object', 'fixed_in': 'Minor', 'introduced_in': 'Minor', 'fixed_by': 'client'}, {'category': 'change one rule', 'fixed_in': 'Patch', 'introduced_in': 'Minor', 'fixed_by': 'client'}, {'category': 'change one rule', 'fixed_in': '--', 'introduced_in': 'Patch', 'fixed_by': '--'}, {'category': 'change one rule', 'fixed_in': 'Patch', 'introduced_in': 'Minor', 'fixed_by': 'client'}, {'category': 'change type of object', 'fixed_in': 'Patch', 'introduced_in': 'Patch', 'fixed_by': 'provider'}, {'category': 'change type of object', 'fixed_in': 'Patch', 'introduced_in': 'Minor', 'fixed_by': 'client'}, {'category': 'change one rule', 'fixed_in': 'Patch', 'introduced_in': 'Patch', 'fixed_by': 'client'}, {'category': 'wrong code', 'fixed_in': 'Patch', 'introduced_in': 'Minor', 'fixed_by': 'client'}, {'category': 'incompatible providers versions', 'fixed_in': 'Minor', 'introduced_in': 'Major', 'fixed_by': 'provider'}, {'category': 'incompatible providers versions', 'fixed_in': 'Patch', 'introduced_in': 'Minor', 'fixed_by': 'provider'}, {'category': 'change one rule', 'fixed_in': 'Patch', 'introduced_in': 'Patch', 'fixed_by': 'client'}, {'category': 'incompatible providers versions', 'fixed_in': 'Patch', 'introduced_in': 'Minor', 'fixed_by': 'client'}, {'category': 'incompatible providers versions', 'fixed_in': 'Patch', 'introduced_in': 'Minor', 'fixed_by': 'provider'}, {'category': 'change one rule', 'fixed_in': 'Patch', 'introduced_in': 'Patch', 'fixed_by': 'client'}, {'category': 'incompatible providers versions', 'fixed_in': 'Minor', 'introduced_in': 'Minor', 'fixed_by': 'client'}, {'category': 'change one rule', 'fixed_in': 'Patch', 'introduced_in': 'Minor', 'fixed_by': 'client'}, {'category': 'change one rule', 'fixed_in': 'Patch', 'introduced_in': 'Patch', 'fixed_by': 'client'}, {'category': 'change one rule', 'fixed_in': 'Patch', 'introduced_in': 'Minor', 'fixed_by': 'client'}, {'category': 'change one rule', 'fixed_in': 'Minor', 'introduced_in': 'Patch', 'fixed_by': 'client'}, {'category': 'just update provider', 'fixed_in': '--', 'introduced_in': 'Minor', 'fixed_by': '--'}, {'category': 'undefined object', 'fixed_in': 'Minor', 'introduced_in': 'Patch', 'fixed_by': 'provider'}, {'category': 'change one rule', 'fixed_in': 'Patch', 'introduced_in': 'Minor', 'fixed_by': 'client'}]


def insert_category(category):
	try:
		category_map[category]
	except KeyError:
		category_map[category] = {}

# category -> 'Codigo Errado' | 'Provedores Imcompativeis' | ...
# field    -> 'Introduzido em ' | 'Consertado em ' | 'Consertado por '
# level    -> 'Major' | 'Minor' | 'Patch' | 'Pre-release'
def insert_value(category, field, level):
	try:
		category_map[category]['{0} {1}'.format(field, level)] += 1
	except KeyError:
		category_map[category]['{0} {1}'.format(field, level)] = 1

def get_mapped(category, value):
	try:
		return category_map[category][value]
	except KeyError:
		return 0

def normalize(values, i, e):
	s = sum(values[i:e])
	for i in range(i, e):
		values[i] = round(values[i]*100/s, 1)

def get_values():
	lists      = []
	categories = []
	for category in ['undefined object', 'incompatible providers versions', 'change one rule', 'change type of object', 'wrong code', 'just update provider', 'renamed function', 'file not found']:
		values = []
		for level in ['Major', 'Minor', 'Patch', 'Pre-release']:
			values.append(get_mapped(category, 'Introduzido em {}'.format(level)))
		for level in ['Major', 'Minor', 'Patch']:
			values.append(get_mapped(category, 'Consertado em {}'.format(level)))
		for pck in ['provider', 'client']:
			values.append(get_mapped(category, 'Consertado por {}'.format(pck)))

		normalize(values, 0, 3+1)
		normalize(values, 4, 6+1)
		normalize(values, 7, 8+1)

		lists.append(values)
		categories.append(category)
		print('{0} -> {1}'.format(category, values))

	return categories, lists

category_map = {}
for client_name in list(result.keys()):
	for case in result[client_name]:
		insert_category(case['category'])
		insert_value(case['category'], 'Introduzido em', case['introduced_in'])
		insert_value(case['category'], 'Consertado em', case['fixed_in'])
		insert_value(case['category'], 'Consertado por', case['fixed_by'])
		# source.append(case['category'])
		# target.append(case['introduced_in'])
		# data.append({
		# 	'category'     : case['category'],
		# 	'introduced_in': case['introduced_in'],
		# 	'fixed_in'     : case['fixed_in'],
		# 	'fixed_by'     : case['fixed_by']
		# })

# categories, lists = get_values()
# print('categories=c{},'.format(categories).replace('[', '(').replace(']', ')'))
# for i, field in enumerate(['i_major','i_minor','i_patch','i_pre']):#,'f_major','f_minor','f_patch','f_provider', 'f_client']):
# 	print('{}=c('.format(field), end='')
# 	for k, l in enumerate(lists):
# 		end = '' if k == len(lists)-1 else ','
# 		print('{0}{1}'.format(l[i], end), end='')

# 	print('),')

# ============
# FOURTH GRAPH
# ============
result = json.load(open('results.json'))
fix = []
for client_name in list(result.keys()):
	for case in result[client_name]:
		if case['category'].__eq__('incompatible providers versions') and case['introduced_in'].__eq__('Minor'):
			fix.append(1 if case['fixed_by'].__eq__('provider') else 0)

print(fix)