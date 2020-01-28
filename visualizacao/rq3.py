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

count = 0
for client_name in list(result.keys()):
    for case in result[client_name]:
        if case['client_affected_by'].__eq__('implicit') and case['fixed_by'].__eq__('client') and case['provider_was'].__eq__('--'):
            count += 1

print(count)