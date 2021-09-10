
filename = 'Add.asm'

with open(filename) as file:
    lines = file.readlines()
    lines = [line.rstrip().lstrip() for line in lines]

count = 0
for line in lines:

    line = line.partition('//')[0]
    if not line:
        continue

    

    print(line)
    count += 1






