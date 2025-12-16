import sys

def wc_stream(stream):
    line_cnt = 0
    word_cnt = 0
    byte_cnt = 0

    for line in stream:
        line_cnt += 1
        word_cnt += len(line.split())
        byte_cnt += len(line.encode("utf-8"))

    return line_cnt, word_cnt, byte_cnt

def wc_file(name):
    try:
        with open(name, "r", encoding="utf-8") as file:
            return wc_stream(file)
    except FileNotFoundError:
        sys.stderr.write(f"wc.py: {name}: File not found")
        return None

def main():
    names = sys.argv[1:]
    if not names:
        l, w, b = wc_stream(sys.stdin)
        sys.stdout.write(f"{l:6}{w:6}{b:6}")
        return

    line_cnt = 0
    word_cnt = 0
    byte_cnt = 0

    results = []
    for name in names:
        res = wc_file(name)
        if res is None:
            continue

        l, w, b = res
        results.append((l, w, b, name))
        line_cnt += l
        word_cnt += w
        byte_cnt += b

    for l, w, b, name in results:
        sys.stdout.write(f"{l:6}{w:6}{b:6} {name}\n")

    if len(results) > 1:
        sys.stdout.write(f"{line_cnt:6}{word_cnt:6}{byte_cnt:6} total")

if __name__ == "__main__":
    main()
