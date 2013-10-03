

def funlexicalscope(functioncount,astcode):
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
        mall=0
        
        for x,i in enumerate(astcode):
            line+=1
            if i[0][0]=='LCURLY':
                block_track+=1
                blockstack.append(line)
                variablestack.append(i[0][0])
            if i[0][0]=='FUNCTION':
                    astcode.insert(line,[['LCURLY', '{']])
            if i[0][0]=='RETURN':
                    astcode.insert(line,[['RCURLY', '}']])
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
                                        m='f'+str(functioncount)+'_'+str(block_track)+'_'+m
                             
                             else:
                                if  j[0]=='IDENTIFIER' and j[1] == temp:
                                    j[1]='f'+str(functioncount)+'_'+str(block_track)+'_'+j[1]
                                    
                             for m in j: 
                                 if type(m)==list and m[0]=='IDENTIFIER' and mall==0:
                                     m[1]='f'+str(functioncount)+'_'+str(block_track)+'_'+m[1]
                                     mall=1
                                
                              
                       for i in astcode[lcurl:rcurl+1]:
                          if i[0][0] in ['IF','DOWHILE','WHILE']:
                                  
                                if i[1][0][0]=='IDENTIFIER' and i[1][0][1]==temp:
                                     i[1][0][1]='f'+str(functioncount)+'_'+str(block_track)+'_'+i[1][0][1]
                          if i[0] == ['FOR', 'for']:

                                if len(i)>1 and i[1]!=None:
                                        for j in i[1]:
                                                if j[0]=='IDENTIFIER' and j[1]==temp:
                                                        j[1]='f'+str(functioncount)+'_'+str(block_track)+'_'+j[1]
        

               block_track-=1
               var=[]
               temp=0
            if i[0][0] in ['INT','BOOL','CLASSID']:
                for j in i:
##                    print "call comes here..."
                    if j[0]=='IDENTIFIER':
                            
                        variablestack.append(j[1])
                        declared.append(j[1])
                        
            if i[0][0] in ['JIFF','JFALSE','LPAREN','CLASS']:
                for j in i:
                    if j[0]=='IDENTIFIER':
                        variablestack.append(j[1])
                        
                    
            if i[0][0]=='LPAREN':
                for j in i:
                        if j[0]=='IDENTIFIER':
                                variablestack.append(j[1])
                                declared.append(j[1])
             
        



def  declare_first (astcode):      # it is same as declare before use....
        variablestack=[]
        declared=[]
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
                            print "Error: Used before declared identifier ="
                            quit()
    





def declare_once(astcode):
    declared_once=[];
    symbol_table_declare={}
    for i in astcode: 
        if i[0][0] =='INT':
            for j in i:
                if j[0]=='IDENTIFIER' and j[1] not in symbol_table_declare:
                    symbol_table_declare[j[1]]='INT'
                elif j[0]=='IDENTIFIER' and j[1] in symbol_table_declare:
                    print "The element has already been declared before"
                    quit()
                    
        if i[0][0] =='BOOL':
            for j in i:
                if j[0]=='IDENTIFIER' and j[1] not in symbol_table_declare:
                    symbol_table_declare[j[1]]='INT'
                elif j[0]=='IDENTIFIER' and j[1] in symbol_table_declare:
                    print "The element has already been declared before"
                    quit()

    
                
    

def well_typed(astcode):
    pass

def return_test(astcode):
    line=-1
    count=0
    functionalstack=[]
    functioncount=0
    for i in astcode:
        line+=1
        
        returncount=0
        lineinsidefunction=0
        if i[0][0]=='FUNCTION':
            functioncount+=1
            for j in astcode[line:len(astcode)]:
                lineinsidefunction+=1
                if j[0][0]=='LCURLY':
                    functionalstack.append(j[0][0])
                    count=count+1

                if j[0][0]=='RETURN':
                    returncount+=1
                    j[0][1]=i[0][1]
                
                if j[0][0]=='RCURLY':
                    functionalstack.pop()
                    count=count-1
                    if(count==0):
                        if(returncount>0):
                            pass
                        else:
                            print "function does not return at the end of program"
                            quit()
                        break
                


def static_semantic_check(astcode):
    
     funlexicalscope(0,astcode)
##     for i in astcode:
##        print i
     well_typed(astcode)
     return_test(astcode)
