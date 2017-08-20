from os import walk
from os.path import join

class NotRelevantProperty(Exception):
    pass

def is_int(x):
    try:
        int(x)
    except ValueError:
        return False

    return True

def adjust_property(name, value):
    if name == "Name":
        return "name", value

    if name == "Threads":
        return "threads", int(value)

    if name == "State":
        return "state", value[3:-1]

    if name == "PPid":
        return "parent_pid", int(value)

    if name == "VmSize":
        return "address_space", int(value[:-3])

    if name == "VmRSS":
        return "memory_usage", int(value[:-3])

    if name == "voluntary_ctxt_switches":
        return "context_switches", int(value)

    raise NotRelevantProperty()

def get_pids():
    for dir_name in next(walk("/proc"))[1]:
        if is_int(dir_name):
            yield dir_name

def read_infos(pid):
    with open(join("/proc", pid, "status")) as f:
        lines = f.readlines()

    infos = {}

    for line in lines:
        items = line.split(":")

        name = items[0].strip()
        value = "".join(items[1:]).strip()

        try:
            name, value = adjust_property(name, value)
        except NotRelevantProperty:
            continue

        infos[name] = value

    return infos

def get_processes_infos():
    processes_infos = {}

    for pid in get_pids():
        try:
            infos = read_infos(pid)
        except FileNotFoundError:
            continue

        if "memory_usage" in infos:
            processes_infos[pid] = infos

    return processes_infos
