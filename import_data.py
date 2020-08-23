#!/usr/bin/python3

from terminusdb_client import WOQLClient
from terminusdb_client import WOQLQuery as WQ

server_url = "https://127.0.0.1:6363"
user = "admin"
account = "admin"
key = "root"
db = "roster"
repository = "local"
label = "Roster CSV Example"
description = "An example database for playing with bank accounts"
client = WOQLClient(server_url)
client.connect(user=user, account=account, key=key, db=db)

#client.delete_database(db)
try:
    client.create_database(db,account,label=label,
                           description=description,
                           include_schema=None)
except Exception as E:
    pass

query = WQ().woql_and(
    WQ().get(WQ().woql_as("Name","v:Name")
                 .woql_as("Registration_Date", "v:Date")
                 .woql_as("Paid", "v:Paid")
            ).post('roster.csv'),
    WQ().idgen("doc:RosterRecord",["v:Name","v:Date","v:Paid"],"v:ID"),
    WQ().add_triple("v:ID","scm:name","v:Name"),
    WQ().add_triple("v:ID","scm:date","v:Date"),
    WQ().add_triple("v:ID","scm:paid","v:Paid"))
client.query(query,
    "Adding Roster Data",
    {'roster.csv' : '/home/gavin/tmp/roster.csv'}
    )

