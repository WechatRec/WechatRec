Max = 10000000
a = [False] * Max
p = []
for i in xrange(2, Max):
    if not a[i]:
        p.append(i)
        for j in xrange(i + i, Max, i):
            a[j] = True
print p
