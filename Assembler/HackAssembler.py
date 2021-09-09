
print('Hello world!!')

filename = 'Add.asm'

with open(filename) as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]


for line in lines:

    print(line)






