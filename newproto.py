'''

Created on April 20, 2013

@author: ameya

'''

import sys

import GC

import FCG

import ply.lex as lex

from liveness import*

from static_semantics import *





reserved = {

    'print' : 'PRINT',

    'input' : 'INPUT',

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

##Hack1----#

	'animal' :	'animal',
	'dog' :	'dog',


    

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









##--HACK2----#

def t_animal(t): 
 	r'animal'   
 	t.type = reserved.get(t.value,'animal') 
 	return t
def t_dog(t): 
 	r'dog'   
 	t.type = reserved.get(t.value,'dog') 
 	return t




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





s_table = {'true':['KEYWORD','bool','1', None],'false':['KEYWORD','bool','0', None],'void':['KEYWORD','void', None, None]}

c_table = {}

f_table = {}

cf_table= {}

#------------------------------------------------------------------

def insert_in_s_table(key,entity,key_type,initialise,dimension):

    global s_table

    if key not in s_table.keys():

        s_table[key]=[entity,key_type,initialise,dimension]

        #print "entry made ->",key,s_table[key]

    elif key == 'this':

        s_table[key] = [entity,key_type,initialise,dimension]



#------------------------------------------------------------------

import ply.yacc as yacc



precedence = (

    ('right', 'EQUALS'),

    ('left', 'LOR'),

    ('left', 'LAND'),

    ('nonassoc', 'EQ','NEQ','LT','LTEQ', 'GT','GTEQ'),

    ('left', 'MINUS', 'PLUS'),

    ('left', 'TIMES', 'SLASH', 'MOD'),

    ('nonassoc', 'NOT'),

    ('nonassoc', 'UMINUS')   

)





def p_Pgm(p):

    '''Pgm : Declstar '''

    p[0]=p[1]



def p_Declstar(p):

    '''Declstar : empty

                | Decl Declstar'''

    

    if len(p)>2:

        p[0]=[]

        p[0].extend(p[1])

        if p[2]!=None:

            p[0].extend(p[2])

    

    



def p_empty(p):

    'empty :'

    p[0]=None

    

def p_Decl(p):

    '''Decl : VarDecl

            | FunDecl

            | ClassDecl'''

    

    p[0] = []

    p[0].append(p[1])

    



def p_VarDecl(p):

    '''VarDecl : Type VarList SEMICOLON'''

    

    p[0]=[]

    p[0].extend(p[1])

    p[0].extend(p[2])

    p[0].append(['SEMICOLON',';'])

    





def p_FunDecl(p):

    '''FunDecl : Type Var LPAREN  FormalsQ RPAREN  Stmt'''



    p[0]=[]

    FunDecl_temp=[]

    argc=0

    p[0].extend([['FUNCTION',p[2][0][1]]])

    dim = 0

    if len(p[2])>1:

        dim=len(p[2])-1

        dim/=2

    FunDecl_temp.extend([['LPAREN','(']])

    if p[4]!=None:

        FunDecl_temp.extend(p[4])

        argc = len(p[4])/2

    FunDecl_temp.extend([['RPAREN',')']])

    p[0].append(FunDecl_temp)

    p[0].extend([p[6]])

    insert_in_s_table(p[2][0][1],"FUNCTION",p[1][0][1],argc,dim)

    

    





def p_ClassDecl(p):

    '''ClassDecl : CLASS class_name ExtendsQ LCURLY  MemberDeclstar RCURLY'''

    p[0]=[['CLASS','class']]

    p[0].extend([['CLASS',p[2]]])

    if p[3]!=None:

        p[0].extend(p[3])

    p[0].append(['LCURLY','{'])

    if p[5]!=None:

        p[0].extend([p[5]])

    p[0].append(['RCURLY','}'])

    

    

##--Hack3---#

def p_class_name(p):
	'''class_name : animal
| dog'''
	p[0]=p[1]
 



def p_ExtendsQ(p):

    '''ExtendsQ : empty

                | Extends'''

    p[0]=p[1]

    



def p_Extends(p):

    '''Extends : EXTENDS class_name'''



    p[0]=[['EXTENDS','extends'], ['CLASS',p[2]]]





def p_MemberDeclstar(p):

    '''MemberDeclstar : empty

                      | MemberDecl MemberDeclstar'''

    p[0]=[]

    if p[1]!= None:

        p[0]=[p[1]]

    if len(p)>2:

        if p[2]!=None:

            p[0].extend(p[2])

    

    



def p_MemberDecl(p):

    '''MemberDecl : VarDecl

                  | FunDecl'''

    if p[1]!=None:

        p[0]=p[1]

    

    

    

def p_FormalsQ(p):

    '''FormalsQ : empty

                | Formals'''

    p[0]=p[1]



    



def p_VarDeclstar(p):

    '''VarDeclstar : empty

                   | VarDecl VarDeclstar'''

    if len(p)>2:

        p[0]=[]

        p[0].append(p[1])

        if p[2]!=None:

            p[0].extend(p[2])



##---Hack4-----#

def p_Type(p): 
	'''Type : INT 
| BOOL 
| VOID 
| Type LSQR RSQR 
| animal
| dog'''
	if p[1]=='int':p[0]=[['INT','int']]
	elif p[1]=='bool':p[0]=[['BOOL','bool']]
	elif p[1]=='void':p[0]=[['VOID','void']]
	elif len(p) > 3:
		p[0]=[]
		p[0].extend(p[1])
		p[0].append(['LSQR','['])
		p[0].append(['RSQR',']']) 
	elif p[1]=='animal':p[0]=[['CLASSID','animal']]
	elif p[1]=='dog':p[0]=[['CLASSID','dog']]
	else:
		p[0] = p[1] 
            



def p_VarList(p):

    '''VarList : Var COMMA VarList

               | Var'''

    p[0]=[]

    p[0].extend(p[1])

    if len(p)>2:

        p[0].append(['COMMA',','])

        p[0].extend(p[3])





def p_Var(p):

    '''Var : IDENTIFIER Dimstar'''

    p[0]=[['IDENTIFIER',p[1]]]

    if p[2]!=None:

        p[0].extend(p[2])

        



def p_Formals(p):

    '''Formals : Type Var COMMA Formals

               | Type Var '''

    p[0]=[]

    p[0].extend(p[1])

    p[0].extend(p[2])    

    if len(p)>3:

        p[0].extend(p[4])



        





def p_Stmtstar(p):

    '''Stmtstar : empty

                | Stmt Stmtstar'''

    if len(p)>2:

        p[0]=[]

        p[0].append(p[1])

        if p[2]!=None:

            p[0].extend(p[2])

    

    

def p_Stmt(p):

    '''Stmt : SE SEMICOLON

            | Print

            | Block

            | If

            | While

            | for

            | Do_while

            | Return '''

    p[0]=p[1]





def p_SE(p):

    '''SE : Assign

          | MethodCall '''

    p[0]=p[1]



    

def p_Assign(p):

    ''' Assign : Lhs EQUALS AE

                | Lhs Inc

                | Lhs Dec

                | Inc Lhs

                | Dec Lhs'''

    

    p[0]=[]

    if p[1]==['DEC','--']:

        p[0].extend(p[2])

        p[0].extend([['PDEC','--']])

    elif p[1]==['INC','++']:

        p[0].extend(p[2])

        p[0].extend([['PINC','++']])

    else:

        p[0].extend(p[1])

        if p[2]=='=':

            p[0].extend(p[3])

            p[0].extend([['EQUALS','=']])

        elif p[2]==['INC','++']:p[0].extend([['POINC','++']])

        elif p[2]==['DEC','--']:p[0].extend([['PODEC','--']])

    



def p_Dec(p):

    'Dec : DEC'

    p[0]=['DEC','--']



def p_Inc(p):

    'Inc : INC'

    p[0]=['INC','++']



def p_print(p):

    '''Print : PRINT LPAREN AE RPAREN SEMICOLON'''

    p[0]=[]

    p[0].extend(p[3])

    p[0].extend([['PRINT',p[1]]])





def p_Block(p):

    ''' Block : LCURLY VarDeclstar Stmtstar RCURLY'''    

    p[0]=[['LCURLY','{']]

    if p[2]!=None:

        p[0].extend(p[2])

    if p[3]!=None:

        p[0].extend(p[3])

    p[0].extend([['RCURLY','}']])





def p_If(p):

    ''' If : IF AE THEN Stmt

            | IF AE THEN Stmt ELSE Stmt'''

    p[0]=[['IF','if']]

    p[0].append(p[2])

    p[0].extend([['THEN','then']])

    if(len(p)<6):

        p[0].append(p[4])

    else:

        p[0].append(p[4])

        p[0].extend([['ELSE','else']])

        p[0].append(p[6])



def p_While(p):

    ''' While : WHILE AE DO Stmt'''

    p[0]=[['WHILE','while']]

    p[0].append(p[2])

    p[0].extend([['DO','do']])

    p[0].append(p[4])



def p_Do_while(p):

    ''' Do_while : DO Stmt WHILE AE SEMICOLON'''

    p[0]=[['DO','do']]

    p[0].append(p[2])

    p[0].extend([['DOWHILE','dowhile']])

    p[0].append(p[4])

    

def p_for(p):

    '''for : FOR LPAREN SEQ SEMICOLON AEQ SEMICOLON SEQ RPAREN Stmt'''

    p[0]=[['FOR','for']]

    p[0].append(p[3])

    p[0].append(p[5])

    p[0].append(p[7])

    p[0].append(p[9])





def p_SEQ(p):

    '''SEQ : empty

           | SE'''

    p[0]=p[1]





def p_AEQ(p):

    '''AEQ : empty

           | AE'''

    p[0]=p[1]



    

def p_Return(p):

    '''Return : RETURN AEQ SEMICOLON'''

    p[0] = [['RETURN','return']]        

    if p[2]!=None:

        p[0].extend(p[2])

    else:

        p[0].extend([['VOID','void']])

    



def p_Lhs(p):

    '''Lhs : FieldAccess

            | ArrayAccess'''

    p[0]=p[1]



def p_AE_BinOp(p):

    ''' AE : AE TIMES AE

            | AE SLASH AE

            | AE PLUS AE

            | AE MINUS AE

            | AE LT AE

            | AE EQ AE

            | AE GT AE

            | AE GTEQ AE

            | AE LTEQ AE

            | AE NEQ AE

            | AE LAND AE

            | AE LOR AE

            | AE MOD AE '''



    p[0]=[]

    p[0].extend(p[1])

    p[0].extend(p[3])

    if p[2]=='*':

        p[0].extend([['TIMES','*']])

    elif p[2]=='/':

        p[0].extend([['SLASH','/']])

    elif p[2]=='+':

        p[0].extend([['PLUS','+']])

    elif p[2]=='-':

        p[0].extend([['MINUS','-']])

    elif p[2]=='%':

        p[0].extend([['MOD','%']])



    elif p[2]=='<':

        p[0].extend([['LT','<']])

    elif p[2]=='==':

        p[0].extend([['EQ','==']])

    elif p[2]=='>':

        p[0].extend([['GT','>']])

    elif p[2]=='>=':

        p[0].extend([['GTEQ','>=']])

    elif p[2]=='<=':

        p[0].extend([['LTEQ','<=']])

    elif p[2]=='!=':

        p[0].extend([['NEQ','!=']])

    elif p[2]=='&&':

        p[0].extend([['LAND','&&']])

    elif p[2]=='||':

        p[0].extend([['LOR','||']])







def p_AE_UnOp(p):

    ''' AE : MINUS AE %prec UMINUS'''

    p[0]=[]

    p[0].extend(p[2])

    p[0].extend([['UMINUS','-']])

        

def p_AE_NT(p):

    '''AE : NOT AE''' 

    p[0]=p[2]

    p[0].extend([['NOT','!']])



def p_AE(p):

    '''AE : Primary

          | SE

          | NewArray'''

    p[0]=p[1]

    

   

def p_Primary(p):

    '''Primary : intconst

               | true

               | false

               | this

               | super

               | Input

               | LPAREN AE RPAREN

               | FieldAccess

               | ArrayAccess

               | NewObject '''

      #         | MethodCall



    if len(p)<3:

        p[0]=p[1]

    else:

        p[0]=p[2]



def p_intconst(p):

    '''intconst : NUMBER'''

    p[0]=[['NUMBER',p[1]]]



def p_true(p):

    '''true : TRUE'''

    p[0]=[['TRUE','true']]



def p_false(p):

    '''false : FALSE'''

    p[0]=[['FALSE','false']]



def p_this(p):

    '''this : THIS'''

    p[0]=[['THIS','this']]



def p_super(p):

    '''super : SUPER'''

    p[0]=[['SUPER','super']]



    

def p_Input(p):

    ''' Input : INPUT LPAREN RPAREN'''

    p[0]=[['INPUT','input']]

        

     

def p_ArrayAccess(p):

    '''ArrayAccess : Primary LSQR AE RSQR '''

    p[0]=p[1]

    p[0].extend([['LSQR','[']])

    p[0].extend(p[3])

    p[0].extend([['RSQR',']']])



def p_FieldAccess(p):

    '''FieldAccess : Primary DOT IDENTIFIER

                   | IDENTIFIER '''

    

    if len(p)>2:

        p[0]=[]

        p[0].extend(p[1])

        p[0].extend([['IDENTIFIER',p[3]]])

        p[0].extend([['DOT','.']])

        

    else:

        p[0]=[['IDENTIFIER',p[1]]]





def p_MethodCall(p):

    '''MethodCall : FieldAccess LPAREN ArgsQ RPAREN '''

    p[0]=[]

    p[0].extend(p[1])

    #print ";;",p[0]

    #p[0].append(['LPAREN','('])

    

    #if p[3]!=None:

    #    p[0].extend(p[3])

    #p[0].extend([['RPAREN',')']])

    

    temp=[]

    temp.append(['LPAREN','('])

    

    if p[3]!=None:

        temp.extend(p[3])

    temp.extend([['RPAREN',')']])

    if p[0][-1]==['DOT', '.']:

        p[0].pop()

        p[0].append(['MDOT', '..'])

        p[0].extend(temp)

    else:

        p[0].extend(temp)



    

    

def p_ArgsQ(p):

    '''ArgsQ : empty

           | Args'''

    if len(p)>1:

        p[0]=p[1]



        

def p_Args(p):

    '''Args : AE COMMA Args

            | AE '''

    p[0]=[p[1]]

    if len(p)>2:

        #p[0].extend([['COMMA',',']])

        p[0].extend(p[3])



##--Hack5-#

def p_NewObject(p): 
 	 '''NewObject : NEW animal LPAREN RPAREN 
|  NEW dog LPAREN RPAREN'''
 	 p[0] = [['CLASS',p[2]],['NEW','new']]#,['LPAREN','('],['RPAREN',')']] 





    

def p_NewArray(p):

    ''' NewArray : NEW Type DimExpr Dimstar'''

    p[0]=[]

##    if p[4]!=None:

##        p[0].extend(p[4])

    p[0].extend(p[3])

    p[0].extend(p[2])

    p[0].extend([['NEW','new']])

    



def p_DimExpr(p):

    '''DimExpr : LSQR AE RSQR'''

    p[0]=[]

    p[0].extend(p[2])





def p_Dimstar(p):

    '''Dimstar : empty

               | Dim Dimstar'''

    if len(p)>2:

        p[0]=[]

        p[0].extend(p[1])

        if p[2]!=None:

            p[0].extend(p[2])



        

def p_Dim(p):

    '''Dim : LSQR RSQR '''

    p[0] = [['LSQR','['],['RSQR',']']]





def p_error(p):

    if p:

        print "Syntax error at \'",p.value ,"\' @ line No: ", p.lineno-1  

    else:

        print("Syntax error at EOF") 

    quit()







#------------------------------------------------------------------

#..................................................................

#..............Static SEMANTIC ANALYSIS of Program.................

#..................................................................

def def_use(pgm):

    #print pgm,'\n'

    if pgm[-1]==['EQUALS', '=']: # stmt has two parts,

        lhs = pgm[0]

        if pgm[-2] == ['EQUALS', '=']:

            defined.append(lhs)

            def_use(pgm[1:-1:])

            lhs=[]

            rhs=[]

        else:

            rhs = pgm[1:-1:]

    elif pgm[-1]==['PRINT', 'print']:

        lhs = []

        rhs = pgm[0:-1:]

    elif pgm[0]==['IF', 'if']:

        # if stmt

        lhs = []

        rhs = pgm[1][::]

    elif pgm[0]==['WHILE', 'while']:

        # while stmt

        lhs = []

        rhs = pgm[1][::]

    elif pgm[-1][1] in ['<','<=','>','>=','==','!=','&&','||','--','++']:

        lhs = []

        rhs = pgm[0:-1:]

    else:

        lhs=[]

        rhs=[]

    for x in rhs:

        if x[0]=='IDENTIFIER' and x not in defined:

            usebefore.append(x)

        defined.append(lhs)



#-----------------------------------------------------------------------------

#---------------Lexical Scope ----------------------------------------------!

#---------------------------------------------------------------------------------



def lexical_scope(astcode):

        line=0

        blockstack=[]

        variablestack=['LCURLY']

        curly_block_set=set()

        symbol_table={}

        var=[]

        temp=0

        block_track=0

        astcode.insert(0,[['LCURLY', '{']])

        astcode.insert(len(astcode)+1,[['RCURLY', '}']])

        curly_block_list=[]

        declared=[]

        for x,i in enumerate(astcode):

            line+=1

            if i[0][0]=='LCURLY':

                block_track+=1

                blockstack.append(line)

                variablestack.append(i[0][0])

            if i[0][0]=='RCURLY':

               lcurl=blockstack.pop()

               rcurl=line   

               curly_block_set=lcurl,rcurl,block_track

               

               if temp!='LCURLY':

                  while (1):

                       temp=variablestack.pop()

                       if(temp=='LCURLY'):

                            break

                       for i in astcode[lcurl:rcurl]:

                          for j in i:

                             

                             if isinstance(j[0],list):

                                 for m in j[0]:  

                                     if m ==temp:

                                        m=str(block_track)+'_'+m

                             

                             else:

                                if  j[0]=='IDENTIFIER' and j[1] == temp:

                                    j[1]=str(block_track)+'_'+j[1]

                                    

                             

                       for i in astcode[lcurl:rcurl+1]:

                          if i[0][0] in ['IF','DOWHILE','FOR','WHILE']:

                                if i[1][0][0]=='IDENTIFIER' and i[1][0][1]==temp:

                                     i[1][0][1]=str(block_track)+'_'+i[1][0][1]

                                     



                        

               block_track-=1

               var=[]

               temp=0

            if i[0][0] in ['INT','BOOL']:

                for j in i:

                    if j[0]=='IDENTIFIER':

                        

                        variablestack.append(j[1])

                        declared.append(j[1])           

        



#-------Used before declaration -----------------#





        for i in astcode:

            

            if i[0][0] in ['INT','BOOL']:

                for j in i:

                    if j[0]=='IDENTIFIER':

                        variablestack.append(j[1])

                        declared.append(j[1])

            else:

                for j  in i:

                    if j[0]=='IDENTIFIER' and j[1] not in ['T0']:

                        if j[1] not in declared:

                            print "Error: Used before declared identifier =",j[1]

                            quit()

    



   

#------------------------------------------------------------------

astcode=[]

index=0

defined=[]

usebefore=[]

labelc=0

f_name=''

def AST(pmg):

    global labelc, f_name

    #print "\n>>",pmg

    for i in pmg:

        #print "\n-|-",i

        if i[0]==['LCURLY', '{']:

            astcode.append([['LCURLY', '{']])

            AST(i[1:-1:])

            astcode.append([['RCURLY', '}']])

        elif i[0]==['WHILE', 'while']:

            lx,ly='label'+str(labelc),'label'+str(labelc+1)

            labelc+=2

            astcode.append([['LABEL', lx]])

            temp=[]

            temp.extend(i[0:3:])

            astcode.append(temp)

            def_use(temp)

            astcode.append([['JIFF','jfalse'],['LABEL',ly],['IDENTIFIER','506'],['NOP','None']])#

            temp=[[]]

            temp[0].extend(i[3])

            AST(temp)

            astcode.append([['JUMP','j'], ['LABEL',lx], ['NOP','None'],['NOP','None']])

            astcode.append([['LABEL', ly]])

            

        elif i[0]==['IF', 'if']:

            if(len(i)>4):

                lx,ly='label'+str(labelc),'label'+str(labelc+1)

                labelc+=2

            else:

                lx='label'+str(labelc)

                labelc+=1

            temp=[]

            temp.extend(i[0:3:])

            astcode.append(temp)

            def_use(temp)

            astcode.append([['JIFF','jfalse'],['LABEL',lx],['IDENTIFIER','506'],['NOP','None']])

            temp=[[]]

            temp[0].extend(i[3])

            AST(temp)

            if(len(i)>4):

                astcode.append([['JUMP','j'], ['LABEL',ly], ['NOP','None'],['NOP','None']])

                astcode.append([['LABEL', lx]])

                temp=[[]]

                temp[0].extend(i[5])

                AST(temp)

                astcode.append([['LABEL', ly]])

            else:

                astcode.append([['LABEL', lx]])

            

        elif i[0]==['DO', 'do']:

            lx='label'+str(labelc)

            labelc+=1

            astcode.append([['DO', 'do']])

            astcode.append([['LABEL', lx]])

            temp=[[]]

            temp[0].extend(i[1])

            AST(temp)

            temp=[]

            temp.extend(i[2:4:])

            astcode.append(temp)

            def_use(temp)

            astcode.append([['JIFT','jtrue'],['LABEL',lx],['IDENTIFIER','506'],['NOP','None']])

            

        elif i[0]==['FOR', 'for']:

            lx,ly='label'+str(labelc),'label'+str(labelc+1)

            labelc+=2

            if i[1]!=None:

                astcode.append(i[1])

                def_use(i[1])

            astcode.append([['LABEL', lx]])

            if i[2]==None:

                i[2]=['TRUE','true']

            astcode.append([['FOR', 'for'],i[2]])

            if i[1]!=None:def_use(i[2])

            astcode.append([['JIFF','jfalse'],['LABEL',ly],['IDENTIFIER','506'],['NOP','None']])

            AST([i[4]])

            if i[1]!=None:

                astcode.append(i[3])

                def_use(i[3])

            astcode.append([['JUMP','j'], ['LABEL',lx], ['NOP','None'],['NOP','None']])

            astcode.append([['LABEL', ly]])



        elif i[0][0] in ['FUNCTION']:

            f_name = i[0][1]

            astcode.append([['FUNCTION', i[0][1]]])

            astcode.append(i[1])

            AST([i[2]])



        elif i[0][0]=='CLASS':

            astcode.append(i)

            

        else:

            if i[0][0]=='RETURN':

                i[0][1]= f_name

            astcode.append(i)

            def_use(i)



#--------------------------------------------------------------------------

#.....................Intermediate Code Generation.........................

#..........................................................................

USE=[]

DEF=[]

counter=0

dummyc=0

imcode=[]

arrayt={}



def get_dim(function):

    global s_table

    if function[1] in s_table.keys():

        return s_table[function[1]][3]

    else:

        print "Function not found.."

        quit()



def get_type(oper1,oper2):

    global s_table

    keys = s_table.keys()

    

    #print "searching for :",oper1[1],',',oper2[1]," in ",keys

    ty1,ty2= '',''

    

    o=oper1[1]

    if oper1[0]=='NUMBER':ty1='NUMBER'

    elif o in keys: ty1=s_table[o][1]

    else:

        print  "Type error: variable used before declared.."

        quit()

        

        

    o=oper2[1]

    if oper2[0]=='NUMBER':ty2='NUMBER'

    elif o in keys: ty2=s_table[o][1]

    else:

        print "Typr error: Variable used before declared.."

        quit()

    return ty1,ty2



def typecheck_return_value(fname,return_v):

    type1,type2 = get_type(['FUNCTION',fname],return_v)

    if type1 == 'int':

        if type2 not in ['int','NUMBER']:

            print "Type error: Return type mismatch- '",fname ,"'"

            quit()

    elif type1 != type2:

        print "Type error: Return type mismatch- '",fname, "'"

        quit()



    



def check_argc_sent_received(fname,argc):

##    key = s_table.keys()

##    for i in key :

##        print "%-15s %-15s %-10s %-10s" % (i,s_table[i][0],s_table[i][1],s_table[i][2])

    if fname[1] in s_table.keys():

        if argc == s_table[fname[1]][2]:

            pass

        else:

            print "'",fname[1],"' :Function takes ",s_table[fname[1]][2]," arguments, sent ",argc

            quit()

    else:

        print "'",fname[1],"' : Function NOT defined.."

        quit()

        

def assignment_typecheck(oper1,oper2):

    type1,type2 = get_type(oper1,oper2)

    if type1 == 'int' and type2 in ['int','NUMBER']:

        return 'int'

    elif type1 == 'bool' and type2 == 'bool':

        return 'bool'

    elif type1 ==  type2 :

        return type1

    else:

        print "Type Error: Invalid Assignment.."

        quit()







def arithmetic_typecheck(oper1,oper2):

    #print "-------------",oper1,oper2

    type1,type2 = get_type(oper1,oper2)

    

    #print "------->><<------",type1, type2

    if type1 in ['int','NUMBER'] and type2 in ['int','NUMBER']:

        return 'int'

    else:

        print "Type Error: Invalid use of arithmetic operation"

        quit()





def typecheck(oper1,oper2,op):

    type1,type2 = get_type(oper1,oper2)

    if op in ['&&','||']:

        if type1 == type2 == 'bool': return 'bool'

        else:

            print "Type Error: Invalid Logical operation"

            quit()

    elif op in ['<','<=','>','>=']:

        if type1 in ['int','NUMBER'] and type2 in ['int','NUMBER']: return 'bool'

        else:

            print "Type Error: Invalid use of Comparison operation"

            quit()

    elif op in ['!=','==']:

        if (type1 in ['int','NUMBER'] and type2 in ['int','NUMBER']) or (type1 == type2 == 'bool') : return 'bool'

        else:

            print "Type Error: Invalid Equality operation"

            quit()



def Address_to_Value(adr):

    type1,type2 = get_type(adr,['NUMBER','1'])    

    global counter

    tv='T'+str(counter)

    counter+=1

    insert_in_s_table(tv,'IDENTIFIER',type1,None,None)

    

    if adr[1] in arrayt.keys():

        adr[0]='ADDRESS'

    imcode.append([['IDENTIFIER',tv],['NOP','None'],['LW','load'],adr])

    return ['IDENTIFIER',tv]



    

def IN():

    global counter

    tv='T'+str(counter)

    counter+=1

    insert_in_s_table(tv,'IDENTIFIER','int',None,None)

    

    imcode.append([['IDENTIFIER',tv],['NOP','None'],['INPUT','input'],['NOP','None']])

    return ['IDENTIFIER',tv]





def PRINT(f1):

    type1,type2 = get_type(f1,['NUMBER','1'])

    if type1 not in ['int','NUMBER']:

        print "Typr Error: Invalid Print operation"

        quit()

    if f1[0]=='ADDRESS' or f1[1] in arrayt.keys():

        f1=Address_to_Value(f1)   

    imcode.append([['NOP','None'],f1,['PRINT','print'],['NOP','None']])

    return f1





def ASS(f1, f2):

    ty=assignment_typecheck(f1, f2)

    #if type1 == type2

    if f2[0]=='ADDRESS' or f2[1] in arrayt.keys():

        f2=Address_to_Value(f2)

    if f1[0]=='ADDRESS' or f1[1] in arrayt.keys():

        imcode.append([['NOP','None'],f2,['SW','store'],f1])

    else:

        if f2 == ['TRUE','true']: f2 = ['NUMBER',1]

        elif f2 == ['FALSE','false']: f2 = ['NUMBER',0]

        imcode.append([f1,f2,['NOP','None'],['NOP','None']])

    return f2



def BinOP(op1, op2 ,bop):

    global counter

    tv='T'+str(counter)

    counter+=1

    ty=arithmetic_typecheck(op1, op2)

    insert_in_s_table(tv,'IDENTIFIER',ty,None,None)

    

    

    if op1[0]=='ADDRESS'or op1[1] in arrayt.keys():

        op1=Address_to_Value(op1)

    if op2[0]=='ADDRESS'or op2[1] in arrayt.keys():

        op2=Address_to_Value(op2)

        

    imcode.append([['IDENTIFIER',tv],op1,bop,op2])    

    return ['IDENTIFIER',tv]





def ConOP(op1, op2 ,cop):

    global counter

    tv='T'+str(counter)

    counter+=1

    ty = typecheck(op1,op2,cop[1])

    insert_in_s_table(tv,'IDENTIFIER',ty,None,None)

    

    if op1[0]=='ADDRESS'or op1[1] in arrayt.keys():

        op1=Address_to_Value(op1)

    if op2[0]=='ADDRESS'or op2[1] in arrayt.keys():

        op2=Address_to_Value(op2)



    imcode.append([['IDENTIFIER',tv],op1,cop,op2])

    

    return ['IDENTIFIER',tv]



def NOT(op1):

    global counter

    tv='T'+str(counter)

    counter+=1

    if op1[0] != 'NUMBER':

        type1,type2 = get_type(op1,['NUMBER','1'])

        if type1 != 'bool':

            print "Type Error: Invalid NOT operation"

            quit()

    else:

        print "Type Error: Invalid NOT operation"

        quit()



    if op1[0]=='ADDRESS'or op1[1] in arrayt.keys():

        op1=Address_to_Value(op1)

    

    imcode.append([['IDENTIFIER',tv],op1,['NOT','!'],['NOP','None']])

    insert_in_s_table(tv,'IDENTIFIER',type1,None,None)

    

    return ['IDENTIFIER',tv]





def CALL(function):

    global counter

    tv='T'+str(counter)

    counter+=1

    type1,type2 = get_type(function,['NUMBER','1'])

    d = get_dim(function)

    insert_in_s_table(tv,'IDENTIFIER',type1,None,d)

    imcode.append([['JAL','jal'],['FNAME',function[1]],['NOP','None'],['NOP','None']])

    imcode.append([['RECEIVE','receive'],['IDENTIFIER',tv],['NOP','None'],['NOP','None']])

    return ['IDENTIFIER',tv]





def INC(op1):

    type1,type2 = get_type(op1,['NUMBER','1'])

    if type1 != 'int':

        print "Type Error: Invalid Pre-Increment operation"

        quit()

        

    if op1[0]=='ADDRESS'or op1[0] in arrayt.keys():

        op2=Address_to_Value(op1)

        imcode.append([op2,op2,['PLUS','+'],['NUMBER','1']])

        imcode.append([['NOP','None'],op2,['SW','store'],op1])

        return op2

    else:

        imcode.append([op1,op1,['PLUS','+'],['NUMBER','1']])

        return op1



def POINC(op1):

    type1,type2 = get_type(op1,['NUMBER','1'])

    if type1 != 'int':

        print "Type Error: Invalid Post-Increment operation"

        quit()

        

    global dummyc

    dummy=['IDENTIFIER','temp_'+op1[1]+str(dummyc)]

    dummyc+=1

    

    insert_in_s_table(dummy[1],'IDENTIFIER',type1,None,None)

    

    if op1[0]=='ADDRESS' or op1[1] in arrayt.keys():

        op2=Address_to_Value(op1)

        imcode.append([dummy,op2,['NOP','None'],['NOP','None']])

        imcode.append([op2,op2,['PLUS','+'],['NUMBER','1']])

        imcode.append([['NOP','None'],op2,['SW','store'],op1])

    else:

        imcode.append([dummy,op1,['NOP','None'],['NOP','None']])

        imcode.append([op1,op1,['PLUS','+'],['NUMBER','1']])

    return dummy



def DEC(op1):

    type1,type2 = get_type(op1,['NUMBER','1'])

    if type1 != 'int':

        print "Type Error: Invalid Pre-Decrement operation"

        quit()

        

    if op1[0]=='ADDRESS' or op1[1] in arrayt.keys():

        op2=Address_to_Value(op1)

        imcode.append([op2,op2,['MINUS','-'],['NUMBER','1']])

        imcode.append([['NOP','None'],op2,['SW','store'],op1])

        return op2

    else:

        imcode.append([op1,op1,['MINUS','-'],['NUMBER','1']])

        return op1



def PODEC(op1):

    type1,type2 = get_type(op1,['NUMBER','1'])

    if type1 != 'int':

        print "Type Error: Invalid Post-Decrement operation"

        quit()

        

    global dummyc

    dummy=['IDENTIFIER','temp_'+op1[1]+str(dummyc)]

    dummyc+=1

    insert_in_s_table(dummy[1],'IDENTIFIER',type1,None,None)

    

    if op1[0]=='ADDRESS' or op1[1] in arrayt.keys():

        op2=Address_to_Value(op1)

        imcode.append([dummy,op2,['NOP','None'],['NOP','None']])

        imcode.append([op2,op2,['MINUS','-'],['NUMBER','1']])

        imcode.append([['NOP','None'],op2,['SW','store'],op1])

    else:

        imcode.append([dummy,op1,['NOP','None'],['NOP','None']])

        imcode.append([op1,op1,['MINUS','-'],['NUMBER','1']])

    return dummy



def check_bound(index,base):

    type1,type2 = get_type(index,base)

    if type1 not in ['int','NUMBER']:

        print "Type Error: Array index is non-numeric value.."

        quit()

    global counter

    if index[0]=='NUMBER':

        tv='T'+str(counter)

        counter+=1

        imcode.append([['IDENTIFIER',tv],index,['NOP','None'],['NOP','None']])

        index=['IDENTIFIER',tv]

    tv2='T'+str(counter)

    counter+=1

    arraysize=['IDENTIFIER',tv2]

    if base[0]=='ADDRESS':

        base=Address_to_Value(base)

    imcode.append([arraysize,['NOP','None'],['LW','load'],['ADDRESS',base[1]]])

    imcode.append([['JIFLE','ble'],arraysize,index,['INDXERROR','indexerror']])

    imcode.append([['JIFLTZ','bltz'],index,['NOP','None'],['INDXERROR','indexerror']])

    



def INDEX(op1,op2):

    global counter

    tv='T'+str(counter)

    counter+=1

    if op1[0]=='ADDRESS' or op1[1] in arrayt.keys():

        op1=Address_to_Value(op1)

    check_bound(op1,op2)

    imcode.append([['IDENTIFIER',tv],op1,['PLUS','+'],['NUMBER',1]])      

    imcode.append([['IDENTIFIER',tv],['IDENTIFIER',tv],['TIMES','*'],['NUMBER',4]])

    tv2='T'+str(counter)

    counter+=1

    if op2[0]=='ADDRESS':

        op2=Address_to_Value(op2)

    imcode.append([['IDENTIFIER',tv2],op2,['PLUS','+'],['IDENTIFIER',tv]])

    type1,type2 = get_type(op1,op2)

    insert_in_s_table(tv2,'INDENTIFIER',type2,None,None)

    return ['ADDRESS',tv2]





def ALLOCK(typeinfo,size,base):

    global counter

    tv='T'+str(counter)

    counter+=1

    if size[0]=='ADDRESS' or size[1]in arrayt.keys():

        size=Address_to_Value(size)

    

    imcode.append([['IDENTIFIER',tv],size,['PLUS','+'],['NUMBER',1]])   # for storing size

    newsize=['IDENTIFIER',tv]

    if base[0] == 'ADDRESS':   # for multi D array

        tv2='T'+str(counter)

        counter+=1

        imcode.append([['IDENTIFIER',tv2],typeinfo,['ALLOCATE','allocate'],newsize])

        imcode.append([['NOP','None'],['IDENTIFIER',tv2],['SW','store'],base])

        imcode.append([['NOP','None'],size,['SW','store'],['ADDRESS',tv2]])

    else:

        imcode.append([base,typeinfo,['ALLOCATE','allocate'],newsize])

        imcode.append([['NOP','None'],size,['SW','store'],['ADDRESS',base[1]]])

    return ['NUMBER',1]





def ARGUMENT_receive(argv):

    argc = (len(argv)/2)

    argc-=1

    while argc>-1:

        insert_in_s_table(argv[argc*2+1][1],argv[argc*2+1][0],argv[argc*2][1],None, None)

        imcode.append([argv[argc*2+1],['NOP','None'],['ARGC',argc],['ARGUMENT','argument']])

        argc-=1

    return None



def ARGUMENT_send(argv):

    argc = len(argv)

    

    i=0

    while i < argc:

        imcode.append([['NOP','None'],argv[i],['ARGC',i],['PARAMETER','parameter']])

        i+=1

    return None



def make_record(classname,fields,superclass):

    global c_table,cf_table

    superfield = []

    if superclass!=[]:

        if superclass[1] in c_table.keys():

            superfield.extend(c_table[superclass[1]])

            

    field = []

    for l in fields:

        if l[0][0]=='FUNCTION':

            global f_table

            f_table[l[0][1]]=classname[1]

            

            if classname[1] in c_table.keys():

                c_table[classname[1]].append(l[0][1])

            gencode([l[0]])

            insert_in_s_table('this','OBJECT',classname[1],None,None)

            imcode.append([['RECEIVEOBJ','receiveobj'],['IDENTIFIER','this'],['NOP', 'None'], ['NOP', 'None']])

            allfields = c_table[classname[1]]

            class_gencode(l[1],allfields,superclass)

            if l[2][0]==['LCURLY', '{']:

                for s in l[2]:

                    if s not in [['LCURLY', '{'],['RCURLY', '}']]:

                        if s[0]==['RETURN','return']:

                            s[0][1]=l[0][1]

                        class_gencode(s,allfields,superclass)

                        

            else:

                class_gencode(l[2],allfields,superclass)

        else:            

##            field=[]

##            for i in range(1,len(l)):

##                if l[i] not in [['COMMA', ','],['SEMICOLON', ';']]:

##                    field.append(l[i])

##            

##            if classname[1] in c_table.keys():

##                for i in field:

##                    c_table[classname[1]].append(i[1])

##                    insert_in_s_table(i[1],'IDENTIFIER',l[0][1],None,None)

##                c_table[classname[1]].extend(superfield)

##            else:

##                print classname,"error"

            if classname[1] not in cf_table.keys():

                cf_table[classname[1]]=0

            

            vard=[]

            for i in range(1,len(l)):

                if l[i] not in [['COMMA', ','],['SEMICOLON', ';']]:

                    vard.append(l[i])

                else:

                    if len(vard)>1:

                        if vard[1]==['LSQR','[']:

                            insert_in_s_table(vard[0][1],'ARRAY',l[0][1],None,(len(vard)-1)/2)

                            arrayt[vard[0][1]]=None

                            c_table[classname[1]].append(vard[0][1])

                            cf_table[classname[1]]+=1

                    else:

                        c_table[classname[1]].append(vard[0][1])

                        insert_in_s_table(vard[0][1],'IDENTIFIER',l[0][1],None,None)

                        cf_table[classname[1]]+=1

                    vard=[]

            c_table[classname[1]].extend(superfield)

    

    

def ALLOCK_OBJECT(classname):

    global c_table

    global counter

    if classname in c_table.keys():

        size = len(c_table[classname])

        tv='T'+str(counter)

        counter+=1

        imcode.append([['IDENTIFIER',tv],['NOP','None'],['ALLOCATE','allocate'],['NUMBER',size]])

        insert_in_s_table(tv,'OBJECT',classname,None,None)

        return ['IDENTIFIER',tv]

    else:

        print "Classname Not found"





def field_access(field,obj):

    cname=''

    fields=[]

    global c_table

    if obj[1] in s_table.keys():

        cname = s_table[obj[1]][1]

    else:

        print obj[1],"not found in symbol table"

        quit()

    if cname in c_table.keys():

        fields = c_table[cname]

    else:

        print cname,"class name not fould"

        quit()

    if field[1] in fields:

        global counter

        tv='T'+str(counter)

        counter+=1

        ind = fields.index(field[1]) * 4

        imcode.append([['IDENTIFIER',tv],obj,['PLUS','+'],['NUMBER',ind]])

        type1,type2 = get_type(field,['NUMBER',1])

        insert_in_s_table(tv,'INDENTIFIER',type1,None,None)

        return ['ADDRESS',tv]



    else:

        print "Not wel formed: Invalid field access.."

        quit()

        

def adjustobj(obj,fcount):

    if fcount < 1:

        return obj

    fcount = fcount * 4

    global counter

    tv='T'+str(counter)

    counter+=1

    imcode.append([['IDENTIFIER',tv],obj,['PLUS','+'],['NUMBER',fcount]])

    return ['IDENTIFIER',tv] 



    

        

stackk =[]

def gencode(l):

    #global counter

    global DEF,USE

    global stackk

    global arrayt,f_table,cf_table

    #counter =0

    stack = []

    error = False



    #print "->",l

    try:

        if l==None:return None

        elif l[0][0] in ['WHILE','IF','DOWHILE','FOR']:

            if l[1]==None:stackk.append(['NUMBER','1'])

            else:

                stackk.append(gencode(l[1]))

            return None

        elif l[0][0] in ['LCURLY','RCURLY','DO','FOR']:

            return None

        elif l[0][0] in ['LPAREN']:

            if len(l)>2:            # function with argument

                ARGUMENT_receive(l[1:-1])

            imcode.append([['SAVE_RA','save_ra'],['NOP','None'],['NOP','None'],['NOP','None']])

            return None

        elif l[0][0] == 'JUMP':

            imcode.append(l)

            return None

        elif l[0][0] == 'LABEL':

            imcode.append([['LABEL',l[0][1]], ['NOP', 'None'], ['NOP', 'None'], ['NOP', 'None']])

            return None

        elif l[0][0] =='FUNCTION':

            imcode.append([['LABEL',l[0][1]], ['FUNCTION','function'], ['NOP', 'None'], ['NOP', 'None']])

            return None

        

        elif l[0][0] in ['INT','BOOL']:      # Variable decleration

            vard=[]

            for i in range(1,len(l)):

                if l[i] not in [['COMMA', ','],['SEMICOLON', ';']]:

                    vard.append(l[i])

                else:

                    #imcode.append([l[0],vard[0],['DIM',(len(vard)-1)/2],['NOP','None']])

                    if len(vard)>1:

                        if vard[1]==['LSQR','[']:

                            insert_in_s_table(vard[0][1],'ARRAY',l[0][1],None,(len(vard)-1)/2)

                            arrayt[vard[0][1]]=None

                    else:

                        insert_in_s_table(vard[0][1],'IDENTIFIER',l[0][1],None,None)

                    vard=[]

            return None

        

        elif l[0][0] == 'CLASSID':               

            vard=[]

            for i in range(1,len(l)):

                if l[i] not in [['COMMA', ','],['SEMICOLON', ';']]:

                    vard.append(l[i])

                else:

                    if len(vard)>1:

                        if vard[1]==['LSQR','[']:

                            insert_in_s_table(vard[0][1],'ARRAY',l[0][1],None,(len(vard)-1)/2)

                            arrayt[vard[0][1]]=None

                    else:

                        insert_in_s_table(vard[0][1],'OBJECT',l[0][1],None,None)

                    vard=[]

            return None

        

        elif l[0][0] in ['JIFT','JIFF']:

            l[2]=stackk.pop()

            if l[2][0]=='ADDRESS' or l[2][1] in arrayt.keys():

                op=Address_to_Value(l[2])

                l[2]=op

            type1,type2= get_type(l[2],['NUMBER',1])

            

            if type1 != 'bool':

                print "Type Error: Invalid conditon.."

                quit()

            imcode.append(l)

            return None

        elif l[0][0] == 'RETURN':

            if l[1] == ['VOID', 'void']:

                ret_v = ['NUMBER',1]

                typecheck_return_value(l[0][1],l[1])

            else:

                ret_v = gencode(l[1:])

                if ret_v[1] in s_table.keys():

                    if s_table[ret_v[1]][0]=='OBJECT':

                        if s_table[ret_v[1]][2]!='yes':

                            print "Not well-formed..."

                            quit()

                typecheck_return_value(l[0][1],ret_v)

            imcode.append([['JR','jr'],ret_v, ['NOP', 'None'], ['NOP', 'None']])

            return None

        elif l[0] == ['CLASS', 'class']:

            if l[2] == ['EXTENDS', 'extends'] and l[3][0]=='CLASS':

                if l[4]==['LCURLY', '{'] and l[5]!=['RCURLY', '}']:

                    make_record(l[1],l[5],l[3])

            elif l[2]==['LCURLY', '{'] and l[3]!=['RCURLY', '}']:

                make_record(l[1],l[3],[])

            else:

                make_record(l[1],[],[])

            return None

        else:

            for token in l:

                if token[0] in ['NUMBER', 'IDENTIFIER', 'INT', 'BOOL' , 'TRUE', 'FALSE', 'CLASS']:

                    stack.append(token)

                elif token[1] == '-':

                    if token[0] == 'MINUS' and len(stack)>=2:

                        op2 = stack.pop()

                        op1 = stack.pop()

                        stack.append(BinOP(op1, op2, token))

                    elif token[0] == 'UMINUS': 

                        op1 = stack.pop()

                        op2=  ['NUMBER','-1']

                        stack.append(BinOP(op2, op1, ['TIMES','*']))

                elif token[1] == '!':

                    op1 = stack.pop()

                    stack.append(NOT(op1))

                elif token[1] == '=':

                    op2 = stack.pop()

                    op1 = stack.pop()

                    stack.append(ASS(op1, op2))

                elif token[1] == 'print':

                    op1 = stack.pop()

                    stack.append(PRINT(op1))

                elif token[1] == 'input':

                    stack.append(IN())

                    

                elif token[0] == 'PINC':

                    op1 = stack.pop()

                    stack.append(INC(op1))

                elif token[0] == 'PDEC':

                    op1 = stack.pop()

                    stack.append(DEC(op1))

                elif token[0] == 'POINC':

                    op1 = stack.pop()

                    stack.append(POINC(op1))

                elif token[0] == 'PODEC':

                    op1 = stack.pop()

                    stack.append(PODEC(op1))

                    

                elif token[1] in ['<','<=','>','>=','==','!=','&&','||']:

                    op2 = stack.pop()

                    op1 = stack.pop()

                    stack.append(ConOP(op1, op2, token))



                elif token[1] in ['*','/','%','+']:

                    op2 = stack.pop()

                    op1 = stack.pop()

                    stack.append(BinOP(op1, op2, token))



                elif token == ['DOT', '.']:

                    field = stack.pop()

                    obj   =  stack.pop()

                    stack.append(field_access(field,obj))



                elif token == ['MDOT', '..']:

                    fname = stack.pop()

                    obj  = stack.pop()

                    if fname[1] not in c_table[s_table[obj[1]][2]]:

                        print "Method NOT accessible..."

                        quit()

                    if f_table[fname[1]]!=s_table[obj[1]][2]:                      #if method does not belong to object's class

                        obj=adjustobj(obj,cf_table[s_table[obj[1]][2]])            #get number of fields in object's class and adjust

                    imcode.append([['PASSOBJ','passobj'],obj,['NOP', 'None'], ['NOP', 'None']])

                    stack.append(fname)



                elif token[0] == 'LSQR':

                    op1 = stack.pop()

                    if op1[1] not in arrayt.keys() and op1[0]!='ADDRESS':

                        print "-Illegal operation on non array element..!"

                        quit()

                    stack.append(op1)

                elif token[0] == 'RSQR':

                    op1 = stack.pop()

                    op2 = stack.pop()

                    stack.append(INDEX(op1, op2))



                elif token[0] == 'NEW':

                    typeinfo = stack.pop()

                    if typeinfo[0]=='CLASS':

                        if len(stack)>0:

                            s_table[stack[-1][1]][2]=typeinfo[1]

                        stack.append(ALLOCK_OBJECT(typeinfo[1]))

                        

                        #insert_in_s_table

                    else:

                        size = stack.pop()

                        if len(l)>(l.index(token)+1) and l[l.index(token)+1]==['EQUALS','=']:

                            base = stack.pop()

                            

                            if base[1] in arrayt.keys() or base[0]=='ADDRESS':

                                stack.append(ALLOCK(typeinfo,size,base))

                            else:

                                print "Illegal allocation on non array element..!"

                                quit()

                        return ['NUMBER',1]

                

                elif token[1] in ['else']:

                    return None

                

                elif token[1] == '(':

                    

                    bracestart = l.index(token)

                    bracetrack = bracestart+1

                    makeargv=[]

                    while bracetrack < len(l):

                        if l[bracetrack] == ['RPAREN', ')']:

                            break

                        else:

                            makeargv.append(gencode(l[bracetrack]))

                            bracetrack+=1



                    #save all registers first

                    imcode.append([['SAVE','save'],['NOP','None'],['NOP','None'],['NOP','None']])

                    #now continue

                    if (bracestart+1) < bracetrack:            # function with argument

                        

                        ARGUMENT_send(makeargv)

                    for i in range(bracetrack,bracestart,-1):

                        l.remove(l[i])



                    fname = stack.pop()

                    check_argc_sent_received(fname,len(makeargv))

                    stack.append(CALL(fname))





                    

                else:

                    error = True

                    print "Syntax error near- '" + str(token[1]) + "'"

                    break

                

    except IndexError:

        error = True

        print "Syntax error near '" + str(l[0][1]) + "'"

        

            

    if (not error):

        try:

            return stack.pop()

        except IndexError:

            print "Empty string?"

            return None

    else:

        return None

#-----------------------------------------------------------------------------

def this_field_access(field,obj,fields):

    if field[1] in fields:

        global counter

        tv='T'+str(counter)

        counter+=1

        ind = fields.index(field[1]) * 4

        imcode.append([['IDENTIFIER',tv],obj,['PLUS','+'],['NUMBER',ind]])

        type1,type2 = get_type(field,['NUMBER',1])

        insert_in_s_table(tv,'INDENTIFIER',type1,None,None)

        return ['ADDRESS',tv]



    else:

        print "Invalid field access.."

        quit()



def super_field_access(field,obj,fields,superclass):

    if superclass[1] in c_table.keys():

        superfld = c_table[superclass[1]]

    else:

        print "Class not found.."

        quit()

             

    if field[1] in superfld:

        global counter

        tv='T'+str(counter)

        counter+=1

        if fields.count(field[1])==1:

            ind = fields.index(field[1]) * 4

        elif fields.count(field[1])>1:

            ind = fields.index(field[1])

            fields2 = fields[ind+1:]

            ind2 = fields2.index(field[1])

            ind = ind + ind2 + 1

            ind = ind * 4

        imcode.append([['IDENTIFIER',tv],obj,['PLUS','+'],['NUMBER',ind]])

        type1,type2 = get_type(field,['NUMBER',1])

        insert_in_s_table(tv,'INDENTIFIER',type1,None,None)

        return ['ADDRESS',tv]



    else:

        print "Invalid field access.."

        quit()



stackk =[]

def class_gencode(l,currentclass,superclass):

    #global counter

    global stackk

    global arrayt

    #counter =0

    stack = []

    error = False



##    print "-=>",l

    try:

        if l==None:return None

        elif l[0][0] in ['WHILE','IF','DOWHILE','FOR']:

            if l[1]==None:stackk.append(['NUMBER','1'])

            else:

                stackk.append(class_gencode(l[1],currentclass,superclass))

            return None

        elif l[0][0] in ['LCURLY','RCURLY','DO','FOR']:

            return None

        elif l[0][0] == 'JUMP':

            imcode.append(l)

            return None

        elif l[0][0] in ['LPAREN']:

            if len(l)>2:            # function with argument

                ARGUMENT_receive(l[1:-1])

            imcode.append([['SAVE_RA','save_ra'],['NOP','None'],['NOP','None'],['NOP','None']])

            return None

        elif l[0][0] == 'LABEL':

            imcode.append([['LABEL',l[0][1]], ['NOP', 'None'], ['NOP', 'None'], ['NOP', 'None']])

            return None

        elif l[0][0] in ['INT','BOOL']:      # Variable decleration

            vard=[]

            for i in range(1,len(l)):

                if l[i] not in [['COMMA', ','],['SEMICOLON', ';']]:

                    vard.append(l[i])

                else:

                    if len(vard)>1:

                        if vard[1]==['LSQR','[']:

                            insert_in_s_table(vard[0][1],'ARRAY',l[0][1],None,(len(vard)-1)/2)

                            arrayt[vard[0][1]]=None

                    else:

                        insert_in_s_table(vard[0][1],'IDENTIFIER',l[0][1],None,None)

                    vard=[]

            return None

        

        elif l[0][0] == 'CLASSID':               

            vard=[]

            for i in range(1,len(l)):

                if l[i] not in [['COMMA', ','],['SEMICOLON', ';']]:

                    vard.append(l[i])

                else:

                    if len(vard)>1:

                        if vard[1]==['LSQR','[']:

                            insert_in_s_table(vard[0][1],'ARRAY',l[0][1],None,(len(vard)-1)/2)

                            arrayt[vard[0][1]]=None

                    else:

                        insert_in_s_table(vard[0][1],'OBJECT',l[0][1],None,None)

                    vard=[]

            return None

        

        elif l[0][0] in ['JIFT','JIFF']:

            l[2]=stackk.pop()

            type1,type2= get_type(l[2],['NUMBER',1])

            if type1 != 'bool':

                print "Type Error: Invalid conditon.."

                quit()

            imcode.append(l)

            return None

        

        elif l[0][0] == 'RETURN':

            if l[1] == ['VOID', 'void']:

                ret_v = ['NUMBER',1]

                typecheck_return_value(l[0][1],l[1])

            else:

                ret_v = class_gencode(l[1:],currentclass,superclass)

                if ret_v[0]=='ADDRESS':

                    ret_v=Address_to_Value(ret_v)

                typecheck_return_value(l[0][1],ret_v)

            imcode.append([['JR','jr'],ret_v, ['NOP', 'None'], ['NOP', 'None']])

            return None

        

        else:

            for token in l:

                if token[0] ==  'IDENTIFIER':

                    if len(stack)>0:

                        element=stack.pop()

                        if element == ['THIS','this']:

                            stack.append(this_field_access(token,['IDENTIFIER','this'],currentclass))

                        elif element == ['SUPER','super']:

                            stack.append(super_field_access(token,['IDENTIFIER','this'],currentclass,superclass))

                        else:

                            stack.append(element)

                            stack.append(token)

                    else:

                        if token[1] in currentclass:

                            stack.append(this_field_access(token,['IDENTIFIER','this'],currentclass))

                        else:

                            stack.append(token)

                elif token[1] in ['super','this']:

                    stack.append(token)

                elif token[0] in ['NUMBER', 'INT', 'BOOL' , 'TRUE', 'FALSE', 'CLASS']:

                    stack.append(token)

                elif token[1] == '-':

                    if token[0] == 'MINUS' and len(stack)>=2:

                        op2 = stack.pop()

                        op1 = stack.pop()

                        stack.append(BinOP(op1, op2, token))

                    elif token[0] == 'UMINUS': 

                        op1 = stack.pop()

                        op2=  ['NUMBER','-1']

                        stack.append(BinOP(op2, op1, ['TIMES','*']))

                elif token[1] == '!':

                    op1 = stack.pop()

                    stack.append(NOT(op1))

                elif token[1] == '=':

                    op2 = stack.pop()

                    op1 = stack.pop()

                    stack.append(ASS(op1, op2))

                elif token[1] == 'print':

                    op1 = stack.pop()

                    stack.append(PRINT(op1))

                elif token[1] == 'input':

                    stack.append(IN())

                    

                elif token[0] == 'PINC':

                    op1 = stack.pop()

                    stack.append(INC(op1))

                elif token[0] == 'PDEC':

                    op1 = stack.pop()

                    stack.append(DEC(op1))

                elif token[0] == 'POINC':

                    op1 = stack.pop()

                    stack.append(POINC(op1))

                elif token[0] == 'PODEC':

                    op1 = stack.pop()

                    stack.append(PODEC(op1))

                    

                elif token[1] in ['<','<=','>','>=','==','!=','&&','||']:

                    op2 = stack.pop()

                    op1 = stack.pop()

                    stack.append(ConOP(op1, op2, token))



                elif token[1] in ['*','/','%','+']:

                    op2 = stack.pop()

                    op1 = stack.pop()

                    stack.append(BinOP(op1, op2, token))



                elif token == ['DOT', '.']:

                    pass



                elif token == ['MDOT', '..']:

                    fname = stack.pop()

                    obj  = stack.pop()

                    imcode.append([['PASSOBJ','passobj'],obj,['NOP', 'None'], ['NOP', 'None']])

                    stack.append(fname)



                elif token[0] == 'LSQR':

                    op1 = stack.pop()

                    if op1[1] not in arrayt.keys() and op1[0]!='ADDRESS':

                        print "-Illegal operation on non array element..!"

                        quit()

                    stack.append(op1)

                elif token[0] == 'RSQR':

                    op1 = stack.pop()

                    op2 = stack.pop()

                    stack.append(INDEX(op1, op2))



                elif token[0] == 'NEW':

                    typeinfo = stack.pop()

                    if typeinfo[0]=='CLASS':

                        stack.append(ALLOCK_OBJECT(typeinfo[1]))

                    else:

                        size = stack.pop()

                        if len(l)>(l.index(token)+1) and l[l.index(token)+1]==['EQUALS','=']:

                            base = stack.pop()

                            

                            if base[1] in arrayt.keys() or base[0]=='ADDRESS':

                                stack.append(ALLOCK(typeinfo,size,base))

                            else:

                                print "Illegal allocation on non array element..!"

                                quit()

                        return ['NUMBER',1]

                

                elif token[1] in ['else']:

                    return None

                

                elif token[1] == '(':

                    bracestart = l.index(token)

                    bracetrack = bracestart+1

                    makeargv=[]

                    while bracetrack < len(l):

                        if l[bracetrack] == ['RPAREN', ')']:

                            break

                        else:

                            makeargv.append(class_gencode(l[bracetrack],currentclass,superclass))

                            bracetrack+=1



                    #save all registers first

                    imcode.append([['SAVE','save'],['NOP','None'],['NOP','None'],['NOP','None']])

                    #now continue

                    if (bracestart+1) < bracetrack:            # function with argument

                        

                        ARGUMENT_send(makeargv)

                    for i in range(bracetrack,bracestart,-1):

                        l.remove(l[i])



                    fname = stack.pop()

                    check_argc_sent_received(fname,len(makeargv))

                    

                    stack.append(CALL(fname))

                    

                else:

                    error = True

                    print "Syntax error near- '" + str(token[1]) + "'"

                    break

                

    except IndexError:

        error = True

        print "Syntax error near '" + str(l[0][1]) + "'"

        

            

    if (not error):

        try:

            return stack.pop()

        except IndexError:

            print "Empty string?"

            return None

    else:

        return None

#-----------------------------------------------------------------------------    

#.............................................................................

#-----------------------------------------------------------------------------

        

# main

def main_main(filename, c):

    global s_table

    global c_table

    for i in c:

        c_table[i]=[]

    try:

        parser = yacc.yacc()

        f = open(filename,'r')

        s=f.read()

    except EOFError:

        print "ERROR encountered while reading input file!!"

        quit()

    

    result = parser.parse(s)

    if 'main' not in s_table.keys():

        print "Program does NOT contain 'Main' function.."

        quit()

    else:

        if s_table['main'][0] != 'FUNCTION':

            print "Program does NOT contain 'Main' function.."

            quit()

        

    AST(result)

    result=[]

    

    static_semantic_check(astcode)



    for i in  astcode:

        gencode(i)



    

        

##    key = s_table.keys()

##    for i in key :

##        print "%-15s %-15s %-10s %-10s" % (i,s_table[i][0],s_table[i][1],s_table[i][2])

      

##    if usebefore!=[]:

##        print"Variables used before declaration:"

##        for var in usebefore: print var[1]

##        print "Exiting..."

##        quit()

##    else:

    

    

            

    

#------------------------------------------------------------------------

    imco=[]

    addr=0

    stable=[]

    imco,stable,addr=separatefunctions(imcode,stable,addr,arrayt)



    

#-------------------------------------------------------------------------------------                      

##    idx=-1

##    for i in imco:

##        idx+=1

##        print idx,">- ",i        





    FCG.generate_final_code(imco,stable,filename)



