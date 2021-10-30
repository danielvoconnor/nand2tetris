

def compile_class(tokens,token_types):

    xml = ['<class>']
    xml_className, tokens, token_types = compile_className(tokens[1:],token_types[1:])
    xml = xml + xml_className

    xml = xml + ['<symbol> { </symbol>']
    tokens = tokens[1:]
    token_types = token_types[1:]

    while tokens[0] in ['static','field']:

        xml_classVarDec, tokens, token_types = compile_classVarDec(tokens,token_types)
        xml = xml + xml_classVarDec

    while tokens[0] in ['constructor','function','method']:

        xml_subroutineDec, tokens, token_types = compile_subroutineDec(tokens,token_types)
        xml = xml + xml_subroutineDec

    xml = xml + ['<symbol> } </symbol>', '</class>']

    return xml

def compile_className(tokens,token_types):

    xml = ['<className>','<identifier> ' + tokens[0] + ' </identifier>', '</className>']
    return xml, tokens[1:], token_types[1:]

def compile_classVarDec(tokens,token_types):
    # PICK UP HERE. I NEED A compile_type FUNCTION. 
    # EACH NONTERMINAL ELEMENT NEEDS ITS OWN OPENING AND CLOSING TAGS.
    # BE CONSISTENT ABOUT THAT.
    xml = ['<classVarDec>', '<keyword> ' + tokens[0] + ' </keyword>', \
           '<type> ' + tokens[1] + ' </type>','<varName> ' + tokens[2] + ' </varName>']

    i = 3
    while tokens[i] == ',':
        xml = xml + ['<symbol> , </symbol>', '<varName> ' + tokens[i+1] + ' </varName>']
        i = i+2

    xml = xml + ['<symbol> ; </symbol>', '</classVarDec>']
    tokens = tokens[i+1:]
    token_types = token_types[i+1,:]

    return xml, tokens, token_types

def compile_subroutineDec(tokens,token_types):

    xml = ['<subroutineDec>', '<keyword> ' + tokens[0] + '</keyword>']
    if tokens[1] == 'void':
        xml = xml + ['<keyword> void </keyword>']
    else:
        xml = xml + ['<type> ' + tokens[1] + ' </type>']

    xml = xml + ['<subroutineName> ' + tokens[2] + ' </subroutineName>','<symbol> ( </symbol>']
    tokens = tokens[4:]
    token_types = token_types[4:]

    xml_parameterList, tokens, token_types =  compile_parameterList(tokens,token_types) 
    xml = xml + xml_parameterList + ['<symbol> ) </symbol>']
    xml_subroutineBody, tokens, token_types = compile_subroutineBody(tokens[1:],token_types[1:])
    xml = xml + xml_subroutineBody

    return xml, tokens, token_types


    # PICK UP HERE. WRITE compile_parameterList and compile_subroutineBody.














