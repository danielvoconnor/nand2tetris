# This code implements the virtual machine presented in chapters 7 and 8
# of The Elements of Computing Systems (2nd edition) by Nisan and Schocken.
# This book is also called ``nand2tetris". I'll sometimes refer to it by that name below.

import sys
import os

push_D = ['@SP','A=M','M=D','@SP','M=M+1']
push_0 = ['@SP','A=M','M=0','@SP','M=M+1']
segment_names = {'local':'LCL','argument':'ARG','this':'THIS','that':'THAT'}
logic_op_count = 0 # Isn't there some way to avoid needing this counter?

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
    comment = ['// goto ' + full_label]
    commands = comment + ['@' + full_label, '0;JMP']

    return commands

def write_if(lbl,fun_name):

    full_label = fun_name + '$' + lbl
    commands = pop_to_D + ['@' + full_label, 'D;JNE']

    return commands

def write_call(fun_name, num_args,caller_name,i):
    # This function translates the command: call fun_name num_args.
    # To understand what i is, see p. 163 of The Elements of Computing Systems:
    # "Let foo be a function within the file Xxx.vm.
    # "The handling of each call command within foo's code generates, and
    # "injects into the assembly code stream, a symbol XXX.foo@ret.i, where i is
    # "a running integer (one such symbol is generated for each call command within foo)."

    comment = ['// call ' + fun_name + ' ' + str(num_args)]
    return_label = caller_name + '$ret.' + str(i)
    push_return_addr = ['// Push return address','@' + return_label,'D=A'] + push_D
    push_LCL = ['// Push LCL','@LCL','D=M'] + push_D
    push_ARG = ['// Push ARG','@ARG','D=M'] + push_D
    push_THIS = ['// Push THIS','@THIS','D=M'] + push_D
    push_THAT = ['// Push THAT', '@THAT','D=M'] + push_D
#    reposition_ARG = ['// Reposition ARG','@SP','D=M','@5','D=D-A','@' + str(num_args),'D=D-A'] + push_D # Why was I pushing D? Bug right?
    reposition_ARG = ['// Reposition ARG','@SP','D=M','@5','D=D-A','@' + str(num_args),'D=D-A','@ARG','M=D']
    reposition_LCL = ['// Reposition LCL', '@SP','D=M','@LCL','M=D']
    goto_f = ['// goto ' + fun_name,'@' + fun_name,'0;JMP']
    place_return_label = ['(' + return_label + ')']

    commands = comment + push_return_addr + push_LCL + push_ARG +\
               push_THIS + push_THAT + reposition_ARG \
               + reposition_LCL + goto_f + place_return_label

    return commands

def write_function(fun_name, num_vars):
    # This function translates the command: function fun_name num_vars.
    # The function fun_name has num_vars local variables.
    # See p. 161 of nand2tetris for pseudocode for write_function.

    comment = ['//function ' + fun_name + ' ' + str(num_vars)]
    loop_start_label = fun_name + '$push_zeros_loop_start'
    loop_end_label = fun_name + '$push_zeros_loop_end'
    initialize_num_zeros_pushed = ['@num_zeros_pushed','M=0']
    if_pushed_all_goto_end_of_loop = \
            ['@num_zeros_pushed','D=M','@'+ str(num_vars),'D=D-A','@' + loop_end_label,'D;JEQ'] 
    increment_count = ['@num_zeros_pushed','M=M+1'] # num_zeros_pushed += 1
    commands =   comment \
               + ['(' + fun_name + ')'] \
               + initialize_num_zeros_pushed + ['('+loop_start_label+')'] \
               + if_pushed_all_goto_end_of_loop + push_0 + increment_count \
               + ['@' + loop_start_label,'0;JMP'] + ['(' + loop_end_label + ')']

    return commands

def write_return():
    # This function translates the command: return.
    # See p. 161 for pseudocode for this function.

    # I think this function could be just a string, rather than a function.

    comment = ['//return']
    set_frame = ['// set frame','@LCL','D=M','@frame','M=D']
    set_return = ['// set return','@5','D=A','@frame','A=M-D','D=M','@ret_addr','M=D']
    set_ARG = pop_to_D + ['// set ARG','@ARG','A=M','M=D'] # The value to be returned is on top of the stack. We place it in ARG[0].
    reposition_SP = ['// reposition SP','@ARG','D=M','@SP','M=D+1']
    restore_THAT = ['// restore THAT','@frame','A=M-1','D=M','@THAT','M=D']
    restore_THIS = ['// restore THIS','@2','D=A','@frame','A=M-D','D=M','@THIS','M=D']
    restore_ARG = ['// restore ARG','@3','D=A','@frame','A=M-D','D=M','@ARG','M=D']
    restore_LCL = ['// restore LCL','@4','D=A','@frame','A=M-D','D=M','@LCL','M=D']
    goto_retAddr = ['//goto retAddr','@ret_addr','A=M','0;JMP']

    commands = comment + set_frame + set_return + set_ARG + reposition_SP + restore_THAT + restore_THIS \
               + restore_ARG + restore_LCL + goto_retAddr

    return commands

############################# Now do the translation. #####################
if True:

    # First create the bootstrap code (see p. 162 for pseudocode)
    initialize_SP = ['// Initialize SP','@256','D=A','@SP','M=D']
    call_Sys_init = write_call('Sys.init',0,'VM_bootstrap_code',0)
    hack_code = initialize_SP + call_Sys_init # Warning: SimpleFunction.tst and earlier tests assume you are NOT calling Sys.init.

    # Now translate all of the given .vm files.
    s = sys.argv[1]
    if s.endswith('.vm'):
        fname_list = [s]
        fname_out = s[:-3] + '.asm'
    else:
        if s[-1] == '/': s = s[:-1]
        fname_list = [s + '/' + fname for fname in os.listdir(s) if fname.endswith('.vm')]
        fname_out = s + '/' + s.split('/')[-1] + '.asm'

    for fname in fname_list:

        # Read in the code
        print('Currently translating file: ', fname)
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

        current_function = '' # This is the current function we're translating. What is the best way to initialize this?
        call_counter = 0 # call_counter counts the number of call statements we have translated so far
                         # while we have been translating current_function.

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
                hack_code = hack_code + write_label(lbl,current_function)
            elif words[0] == 'goto':
                lbl = words[1]
                hack_code = hack_code + write_goto(lbl,current_function)
            elif words[0] == 'if-goto':
                lbl = words[1]
                hack_code = hack_code + write_if(lbl,current_function)
            elif words[0] == 'call':
                hack_code = hack_code + write_call(words[1],words[2],current_function,call_counter)
                call_counter += 1
            elif words[0] == 'function':
                current_function = words[1]
                call_counter = 0
                # fun_name = fname_without_path + '.' + current_function # I think this was unnecessary. 
                                                                         # We can assume functions are already named that way.
                num_vars = words[2]
                hack_code = hack_code + write_function(current_function,num_vars)
            elif words[0] == 'return':
                hack_code = hack_code + write_return()
            else:
                print('ERROR: words[0] not recognized!')

    # hack_code = hack_code + infinite_loop
    hack_code = [s + '\n' for s in hack_code]

    target = open(fname_out,'w')
    target.writelines(hack_code)
    target.close()













