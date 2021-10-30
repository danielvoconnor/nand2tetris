

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

# PICK UP HERE. FINISH WRITING THIS AND TEST IT.

