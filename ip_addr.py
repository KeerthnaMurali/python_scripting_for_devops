import re
from  collections import Counter
first_word_count = Counter()
with open('./access.log','r') as logFile:
    for line in logFile:
        words = line.strip().split()
        if words:
            first_word_count[words[0]] += 1

for words,count in first_word_count.most_common(1):
    print(f"{word}: {count}")



