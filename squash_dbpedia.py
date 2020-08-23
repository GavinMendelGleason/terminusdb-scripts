import os
import time
from terminusdb_client import WOQLClient
from terminusdb_client import WOQLQuery as WQ


server_url = "https://127.0.0.1:6363"
db = "DBPedia_squash"
user = "admin"
account = "admin"
key = "root"
client = WOQLClient(server_url)
client.connect(user=user, account=account, key=key, db=db)

client.branch("squash", empty=True)
client.checkout("squash")
query = WQ().and(WQ().using("{account}/{db}").triple("v:X","v:Y","v:Z"),
                 WQ().add_triple("v:X","v:Y","v:Z"))
client.query(query, "Squash commit")
