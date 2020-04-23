""" example.py
"""

import json
from datetime import datetime

import requests

USER = "user"
PSWD = "pswd"
MDCS_URL = "http://127.0.0.1:8000"

POST_TEMPLATE_URL = MDCS_URL + "/rest/template/user/"
POST_DATA_URL = MDCS_URL + "/rest/data/"
GET_DATA_URL = MDCS_URL + "/rest/data/"
QUERY_DATA_URL = MDCS_URL + "/rest/data/query/"

json_schema = {
    "$id": "https://example.com/person.schema.json",
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Person",
    "type": "object",
    "properties": {
        "firstName": {
            "type": "string",
            "description": "The person's first name."
        },
        "lastName": {
            "type": "string",
            "description": "The person's last name."
        },
        "age": {
            "description": "Age in years which must be equal to or greater than zero.",
            "type": "integer",
            "minimum": 0
        }
    }
}

data_json = {
    "firstName": "John",
    "lastName": "Doe",
    "age": 21
}

print(" ### Add Template ###")
data = {"title": "Template-" + str(datetime.now()),
        "filename": "schema.json",
        "content": json.dumps(json_schema)}

r = requests.post(POST_TEMPLATE_URL,
                  data, auth=(USER, PSWD),
                  verify=False)
response = r.json()
print(response)
assert r.status_code == 201
template_id = response['id']


print(" ### Add Data ###")
data_to_send = {"title": "Data-" + str(datetime.now()),
                "template": str(template_id),
                "dict_content": data_json}

r = requests.post(POST_DATA_URL,
                  json=data_to_send,
                  auth=(USER, PSWD),
                  verify=False)
response = r.json()
print(response)
assert r.status_code == 201
data_id = response['id']


print(" ### Get Data ###")
r = requests.get(GET_DATA_URL + data_id,
                 auth=(USER, PSWD),
                 verify=False)
response = r.json()
print(response)
assert r.status_code == 200


print(" ### Query Data ###")
data_to_send = {"query": {"firstName": "John"}}
r = requests.get(QUERY_DATA_URL,
                 json=data_to_send,
                 auth=(USER, PSWD),
                 verify=False)
response = r.json()
print(response)
assert r.status_code == 200
