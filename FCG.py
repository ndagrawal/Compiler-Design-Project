
def generate_final_code(imcode,stable,fname):
    fname=fname[0:len(fname)-6]
    fname+=".asm"
    f = open(fname , 'w')
    
    #f.write("main:\n")


    for i in imcode:
        if i[0][0] in ['INT','BOOL']:
            continue
        elif i[0][0]=='LABEL':
            f.write('\n'+str(i[0][1])+":" +'\n')
        elif i[0][0]=='JUMP':
            f.write("j "+str(i[1][1])+'\n')

        elif i[0] == ['SAVE','save']:
            #save all registers first
            for reg in range(0,10):
                f.write("sw $t"+str(reg)+", ($sp)\naddi $sp, $sp, -4\n")
            for reg in range(0,8):
                f.write("sw $s"+str(reg)+", ($sp)\naddi $sp, $sp, -4\n")
            #now call
                
        elif i[2][0]=='ARGC' and i[3][0]=='PARAMETER':
            if i[1][0]=='IDENTIFIER' :
                f.write("sw "+str(i[1][1])+", ($sp)\n")
            elif i[1][0]=='NUMBER':
                f.write("li $s0, "+str(i[1][1])+'\n')
                f.write("sw $s0,($sp)\n")
            f.write("addi $sp, $sp, -4\n")

        elif i[0] == ['JAL', 'jal']:
            f.write("jal "+str(i[1][1])+'\n')
            
        elif i[2][0]=='ARGC' and i[3][0]=='ARGUMENT':
            if i[0][0]=='IDENTIFIER' :
                f.write("addi $sp, $sp, 4\nlw "+str(i[0][1])+", ($sp)\n")

        elif i[0]==['SAVE_RA','save_ra']:
            f.write("sw $ra,($sp) \naddi $sp, $sp, -4\n")   #push return address on stack
                
        elif i[0] == ['JR', 'jr']:
            #copy return value to $v0 first
            if i[1][0]=='IDENTIFIER' :
                f.write("move $v0, " +str(i[1][1])+"\n")
            elif i[1][0]=='NUMBER':
                f.write("li $s0, "+str(i[1][1])+'\n')
                f.write("move $v0, $s0\n")
            # now copy back return address from stack
            f.write("addi $sp, $sp, 4 \nlw $ra,($sp)\n")
            #now restore back all registers 
            for reg in range(7,-1,-1):
                f.write("addi $sp, $sp, 4\nlw $s"+str(reg)+", ($sp)\n")
            for reg in range(9,-1,-1):
                f.write("addi $sp, $sp, 4\nlw $t"+str(reg)+", ($sp)\n")

            #now return to caller
            f.write("jr $ra\n")
            
        elif i[0] == ['RECEIVE', 'receive']:
            f.write("move "+str(i[1][1])+", $v0\n")

        elif i[0] == ['PASSOBJ', 'passobj']:
            f.write("move $a0, "+str(i[1][1])+"\n")

        elif i[0] == ['RECEIVEOBJ', 'receiveobj']:
            f.write("move "+str(i[1][1])+", $a0\n")
            
        elif i[2][0]=='NOP' and i[3][0]=='NOP':
            if i[1][0]=='IDENTIFIER' :
                f.write("move "+str(i[0][1])+', '+str(i[1][1])+'\n')
            elif i[1][0]=='NUMBER':
                f.write("li "+str(i[0][1])+', '+str(i[1][1])+'\n')


        elif i[2][0]=='ALLOCATE':
            if i[3][0] == 'NUMBER':
                f.write("li $s0 ,"+str(i[3][1])+ '\n')
                f.write("li $s1 ,4 \n")
                f.write("mulo $a0 ,$s0 , $s1 \n")
            elif i[3][0] == 'IDENTIFIER':
                f.write("li $s1 ,4 \n")
                f.write("mulo $a0 ," + str(i[3][1]) +", $s1 \n")

            f.write("li $v0, 9 \nsyscall \n")
            f.write("move " +str(i[0][1]) +", $v0 \n")

        elif i[2][0]=='PLUS':    
            if i[2][1]=='+':
                if i[1][0]=='IDENTIFIER'  and  i[3][0]=='IDENTIFIER' :
                    f.write("add "+str(i[0][1])+', '+str(i[1][1])+', '+str(i[3][1])+'\n')
                elif i[1][0]=='NUMBER' and  i[3][0]=='IDENTIFIER' :
                    f.write("addi "+str(i[0][1])+', '+str(i[3][1])+', '+str(int(float(i[1][1])))+'\n')
                elif i[1][0]=='IDENTIFIER'  and  i[3][0]=='NUMBER':
                    f.write("addi "+str(i[0][1])+', '+str(i[1][1])+', '+str(int(float(i[3][1])))+'\n')
                if i[1][0]=='NUMBER' and  i[3][0]=='NUMBER':
                    f.write("li "+str(i[0][1])+', '+str(i[1][1])+ '\n')
                    f.write("addi "+str(i[0][1])+', '+str(i[3][1])+'\n')
            
        elif i[2][0]=='MINUS':
            #Subtraction:-
            if i[2][1]=='-':
                if i[1][0]=='IDENTIFIER'  and  i[3][0]=='IDENTIFIER' :
                    f.write("sub "+str(i[0][1])+', '+str(i[1][1])+', '+str(i[3][1])+'\n')
                elif i[1][0]=='IDENTIFIER'  and  i[3][0]=='NUMBER':
                    f.write("addi "+str(i[0][1])+', '+str(i[1][1])+', -'+str(int(i[3][1]))+'\n')
                elif i[1][0]=='NUMBER' and  i[3][0]=='IDENTIFIER' :
                    f.write("li "+str(i[0][1])+', '+str(i[1][1])+ '\n')
                    f.write("sub "+str(i[0][1])+', '+str(i[0][1])+', '+str(i[3][1])+'\n')
                elif i[1][0]=='NUMBER' and  i[3][0]=='NUMBER':
                    f.write("li "+str(i[0][1])+', '+str(i[1][1])+ '\n')
                    f.write("addi "+str(i[0][1])+', -'+str(i[3][1])+'\n')   
           
        elif i[2][0]=='TIMES':
            #Multiplication:-
            if i[2][1]=='*':
                if i[1][0]=='IDENTIFIER'  and  i[3][0]=='IDENTIFIER' :
                    f.write("mult "+str(i[1][1])+', '+str(i[3][1])+'\n')
                    f.write("mflo "+str(i[0][1])+'\n')
                    
                elif i[1][0]=='IDENTIFIER'  and  i[3][0]=='NUMBER': 
                    f.write("li $s0 ," +str(i[3][1])+ '\n')
                    f.write("mulo "+str(i[0][1])+', $s0 ,'+str(i[1][1])+'\n')
                  
                elif i[1][0]=='NUMBER' and  i[3][0]=='IDENTIFIER' :
                    f.write("li $s0 ,"+str(i[1][1])+ '\n')
                    f.write("mulo "+str(i[0][1])+',$s0 , '+str(i[3][1])+'\n')
                 
                elif i[1][0]=='NUMBER' and  i[3][0]=='NUMBER' :
                    f.write("li $s0 ,"+str(i[1][1])+ '\n')
                    f.write("li $s1 ,"+str(i[3][1])+ '\n')
                    f.write("mulo "+str(i[0][1])+',$s0 , $s1 \n')    

        elif i[2][0]=='SLASH':
            #Division:-
            if i[2][1]=='/':
                if i[1][0]=='IDENTIFIER'  and  i[3][0]=='IDENTIFIER' :
                    f.write("div "+str(i[1][1])+', '+str(i[3][1])+'\n')
                    f.write("mflo "+str(i[0][1])+'\n')
                    
                elif i[1][0]=='NUMBER' and  i[3][0]=='IDENTIFIER' :
                    f.write("li $s0 ," +str(i[1][1])+ '\n')
                    f.write("div $s0 ," +str(i[3][1])+'\n')
                    f.write("mflo "+str(i[0][1])+'\n')
                    
                elif i[1][0]=='IDENTIFIER'  and  i[3][0]=='NUMBER':
                    f.write("li $s0 ," +str(i[3][1])+ '\n')
                    f.write("div "+str(i[1][1])+', $s0 \n')
                    f.write("mflo "+str(i[0][1])+'\n')
                    
                elif i[1][0]=='NUMBER' and  i[3][0]=='NUMBER':
                    f.write("li "+str(i[0][1])+', '+str(int(i[1][1])/int(i[3][1]))+ '\n')   

        elif i[2][0]=='MOD':
            #Mod Operator:-
            if i[2][1]=='%':
                if i[1][0]=='IDENTIFIER'  and  i[3][0]=='IDENTIFIER' :
                    f.write("div "+str(i[1][1])+', '+str(i[3][1])+'\n')
                    f.write("mfhi "+str(i[0][1])+'\n')
                elif i[1][0]=='NUMBER' and  i[3][0]=='IDENTIFIER' :
                    f.write("li $s0 ," +str(i[1][1])+ '\n')
                    f.write("div $s0 , "+str(i[3][1])+'\n')
                    f.write("mfhi "+str(i[0][1])+'\n')  
                elif i[1][0]=='IDENTIFIER'  and  i[3][0]=='NUMBER':
                    f.write("li $s0 ,"+str(i[3][1])+ '\n')
                    f.write("div "+str(i[1][1])+', $s0 \n')
                    f.write("mfhi "+str(i[0][1])+'\n')
                elif i[1][0]=='NUMBER' and  i[3][0]=='NUMBER':
                    f.write("li "+str(i[0][1])+', '+str(int(i[1][1])%int(i[3][1]))+ '\n')

        elif i[2][0]=='LTEQ':
            #Less than or Equal to:-

            if i[2][1]=='<=':
                if i[1][0]=='IDENTIFIER' and i[3][0]=='IDENTIFIER':
                    f.write("sle "+str(i[0][1])+', '+str(i[1][1])+', '+str(i[3][1])+ '\n')

                elif i[1][0]=='NUMBER' and i[3][0]=='IDENTIFIER':
                    f.write("li $s0 ," +str(i[1][1])+ '\n')
                    f.write("sle "+str(i[0][1])+', $s0 ,'+str(i[3][1])+'\n')

                elif i[1][0] =='NUMBER' and i[3][0]=='NUMBER':
                    f.write("li $s0 ," + str(i[1][1])+ '\n')
                    f.write("li $s1 ," + str(i[3][1])+ '\n')
                    f.write("sle "+str(i[0][1])+', $s0 , $s1 \n')
                    
                elif i[1][0]=='IDENTIFIER' and i[3][0]=='NUMBER':
                    f.write("li $s0 ," +str(i[3][1])+ '\n')
                    f.write("sle "+str(i[0][1])+', '+str(i[1][1])+', $s0 \n')

        elif i[2][0]=='GT':
            #Greater than:-
            if i[2][1]=='>':
                if i[1][0]=='IDENTIFIER' and i[3][0]=='IDENTIFIER':
                    f.write("sgt "+str(i[0][1])+', '+str(i[1][1])+', '+str(i[3][1])+ '\n')

                elif i[1][0]=='NUMBER' and i[3][0]=='IDENTIFIER':
                    f.write("li $s0 ," +str(i[1][1])+ '\n')
                    f.write("sgt "+str(i[0][1])+', $s0 ,'+str(i[3][1])+'\n')

                elif i[1][0] =='NUMBER' and i[3][0]=='NUMBER':
                    f.write("li $s0 ," + str(i[1][1])+ '\n')
                    f.write("li $s1 ," + str(i[3][1])+ '\n')
                    f.write("sgt "+str(i[0][1])+', $s0 , $s1 \n')
                    
                elif i[1][0]=='IDENTIFIER' and i[3][0]=='NUMBER':
                    f.write("li $s0, " +str(i[3][1])+ '\n')
                    f.write("sgt "+str(i[0][1])+', '+str(i[1][1])+', $s0 \n')

            
        elif i[2][0]=='GTEQ':
            #Greater than or Equal to:-
            if i[2][1]=='>=':
                if i[1][0]=='IDENTIFIER' and i[3][0]=='IDENTIFIER':
                    f.write("sge "+str(i[0][1])+', '+str(i[1][1])+', '+str(i[3][1])+ '\n')

                elif i[1][0]=='NUMBER' and i[3][0]=='IDENTIFIER':
                    f.write("li $s0 ," +str(i[1][1])+ '\n')
                    f.write("sge "+str(i[0][1])+', $s0 ,'+str(i[3][1])+'\n')

                elif i[1][0] =='NUMBER' and i[3][0]=='NUMBER':
                    f.write("li $s0 ," + str(i[1][1])+ '\n')
                    f.write("li $s1 ," + str(i[3][1])+ '\n')
                    f.write("sge "+str(i[0][1])+', $s0 , $s1 \n')
                    
                elif i[1][0]=='IDENTIFIER' and i[3][0]=='NUMBER':
                    f.write("li $s0 ," +str(i[3][1])+ '\n')
                    f.write("sge "+str(i[0][1])+', '+str(i[1][1])+', $s0 \n')

            

        
        elif i[2][0]=='LT':
            #Less than
            if i[2][1]=='<':
                if i[1][0]=='IDENTIFIER' and i[3][0]=='IDENTIFIER':
                    f.write("slt "+str(i[0][1])+', '+str(i[1][1])+', '+str(i[3][1])+ '\n')

                elif i[1][0]=='NUMBER' and i[3][0]=='IDENTIFIER':
                    f.write("li $s0 ," +str(i[1][1])+ '\n')
                    f.write("slt "+str(i[0][1])+', $s0 ,'+str(i[3][1])+'\n')

                elif i[1][0] =='NUMBER' and i[3][0]=='NUMBER':
                    f.write("li $s0 ," + str(i[1][1])+ '\n')
                    f.write("li $s1 ," + str(i[3][1])+ '\n')
                    f.write("slt "+str(i[0][1])+', $s0 , $s1 \n')
                    
                elif i[1][0]=='IDENTIFIER' and i[3][0]=='NUMBER':
                    f.write("li $s0 ," +str(i[3][1])+ '\n')
                    f.write("slt "+str(i[0][1])+', '+str(i[1][1])+', $s0 \n')



        elif i[2][0]=='NEQ':   
            #Not Equal To
            if i[2][1]=='!=':
                if i[1][0]=='IDENTIFIER' and i[3][0]=='IDENTIFIER':
                    f.write("sne "+str(i[0][1])+', '+str(i[1][1])+', '+str(i[3][1])+ '\n')

                elif i[1][0]=='NUMBER' and i[3][0]=='IDENTIFIER':
                    f.write("li $s0 ," +str(i[1][1])+ '\n')
                    f.write("sne "+str(i[0][1])+', $s0 ,'+str(i[3][1])+'\n')

                elif i[1][0] =='NUMBER' and i[3][0]=='NUMBER':
                    f.write("li $s0 ," + str(i[1][1])+ '\n')
                    f.write("li $s1 ," + str(i[3][1])+ '\n')
                    f.write("sne "+str(i[0][1])+', $s0 , $s1 \n')
                    
                elif i[1][0]=='IDENTIFIER' and i[3][0]=='NUMBER':
                    f.write("li $s0 ," +str(i[3][1])+ '\n')
                    f.write("sne "+str(i[0][1])+', '+str(i[1][1])+', $s0 \n')

            

        elif i[2][0]=='EQ':
            #Equal to 
            if i[2][1]=='==':
                if i[1][0]=='IDENTIFIER' and i[3][0]=='IDENTIFIER':
                    f.write("seq "+str(i[0][1])+', '+str(i[1][1])+', '+str(i[3][1])+ '\n')

                elif i[1][0]=='NUMBER' and i[3][0]=='IDENTIFIER':
                    f.write("li $s0 ," +str(i[1][1])+ '\n')
                    f.write("seq "+str(i[0][1])+', $s0 ,'+str(i[3][1])+'\n')

                elif i[1][0] =='NUMBER' and i[3][0]=='NUMBER':
                    f.write("li $s0 ," + str(i[1][1])+ '\n')
                    f.write("li $s1 ," + str(i[3][1])+ '\n')
                    f.write("seq "+str(i[0][1])+', $s0 , $s1 \n')
                    
                elif i[1][0]=='IDENTIFIER' and i[3][0]=='NUMBER':
                    f.write("li $s0 ," +str(i[3][1])+ '\n')
                    f.write("seq "+str(i[0][1])+', '+str(i[1][1])+', $s0 \n')


        elif i[2][0]=='LAND':   #AND 
            if i[2][1]=='&&':
                if i[1][0]=='IDENTIFIER' and i[3][0]=='IDENTIFIER':
                    f.write("sgt $s0, "+ str(i[1][1]) + ', $0'+ '\n')
                    f.write("sgt $s1, "+ str(i[3][1]) + ', $0'+ '\n')
                    f.write("and "+str(i[0][1])+", $s0, $s1\n")

                elif i[1][0]=='NUMBER' and i[3][0]=='IDENTIFIER':
                    f.write("slti $s0, $0, "+ str(i[1][1]) +'\n')
                    f.write("sgt $s1, "+ str(i[3][1]) + ', $0'+ '\n')
                    f.write("and "+str(i[0][1])+", $s0, $s1\n")
                 
                elif i[1][0]=='IDENTIFIER' and i[3][0]=='NUMBER':
                    f.write("slti $s0, $0, "+ str(i[3][1]) +'\n')
                    f.write("sgt $s1, "+ str(i[1][1]) + ', $0'+ '\n')
                    f.write("and "+str(i[0][1])+", $s0, $s1\n")

                elif i[1][0] =='NUMBER' and i[3][0]=='NUMBER':
                    f.write("slti $s0, $0, "+ str(i[1][1]) +'\n')
                    f.write("slti $s1, $0, "+ str(i[3][1]) +'\n')
                    f.write("and "+str(i[0][1])+", $s0, $s1\n")


        elif i[2][0]=='LOR':           #OR 
            if i[2][1]=='||':
                if i[1][0]=='IDENTIFIER' and i[3][0]=='IDENTIFIER':
                    f.write("sgt $s0, "+ str(i[1][1]) + ', $0'+ '\n')
                    f.write("sgt $s1, "+ str(i[3][1]) + ', $0'+ '\n')
                    f.write("or "+str(i[0][1])+", $s0, $s1\n")

                elif i[1][0]=='NUMBER' and i[3][0]=='IDENTIFIER':
                    f.write("slti $s0, $0, "+ str(i[1][1]) +'\n')
                    f.write("sgt $s1, "+ str(i[3][1]) + ', $0'+ '\n')
                    f.write("or "+str(i[0][1])+", $s0, $s1\n")
                 
                elif i[1][0]=='IDENTIFIER' and i[3][0]=='NUMBER':
                    f.write("slti $s0, $0, "+ str(i[3][1]) +'\n')
                    f.write("sgt $s1, "+ str(i[1][1]) + ', $0'+ '\n')
                    f.write("or "+str(i[0][1])+", $s0, $s1\n")

                elif i[1][0] =='NUMBER' and i[3][0]=='NUMBER':
                    f.write("slti $s0, $0, "+ str(i[1][1]) +'\n')
                    f.write("slti $s1, $0, "+ str(i[3][1]) +'\n')
                    f.write("or "+str(i[0][1])+", $s0, $s1\n")


        
        elif i[2][0]=='NOT':            #NOT 
            if i[2][1]=='!':
                if i[1][0]=='IDENTIFIER':
                    f.write("slt "+str(i[0][1])+', '+str(i[1][1])+', '+'1'+'\n')

                elif i[1][0]=='NUMBER':
                    f.write("li $s0 ," +str(i[1][1])+ '\n')
                    f.write("slt "+str(i[0][1]),+', $s0, '+'1'+'\n')

        elif i[2][0]=='LW':          #LOAD WORD -spill
            if i[3][0]=='ADDRESS':
                f.write("lw "+str(i[0][1])+', 0('+str(i[3][1])+') \n')
            else:
                f.write("lw "+str(i[0][1])+', '+str(i[3][1])+'\n')

        elif i[2][0]=='SW':         #STORE WORD -spill
            if i[3][0]=='ADDRESS':
                if i[1][0]=='IDENTIFIER':
                    f.write("sw "+str(i[1][1])+', 0('+str(i[3][1])+') \n')
                elif i[1][0]=='NUMBER':
                    f.write("li $s0 ," +str(i[1][1])+ '\n')
                    f.write("sw $s0, 0("+str(i[3][1])+') \n')
            else:
                f.write("sw "+str(i[1][1])+", "+ str(i[3][1])+'\n')


     
        #Conditional Jump
        elif i[0][0]=='JIFF':
            if i[2][0]=='IDENTIFIER' and i[1][0]=='LABEL':
                f.write("beqz "+str(i[2][1])+', '+str(i[1][1])+'\n')
            elif i[2][0]=='NUMBER' and i[1][0]=='LABEL':
                f.write("li $s0 ," +str(i[2][1])+ '\n')
                f.write("beqz $s0, "+str(i[1][1])+'\n')

        
        elif i[0][0]=='JIFT':
            if i[2][0]=='IDENTIFIER' and i[1][0]=='LABEL':
                f.write("bgtz "+str(i[2][1])+', '+str(i[1][1])+'\n')
            elif i[2][0]=='NUMBER' and i[1][0]=='LABEL':
                f.write("li $s0 ," +str(i[2][1])+ '\n')
                f.write("bgtz $s0, "+str(i[1][1])+'\n')


        elif i[0][0]=='JIFLE':
            if i[1][0]=='IDENTIFIER' and i[2][0]=='IDENTIFIER':
                f.write("ble "+str(i[1][1])+', '+str(i[2][1])+', '+i[3][1]+' \n')

        elif i[0][0]=='JIFLTZ':
            if i[1][0]=='IDENTIFIER':
                f.write("bltz "+str(i[1][1])+', '+i[3][1]+' \n')          

            


        elif i[2][0]=='PRINT':                           #PRINT Stmt                         # Print or Input
            if i[1][0]=='IDENTIFIER':                                                 #if printing variable   
                f.write("\n\nmove    $a0, " +str(i[1][1]) +"\nli    $v0, 1\nsyscall\n")
            else:                                                                     #if printing number
                f.write("\n\nli    $a0, " +str(int(float(i[1][1]))) +"\nli    $v0, 1\nsyscall\n")
            f.write("la    $a0, nl\nli    $v0, 4\nsyscall\n\n")                   # print new line

                
        elif i[2][0]=='INPUT':                                                    #Input stmt
            f.write("\n\nla    $a0, prompt\nli    $v0, 4\nsyscall\n\n")         # print prompt
            f.write("li    $v0, 5\nsyscall\nmove    " +str(i[0][1]) +", $v0\n\n")    # get number in t0
            
     
##    # print exiting program   
##    f.write("la    $a0, bye\nli    $v0, 4\nsyscall\n")
##    # exit program
##    f.write("li    $v0, 10\nsyscall\n")


#-----------------------------------------------------------------------
    f.write("\nindexerror:")
    # print index error msg   
    f.write("la    $a0, indexerror_msg\nli    $v0, 4\nsyscall\n")
    # exit program
    f.write("li    $v0, 10\nsyscall\n")
#-----------------------------------------------------------------------
    
    f.write("\n\n.data \n")
    for i in stable:
        f.write(i+':        .word    0\n') 
    
    f.write("\nprompt:            .asciiz    \"Please Enter a Positive Integer:\" \n")
    f.write("indexerror_msg:    .asciiz    \"Array Index Out Of Range..! exiting..\" \n")
    f.write("bye:               .asciiz    \"Execution Finished! exiting...\"\n")
    f.write("nl:                .asciiz    \"\\n\"")
    f.close()
    
    print "Code Compiled Successfully!!\nOut file is generated.."
