import sys
from interpreter import interpret

def format_row(row):
    column_width = 16
    formatted = []

    for item in row:
        s = str(item)

        if len(s) > column_width:
            formatted.append(s[:column_width])
        else:
            formatted.append(s.center(column_width))

    return " | ".join(formatted)

def print_help():
    print("Usage:")
    print("$ sys-query <query>")
    print("$ sys-query --help")

def main():
    if len(sys.argv) == 1 or sys.argv[1] == "--help":
        print_help()
        return

    columns, result_set = interpret(sys.argv[1])

    print(format_row(columns[0]))

    for row in result_set:
        print(format_row(row))

if __name__ == "__main__":
    main()
