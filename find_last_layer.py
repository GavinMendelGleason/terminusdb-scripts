#!/usr/bin/python3

import os
import re
import time
from terminusdb_client import WOQLClient
from terminusdb_client import WOQLQuery as WQ

dirs = []
for f in os.listdir('.'):
    if re.match('.*label',f):
        pass
    elif re.match('SERVER_VERSION', f):
        pass
    else:
        dirs.append(f)

optimum_commit = []
ingest_commit = []
something_else = []
commit_graph = []
repo_graph = []
schema_graph = []
forecast = []
system_graph = []
empty = []
times = 0
for d in dirs:
    for sub in os.listdir(d):
        path = f'{d}/{sub}'
        node_dict = f'{path}/node_dictionary_blocks.pfc'
        if os.path.exists(node_dict):
            res = open(node_dict,'rb')
            line = res.read()
            if (re.match(b'.*MonteCarlo.*',line) or
                re.match(b'.*SuggestedOrder.*', line)):
                optimum_commit.append(path)
            elif (re.match(b'.*Capability.*',line) or
                  re.match(b'.*finalized.*', line) or
                  re.match(b'.*deleting.*', line) or
                  re.match(b'.*capability_scop.*', line)):
                system_graph.append(path)
            elif re.match(b'.*DailyForecast_.*',line):
                forecast.append(path)
            elif (re.match(b'.*OrderLine.*',line) or
                  re.match(b'.*Warehouse_.*',line) or
                  re.match(b'.*Stock_.*',line) or
                  re.match(b'.*Supplier_.*', line) or
                  re.match(b'.*Product_.*',line) or
                  re.match(b'.*SupplierOrder.*', line)):
                ingest_commit.append(path)
            elif (re.match(b'.*Graph_.*',line) or
                  re.match(b'.*Branch_.*', line)):
                commit_graph.append(path)
            elif (re.match(b'.*Layer_.*',line) or
                  re.match(b'.*Local_.*',line) or
                  re.match(b'.*Database_admin_rational_warehouse_.*', line)):
                repo_graph.append(path)
            elif re.match(b'.*creativecommons.org.*', line):
                schema_graph.append(path)
            elif re.match(b'.DailyForecast_.*', line):
                forecast.append(path)
            elif re.match(b'^\x00+$',line):
                empty.append(path)
            else:
                something_else.append(path)

commit_dict = {}
for f in commit_graph:
    value_dict = f'{f}/value_dictionary_blocks.pfc'
    res = open(value_dict,'rb')
    line = res.read()
    matchobj = re.match(b'.*(159.*)"\^\^\'http://www.w3.org/2001/XMLSchema#decimal\'', line)
    if matchobj:
        timestamp_str = matchobj.group(1)
        commit_dict[f] = float(timestamp_str)
        print(f"Time: {timestamp}")

print(len(optimum_commit))
