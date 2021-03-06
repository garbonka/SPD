import time

def makespan(per, czas, maszyny):

    c_max = [[0]*(len(per)+1) for i in range(maszyny)]
    for j in range(1, len(per)+1): # wiersze
        c_max[0][j] = c_max[0][j - 1] + czas[0][per[j - 1]]

    for i in range(1, maszyny): #kolumny
        for j in range(1, len(per)+1):
            c_max[i][j] = max(c_max[i - 1][j], c_max[i][j - 1]) + czas[i][per[j - 1]] #schodzi drabinkowo daje max
    return c_max

def permute(xs, low=0):
    if low + 1 >= len(xs):
        yield xs
    else:
        for p in permute(xs, low + 1):
            yield p
        for i in range(low + 1, len(xs)):
            xs[low], xs[i] = xs[i], xs[low]
            for p in permute(xs, low + 1):
                yield p 
            xs[low], xs[i] = xs[i], xs[low]
            
dane = [0,1,2,3,4]
czas = [[4,4,10,6,2], [5,1,4,10,3]]
maszyny = 2
zadania = 5

for p in permute(dane):
    print(" {} cmax {}".format(p,makespan(p, czas, maszyny)[maszyny-1][zadania] ))
    
