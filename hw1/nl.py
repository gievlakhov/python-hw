import sys

def nl(stream):
    for i, line in enumerate(stream, start=1):
        sys.stdout.write(f"{i}\t{line}")

def main():
    if len(sys.argv) > 2:
        sys.stderr.write("Syntax: nl.py [file]")
        sys.exit(1)

    if len(sys.argv) == 2:
        name = sys.argv[1]
        try:
            with open(name, "r", encoding="utf-8") as file:
                nl(file)
        except FileNotFoundError:
            sys.stderr.write(f"nl.py: {name}: File not found")
            sys.exit(1)
    else:
        nl(sys.stdin)

if __name__ == "__main__":
    main()
