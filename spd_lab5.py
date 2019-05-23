from copy import deepcopy


def file_reader(name):
    """generator zwracjacy zawartosc danych z pliku data"""
    with open(name, encoding='utf8') as file:
        lines = file.readlines()
        start = re.compile(r'data\.\d+:')
        end = re.compile(r'\n')
        flag = False
        for line in lines:
            if re.match(start, line):
                data = []
                flag = True
                continue
            if re.fullmatch(end, line):
                flag = False
            if flag:
                tmp = list(map(int, line.split()))
                data.append(tmp)
                if data[0][0] + 1 == len(data):
                    yield {key: value for key, value in enumerate(data[1:])}
        return StopIteration


def schrage(data):
    zadania = OrderedDict(sorted(data.items(), key=lambda x: x[0]))
    gotowy = OrderedDict()
    kolejnosc = []
    schlodzenie = []
    t = min(zadania.values(), key=lambda x: x[0])[0]

    while gotowy or zadania:
        dostepne = OrderedDict(i for i in zadania.items() if i[1][0] <= t)
        gotowy.update(dostepne)
        for i in dostepne.keys():
            del zadania[i]
        if not gotowy:
            t = min(zadania.values(), key=lambda x: x[0])[0]
        else:
            dlugosc = max(gotowy.items(), key=lambda x: x[1][2])
            del gotowy[dlugosc[0]]
            kolejnosc.append(dlugosc[0])
            t += dlugosc[1][1]
            schlodzenie.append((kolejnosc[-1], t + dlugosc[1][2]))

    return kolejnosc, max(schlodzenie, key=lambda x: x[1])[1],\
        sorted(schlodzenie, key=lambda x: x[1])[-1][0]
        


def PTM_Shrage(data):
    zadania = OrderedDict(sorted(data.items(), key=lambda x: x[0]))
    zadania_copy = deepcopy(zadania)
    gotowy = OrderedDict()
    t = 0
    cmax = 0
    l = None

    while gotowy or zadania:
        while zadania and min(zadania.values(), key=lambda x: x[0])[0] <= t:
            tmp = min(zadania.items(), key=lambda x: x[1][0])
            gotowy.update({tmp[0]: tmp[1]})
            del zadania[tmp[0]]
            if l is not None:
                if tmp[1][2] > zadania_copy[l][2]:
                    zadania_copy[l][1] = t - tmp[1][0]
                    t = tmp[1][0]
                    if zadania_copy[l][1] > 0:
                        gotowy.update({l: zadania_copy[l]})
        if not gotowy:
            t = min(zadania.values(), key=lambda x: x[0])[0]
        else:
            tmp = max(gotowy.items(), key=lambda x: x[1][2])
            del gotowy[tmp[0]]
            l = tmp[0]
            t += tmp[1][1]
            cmax = max(cmax, t + tmp[1][2])

    return cmax

    
def obtain_C(data, path):
    jobs = OrderedDict((x, data[x]) for x in path)
    qb = jobs[path[-1]][2]
    for c in path[-2::-1]:
        if jobs[c][2] < qb:
            return c
    return None


def variables(data, path):
    jobs = OrderedDict((x, data[x]) for x in path)
    rk = min(jobs[x][0] for x in path)
    qk = min(jobs[x][2] for x in path)
    pk = sum(jobs[x][1] for x in path)

    return rk, qk, pk

def CRIT(data, kolejnosc, b):
    jobs = OrderedDict((x, data[x]) for x in kolejnosc)
    crit = [kolejnosc[0]]
    done = sum(jobs[kolejnosc[0]][:-1])
    for i in kolejnosc[1:kolejnosc.index(b)+1]:
        if jobs[i][0] > done:
            crit.clear()
            crit.append(i)
            done = sum(jobs[i][:-1])
        else:
            crit.append(i)
            done += jobs[i][1]
    return crit


def CMAX(data, kolejnosc):
    Full_time = sum(data[kolejnosc[0]][:-1])
    Qk = [sum(data[kolejnosc[0]][:-1]) + data[kolejnosc[0]][2]]
    for i in kolejnosc[1:]:
        if data[i][0] > Full_time:
            Full_time = sum(data[i][:-1])
            Qk.append(Full_time + data[i][2])
        else:
            Full_time += data[i][1]
            Qk.append(Full_time + data[i][2])
    return max(Qk)


def do_Carlier(data):


    jobs = deepcopy(data)
    distribution, U, b = schrage(jobs)
    try:
        if U < Ub:
            Ub = U
            done = distribution
    except UnboundLocalError:
        Ub = U
        done = distribution
    path = CRIT(jobs, distribution, b)

    real_C = obtain_C(jobs, path)
    if real_C is None:
        return done
    idxc = path.index(real_C)
    k = path[idxc+1:]

    rk, qk, pk = variables(jobs, k)

    rpc = jobs[real_C][0]
    jobs[real_C][0] = max(rpc, rk + pk)

    lb = PTM_Shrage(jobs)
    lb = max(sum([rk, qk, pk]), sum(variables(jobs, path[idxc:])), lb)
    if lb < Ub:
        return do_Carlier(jobs)
    jobs[real_C][0] = rpc

    QPC = jobs[real_C][2]
    jobs[real_C][2] = max(QPC, qk + pk)

    lb = PTM_Shrage(jobs)
    lb = max(sum([rk, qk, pk]), sum(variables(jobs, path[idxc:])), lb)
    if lb < Ub:
        return do_Carlier(jobs)
    jobs[real_C][2] = QPC
    return done


samples = file_reader("schr.data_n.txt")
for i, sample in enumerate(samples):
    if i == i:
        last = do_Carlier(sample)
        print(last)
        print(CMAX(sample, last))
