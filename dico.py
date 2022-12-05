import re


with open(r'C:\Users\mb692\PycharmProjects\Crucibilistic\dictionnaire.txt', encoding = "utf-8") as f :
    lines_1 = f.readlines()

words = {}

for word in lines_1:
    word = re.sub(r"\n", '', word)
    words[word] = 1

with open(r'C:\Users\mb692\PycharmProjects\Crucibilistic\cwdb.txt', encoding = "utf-8") as f :
    lines_2 = f.readlines()

for line in lines_2:
    li = line.split("\t")
    words[li[3]] = 1