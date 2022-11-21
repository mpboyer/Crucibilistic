import re


with open(r'C:\Users\mb692\PycharmProjects\Crucibilistic\dictionnaire.txt', encoding = "utf-8") as f :
    lines = f.readlines()

words = []

for word in lines :
    word = re.sub(r"\n", '', word)
    words.append(word)




