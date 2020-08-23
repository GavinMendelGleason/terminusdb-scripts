#!/usr/bin/python3

from terminusdb_client import WOQLClient
from terminusdb_client import WOQLQuery as WQ

server_url = "https://127.0.0.1:6363"
db = "foo"
user = "admin"
account = "admin"
key = "root"
client = WOQLClient(server_url)
client.connect(user=user, account=account, key=key, db=db)

try:
    client.create_database(db,account,label="foo",
                           description="foo and bar, together again")
except Exception as E:
    print(E)

[x,y,z] = WQ().vars("x","y","z")
query = WQ().get(
    WQ().woql_as(x).woql_as(y).woql_as(z)
).file("/home/gavin/dev/terminus-server/terminus-schema/api.owl.ttl",
       {"type" : "turtle"})
client.query(query)
