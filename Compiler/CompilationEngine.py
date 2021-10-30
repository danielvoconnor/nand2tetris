

def compile_class(tokens,token_types):

    xml = ['<class>','<classname> ' + tokens[1] + '</classname>'] + \
          ['<symbol> { </symbol>']

    tokens = tokens[3:]
    token_types = token_types[3:]
    while tokens[0] in ['static','field']:

        xml_classVarDec, tokens, token_types = compile_classVarDec(tokens,token_types)
        xml = xml + xml_classVarDec

    while tokens[0] in ['constructor','function','method']:

        xml_subroutineDec, tokens, token_types = compile_subroutineDec(tokens,token_types)
        xml = xml + xml_subroutineDec

    xml = xml + ['<symbol> } </symbol>', '</class>']

    return xml

def compile_classVarDec(tokens,token_types):

    xml = ['<keyword> ' + tokens[0] + ' </keyword>', '<type> ' + tokens[1] + ' </type>',\
          ['<varName> ' + tokens[2] + ' </varName>']

    i = 3
    while tokens[i] == ',':
        xml = xml + ['<symbol> , </symbol>', '<varName> ' + tokens[i+1] + ' </varName>']
        i = i+2

    xml = xml + ['<symbol> ; </symbol>']
    tokens = tokens[i+1:]
    token_types = token_types[i+1,:]

    return xml, tokens, token_types

def compile_subroutineDec(tokens,token_types):

    xml = ['<keyword> ' + tokens[0] + '</keyword>']
    if tokens[1] == 'void':
        xml = xml + ['<keyword> void </keyword>']
    else:
        xml = xml + ['<type> ' + tokens[1] + ' </type>']
















