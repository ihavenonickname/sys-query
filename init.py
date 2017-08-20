from process import get_processes_infos
from parser import Parser, ParserException

def main():
    processes_infos = get_processes_infos()

    print(len(processes_infos))
    print(sum(processes_infos[pid]["threads"] for pid in processes_infos))

    try:
        query = Parser().parse("select pid, name, memory_usage from processes")
        print(query["columns"])
        print(query["tables"])
    except ParserException as e:
        print(e)

if __name__ == "__main__":
    main()
