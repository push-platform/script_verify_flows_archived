import requests
import json


ALL_FLOWS = []

api_token = input("Digite o token da API: ")


def get_name_and_uuid_flows(results, headers):
    for flow in results:
        url = "https://api.rapidpro.io/api/v2/runs.json"
        uuid = flow.get('uuid')
        response = requests.get(
            url=url,
            headers=headers,
            params={'flow': uuid}
        )
        print('requesting run for flow: {}'.format(uuid))
        data = response.json()
        if data.get('results'):
            print('flow-{} ADDED TO LIST'.format(uuid))
            flows_not_archived = dict(
                 name=flow.get('name'),
                 uuid=flow.get('uuid')
            )
            ALL_FLOWS.append(flows_not_archived)


def requisition(url, api_token):
    headers = {
            'Authorization': 'Token {}'.format(api_token),
            'Content-Type': 'application/json'
        }
    response = requests.get(url=url, headers=headers)
    response_json = response.json()

    results = response_json.get('results')
    get_name_and_uuid_flows(results, headers)

    new_page = response_json.get('next')
    if new_page:
        requisition(url=new_page, api_token=api_token)


requisition(
    url="https://api.rapidpro.io/api/v2/flows.json",
    api_token=api_token
)

with open('details.json', 'w') as outfile:
    json.dump(ALL_FLOWS, outfile)

print('{} flows archived. Details about flows see file details.json'.format(len(ALL_FLOWS)))
