#-----------------------------------------------------------------------------    
#....................................Graph Coloring...........................
#.............................................................................

def spill_priority(spillq,arrayt):
    var=''
    maxd = 0
    for i in spillq:
        if maxd<spillq[i]:
            maxd=spillq[i]
            var=i
    return {var:maxd}


def color_it(color,Graph,v):
    regs= reg =['$t0', '$t1','$t2', '$t3', '$t4', '$t5', '$t6','$t7', '$t8', '$t9', '$s2','$s3','$s4','$s5','$s6','$s7']
    colors = []
    for u,e in Graph.iteritems():
        if v in e:
            colors += [color[u]]
        else:
            colors += []
    for r in regs:
        if r not in colors:
            return r
        

def k_color(Graph,k,arrayt):
    stack = []
    Vertices = {}
    color = {}
    spillit={}
    fail=False
    for (v,e) in Graph.iteritems():
        Vertices[v] = len(e)
        color[v] = []
    for (v,d) in Vertices.iteritems():
        
        if d < k:
            edges = Graph[v]
            vertices = Vertices[v]
            del Graph[v]
            #del Vertices[v]
            stack.append((v,edges))
        else:
            spillit[v]= d
            fail=True
    
    if fail:
        return False,spill_priority(spillit,arrayt)
    else:
        if not Graph:
            while stack:
                (v,e) = stack.pop()
                Graph[v] = e
                Vertices[v] = len(e)
                r = color_it(color,Graph,v)
                color[v] = r
        return True,color

