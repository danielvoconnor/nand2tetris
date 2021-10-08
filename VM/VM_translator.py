import sys

initialize_SP = ['// Initialize SP','@256','D=A','@SP','M=D']
infinite_loop = ['(INFINITELOOP)','@INFINITELOOP','0;JMP']
push_D = ['// Now we push D','@SP','A=M','M=D','@SP','M=M+1','// Finished push D']
push_0 = ['@SP','A=M','M=0','@SP','M=M+1']
segment_names = {'local':'LCL','argument':'ARG','this':'THIS','that':'THAT'}
logic_op_count = 0

def write_push(segment, i):
    # I'll assume i is already a string, rather than an int
    comment = ['// push ' + segment + ' ' + i]

    if segment in ['local', 'argument', 'this', 'that']:
        seg_name = segment_names[segment]
        commands = ['@'+i,'D=A','@'+seg_name,'A=M+D','D=M'] + push_D
    elif segment == 'pointer':
        if i == '0':
            commands = ['@'+'THIS','D=M'] + push_D
        elif i == '1':
            commands = ['@'+'THAT','D=M'] + push_D
        else:
            print('ERROR: POINTER INDEX SHOULD BE 0 OR 1')
    elif segment == 'temp':
        commands = ['@'+i,'D=A','@5','A=A+D','D=M'] + push_D
    elif segment == 'constant':
        commands = ['@'+i,'D=A'] + push_D
    elif segment == 'static':
        commands = ['@' + fname_without_path + '.' + i, 'D = M'] + push_D

    return comment + commands
   
#pop_to_R13 = ['@SP','M=M-1', 'A=M', 'D=M', '@R13', 'M=D']
pop_to_D = ['// Now we pop to D','@SP','M=M-1', 'A=M', 'D=M','// Finished popping to D']
def write_pop(segment, i):
    # I'll assume i is already a string, rather than an int

    comment = ['// pop ' + segment + ' ' + i]

    if segment in ['local', 'argument', 'this', 'that']:
        seg_name = segment_names[segment]
        put_addr_in_R13 = ['@'+i,'D=A','@'+seg_name,'D=D+M','@R13','M=D']
        commands = put_addr_in_R13 + pop_to_D + ['@R13','A=M','M=D']

    elif segment == 'pointer':
        if i == '0':
            commands = pop_to_D + ['@THIS','M=D']
        elif i == '1':
            commands = pop_to_D + ['@THAT','M=D']
        else:
            print('ERROR: POINTER INDEX SHOULD BE 0 OR 1')

    elif segment == 'temp':
        put_addr_in_R13 = ['@'+i,'D=A','@5','D=D+A','@R13','M=D']
        commands = put_addr_in_R13 + pop_to_D + ['@R13','A=M','M=D']

    elif segment == 'static':
        commands = pop_to_D + ['@'+fname_without_path + '.' + i,'M=D']

    return comment + commands

op_symbols = {'add':'+','sub':'-','and':'&','or':'|','neg':'-','not':'!'}
jump_commands = {'eq':'D;JEQ','gt':'D;JGT','lt':'D;JLT'}
def write_arithmetic(operation):

    comment = ['// '+operation]
    global logic_op_count

    if operation in ['add','sub','and','or']:

        op = op_symbols[operation]
        commands = pop_to_D + ['@SP','A=M-1','M=M' + op + 'D']

    elif operation in ['neg','not']:

        op = op_symbols[operation]
        commands = ['@SP','A=M-1','M=' + op + 'M']

    elif operation in ['eq','gt','lt']:

        jump_command = jump_commands[operation]
        true_label = 'PUSHTRUE' + str(logic_op_count)
        finished_op_label = 'FINISHEDLOGICOP' + str(logic_op_count)
        logic_op_count += 1
        commands = pop_to_D + ['@SP','A=M-1','D=M-D','@'+true_label,jump_command] + \
                   ['@SP','A=M-1','M=0','@'+finished_op_label,'0;JMP'] + \
                   ['(' + true_label + ')','@SP','A=M-1','M=-1'] + \
                   ['(' + finished_op_label + ')']

    return comment + commands

def write_label(lbl, fun_name):
    # fun_name is the name of the function that we are currently translating.

    commands = ['(' + fun_name + '$' + lbl + ')']
    return commands

def write_goto(lbl, fun_name):

    full_label = fun_name + '$' + lbl
    commands = ['@' + full_label, '0;JMP']

    return commands

def write_if(lbl,fun_name):

    full_label = fun_name + '$' + lbl
    commands = pop_to_D + ['@' + full_label, 'D;JNE']

    return commands

def write_call(fun_name, num_args,i):
    # To understand what i is, see p. 163 of The Elements of Computing Systems:
    # "The handling of each call command within foo's code generates, and
    # injects into the assembly code stream, a symbol XXX.foo@ret.i, where i is
    # a running integer (one such symbol is generated for each call command within foo).

    return_label = fun_name + '$ret.' + str(i)
    push_return_addr = ['@' + return_label,'D=A'] + push_D
    push_LCL = ['@LCL','D=M'] + push_D
    push_ARG = ['@ARG','D=M'] + push_D
    push_THIS = ['@THIS','D=M'] + push_D
    push_THAT = ['@THAT','D=M'] + push_D
    reposition_ARG = ['@SP','D=M','@5','D=D-A','@' + str(num_args),'D=D-A'] + push_D
    reposition_LCL = ['@SP','D=M','@LCL','M=D']
    goto_f = ['@' + fun_name,'0;JMP']
    place_return_label = ['(' + return_label + ')']

    commands = push_return_addr + push_LCL + push_ARG + push_THIS + push_THAT + reposition_ARG \
               + reposition_LCL + goto_f + place_return_label

    return commands

def write_function(fun_name, num_vars):

    loop_label = fun_name + '$push_zeros_loop'
    increment_i = ['@i','M=M+1'] # is i used elsewhere in my assembly code? Is this name a conflict?
    commands = ['(' + fun_name + ')', '@i','M=0','('+loop_label+')'] + push_0 \
               + increment_i + ['@i','D=M','@' + str(num_vars),'D=D-A','@' + loop_label,'D;JLT']

    return commands

############################# Now do the translation. #####################
if False:
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

    fun_name = 'Main.main'
    hack_code = initialize_SP
    for line in lines_trimmed:

        words = line.split()
        if words[0] == 'push':
            segment = words[1]
            i = words[2]
            hack_code = hack_code + write_push(segment,i)
        elif words[0] == 'pop':
            segment = words[1]
            i = words[2]
            hack_code = hack_code + write_pop(segment,i)
        elif words[0] in ['add','sub','neg','eq','gt','lt','and','or','not']:
            hack_code = hack_code + write_arithmetic(words[0])
        elif words[0] == 'label':
            lbl = words[1]
            hack_code = hack_code + write_label(lbl,fun_name)
        elif words[0] == 'goto':
            lbl = words[1]
            hack_code = hack_code + write_goto(lbl,fun_name)
        elif words[0] == 'if-goto':
            lbl = words[1]
            hack_code = hack_code + write_if(lbl,fun_name)
        else:
            print('ERROR: words[0] not recognized!')

    hack_code = hack_code + infinite_loop
    hack_code = [s + '\n' for s in hack_code]
    fname_out = fname[:-3] + '.asm'
    print('fname_out: ', fname_out)
    target = open(fname_out,'w')
    target.writelines(hack_code)
    target.close()













