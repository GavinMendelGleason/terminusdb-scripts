#!/usr/bin/python3

import os
import time
from terminusdb_client import WOQLClient
from terminusdb_client import WOQLQuery as WQ

# Assumes database already exists.

server_url = "https://127.0.0.1:6363"
db = "DBPedia_squash"
user = "admin"
account = "admin"
key = "root"
client = WOQLClient(server_url)
client.connect(user=user, account=account, key=key, db=db)

result = client.squash('Squash commit of properties and types')
print(f"result {result}")
client.reset(result['api:commit'])
