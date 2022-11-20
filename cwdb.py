with open(r'C:\Users\mb692\PycharmProjects\TIPE_2022_2023\cwdb.txt', encoding = "utf-8") as f :
    lines = f.readlines()

clues = []

for line in lines :
    l = line.split("\t")
    clues.append((l[2], l[3]))




