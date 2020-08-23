#!/usr/bin/python3

from terminusdb_client import WOQLClient
from terminusdb_client import WOQLQuery as WQ

server_url = "https://127.0.0.1:6363"
client = WOQLClient(server_url)
client.connect(user="admin", account="admin", key="root", db="bike")


test3 = WQ().select("v:Time", "v:Message").using("_commits").woql_and(
    WQ().order_by("v:Time", "v:Message", order=["desc", "asc"]).woql_and(
        WQ().triple("v:A", "ref:commit_timestamp", "v:Time"),
        WQ().triple("v:A", "ref:commit_message", "v:Message")
    )
)

print(client.query(test3))
