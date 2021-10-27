import sys

# Now tokenize the code
symbols = ['{','}','(',')','[',']','.',',',';','+','-','*','/','&','|','<','>','=','~']

def extract_token(code):
    # code is a string containing the contents of a .jack file
    # I'll assume that comments have already been removed.
    # I'll also assume code is not pure whitespace.

    code = code.strip()
    if len(code) == 1:
        return code, ''

    if code[0] == '"':
        parts = code[1:].partition('"')
        token = parts[0]
        code = parts[2]
        return token, code

    if code[0] in symbols:

        token = code[0]
        code = code[1:]
        return token, code

    if code[0].isdigit():

        token = ''
        i = 0
        while code[i].isdigit():
            token = token + code[i]
            i = i + 1
        code = code[i:]
        return token, code

    token = ''
    i = 0
    while (code[i] not in symbols) and (not code[i].isspace()):
        token = token + code[i]
        i = i + 1

    code = code[i:]
    return token, code

    print('ERROR: TOKEN EXTRACTION FAILED')
    sys.exit()



if True:
    # Read the code to be tokenized into a string.
    fname = sys.argv[1]
    f = open(fname)
    code = f.read()
    f.close()

    # Remove /* ... */ style comments from the code
    code_without_comments = ''
    tail = code
    while tail != '':

        parts = tail.partition('/*')
        code_without_comments = code_without_comments + parts[0]
        tail = parts[2].partition('*/')[2]

    code = code_without_comments

    # Remove // style comments from the code
    code_without_comments = ''
    tail = code
    while tail != '':

        parts = tail.partition('//')
        code_without_comments = code_without_comments + parts[0]
        tail = parts[2]

        parts = tail.partition('\n')
        tail = parts[1] + parts[2]

    code = code_without_comments



    check_file = open('code_without_comments.jack','w')
    check_file.write(code_without_comments)
    check_file.close()

    tokens = []

























