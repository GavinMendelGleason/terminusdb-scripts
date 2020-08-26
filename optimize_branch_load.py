#!/usr/bin/python3

import os
import time
from terminusdb_client import WOQLClient
from terminusdb_client import WOQLQuery as WQ

server_url = "https://127.0.0.1:6363"
db = "DBPedia_optimize"
db_label = "DBPedia speed test"
db_comment = "Testing new synchronous writes + optimize"
user = "admin"
account = "admin"
key = "root"
client = WOQLClient(server_url)
client.connect(user=user, account=account, key=key, db=db)

def optimizer(client):
    client.optimize(f'{account}/{db}/_meta')
    client.optimize(f'{account}/{db}/local/_commits')

try:
    client.delete_database(db)
except Exception as E:
    print(E)

client.create_database(db,account,label=db_label,
                       description=db_comment,
                       include_schema=False)

client.branch('properties')
client.checkout('properties')
times = []
directory = 'properties_100k'
for f in os.listdir(directory):
    optimizer(client)
    filename = f'{directory}/{f}'
    ttl_file = open(filename)
    contents = ttl_file.read()
    ttl_file.close()
    before = time.time()
    client.insert_triples(
        "instance","main",
        contents,
        f"Adding properties in 100k chunk ({f})")
    after = time.time()
    total = (after - before)
    times.append(total)
    print(f"Update took {total} seconds")
print(times)

# Branch from 'main' to 'types'
client.checkout('main')
client.branch('types')
client.checkout('types')
times = []
directory = 'instance_100k'
for f in os.listdir(directory):
    optimizer(client)
    filename = f'{directory}/{f}'
    ttl_file = open(filename)
    contents = ttl_file.read()
    ttl_file.close()
    before = time.time()
    client.insert_triples(
        "instance","main",
        contents,
        f"Adding types in 100k chunk ({f})")
    after = time.time()
    total = (after - before)
    times.append(total)
    print(f"Update took {total} seconds")
print(times)
