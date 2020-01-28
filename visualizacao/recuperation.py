# about third conclusion
import json

result = json.load(open('results.json'))
qtd    = {}
for client_name in list(result.keys()):
	for case in result[client_name]:
		try:
			qtd[case['fixed_by']] += 1
		except KeyError:
			qtd[case['fixed_by']] = 1

#print(qtd)

# ===========
# FIRST TABLE
# ===========
result = json.load(open('results.json'))
var    = {}
for client_name in list(result.keys()):
	for case in result[client_name]:
		try:
			var[case['fixed_by']]['days'].append(case['fixed_after_days'])
			var[case['fixed_by']]['releases'].append(case['fixed_after_releases'])
		except KeyError:
			var[case['fixed_by']] = {'days': [case['fixed_after_days']], 'releases': [case['fixed_after_releases']]}

#print(var)

# ===========
# FIRST GRAPH
# ===========
days = []
for client_name in list(result.keys()):
	for case in result[client_name]:
		if case['fixed_by'].__eq__('provider') and case['provider_was'].__eq__('dowgraded'):
			days.append(case['fixed_after_days'])

print(len(days))