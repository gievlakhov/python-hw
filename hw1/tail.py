import sys
from collections import deque

def tail_stream(stream, n):
    lines = deque(maxlen=n)
    for line in stream:
        lines.append(line)

    return lines

def tail_file(name, n, show_name=False):
    try:
        with open(name, "r", encoding="utf-8") as file:
            lines = tail_stream(file, n)
        if show_name:
            sys.stdout.write(f"==> {name} <==\n")
        for line in lines:
            sys.stdout.write(line)
    except FileNotFoundError:
        sys.stderr.write(f"tail.py: {name}: File not found")

def main():
    args = sys.argv[1:]
    if len(args) == 0:
        for line in tail_stream(sys.stdin, 17):
            sys.stdout.write(line)
    else:
        multi = len(args) > 1
        for i, name in enumerate(args):
            if i > 0:
                sys.stdout.write("\n")
            tail_file(name, 10, show_name=multi)

if __name__ == "__main__":
    main()
