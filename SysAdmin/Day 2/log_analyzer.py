import re
from collections import Counter
#step 1 read the file
pattern = re.compile(r'\d{3}')
freq = Counter()

def function():
    try:
        with open('./access.log','r') as file:
            for line in file:
                status = pattern.findall(line)
                if status:
                    code = status[0]
                    freq[code]+=1
    except FileNotFoundError as e:
        print(f"{e}")

    for code, count in freq.most_common():
        print(f"{code}:{count}")


print(function())

