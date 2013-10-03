import GC
def liveness(blocksegment):
    Def=[]
    use=[]
    In=[]
    Out=[]
    index=-1
    count=-1

    for i in blocksegment:
        count+=1
        
        if i[0][0] in ['IDENTIFIER']:
            Def.append(i[0][1])
        if i[0][0] in ['JUMP','LABEL','RECEIVE','SAVE_RA','SAVE','JAL']:
            continue
        index+=1
        if i[0][0]=='PASSOBJ':
            use.append(i[1][1])
        if i[0][0]=='RECEIVEOBJ':
            Def.append(i[1][1])
        if i[2][0] in ['PLUS','MINUS','MOD','SLASH','TIMES']:      #AE
            if i[1][0]=='NUMBER':pass
            else:
                if count<1:
                    use.append(i[1][1])
                for j in blocksegment[0:count]:
                    if i[1][1] not in Def:
                        use.append(i[1][1])
                        break
            if i[3][0]=='NUMBER':pass
            else:
                if count<1:
                    use.append(i[3][1])
                for j in blocksegment[0:count]:
                    if i[3][1] not in Def:
                        use.append(i[3][1])
                        break;
            
        elif i[2][0] in ['EQ','NEQ','LT','LTEQ', 'GT','GTEQ']:       #AE Logical
            if i[1][0]=='NUMBER':
                pass
            else:
                if count<1:
                    use.append(i[1][1])
                for j in blocksegment[0:count]:
                    if i[1][1] not in Def: 
                        use.append(i[1][1])
                        break;
            if i[3][0]=='NUMBER':pass
            else:
                if count<1:
                    use.append(i[3][1])
                for j in blocksegment[0:count]:
                    
                    if i[3][1] not in Def:     
                        use.append(i[3][1])
                        break
            
                
        elif i[2][0]=='NOP' and i[3][0]=='NOP' and i[0][0]!='SAVE_RA':                    #Only Assignment
            if i[1][0]=='NUMBER':
                pass
            else:
                if count<1:
                    use.append(i[1][1])
                for j in blocksegment[0:count]:
                    if i[1][1] not in Def:
                        use.append(i[1][1])
                        break
            
        elif i[0][0]=='JIFF':
            
            if i[2][0]=='NUMBER':
                pass
            else:
                if count<1:
                    use.append(i[2][1])
                for j in blocksegment[0:count]:
                    if i[2][1] not in Def:
                        use.append(i[2][1])
                        break

        elif i[3][0] =='PARAMETER':
              if i[1][0]=='IDENTIFIER':
                  use.append(i[1][1])

        elif i[3][0] =='ARGUMENT':
              if i[1][0]=='IDENTIFIER':
                  Def.append(i[1][1])

        elif i[0][0]=='JR':
            if i[1][0]=='IDENTIFIER':
                
                use.append(i[1][1])
                  
        elif i[0][0]=='JIFT':
            if i[2][0]=='NUMBER':
                pass
            else:
                for j in blocksegment[0:count]:
                    if i[2][1] not in Def:
                        use.append(i[2][1])
                        break
        elif i[2][0]=='PRINT':                  # Print stmt
            
            if i[1][0]=='IDENTIFIER':
                
                if count<1:
                    use.append(i[1][1])
                for j in blocksegment[0:count]:
                    if i[1][1] not in Def:
                        
                        use.append(i[1][1])
                    
                        break
            else:                               #if printing number
                pass
        elif i[2][0]=='SW':                     # STORE stmt
            if i[1][0]=='IDENTIFIER':                   
                pass               
            else:
                pass
        elif i[2][0]=='LW':                     # LOAD stmt
            if i[0][0]=='IDENTIFIER':                   
                pass
        elif i[2][0]=='INPUT':                  # Input
            pass
    #print "def",Def,"use",use,count
    
    return Def,use

#---------------------------------------------------------------------------------------------------------

dicto1={}                                   
def liveness_statement(blocksegment,outset):
##    print "\n\n>>>>",outset,"\n"
##    for i in blocksegment:
##       print "#->",i
##    print "\n\n\n"
    ind=0;
    blocks=[] 
    blocksegment.reverse()
    Def=[]
    use=[]
    In=[]
    Out=[]
    index=-1
    li=0
    for i in blocksegment:
        index+=1
        
        if i[0][0] in ['JUMP','LABEL','RECEIVE','SAVE_RA','SAVE','JAL']:
            pass

#        if i[0][0] in ['RECEIVE','SAVE_RA','JAL']:continue

        elif i[0][0]=='PASSOBJ':
            use.append([i[1][1]])
            Def.append([])
        elif i[0][0]=='RECEIVEOBJ':
            Def.append([i[1][1]])   
            use.append([])
        elif i[2][0] in ['PLUS','MINUS','MOD','SLASH','TIMES']:      #AE
            Def.append([i[0][1]])
            tl=[]
            if i[1][0]=='NUMBER':pass
            else:tl.append(i[1][1])
            if i[3][0]=='NUMBER':pass
            else:tl.append(i[3][1])    
            use.append(tl)

        elif i[2][0] in ['EQ','NEQ','LT','LTEQ', 'GT','GTEQ', 'LAND', 'LOR', 'NOT']:       #AE Logical
            Def.append([i[0][1]])
            tl=[]
            if i[1][0]=='NUMBER':pass
            else:tl.append(i[1][1])
            if i[3][0]=='NUMBER':pass
            else:tl.append(i[3][1])    
            use.append(tl)

        #----------for the functional call parameters----------------------------------#
            
        elif i[3][0] =='PARAMETER':
              if i[1][0]=='IDENTIFIER':
                  use.append([i[1][1]])
                  Def.append([])
                  
        elif i[3][0] =='ARGUMENT':
              if i[1][0]=='IDENTIFIER':
                  Def.append([i[1][1]])
                  use.append([])
                  
        elif i[0][0]=='JR':
            if i[1][0]=='IDENTIFIER':
                use.append([i[1][1]])
            else:
                use.append([])
            Def.append([])

        elif i[2][0]=='NOP' and i[3][0]=='NOP' :                    #Only Assignment
            Def.append([i[0][1]])
            if i[1][0]=='NUMBER':use.append([])
            else:use.append([i[1][1]])
            
        elif i[0][0] in ['JIFF','JIFT']:
            if i[2][0]=='NUMBER':use.append([])
            else:use.append([i[2][1]])
            Def.append([])

        elif i[0][0] == 'JIFLE':
            Def.append([])
            use.append([i[1][1],i[2][1]])
        elif i[0][0] == 'JIFLTZ':
            Def.append([])
            use.append([i[1][1]])                                    

        elif i[2][0]=='PRINT':                  # Print stmt
            if i[1][0]=='IDENTIFIER':                 #if printing variable   
                use.append([i[1][1]])
                Def.append([])
            else:                               #if printing number
                Def.append([])
                use.append([])
                
        elif i[2][0]=='INPUT':                  # Input
            Def.append([i[0][1]])
            use.append([])

        elif i[2][0]=='SW':                     # STORE stmt
            if i[3][0]!='ADDR':
                uset=[]
                if i[1][0]=='IDENTIFIER' or i[1][0]=='ADDRESS':
                    uset.append(i[1][1])
                if i[3][0]=='IDENTIFIER' or i[3][0]=='ADDRESS':
                    uset.append(i[3][1])
                use.append(uset)
            else:
                use.append([])
            Def.append([])

        elif i[2][0]=='LW' and i[3][0] != 'ADDR':                     # LOAD stmt
            if i[3][0]=='ADDRESS' or i[3][0]=='IDENTIFIER':
                use.append([i[3][1]])
            else:
                use.append([])
            if i[0][0]=='IDENTIFIER':                   
                Def.append([i[0][1]])
            else:Def.append([])

        elif i[2][0]=='LW' and i[3][0] == 'ADDR':                     # LOADspill stmt
            if i[0][0]=='IDENTIFIER':                   
                use.append([])
                Def.append([i[0][1]])

        elif i[2][0]=='ALLOCATE':
            if i[0][0]=='IDENTIFIER' or i[0][0]=='ADDRESS':                   
                Def.append([i[0][1]])
            else:Def.append([])
            if i[3][0] == 'IDENTIFIER' or i[0][0]=='ADDRESS':
                use.append([i[3][1]])
            else:use.append([])
        
        if index>=1:
            
            Out.append(In[index-1])
        else:
            Out.append(outset)
        
        if len(Out)==0:oo=[]
        else: oo=Out[-1]
        if len(Def)==0:dd=[]
        else: dd=Def[-1]
        if len(use)==0:uu=[]
        else: uu=use[-1]

        #print "### %-15s %-15s  %-15s" % (uu,oo,dd)
##        print "$   ",(list(set(uu)|(set(oo)-set(dd))))
        In.append(list(set(uu)|(set(oo)-set(dd))))

    ind=len(use)-1

##
##    for i in range(0,len(Def)):
##          print "Def ",Def[i],"Use  ",use[i]
    
##    
##    print "In list",In
    blocksegment.reverse()
    dicto1={}
    In.reverse() 
    for var in In:
        for elem in var:
            if elem not in dicto1:
                dicto1[elem]=[]
    
    for var in In:
        if var==[]:
            continue
        else:
            for elem in var:
                for elem2 in var:
                    if elem2 != elem and elem2 not in dicto1[elem]:
                        dicto1[elem].append(elem2)

    return dicto1

#---------------------------------------------------        


def InFun(tempindex,UseList,DefList,Outset):
    In=set()
    In = UseList[tempindex] | (Outset[tempindex]-DefList[tempindex])
    return In

def OutFun(tempindex,InList,succdict,block):
    #print tempindex
    tempsucc=[]
    temp=set()
    out=set()
    tempsucc=succdict.get(tempindex)
    if(tempsucc!=None):
        for i,val in enumerate(tempsucc):
            temp=temp|InList[val] 
        out=temp
    return out

def labeldictionary(imcode,block):

    labeldict={}
    line_count=-1
    for i in imcode:
        line_count+=1
        if i[0][0]=='LABEL':
            for j in block:
                bf,bl=j
                if line_count  in range(bf,bl+1):
                    labeldict[i[0][1]]=j
    return labeldict



def separatefunctions(imcode,stable,addr,arrayt):

#-------Step no 1 : Separating Each Function and then Sending Each Function to liveness Analysis ... 
    i_line=-1
    functionalblock=[]
    block=[]
    labeldict={}
    succdict={}
    finaldict={}
    coloredg={}
    blocklastlist=[]
    funcode=[]
    outputcode=[]
    for i in imcode:
        i_line+=1
##        print i_line,i
        
        if i[1][0]=='FUNCTION':
            start_func=i_line
        if i[0][0]=='JR':
            end_func=i_line+1
##            print "------------------------------------"
            functionalset=start_func,end_func
            functionalblock.append(functionalset)
    #print "functionalblock",functionalblock
    for start,end in functionalblock:
        #print functionalblock

        block,labeldict,blocklastlist=make_blocks(imcode[start:end],arrayt) 

        block,succdict=find_successor(imcode[start:end],block,labeldict,blocklastlist,arrayt)

        finaldict,block=performliveness(block,imcode[start:end],succdict,arrayt)
        
        success,coloredg=make_graphcoloring_of_each_function(finaldict,arrayt)

        

        success,coloredg,funcode,stable,addr=spilling(success,coloredg,imcode[start:end],block,stable,addr,arrayt)

        funcode=register_plugging(funcode,coloredg)

        outputcode.extend(funcode)
            
##        print start,end
    return outputcode,stable,addr
    

def make_blocks(imcode,arrayt):

#-------Step no 2 : You make a block of avaliable piece of code to you......[block-making]-------------------------------------------------
        ind=0
	blocklastlist=[]
	blockfirst=0
	blocklast=0
	block=[]
	
	for i in imcode:
                #print "111",i
		if i[0][0] in ['JUMP','JIFF','JIFT']:
			if ind not in blocklastlist: blocklastlist.append(ind)
		if i[0][0] in ['LABEL']:
			if ind-1 not in blocklastlist:
                            if ind-1 > 0:
                                blocklastlist.append(ind-1)
		ind+=1
	if (len(imcode)-1)not in blocklastlist:blocklastlist.append(len(imcode)-1)
	
	temp=0
	bkno=0
	for b in blocklastlist:
		
		blockfirst=temp
		blocklast=b
		blockset=blockfirst,blocklast
		temp=b+1
		bkno+=1
		block.append(blockset)
    
            
#-------------- Maintain a dictionary with label as key and block as value. -------------------#
        labeldict={}
        labeldict=labeldictionary(imcode,block)  
        
        return block,labeldict,blocklastlist
####------------------------------------------------------------------------------##########
        #################-------------------------------------------####################



def find_successor(imcode,block,labeldict,blocklastlist,arrayt):
     
#-------------------Finding Successors using dictionary and the blocklist----------------------#
        succ=[]
        succdict={}
        jiffsucc=[]
        line_count=-1
        presentblock=0
        jumpsucc=[]
        simpsucc=[]
        jiftsucc=[]
        j=[]
        jalsucc=[]
        jruscc=[]
        nextjalsucc=[]
       
        for i in imcode:
            line_count+=1
            if i[0][0]=='JIFT':
                #---------------For true condition ---------#
                for j in block:
                    bf,bl=j
                    if line_count in range(bf,bl+1):
                        jiftsucc.append(j)
                        presentblock=j
                #--------------For False Condition------------#
                    if line_count+1 in range(bf,bl+1):
                        jiftsucc.append(j)
                succ.append(set(jiftsucc))
                succdict[presentblock]=set(jiftsucc)
  


            if i[0][0]=='JIFF':
                #----------for true condition--------------#
                jiffsucc=[]
                for j in block:
                    bf,bl=j
                    if line_count in range(bf,bl+1):
                        presentblock=j
                    if line_count+1 in range(bf,bl+1):
                        jiffsucc.append(j)
                        
                #----for  false condition --------------#
                for keys in labeldict:
                    if i[1][1] in keys:
                        jiffsucc.append(labeldict.get(i[1][1]))
                        succ.append(set(jiffsucc))
                        succdict[presentblock]=set(jiffsucc)
                
            if i[0][0]=='JUMP':
                jumpsucc=[]
                for j in block:
                    
                    bf,bl=j
                    if line_count in range(bf,bl+1):
                        presentblock=j
                for keys in labeldict:
                    if i[1][1] in keys:
                        jumpsucc.append(labeldict.get(i[1][1]))
                        succ.append(set(jumpsucc))
                        succdict[presentblock]=set(jumpsucc)
                        
            if line_count in blocklastlist and (i[0][0] not in [ 'JUMP','JIFF','JIFT']):
                simpsucc=[]
                for j in block:
                    bf,bl=j
                    if line_count+1 in range(bf,bl+1):
                        presentblock=j
                        simpsucc.append(j)
                        succ.append(set(simpsucc))
                        succdict[presentblock]=set(simpsucc)
                        
                       
                    if line_count==len(imcode)-1 and line_count==bl:
                        presentblock=j
                        simpsucc.append(j)
                        succ.append(set(simpsucc))
                        succdict[presentblock]=set(simpsucc)
                        break      

        

#------------------Making Dictionary: Block No : Succ's Block No -------------------------------------------------------------#
##        print "block",block
        blockdict={}
        for i,val in enumerate(block):
            blockdict[val]=i

#---------------Making dictionary of succ where block number is key with successors( in terms of block numbers)as its values----#
        succdict={}
        templist=[]
        ss=[]
        for i,val in enumerate(succ):
            templist=list(val)
            ss=[]
            for k in templist:
                
                for keys in blockdict:
                    if k == keys:
                        ss.append(blockdict.get(k))    
                succdict[i]=ss
        if len(succ)-1 in succdict.keys():
            if succdict[len(succ)-1] == [len(succ)-1]:
                succdict[len(succ)-1] = None
        return block,succdict



    
def performliveness(block,imcode,succdict,arrayt):
#-------------------Call to Liveness analysis------------------ #
        dicto={}
        dictolist=[]
        DefList=[]
        UseList=[]
        Def=[]
        use=[]
        u={}
        for i in block:
            bf,bl=i
            blocksegment=imcode[bf:bl+1]
            Def=[]
            Use=[]
            Def,use=liveness(blocksegment)
            DefList.append(set(Def))
            UseList.append(set(use))    
##        print "Def",DefList
##        print "use",UseList
#----------------Making In, Out of the list ------------------------#

        block.reverse()
        Inset=[]
        PrevInset=[]
        PrevOutset=[]
        Outset=[]
        for i,val in enumerate(block):
            Inset.append(set())
            Outset.append(set())
    
        noofblocks=len(block)-1
        for i,val in enumerate(block):
            tempindex=len(block)-i-1
            #Inset.reverse()
            Out1=OutFun(tempindex,Inset,succdict,block)
            Outset[noofblocks]=Out1
            
            in1=InFun(tempindex,UseList,DefList,Outset)
            Inset[noofblocks]=in1
            #print "oooooooooo",noofblocks,val,Inset,Inset[noofblocks]
            noofblocks-=1



        resultc = True
        while resultc:
            PrevInset=[]
            PrevOutset=[]
            for i in range(len(block)):
                PrevInset.append(Inset[i])
                Inset[i]=set()
                PrevOutset.append(Outset[i])
                Outset[i]=set()
            #input()
            noofblocks=len(block)-1
            for i,val in enumerate(block):
                tempindex=len(block)-i-1
                #Inset.reverse()
                Out1=OutFun(tempindex,PrevInset,succdict,block)
                Outset[noofblocks]=Out1
                
                in1=InFun(tempindex,UseList,DefList,Outset)
                Inset[noofblocks]=in1
                #print "oooooooooo",noofblocks,val,Inset,Inset[noofblocks]
                noofblocks-=1
            if (PrevInset==Inset) and (PrevOutset==Outset):
                resultc = False
        block.reverse()

#-----------Finding In's statement wise to send to graph coloring - -------------------------------------------------#

        
        dicto1={}
        finaldict={}
        outlist=[]
        coloredg={}
        for x,i in enumerate(block):
            bf,bl=i
            blocksegment=imcode[bf:bl+1]
            outlist=list(Outset[x])
            
            dicto1=liveness_statement(blocksegment,outlist)
            ky=dicto1.keys()
            for key in dicto1.keys():
                if key in finaldict.keys():
                    finaldict[key]=list(set(finaldict[key])|set(dicto1[key]))
                else:
                    finaldict[key]=dicto1[key]
##        print finaldict
        return finaldict,block
    
def make_graphcoloring_of_each_function(finaldict,arrayt):
#------------------------- making graph of each block----------------------------------------------##
        success,coloredg=GC.k_color(finaldict,16,arrayt)
        return success,coloredg

#--------------------------------------------------------------------------------------------------#####

        
def spilling(success,coloredg,imcode,block,stable,addr,arrayt):
      
      labeldict={}
      blocklastlist=[]
      succdict={}
      finaldict={}
      
      while success != True:
                spill=coloredg.keys()[0]
##                print coloredg
##		print "Spill:",spill
##		input()
		indx=-1
		t=1
		
		while indx < len(imcode)-1:
			indx+=1
			if imcode[indx][0][1] in ['INT','BOOL']:pass
			elif ['IDENTIFIER',spill] == imcode[indx][0] :
				imcode[indx][0]=['IDENTIFIER','$s0']
				indx+=1
				imcode.insert(indx,[['NOP','None'],['IDENTIFIER','$s0'],['SW','store'],['ADDR','var'+str(addr)]])
				stable.append('var'+str(addr))
				t+=1
			elif ['ADDRESS',spill] == imcode[indx][0] :
				imcode[indx][0]=['ADDRESS','$s0']
				indx+=1
				imcode.insert(indx,[['NOP','None'],['ADDRESS','$s0'],['SW','store'],['ADDR','var'+str(addr)]])
				stable.append('var'+str(addr))
				t+=1
			elif ['IDENTIFIER',spill] in imcode[indx] or ['ADDRESS',spill] in imcode[indx]:
				if imcode[indx][1][1]==spill:
				    imcode.insert(indx,[[imcode[indx][1][0],spill],['NOP','None'],['LW','load'],['ADDR','var'+str(addr)]])
                                    indx+=1
				    t+=1
				elif imcode[indx][3][1]==spill:
				    imcode.insert(indx,[[imcode[indx][3][0],spill],['NOP','None'],['LW','load'],['ADDR','var'+str(addr)]])
				    indx+=1
				    t+=1

              
            #---send to that part of code that ameya wants to send.....
                block,labeldict,blocklastlist=make_blocks(imcode,arrayt) 
                
                block,succdict=find_successor(imcode,block,labeldict,blocklastlist,arrayt)

##                for kkk in imcode:
##                    print ">>>>>",kkk
                
                finaldict,block=performliveness(block,imcode,succdict,arrayt)
            
                success,coloredg=make_graphcoloring_of_each_function(finaldict,arrayt)

            #-remaining part of spilling .... =============#       
		addr+=1
              
      return success,coloredg,imcode,stable,addr
    
#---------------------------------------------------------------------------------------
#...........................PLUGGING IN REGISTERS.......................................
##	print "dicccccccccccc ",
##	for i in coloredg.keys():
##            print i, coloredg[i]

def register_plugging(imcode,coloredg):

        idx=-1
        for i in imcode:
            idx+=1
            for tok in i:
                if tok[0]=='IDENTIFIER' and tok[1]!='$s0':
                    if  coloredg.has_key(tok[1]):
                        i[i.index(tok)]=['IDENTIFIER',coloredg[tok[1]]]
                    else:
                        i[i.index(tok)]=['IDENTIFIER','$s1']
                elif tok[0]=='ADDRESS' and tok[1]!='$s0':
                    if  coloredg.has_key(tok[1]):
                        i[i.index(tok)]=['ADDRESS',coloredg[tok[1]]]
                    else:
                        i[i.index(tok)]=['ADDRESS','$s1']

        return imcode

##        for i in imcode:
##            print "-------",i
#------------------------------Final Code Generation ------------------------------------------------#    
        
        
