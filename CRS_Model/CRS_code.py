from gurobipy import*
DMU=['A','B','C','D','E']
h={}
for k in DMU:
    
    I=2
    O=3
    #X、Y為各DMU的產出與投入
    DMU,X,Y=multidict({('A'):[[11,14],[2,2,1]],('B'):[[7,7],[1,1,1]],('C'):[[11,14],[1,1,2]],('D'):[[14,14],[2,3,1]],('E'):[[14,15],[3,2,3]]})
    v={}
    u={}
    
    m=Model("CRS_System_DEA")
    
    for i in range(I):
        v[i]=m.addVar(vtype=GRB.CONTINUOUS,name="v_%d"%i,lb=0.0001)
    
    for r in range(O):
        u[r]=m.addVar(vtype=GRB.CONTINUOUS,name="u_%d"%r,lb=0.0001)
    
    m.update()
    
    m.setObjective(quicksum(u[r]*Y[k][r] for r in range(O)),GRB.MAXIMIZE)
        
    m.addConstr(quicksum(v[i]*X[k][i] for i in range(I))==1)
    for j in DMU:
        m.addConstr(quicksum(u[r]*Y[j][r] for r in range(O))-quicksum(v[i]*X[j][i] for i in range(I))<=0)
    
    m.optimize()
    h[k]="The efficiency of DMU %s:%4.3g"%(k,m.objVal)
    
for k in DMU:
    print (h[k])