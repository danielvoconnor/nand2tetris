
filename = 'MaxL.asm'


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

with open(filename) as file:
    lines = file.readlines()

output_lines = []
count = 0
for line in lines:

    line = line.partition('//')[0]
#    breakpoint()
    line = ''.join(line.split()) # Remove all white space from the line
    if not line:
        continue

    if line[0] == '@':
        address = int(line[1:])
        bits = '0' + int_to_binary(address)
        output_lines.append(bits)
        print('Full line: ', line)
        print('\n')

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
            
        print('Full line: ', line)
        print('dest: ', dest, '(', translate_dest(dest),')')
        print('comp: ', comp, '(', translate_comp(comp), ')')
        print('jump: ', jump, '(', translate_jump(jump), ')')
        print('\n')



    count += 1






