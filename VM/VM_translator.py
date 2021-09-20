import sys


def write_push(segment, i):

    if segment == 'constant':
        return 0
    else:
        return ['//push ' + segment + ' ' + str(i),
                '@'+str(i),
                'D=A',
                '@'+segment,
                'A=M+D',
                'D=M',
                '@SP',
                'A=M',
                'M=D',
                '@SP',
                'M=M+1']


fname = sys.argv[1]
print('filename: ', fname)
f = open(fname)
lines_raw = f.readlines()
f.close()

# Remove comments and all whitespace
lines_trimmed = []
for line in lines_raw:

    line = line.partition('//')[0]
    if line.strip():
        lines_trimmed.append(line)


for line in lines_trimmed:

    print(line.split())





