#!/usr/bin/python3

import os
import time
from terminusdb_client import WOQLClient
from terminusdb_client import WOQLQuery as WQ


server_url = "https://127.0.0.1:6363"
db = "places"
db_label = "Places"
db_comment = "All DBPedia places"
directory = 'geonames_100k'
user = "admin"
account = "admin"
key = "root"
client = WOQLClient(server_url)
client.connect(user=user, account=account, key=key, db=db)

try:
    client.delete_database(db)
except Exception as E:
    print(E)

client.create_database(db,account,label=f"{db_label}",
                       include_schema=False,
                       description=f"All DBPedia {db} data")

times = []
for f in os.listdir(directory):
    filename = f'{directory}/{f}'
    ttl_file = open(filename)
    contents = ttl_file.read()
    ttl_file.close()
    before = time.time()
    client.insert_triples(
        "instance","main",
        contents,
        f"Adding persondata in 100k chunk ({f})")
    after = time.time()
    total = (after - before)
    times.append(total)
    print(f"Update took {total} seconds")

print(times)
