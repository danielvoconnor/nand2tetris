
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
        print('comp: ', comp)
        print('jump: ', jump)
        print('\n')



    count += 1






