from collections import Counter, defaultdict

student_subject_pairs = [
    ('Alice', 'Math'),
    ('Bob', 'English'),
    ('Alice', 'Science'),
    ('Bob', 'Math'),
    ('Charlie', 'History'),
    ('Alice', 'English')
]

report = defaultdict(list)
for student,sub in student_subject_pairs:
    report[student].append(sub)

for k,v in report.items():
    print(k)
    print(v)

text = "hello world"
chars = defaultdict(int)
for c in text:
    if c != ' ':
        chars[c] += 1

print(chars)

documents = {
    'doc1': "the cat sat on the mat",
    'doc2': "the dog chased the cat",
    'doc3': "the cat climbed the tree"
}


docs = defaultdict(list)

for k,v in documents.items():
    word = v.split(" ")
    docs[k] = word
print(docs)

transactions = [
    ('user1', 'productA'),
    ('user2', 'productB'),
    ('user1', 'productC'),
    ('user3', 'productA'),
    ('user2', 'productA'),
    ('user1', 'productB')
]

t = defaultdict(set)
for k,v in transactions:
    t[v].add(k)

print(t)


print(docs)
# from collections import defaultdict
#
# groups = defaultdict(list)
# pairs = [('fruit', 'apple'), ('fruit', 'banana'), ('veg', 'carrot')]
#
# for category, item in pairs:
#     groups[category].append(item)
#
# print(groups)

# words = ["apple","banana","orange","apple","banana","orange","mango"]
# freq = Counter()
# counts = defaultdict(int)
# for word in words:
#     freq[word] += 1
#     counts[word]+=1
#
# for name, count in freq.items():
#     print(f"{name}:{count}")
#
# print(freq)
# print(counts)



