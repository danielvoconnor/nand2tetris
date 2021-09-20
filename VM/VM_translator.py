import sys

# Read in the code
fname = sys.argv[1] # fname may or may not contain a full path.
print('filename: ', fname)
f = open(fname)
lines_raw = f.readlines()
f.close()
fname_without_path = fname.split('/')[-1][:-3] # '/Users/dvo/foo.VM' becomes 'foo', for example.

# Remove comments and all whitespace
lines_trimmed = []
for line in lines_raw:

    line = line.partition('//')[0]
    if line.strip():
        lines_trimmed.append(line)

push_D = ['@SP','A=M','M=D','@SP','M=M+1']
segment_names = {'local':'LCL','argument':'ARG','this':'THIS','that':'THAT'}

def write_push(segment, i):
    comment = ['// push ' + segment + ' ' + str(i)]

    if segment in ['local', 'argument', 'this', 'that']:
        seg_name = segment_names[segment]
        commands = ['@'+str(i),'D=A','@'+seg_name,'A=M+D','D=M'] + push_D
    elif segment == 'pointer':
        if i == 0:
            commands = ['@'+'THIS','D=A'] + push_D
        elif i == 1:
            commands = ['@'+'THAT','D=A'] + push_D
        else:
            print('ERROR: POINTER INDEX SHOULD BE 0 OR 1')
    elif segment == 'temp':
        commands = ['@'+str(i),'D=A','@5','A=A+D','D=M'] + push_D
    elif segment == 'constant':
        commands = ['@'+str(i),'D=A'] + push_D
    elif segment == 'static':
        commands = ['@' + fname_without_path + '.' + str(i), 'D = M'] + push_D

    return comment + commands
    
def write_pop(segment, i):

    comment = ['// pop ' + segment + ' ' + str(i)]
    # PICK UP HERE




for line in lines_trimmed:

    print(line.split())













