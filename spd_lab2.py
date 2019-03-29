import numpy

# read the data from file
def read_file(filename):
    with open(filename, "r") as plik:
        maszyny = int(plik.readline())
        zadania = int(plik.readline())
        czesc = [[0]*(zadania) for i in range(maszyny)]
        for i in range(maszyny):
            p_i = plik.readline().split()
            for j in range(zadania):
                czesc[i][j] = int(p_i[j])
                
    czesc=numpy.transpose(czesc)
    temp = maszyny
    maszyny = zadania
    zadania = temp
    return maszyny, zadania, czesc
#wiersze z kolumany bo tyd temu


    
def makespan(per, sum_czas, maszyny):
    c_max = [[0]*(len(per)+1) for i in range(maszyny)]

    for j in range(1, len(per) + 1):
        c_max[0][j] = c_max[0][j - 1] + sum_czas[0][per[j - 1]]

    for i in range(1, maszyny):
        for j in range(1, len(per) + 1):
            c_max[i][j] = max(c_max[i - 1][j], c_max[i][j - 1]) + sum_czas[i][per[j - 1]]
    return c_max



def czas_finalny(index_job, dane, maszyny): #krok 2 posortowane nierosnąco
    sum_f = 0
    for i in range(maszyny):
        sum_f += dane[i][index_job]
    return sum_f



def kolej_neh(dane, maszyny, zadania): #porzadkowanie kolejnosci
    per = [] 
    for j in range(zadania):
        per.append(j)
    return sorted(per, key=lambda x: czas_finalny(x, dane, maszyny), reverse=True)


def insertion(sequence, index_position, value):  # wstawianie zadania na "value"
    new_seq = sequence[:]
    new_seq.insert(index_position, value)
    return new_seq


def neh(data, licz_masz, licz_zad):
    kolej_seq = kolej_neh(data, licz_masz, licz_zad)
    seq_current = [kolej_seq[0]]
    for i in range(1, licz_zad):
        min_cmax = float("inf")
        for j in range(0, i + 1):
            tmp_seq = insertion(seq_current, j, kolej_seq[i])
            cmax_tmp = makespan(tmp_seq, data, maszyny)[licz_masz - 1][len(tmp_seq)]
           # print(tmp_seq, cmax_tmp)
            if min_cmax > cmax_tmp:
                best_seq = tmp_seq
                min_cmax = cmax_tmp
        seq_current = best_seq
        #print(seq_current)
    return seq_current, makespan(seq_current, data, maszyny)[maszyny - 1][zadania]


maszyny, zadania, licz_masz = read_file("NEH0.txt")
seq, cmax = neh(licz_masz, maszyny, zadania)
print("Maszyny:", maszyny)
print("Zadania:", zadania)
print(licz_masz)
print("neh:", seq, cmax)
#print (c_max)
#print("\n")



