#!/usr/bin/python3

from terminusdb_client import WOQLClient
from terminusdb_client import WOQLQuery as WQ

server_url = "https://127.0.0.1:6363"
client = WOQLClient(server_url)
client.connect(user="admin", account="admin", key="root", db="bike")

test1 = WQ().count("v:Count").using("_commits").woql_and(
    WQ().triple("v:CID", "ref:commit_timestamp", "v:Y"),
    WQ().triple("v:CID", "ref:commit_message", "v:Message")
).execute(client)
print(test1)
