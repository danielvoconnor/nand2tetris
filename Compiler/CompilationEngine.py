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

# PICK UP HERE. WRITE compile_subroutineBody, ETC.

































