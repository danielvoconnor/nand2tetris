import sys

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


