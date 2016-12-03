f=open('part-00000','rb')
f2=open('inter','w')
count=0
g=""
for line in f:
    a=line.decode('UTF-8').strip().split('\t')[1]
    g+=str(count)+'\t'+a+'\n'
    count+=1
    
g.replace('[','')
g.replace(']','')
g.replace(',','\t')
f2.write(g)
