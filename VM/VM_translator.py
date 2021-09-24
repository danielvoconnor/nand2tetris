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

push_D = ['#Now we push D','@SP','A=M','M=D','@SP','M=M+1','#Finished push D']
segment_names = {'local':'LCL','argument':'ARG','this':'THIS','that':'THAT'}
logic_op_count = 0

def write_push(segment, i):
    comment = ['// push ' + segment + ' ' + str(i)]

    if segment in ['local', 'argument', 'this', 'that']:
        seg_name = segment_names[segment]
        commands = ['@'+str(i),'D=A','@'+seg_name,'A=M+D','D=M'] + push_D
    elif segment == 'pointer':
        if i == 0:
            commands = ['@'+'THIS','D=M'] + push_D
        elif i == 1:
            commands = ['@'+'THAT','D=M'] + push_D
        else:
            print('ERROR: POINTER INDEX SHOULD BE 0 OR 1')
    elif segment == 'temp':
        commands = ['@'+str(i),'D=A','@5','A=A+D','D=M'] + push_D
    elif segment == 'constant':
        commands = ['@'+str(i),'D=A'] + push_D
    elif segment == 'static':
        commands = ['@' + fname_without_path + '.' + str(i), 'D = M'] + push_D

    return comment + commands
   
#pop_to_R13 = ['@SP','M=M-1', 'A=M', 'D=M', '@R13', 'M=D']
pop_to_D = ['#Now we pop to D','@SP','M=M-1', 'A=M', 'D=M','#Finished popping to D']
def write_pop(segment, i):

    comment = ['// pop ' + segment + ' ' + str(i)]

    if segment in ['local', 'argument', 'this', 'that']:
        seg_name = segment_names[segment]
        put_addr_in_R13 = ['@'+str(i),'D=A','@'+seg_name,'D=D+M','@R13','M=D']
        commands = put_addr_in_R13 + pop_to_D + ['@R13','A=M','M=D']

    elif segment == 'pointer':
        if i == 0:
            commands = pop_to_D + ['@THIS','M=D']
        elif i == 1:
            commands = pop_to_D + ['@THAT','M=D']
        else:
            print('ERROR: POINTER INDEX SHOULD BE 0 OR 1')

    elif segment == 'temp':
        put_addr_in_R13 = ['@'+str(i),'D=A','@5','D=D+A','@R13','M=D']
        commands = put_addr_in_R13 + pop_to_D + ['@R13','A=M','M=D']

    elif segment == 'static':
        commands = pop_to_D + ['@'+fname_without_path + '.' + str(i),'M=D']

    return comment + commands

op_symbols = {'add':'+','sub':'-','and':'&','or':'|','neg':'-','not':'!'}
def write_arithmetic(operation):

    comment = ['#'+operation]

    if operation in ['add','sub','and','or']:
        op = op_symbols[operation]
        commands = ['@SP','A=M-1','M=M' + op + 'D']
        return pop_to_D + commands
    elif operation in ['neg','not']:
        op = op_symbols[operation]
        commands = ['@SP','A=M-1','M=' + op + 'M']
    elif operation == 'eq':
        global logic_op_count
        true_label = 'PUSHTRUE' + str(logic_op_count)
        finished_op_label = 'FINISHEDLOGICOP'+str(logic_op_count)
        logic_op_count += 1
        commands = pop_to_D + ['@SP','A=M-1','D=M-D','@'+true_label,'D;JEQ'] + \
                   ['@SP','A=M-1','M=0','@'+finished_op_label,'0;JMP'] + \
                   ['(' + true_label + ')','@SP','A=M-1','M=-1'] + \
                   ['(' + finished_op_label + ')']
    elif operation == 'gt':
        # PICK UP HERE.
        commands = []
    return comment + commands


check = write_arithmetic('eq')
for line in lines_trimmed:

    print(line.split())













