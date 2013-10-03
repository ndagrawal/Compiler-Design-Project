import ply.lex as lex
from liveness import*
from static_semantics import *
import sys


reserved = {
    'print' : 'PRINT',
    'input' : 'INPUT',
    'print' : 'PRINT',
    'if'    : 'IF',
    'then'  : 'THEN',
    'else'  : 'ELSE',
    'while' : 'WHILE',
    'do'    : 'DO',
    'for'   : 'FOR',
    'int'   : 'INT',
    'bool'  : 'BOOL',
    'true'  : 'TRUE',
    'false' : 'FALSE',
    'new'   : 'NEW',
    'class' : 'CLASS',
    'return': 'RETURN',
    'void'  : 'VOID',
    'extends': 'EXTENDS',
    'this'  : 'THIS',
    'super' : 'SUPER',
    
}

tokens = [
    'IDENTIFIER',
    'NUMBER',
    'EQUALS',
    'TIMES',
    'SLASH',
    'PLUS',
    'MINUS',
    'COMMA',
    'LPAREN',
    'RPAREN',
    'LCURLY',
    'RCURLY',
    'GTEQ',
    'LAND',
    'LOR',
    'MOD',
    'LT',
    'GT',
    'LTEQ',
    'NEQ',
    'EQ',
    'NOT',
    'SEMICOLON',
    'LSQR',
    'RSQR',
    'INC',
    'DEC',
    'DOT'
    
] + list(reserved.values())



t_EQUALS                = r'='
t_TIMES                 = r'\*'
t_MOD                   = r'%'
t_SLASH                 = r'/'
t_PLUS                  = r'\+'
t_INC                   = r'\+\+'
t_MINUS                 = r'-'
t_DEC                   = r'--'
t_LPAREN                = r'\('
t_RPAREN                = r'\)'
t_LCURLY                = r'\{'
t_RCURLY                = r'\}'
t_LSQR                  = r'\['
t_RSQR                  = r'\]'
t_GTEQ                  = r'>='
t_LTEQ                  = r'<='
t_NEQ                   = r'!='
t_EQ                    = r'=='
t_LT                    = r'<'
t_GT                    = r'>'
t_NOT                   = r'!'
t_LAND                  = r'&&'
t_LOR                   = r'\|\|'
t_SEMICOLON             = r';'
t_COMMA                 = r','
t_DOT                   = r'\.'




def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value,'IDENTIFIER')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

t_ignore_COMMENT = r'\/\/.*'

def t_comment(t):
    r'/\*.*\*/'
    pass

def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    quit()
    t.lexer.skip(1)
lexer = lex.lex()


c_table={}

def preprocess(prgm):
    global c_table
    flag=0
    lexer.input(prgm)
    classlist=[]
    while True:
        tok = lexer.token()
        if not tok:
            break      # No more input
        if flag ==1:
            flag=0
            c_table[tok.value]=[]
            classlist.append(tok.value)
        elif tok.value == 'class':
            flag=1
    return classlist
    




def hackit(list1):
    fnew =open("Protoplasm.py","r+")
    fwr = open("newproto.py","w")

    line = fnew.readline()
    sline=""

    while line:
            sline = line
            #print line
            fwr.write("%s\n" % line)
            if "##Hack1----#" in sline:
                for i in list1:
                    S= "\t'"+str(i)+"' :\t'"+str(i)+"',"
##                    print S
                    fwr.write("%s\n" % S)
                                    #fwr.write("%s\n" % S)
            if "##--HACK2----#" in sline:
                for i in list1:
                    S="def t_"+str(i)+"(t): \n \tr'"+str(i)+"'   \n \tt.type = reserved.get(t.value,'"+str(i)+"') \n \treturn t"
##                    print S
                    fwr.write("%s\n" % S)
                                    #fwr.write(S)
            if "##--Hack3---#" in sline:
                
                if list1==[]:
                        fwr.write("def p_class_name(p):\n\t'''class_name : IDENTIFIER '''\n\tp[0]=p[1]")
                if list1!=[]:
                    S="def p_class_name(p):\n\t'''class_name : "
                    for i in list1:
                        if(i!=list1[len(list1)-1]):
                            S+=str(i)+"\n| "  
                        if(i==list1[len(list1)-1]):
                            S+=str(i)
                    
                    S+="'''\n\tp[0]=p[1]"   
    ##                print S
                    fwr.write("%s\n" % S)
                
            if "##---Hack4-----#" in sline:
                
                     S="def p_Type(p): \n\t'''Type : INT \n| BOOL \n| VOID \n| Type LSQR RSQR "
                     for i in list1:
                        S+= "\n| "+str(i)  
                     S+="'''\n\t"
                     S+="if p[1]=='int':p[0]=[['INT','int']]\n\telif p[1]=='bool':p[0]=[['BOOL','bool']]\n\telif p[1]=='void':p[0]=[['VOID','void']]\n\telif len(p) > 3:"
                     S+="\n\t\tp[0]=[]\n\t\tp[0].extend(p[1])\n\t\tp[0].append(['LSQR','['])\n\t\tp[0].append(['RSQR',']']) "
                    
                     for i in list1:
                        S+="\n\telif p[1]=='"+str(i)+"':p[0]=[['CLASSID','"+str(i)+"']]"
                     S+= "\n\telse:\n\t\tp[0] = p[1] " 

##                     print S
                     fwr.write("%s\n" % S)
                     
            if "##--Hack5-#" in sline:
                if list1==[]:
                    fwr.write("def p_NewObject(p):\n    '''NewObject : NEW IDENTIFIER LPAREN RPAREN'''\n    p[0] = ['IDENTIFIER',p[2]]")
                if list1!=[]:
                    S ="def p_NewObject(p): \n \t '''NewObject :"

                    for i in list1:
                            if(i!=list1[len(list1)-1]):
                                S+=" NEW "+ str(i) +" LPAREN RPAREN \n| "
                            if(i==list1[len(list1)-1]):
                                S+=" NEW "+ str(i) +" LPAREN RPAREN'''"
                    S+="\n \t p[0] = [['CLASS',p[2]],['NEW','new']]"+"#,['LPAREN','('],['RPAREN',')']] \n"
##                    print S
                    fwr.write("%s\n" % S)
            line = fnew.readline()
            
    fnew.close()
    fwr.close()




if __name__ == '__main__':
    
    try:
        filename = sys.argv[1]
        #filename = "example.proto"
        f = open(filename,'r')
        s=f.read()
    except EOFError:
        print "ERROR encountered while reading input file!!"
        quit()
    c = preprocess(s)
    f.close()
    hackit(c)
    
    #print "Done!!"
    from newproto import *
    main_main(filename,c)
