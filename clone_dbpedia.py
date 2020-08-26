#!/usr/bin/python3

import os
import time
from terminusdb_client import WOQLClient
from terminusdb_client import WOQLQuery as WQ

# Assumes database already exists.

server_url = "https://127.0.0.1:6363"
db = "DBPedia"
user = "admin"
account = "admin"
key = "root"
client = WOQLClient(server_url)
client.connect(user=user, account=account, key=key, db=db)

new_db = "DBPedia_squash"
client.remote_auth({ "type" : "basic",
                     "user" : user,
                     "key" : key})
client.clonedb({ "remote_url" : f"{server_url}/{user}/{db}",
                 "comment" : "Squash test",
                 "label" : "Squash test"},
               new_db)

new_db = "DBPedia_squash"
client = WOQLClient(server_url)
client.remote_auth({ "type" : "basic",
                     "user" : user,
                     "key" : key})
client.connect(user=user, account=account, key=key, db=new_db)
client.branch("types")
client.checkout("types")
client.pull({ "remote" : "origin",
              "remote_branch" : "types" })


client.branch("properties")
client.checkout("properties")
client.pull({ "remote" : "origin",
              "remote_branch" : "properties" })

client.checkout('main')
# Rebase valid data to schema branch
client.rebase({"rebase_from": f'{user}/{new_db}/local/branch/types',
               "author": user,
               "message": "Merging types into main"})

client.checkout('main')
# # Rebase valid data to schema branch
client.rebase({"rebase_from": f'{user}/{new_db}/local/branch/properties',
               "author": user,
               "message": "Merging types into main"})

result = client.squash('Squash commit of properties and types')
client.checkout('main')
client.reset(result['api:commit'])
