import sys
import os
import JackTokenizer
# This code has now passed all of the chapter 10 tests.

def xml_for_type(token):

    if token in ['int','char','boolean']:
        xml = '<keyword> ' + token + ' </keyword>'
    else:
        xml = '<identifier> ' + token + ' </identifier>'

    return xml
   

def compile_class(tokens):

    xml = ['<class>','<keyword> class </keyword>']
    xml = xml + ['<identifier> ' + tokens[1] + ' </identifier>']
    xml = xml + ['<symbol> { </symbol>']
    tokens = tokens[3:]

    while tokens[0] in ['static','field']:

        xml_classVarDec, tokens = compile_classVarDec(tokens)
        xml = xml + xml_classVarDec

    while tokens[0] in ['constructor','function','method']:

        xml_subroutineDec, tokens = compile_subroutineDec(tokens)
        xml = xml + xml_subroutineDec

    xml = xml + ['<symbol> } </symbol>', '</class>']

    return xml

def compile_classVarDec(tokens):
    xml = ['<classVarDec>', '<keyword> ' + tokens[0] + ' </keyword>']
    xml = xml + [xml_for_type(tokens[1]),'<identifier> ' + tokens[2] + ' </identifier>']

    i = 3
    while tokens[i] == ',':
        xml = xml + ['<symbol> , </symbol>', '<identifier> ' + tokens[i+1] + ' </identifier>']
        i = i+2

    xml = xml + ['<symbol> ; </symbol>', '</classVarDec>']
    tokens = tokens[i+1:]

    return xml, tokens

def compile_subroutineDec(tokens):

    xml = ['<subroutineDec>', '<keyword> ' + tokens[0] + ' </keyword>']
    if tokens[1] == 'void':
        xml = xml + ['<keyword> void </keyword>']
    else:
        xml = xml + ['<identifier> ' + tokens[1] + ' </identifier>']

    xml = xml + ['<identifier> ' + tokens[2] + ' </identifier>','<symbol> ( </symbol>']
    tokens = tokens[4:]

    xml_parameterList, tokens =  compile_parameterList(tokens) 
    xml = xml + xml_parameterList + ['<symbol> ) </symbol>']
    xml_subroutineBody, tokens = compile_subroutineBody(tokens[1:])
    xml = xml + xml_subroutineBody + ['</subroutineDec>']

    return xml, tokens

def compile_parameterList(tokens):

    if tokens[0] != ')':

        xml = ['<parameterList>']
        xml = xml + [xml_for_type(tokens[0]),'<identifier> ' + tokens[1] + ' </identifier>']
        tokens = tokens[2:]
        while tokens[0] == ',':
            xml = xml + ['<symbol> , </symbol>',xml_for_type(tokens[1])]
            xml = xml + ['<identifier> ' + tokens[2] + ' </identifier>']
            tokens = tokens[3:]

        xml = xml + ['</parameterList>']
        return xml, tokens

    else:
        xml = ['<parameterList> ', '</parameterList>']
        return xml, tokens

def compile_subroutineBody(tokens):

    xml = ['<subroutineBody>','<symbol> { </symbol>']
    tokens = tokens[1:]
    while tokens[0] == 'var':
        xml_varDec, tokens = compile_varDec(tokens)
        xml = xml + xml_varDec

    xml_statements, tokens = compile_statements(tokens)
    xml = xml + xml_statements

    xml = xml + ['<symbol> } </symbol>','</subroutineBody>']

    return xml, tokens[1:]

def compile_varDec(tokens):

    xml = ['<varDec>','<keyword> var </keyword>',xml_for_type(tokens[1]),\
           '<identifier> ' + tokens[2] + ' </identifier>']

    tokens = tokens[3:]
    while(tokens[0] == ','):
        xml = xml + ['<symbol> , </symbol>','<identifier> ' + tokens[1] + ' </identifier>']
        tokens = tokens[2:]

    xml = xml + ['<symbol> ; </symbol>','</varDec>']

    return xml, tokens[1:]

def compile_statements(tokens):

    xml = ['<statements>']
    while tokens[0] in ['let','if','while','do','return']:

        if tokens[0] == 'let':
            xml_let, tokens = compile_let(tokens)
            xml = xml + xml_let
        elif tokens[0] == 'if':
            xml_if, tokens = compile_if(tokens)
            xml = xml + xml_if
        elif tokens[0] == 'while':
            xml_while, tokens = compile_while(tokens)
            xml = xml + xml_while
        elif tokens[0] == 'do':
            xml_do, tokens = compile_do(tokens)
            xml = xml + xml_do
        elif tokens[0] == 'return':
            xml_return, tokens = compile_return(tokens)
            xml = xml + xml_return
        else:
            print('ERROR: tokens[0] does not match any statement.')
            sys.exit()
    xml = xml + ['</statements>']

    return xml, tokens

def compile_let(tokens):

    xml = ['<letStatement>']
    xml = xml + ['<keyword> let </keyword>','<identifier> ' + tokens[1] + ' </identifier>']
    tokens = tokens[2:]
    if tokens[0] == '[':
        xml = xml + ['<symbol> [ </symbol>']
        xml_expression, tokens = compile_expression(tokens[1:])
        xml = xml + xml_expression + ['<symbol> ] </symbol>']
        tokens = tokens[1:]
    
    xml = xml + ['<symbol> = </symbol>']
    xml_expression, tokens = compile_expression(tokens[1:])
    xml = xml + xml_expression + ['<symbol> ; </symbol>','</letStatement>']

    return xml, tokens[1:]

def compile_if(tokens):

    xml = ['<ifStatement>','<keyword> if </keyword>','<symbol> ( </symbol>']
    xml_expression, tokens = compile_expression(tokens[2:])
    xml = xml + xml_expression + ['<symbol> ) </symbol>','<symbol> { </symbol>']
    xml_statements, tokens = compile_statements(tokens[2:])
    xml = xml + xml_statements + ['<symbol> } </symbol>']
    tokens = tokens[1:]

    if tokens[0] == 'else':
        xml = xml + ['<keyword> else </keyword>','<symbol> { </symbol>']
        xml_statements, tokens = compile_statements(tokens[2:])
        xml = xml + xml_statements + ['<symbol> } </symbol>']
        tokens = tokens[1:]

    xml = xml + ['</ifStatement>']
    return xml, tokens

def compile_while(tokens):

    xml = ['<whileStatement>','<keyword> while </keyword>','<symbol> ( </symbol>']
    xml_expression, tokens = compile_expression(tokens[2:])
    xml = xml + xml_expression + ['<symbol> ) </symbol>','<symbol> { </symbol>']
    xml_statements, tokens = compile_statements(tokens[2:])
    xml = xml + xml_statements + ['<symbol> } </symbol>','</whileStatement>']
    return xml, tokens[1:]

def compile_do(tokens):

    xml = ['<doStatement>','<keyword> do </keyword>']
    tokens = tokens[1:]
    if tokens[1] == '(':
        xml = xml + ['<identifier> ' + tokens[0] + ' </identifier>']
        tokens = tokens[1:]
    else:
        xml = xml + ['<identifier> ' + tokens[0] + ' </identifier>','<symbol> . </symbol>']
        xml = xml + ['<identifier> ' + tokens[2] + ' </identifier>']
        tokens = tokens[3:]

    xml = xml + ['<symbol> ( </symbol>']
    xml_expressionList, tokens = compile_expressionList(tokens[1:])
        
    xml = xml + xml_expressionList + ['<symbol> ) </symbol>'] 
    xml = xml + ['<symbol> ; </symbol>','</doStatement>'] 

    return xml, tokens[2:]

def compile_return(tokens):

    xml = ['<returnStatement>','<keyword> return </keyword>']
    tokens = tokens[1:]

    if tokens[0] != ';':
        xml_expression, tokens = compile_expression(tokens)
        xml = xml + xml_expression

    xml = xml + ['<symbol> ; </symbol>','</returnStatement>']
    return xml, tokens[1:]

# ops = ['+','-','*','/','&','|','<','>','=']
ops = ['+','-','*','/','&amp;','|','&lt;','&gt;','=']
def compile_expression(tokens):

    xml = ['<expression>']
    xml_term, tokens = compile_term(tokens)
    xml = xml + xml_term
    if tokens[0] in ops:
        xml = xml + ['<symbol> ' + tokens[0] + ' </symbol>']
        xml_term, tokens = compile_term(tokens[1:])
        xml = xml + xml_term

    xml = xml + ['</expression>']

    return xml, tokens

keywords = ['class','constructor','function','method','field','static',\
            'var','int','char','boolean','void','true','false','null',\
            'this','let','do','if','else','while','return']
keyword_constants = ['true','false','null','this']
unary_ops = ['-','~']

def compile_term(tokens):
    # I'll assume stringConstant tokens include the quotation marks.

    if tokens[0] in keyword_constants:
        xml = ['<keyword> ' + tokens[0] + ' </keyword>']
        tokens = tokens[1:]
    elif tokens[0][0] == '"':
        xml = ['<stringConstant> ' + tokens[0][1:-1] + ' </stringConstant>']
        tokens = tokens[1:]
    elif tokens[0][0].isdigit():
        xml = ['<integerConstant> ' + tokens[0] + ' </integerConstant>']
        tokens = tokens[1:]
    elif tokens[0] == '(':
        xml_expression, tokens = compile_expression(tokens[1:])
        xml = ['<symbol> ( </symbol>'] + xml_expression + ['<symbol> ) </symbol>']
        tokens = tokens[1:]
    elif tokens[0] in unary_ops:
        xml = ['<symbol> ' + tokens[0] + ' </symbol>']
        xml_term, tokens = compile_term(tokens[1:])
        xml = xml + xml_term
    elif tokens[1] == '[':
        xml = ['<identifier> ' + tokens[0] + ' </identifier>', '<symbol> [ </symbol>']
        xml_expression, tokens = compile_expression(tokens[2:])
        xml = xml + xml_expression + ['<symbol> ] </symbol>']
        tokens = tokens[1:]
    elif tokens[1] == '(':
        xml = ['<identifier> ' + tokens[0] + ' </identifier>','<symbol> ( </symbol>']
        xml_expressionList, tokens = compile_expressionList(tokens[2:])
        xml = xml + xml_expressionList
        xml = xml + ['<symbol> ) </symbol>']
        tokens = tokens[1:]
    elif tokens[1] == '.':
        xml = ['<identifier> ' + tokens[0] + ' </identifier>','<symbol> . </symbol>']
        xml = xml + ['<identifier> ' + tokens[2] + ' </identifier>','<symbol> ( </symbol>']
        xml_expressionList, tokens = compile_expressionList(tokens[4:])
        xml = xml + xml_expressionList
        xml = xml + ['<symbol> ) </symbol>']
        tokens = tokens[1:]
    else:
        xml = ['<identifier> ' + tokens[0] + ' </identifier>']
        tokens = tokens[1:]

    xml = ['<term>'] + xml + ['</term>']

    return xml, tokens

def compile_expressionList(tokens):

    xml = []
    if tokens[0] != ')':
        xml_expression, tokens = compile_expression(tokens)
        xml = xml + xml_expression
        while tokens[0] == ',':
            xml = xml + ['<symbol> , </symbol>']
            xml_expression, tokens = compile_expression(tokens[1:])
            xml = xml + xml_expression

    xml = ['<expressionList>'] + xml + ['</expressionList>']
    return xml, tokens


if __name__ == '__main__':
    
    directory = sys.argv[1]
    jack_files = [fname for fname in os.listdir(directory) if fname.endswith('.jack')]
    
    for fname in jack_files:

        print('Now compiling: ', directory + fname)
        f = open(directory + fname)
        s = f.read()
        f.close()

        tokens, token_types = JackTokenizer.tokenize(s)
        for i in range(len(token_types)):
            if token_types[i] == 'stringConstant':
                tokens[i] = '"' + tokens[i] + '"'

        xml = compile_class(tokens)
        xml = [s + '\n' for s in xml]

        fname_out = directory + fname[:-5] + '_myXml.xml'
        f = open(fname_out,'w')
        f.writelines(xml)
        f.close()
        







    








    































