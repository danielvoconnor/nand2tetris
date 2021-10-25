import sys

# Read the code to be tokenized into a string.
fname = sys.argv[1]
f = open(fname)
code = f.read()
f.close()

# Remove /* ... */ style comments from the code
code_without_comments = ''

comment_flag = False
i = 0
while i < len(code):

    if (i <= len(code) - 2) and (code[i:(i+2)] == '/*'):
        comment_flag = True
        i = i + 2 
    if (i >= 2) and (code[i-2:i] == '*/'):
        comment_flag = False
    
    if comment_flag == False:
        code_without_comments = code_without_comments + code[i]

    i = i + 1

code = code_without_comments

# Remove // style comments from the code
code_without_comments = ''

comment_flag = False
i = 0
while i < len(code):

    if (i <= len(code) - 2) and (code[i:(i+2)] == '//'):
        comment_flag = True
        i = i + 2 
    if comment_flag == True and code[i] == '\n':
        comment_flag = False
        continue
    
    if comment_flag == False:
        code_without_comments = code_without_comments + code[i]

    i = i + 1

code = code_without_comments

check_file = open('code_without_comments.jack','w')
check_file.write(code_without_comments)
check_file.close()








tokens = []


