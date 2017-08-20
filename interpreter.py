from process import get_processes_infos, PROPERTIES
from parser import Parser

def _select_processes_infos(properties):
    processes_infos = get_processes_infos()

    selection = []

    for pid in processes_infos:
        row = []

        for prop in properties:
            row.append(processes_infos[pid][prop])

        selection.append(row)

    return selection

def interpret(query):
    query_dict = Parser().parse(query)

    if query_dict["columns"] == "*":
        columns = list(PROPERTIES)
    else:
        columns = query_dict["columns"]

    result_set = []

    if "processes" in query_dict["tables"]:
        result_set = _select_processes_infos(columns)
    else:
        raise Exception("Table not found")

    if "order by" in query_dict:
        column_idx = columns.index(query_dict["order by"])
        result_set = sorted(result_set, key=lambda x: x[column_idx])

    return columns, result_set
