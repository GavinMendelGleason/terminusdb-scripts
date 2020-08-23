#!/usr/bin/python3

from terminusdb_client import WOQLClient
from terminusdb_client import WOQLQuery as WQ

server_url = "https://127.0.0.1:6363"
db = "schemaless_to_schema"
user = "admin"
account = "admin"
key = "root"
repository = "local"
client = WOQLClient(server_url)
client.connect(user=user, account=account, key=key, db=db)

try:
    client.delete_database(db)
except Exception as E:
    pass

client.create_database(db,account,label="Schemaless to Schema",
                       description="Two branch database one with schema",
                       include_schema=False)

# Add some data which meets the schema
WQ().woql_and(
    WQ().insert("doc:mike", "scm:BankAccount")
        .property("scm:owner", "mike")
        .property("scm:balance", 123)
).execute(client, "Add mike")

# Create the schema graph
client.create_graph("schema","main","Adding schema")

# Add the schema
WQ().woql_and(
    WQ().doctype("scm:BankAccount")
        .label("Bank Account")
        .description("A bank account")
        .property("scm:owner", "xsd:string")
            .label("owner")
            .cardinality(1)
        .property("scm:balance","xsd:nonNegativeInteger")
            .label("balance")
).execute(client, "Adding bank account object to schema")

