import json

result = json.load(open('results.json'))
caso   = {}
caso['explicit'] = {'fixed_by': {'client': 0, 'provider': 0, '--': 0}}
caso['implicit'] = {'fixed_by': {'client': 0, 'provider': 0, '--': 0}}
for client_name in list(result.keys()):
    for case in result[client_name]:
        client_affected_by = case['client_affected_by']
        fixed_by = case['fixed_by']

        caso[case['client_affected_by']]['fixed_by'][fixed_by] += 1

#print(caso)
explicit = []
implicit = []

fixed_client = []
fixed_provider = []

count = 0
for client_name in list(result.keys()):
    for case in result[client_name]:
        if case['client_affected_by'].__eq__('explicit') and case['fixed_by'].__eq__('client'):
            explicit.append(case['fixed_after_days'])
        elif case['client_affected_by'].__eq__('implicit') and case['fixed_by'].__eq__('client'):
            implicit.append(case['fixed_after_days'])

        if case['fixed_by'].__eq__('client'):
        	fixed_client.append(case['fixed_after_days'])
        elif case['fixed_by'].__eq__('provider'):
        	fixed_provider.append(case['fixed_after_days'])

print(explicit)
print(implicit)

print(fixed_client)
print(fixed_provider)
