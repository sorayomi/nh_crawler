
bangos = []
with open('raw.txt', 'r') as f:
    for line in f:
        if '/g/' in line:
            line = line.split('/')
            print(line[-2])
            bangos.append(line[-2])

with open('bango.txt', 'w') as f:
    for bango in bangos:
        f.write(f"{bango}\n")
