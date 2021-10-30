import sys
import JackTokenizer

fname = sys.argv[1]
f = open(fname)
code = f.read()
f.close()

tokens, token_types = JackTokenizer.tokenize(code)




