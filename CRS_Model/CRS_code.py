from gurobipy import*

E={}    
I=2
O=3
#X、Y為各DMU的產出與投入
DMU,X,Y=multidict({('A'):[[11,14],[2,2,1]],('B'):[[7,7],[1,1,1]],('C'):[[11,14],[1,1,2]],('D'):[[14,14],[2,3,1]],('E'):[[14,15],[3,2,3]]})

for r in DMU:
    
    v,u={},{}

    m=Model("CRS_model")
    
    for i in range(I):
        v[r,i]=m.addVar(vtype=GRB.CONTINUOUS,name="v_%s%d"%(r,i),lb=0.0001)
    
    for j in range(O):
        u[r,j]=m.addVar(vtype=GRB.CONTINUOUS,name="u_%s%d"%(r,j),lb=0.0001)
    
    m.update()
    
    m.setObjective(quicksum(u[r,j]*Y[r][j] for j in range(O)),GRB.MAXIMIZE)
        
    m.addConstr(quicksum(v[r,i]*X[r][i] for i in range(I))==1)
    for k in DMU:
        m.addConstr(quicksum(u[r,j]*Y[k][j] for j in range(O))-quicksum(v[r,i]*X[k][i] for i in range(I))<=0)
    
    m.optimize()
    E[r]="The efficiency of DMU %s:%0.3g"%(r,m.objVal)

    
for r in DMU:
    print (E[r])
