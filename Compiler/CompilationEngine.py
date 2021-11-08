import sys

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

    xml = ['<subroutineDec>', '<keyword> ' + tokens[0] + '</keyword>']
    if tokens[1] == 'void':
        xml = xml + ['<keyword> void </keyword>']
    else:
        xml = xml + ['<identifier> ' + tokens[1] + ' </identifier>']

    xml = xml + ['<identifier> ' + tokens[2] + ' </identifier>','<symbol> ( </symbol>']
    tokens = tokens[4:]

    xml_parameterList, tokens =  compile_parameterList(tokens) 
    xml = xml + xml_parameterList + ['<symbol> ) </symbol>']
    xml_subroutineBody, tokens = compile_subroutineBody(tokens[1:])
    xml = xml + xml_subroutineBody

    return xml, tokens

def compile_parameterList(tokens):

    if tokens[0] != ')':

        xml = [xml_for_type(tokens[0]),'<identifier> ' + tokens[1] + ' </identifier>']
        i = 2
        while tokens[i] == ',':
            xml = xml + ['<symbol> , </symbol>',xml_for_type(tokens[i+1])]
            i = i + 2
        tokens = tokens[i:]
        return xml, tokens

    else:
        xml = []
        return xml, tokens

def compile_subroutineBody(tokens):

    xml = ['<symbol> { </symbol>']
    tokens = tokens[1:]
    while tokens[0] == 'var':
        xml_varDec, tokens = compile_varDec(tokens)
        xml = xml + xml_varDec

    xml_statements, tokens = compile_statements(tokens)
    xml = xml + xml_statements

    xml = xml + ['<symbol> } </symbol>']

    return xml, tokens[1:]

def compile_varDec(tokens):

    xml = ['<keyword> var </keyword>',xml_for_type(tokens[1]),\
           '<identifier> ' + tokens[2] + '</identifier>']

    tokens = tokens[3:]
    while(tokens[0] == ','):
        xml = xml + ['<symbol> , </symbol>','<identifier> ' + tokens[1] + ' </identifier>']
        tokens = tokens[2:]

    xml = xml + ['<symbol> ; </symbol>']

    return xml, tokens[1:]

def compile_statements(tokens):

    xml = []
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

    return xml, tokens

def compile_let(tokens):

    xml = ['<keyword> let </keyword>','<identifier> ' + tokens[1] + ' </identifier>']
    if tokens[2] == '[':
        xml = xml + ['<symbol> [ </symbol>']
        xml_expression, tokens = compile_expression(tokens[3:])
        xml = xml_expression + ['<symbol> ] </symbol>']
        tokens = tokens[1:]

    xml = xml + ['<symbol> = </symbol>']
    xml_expression, tokens = compile_expression(tokens[1:])
    xml = xml + xml_expression + ['<symbol> ; </symbol>']

    return xml, tokens[1:]

def compile_if(tokens):

    xml = ['<keyword> if </keyword>','<symbol> ( </symbol>']
    xml_expression, tokens = compile_expression(tokens[2:])
    xml = xml + xml_expression + ['<symbol> ) </symbol>','<symbol> { </symbol>']
    xml_statements, tokens = compile_statements(tokens[2:])
    xml = xml + xml_statements + ['<symbol> } </symbol>']
    tokens = tokens[1:]

    if tokens[0] == 'else':
        xml = xml + ['<symbol> { </symbol>']
        xml_statements, tokens = compile_statements(tokens[1:])
        xml = xml + xml_statements + ['<symbol> } </symbol>']
        tokens = tokens[1:]

    return xml, tokens

def compile_while(tokens):

    xml = ['<keyword> while </keyword>','<symbol> ( </symbol>']
    xml_expression, tokens = compile_expression(tokens[2:])
    xml = xml + xml_expression + ['<symbol> ) </symbol>','<symbol> { </symbol>']
    xml_statements, tokens = compile_statements(tokens[2:])
    xml = xml + xml_statements + ['<symbol> } </symbol>']
    return xml, tokens[1:]

def compile_do(tokens):

    xml = ['<keyword> do </keyword>']
    xml_subroutine, tokens = compile_term(tokens[1:])
    xml = xml + xml_subroutine + ['<symbol> ; </symbol>']

    return xml, tokens[1:]

def compile_return(tokens):

    xml = ['<keyword> return </keyword>']
    tokens = tokens[1:]

    if tokens[0] != ';':
        xml_expression, tokens = compile_expression(tokens)
        xml = xml + xml_expression

    xml = xml + ['<symbol> ; </symbol>']
    return xml, tokens[1:]







    








    































