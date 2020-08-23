#!/usr/bin/python3

from terminusdb_client import WOQLClient
from terminusdb_client import WOQLQuery

server_url = "https://127.0.0.1:6363"
client = WOQLClient(server_url)
client.connect(user="admin", account="admin", key="root", db="bike")

client.delete_database("bike")
client.create_database("bike","admin",label="Bikes", description="description")

query = WOQLQuery().get(
    WOQLQuery().woql_as("Start station","v:Start_Station")
        .woql_as("End station", "v:End_Station")
        .woql_as("Start date", "v:Start_Time")
        .woql_as("End date", "v:End_Time")
        .woql_as("Duration", "v:Duration")
        .woql_as("Start station number", "v:Start_ID")
        .woql_as("End station number", "v:End_ID")
        .woql_as("Bike number", "v:Bike")
        .woql_as("Member type", "v:Member_Type")
).post("bike_csv")
result = client.query(query,
                      "This is a commit string",
                      {'bike_csv' : '/home/gavin/tmp/bike_tutorial.csv'})
