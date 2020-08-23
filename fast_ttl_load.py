#!/usr/bin/python3

from terminusdb_client import WOQLClient
from terminusdb_client import WOQLQuery as WQ

server_url = "https://127.0.0.1:6363"
db = "places"
db_label = "Places"
db_comment = "All DBPedia places (GeoNames)"
user = "admin"
account = "admin"
key = "root"
filename = "geonames_links_en.ttl"
commit_comment = "Adding all geonames"


client = WOQLClient(server_url)
client.connect(user=user, account=account, key=key, db=db)

try:
    client.delete_database(db)
except Exception as E:
    print(E)

client.create_database(db,account,label=db_label,
                       description=db_comment)

ttl_file = open(filename)
contents = ttl_file.read()
ttl_file.close()

client.insert_triples(
    "instance","main",
    contents,
    commit_comment)
