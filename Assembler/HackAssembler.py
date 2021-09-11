import sys

fname = sys.argv[1]
print('filename: ', fname)
f = open(fname)
lines_raw = f.readlines()
f.close()

# Remove comments and all whitespace
lines_trimmed = []
for line in lines_raw:

    line = line.partition('//')[0]
    line = ''.join(line.split())
    if line:
        lines_trimmed.append(line)

# Create symbol table
symbol_table = dict()
symbol_table['R0'] = 0
symbol_table['R1'] = 1
symbol_table['R2'] = 2
symbol_table['R3'] = 3
symbol_table['R4'] = 4
symbol_table['R5'] = 5
symbol_table['R6'] = 6
symbol_table['R7'] = 7
symbol_table['R8'] = 8
symbol_table['R9'] = 9
symbol_table['R10'] = 10
symbol_table['R11'] = 11
symbol_table['R12'] = 12
symbol_table['R13'] = 13
symbol_table['R14'] = 14
symbol_table['R15'] = 15
symbol_table['SP'] = 0
symbol_table['LCL'] = 1
symbol_table['ARG'] = 2
symbol_table['THIS'] = 3
symbol_table['THAT'] = 4
symbol_table['SCREEN'] = 16384
symbol_table['KBD'] = 24576

lines = []
line_number = 0
for line in lines_trimmed:

    if line[0] == '(':
        symbol = line[1:-1]
        symbol_table[symbol] = line_number
    else: 
        lines.append(line)
        line_number += 1

def int_to_binary(m):

    # m is an integer between 0 and 32,767
    s = ''
    for i in range(15):

        r = m % 2
        m = m//2

        s = str(r) + s

    return s

def translate_dest(dest):

    bits = ['0','0','0']
    for ch in dest:
        if ch == 'M':
            bits[2] = '1'
        if ch == 'D':
            bits[1] = '1'
        if ch == 'A':
            bits[0] = '1'

    bits = ''.join(bits)
    return bits

def translate_comp(comp):

    if comp == '0':
        return '0101010'
    elif comp == '1':
        return '0111111'
    elif comp == '-1':
        return '0111010'
    elif comp == 'D':
        return '0001100'
    elif comp == 'A':
        return '0110000'
    elif comp == 'M':
        return '1110000'
    elif comp == '!D':
        return '0001101'
    elif comp == '!A':
        return '0110001'
    elif comp == '!M':
        return '1110001'
    elif comp == '-D':
        return '0001111'
    elif comp == '-A':
        return '0110011'
    elif comp == '-M':
        return '1110011'
    elif comp == 'D+1':
        return '0011111'
    elif comp == 'A+1':
        return '0110111'
    elif comp == 'M+1':
        return '1110111'
    elif comp == 'D-1':
        return '0001110'
    elif comp == 'A-1':
        return '0110010'
    elif comp == 'M-1':
        return '1110010'
    elif comp == 'D+A':
        return '0000010'
    elif comp == 'D+M':
        return '1000010'
    elif comp == 'D-A':
        return '0010011'
    elif comp == 'D-M':
        return '1010011'
    elif comp == 'A-D':
        return '0000111'
    elif comp == 'M-D':
        return '1000111'
    elif comp == 'D&A':
        return '0000000'
    elif comp == 'D&M':
        return '1000000'
    elif comp == 'D|A':
        return '0010101'
    elif comp == 'D|M':
        return '1010101'
    else:
        print('ERROR: COMP NOT RECOGNIZED')
        return -1

def translate_jump(jump):

    if jump == '': 
        return '000'
    elif jump == 'JGT': 
        return '001'
    elif jump == 'JEQ':
        return '010'
    elif jump == 'JGE':
        return '011'
    elif jump == 'JLT':
        return '100'
    elif jump == 'JNE':
        return '101'
    elif jump == 'JLE':
        return '110'
    elif jump == 'JMP':
        return '111'
    else:
        print('ERROR: JUMP NOT RECOGNIZED')
        return -1

next_free_address = 16
output_lines = []
count = 0
for line in lines:

    if line[0] == '@':

        s = line[1:]
        if s[0].isdigit():
            address = int(s)
        elif s in symbol_table:
            address = symbol_table[s]
        else:
            address = next_free_address
            symbol_table[s] = address
            next_free_address += 1

        bits = '0' + int_to_binary(address)
        output_lines.append(bits + '\n')

    else:
        
        if '=' in line:
            parts = line.partition('=')
            dest = parts[0]
            comp_and_jump = parts[2]
        else:
            dest = ''
            comp_and_jump = line

        if ';' in comp_and_jump:
            parts = comp_and_jump.partition(';')
            comp = parts[0]
            jump = parts[2]
        else:
            comp = comp_and_jump
            jump = ''
            
#        print('Full line: ', line)
#        print('dest: ', dest, '(', translate_dest(dest),')')
#        print('comp: ', comp, '(', translate_comp(comp), ')')
#        print('jump: ', jump, '(', translate_jump(jump), ')')
#        print('\n')

        dest_bits = translate_dest(dest)
        comp_bits = translate_comp(comp)
        jump_bits = translate_jump(jump)

        output_lines.append('111' + comp_bits + dest_bits + jump_bits + '\n')

    count += 1

fname_out = fname[:-4] + '_dvo.hack'
print('fname_out: ', fname_out)
target = open(fname_out,'w')
target.writelines(output_lines)
target.close()




