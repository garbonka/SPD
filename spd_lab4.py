from collections import OrderedDict
import re

def file_reader():
    
    with open("schr.data_n.txt", encoding='utf8') as file:
        lines = file.readlines()
        start = re.compile(r'data\.\d:')
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
    end = 0
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
        schlodzenie.append(t + dlugosc[1][2])

    return kolejnosc, max(schlodzenie)




przyklady = file_reader()
for i, przyklad in enumerate(przyklady):
    if i == i:
        result, cmax = schrage(przyklad)
        print(result)
        print(cmax)
