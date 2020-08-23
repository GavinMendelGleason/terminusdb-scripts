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

client.branch('properties')
client.checkout('properties')
times = []
directory = 'properties_200k' # 'properties_100k'
for f in os.listdir(directory):
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

client.checkout('main')
client.branch('types')
client.checkout('types')
times = []
directory = 'instance_200k' # 'instance_100k'
for f in os.listdir(directory):
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
