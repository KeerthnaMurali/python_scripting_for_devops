import re
from collections import Counter
pattern =  re.compile(r'''
[a-zA-Z0-9._%+-]+ 
@
[a-zA-Z0-9]+
\.
[a-zA-Z]{2,3}
''',re.VERBOSE)
count = 0
freq =Counter()
with open('./sample.txt', 'r') as file:
    for line in file:
        email = pattern.findall(line)
        for mail in email:
            freq[mail] += 1

for email, count in freq.items():
    print(f"{email}: {count}")

