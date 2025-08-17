import sys
from collections import defaultdict, Counter
from itertools import count
import re

def funct():
    text = sys.stdin.read()
    lines = text.splitlines()
    count_lines = len(lines)
    words = re.findall(r'\b\w+\b', text.lower())
    freq = Counter(words)
    top5 = freq.most_common(5)
    print(f"Total lines: {count_lines}")
    print("Top 5 words:")
    for word, count in top5:
        print(f"{word}: {count}")


print(funct())