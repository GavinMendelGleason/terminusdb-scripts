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

# Create a schemaless branch
client.branch('schemaless')

# Switch back to main
client.checkout('main')

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

# Add some data which meets the schema
WQ().woql_and(
    WQ().insert("doc:mike", "scm:BankAccount")
        .property("scm:owner", "mike")
        .property("scm:balance", 123)
).execute(client, "Add mike")

# Switch back to the schemaless branch
client.checkout('schemaless')

# Add *valid* data
WQ().woql_and(
  WQ().insert("doc:jim", "scm:BankAccount")
      .property("owner", "jim")
      .property("balance", 8)
).execute(client,"Adding Jim")

# Switch back to main for a rebase
client.checkout('main')
# Rebase valid data to schema branch
client.rebase({"rebase_from": f'{user}/{db}/{repository}/branch/schemaless',
               "author": user,
               "message": "Merging jim into schema branch"})

# Add invalid data to schemaless
client.checkout('schemaless')
WQ().woql_and(
  WQ().insert("doc:joker", "scm:BankAccount")
      .property("owner", "joker")
      .property("elephants", 8)
).execute(client,"Adding the joker")

# Try (and fail) with another rebase
client.checkout('main')
try:
    client.rebase({"rebase_from": f'{user}/{db}/{repository}/branch/schemaless',
                   "author": user,
                   "message": "Merging joker into schema branch"})
except Exception as E:
    error_obj = E.errorObj
    print(f'{error_obj}\n')
