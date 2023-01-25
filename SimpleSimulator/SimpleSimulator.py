import sys

s = sys.stdin.read()
line = s.split("\n")
l1 = []
for i in line:
    if i != '':
        l1.append(i)


# with open("coproject.txt", 'r') as f:
#     l1 = []
#     for line in f:
#         a = line.replace("\n", "")
#         l1.append(a)

n = len(l1)

A = {'add' : '10000', 'sub' : '10001', 'mul' : '10110', 'xor' : '11010', 'or' : '11011', 'and' : '11100'}
B = {'mov' : '10010', 'ls' : '11001', 'rs' : '11000'}
C = {'mov' : '10011', 'div' : '10111', 'not' : '11101', 'cmp' : '11110'}
D = {'ld' : '10100', 'st' : '10101'}                                                                                  #dictionary for ISA types
E = {'jmp' : '11111', 'jlt' : '01100', 'jgt' : '01101', 'je' : '01111'}
F = {'hlt' : '01010'}

A2 = {'10000' : 'add', '10001' : 'sub', '10110' : 'mul', '11010' : 'xor', '11011' : 'or', '11100' : 'and'}
B2 = {'10010' : 'mov', '11001' : 'ls', '11000' : 'rs'}
C2 = {'10011' : 'mov', '10111' : 'div', '11101' : 'not', '11110' : 'cmp'}
D2 = {'10100' : 'ld', '10101' : 'st'}                                                                                  #dictionary for ISA types
E2 = {'11111' : 'jmp', '01100' : 'jlt', '01101' : 'jgt', '01111' : 'je'}
F2 = {'01010' : 'hlt'}

reg = {'000' : 'R0', '001' : 'R1', '010' : 'R2', '011' : 'R3', '100' : 'R4', '101' : 'R5', '110' : 'R6', '111' : 'FLAGS'}

value = {'R0' : '0', 'R1' : '0', 'R2' : '0', 'R3' : '0', 'R4' : '0', 'R5' : '0', 'R6' : '0', 'FLAGS' : '0'}

variable_val = []

for i in l1:
    if i[:5] == D['ld'] or i[:5] == D['st']:
        dec = int(i[8:16], 2)
        variable_val.append(dec-n)
q = sorted(variable_val)
p = list(set(q))

m = len(p)
i = 0
while i < m:
    if p[i] == 0:
        i += 1
        continue
    elif i == m-1:
        break
    elif p[i] != p[i+1]-1:
        p.insert(i+1, 0)
        m += 1
    i += 1

o = len(p)

var_bin = []

for i in range(o):
    var_bin.append('0')


def dectobin(i):
    bi = bin(i).replace("0b", "")
    y = [ch for ch in bi]
    count = len(y)
    f = []
    for i in range(8-count):
        f.append('0')
    h = f + y
    r = ''.join(h)
    return r

def dectobinno(i):
    bi = bin(i).replace("0b", "")
    y = [ch for ch in bi]
    count = len(y)
    f = []
    for i in range(16-count):
        f.append('0')
    h = f + y
    r = ''.join(h)
    return r

def float_to_bin(num, places): 
   
    num = str(num)
    whole, decimal = num.split(".")
    whole = int(whole)
    decimal = int(decimal)
    res = bin(whole)
    res = res.lstrip("0b")
    res = res + "."
    for i in range(places):
        decimal = float("0." + str(decimal))
        decimal = str(decimal * 2)
        whole, decimal = decimal.split(".")
        decimal = int(decimal)
        res += whole
    list = [char for char in res]
    if '.' in list:
        n = list.index('.')
        list.remove('.')
        e = n-1
    else:
        e = len(list) - 1
    list.insert(1, '.')
    new = ''.join(list)
    bi = bin(e).replace("0b", "")
    bis = [char for char in bi]
    if len(bis) < 3:
        for i in range(3-len(bis)):
            bis.insert(0, '0')
    bi = ''.join(bis)
    l = []
    arr = [char for char in list]
    if len(arr) < 7:
        for i in range(2, len(arr)):
            l.append(arr[i])
        for i in range(7-len(arr)):
            l.append('0')
    else:
        for i in range(2, 7):
            l.append(arr[i])
    m = ''.join(l)
    final = bi + m
    final = int(final, 2)
    
    return final


def typeA(x):
    if int(value['FLAGS']) > 0:
        value['FLAGS'] = '0'
    opcode = x[:5]

    a = x[7:10]
    b = x[10:13]
    c = x[13:16]

    ra = reg[a]
    rb = reg[b]
    rc = reg[c]

    if opcode == A['add']:
        value[rc] = str(int(value[ra]) + int(value[rb]))
    elif opcode == A['sub']:
        value[rc] = str(int(value[ra]) - int(value[rb]))
    elif opcode == A['mul']:
        value[rc] = str(int(value[ra]) * int(value[rb]))
    elif opcode == A['xor']:
        value[rc] = str(int(value[ra]) ^ int(value[rb]))
    elif opcode == A['or']:
        value[rc] = str(int(value[ra]) | int(value[rb]))
    elif opcode == A['and']:
        value[rc] = str(int(value[ra]) & int(value[rb]))

    if int(value[rc]) > 65535 or int(value[rc]) < 0:
        value['FLAGS'] = '8'
        if opcode == A['add'] or opcode == A['mul']:
            while int(value[rc]) > 65535:
                value[rc] = str(int(value[rc]) - 65536)
        elif opcode == A['sub']:
            value[rc] = '0'

def typeB(x):
    if int(value['FLAGS']) > 0:
        value['FLAGS'] = '0'
    opcode = x[:5]

    c = x[5:8]
    imm = x[8:16]

    rc = reg[c]

    if opcode == B['mov']:
        value[rc] = str(int(imm, 2))
    elif opcode == B['ls']:
        dec = int(imm, 2)
        bi = bin(int(value[rc])).replace("0b","")
        y = [ch for ch in bi]
        count = 0
        for i in y:
            count += 1
        m = []
        if count < 8:
            for i in range(8-count):
                m.append('0')
        h = ''.join(m + y)
        if dec < 8:
            p = []
            for i in range(dec):
                p.append('0')

            r = h[:8-dec]
            s = [ch for ch in r]
            f = ['00000000']
            q = f + s + p

            t = ''.join(q)
        else:
            p = ['00000000']
            r = h.replace(h[:8], "")
            s = [ch for ch in r]
            f = ['00000000']
            q = f + s + p

            t = ''.join(q)

        value[rc] = str(int(t, 2))
    elif opcode == B['rs']:
        dec = int(imm, 2)
        bi = bin(int(value[rc])).replace("0b","")
        y = [ch for ch in bi]
        count = 0
        for i in y:
            count += 1
        m = []
        if count < 8:
            for i in range(8-count):
                m.append('0')
        h = ''.join(m + y)
        if dec < 8:
            p = []
            for i in range(dec):
                p.append('0')

            r = h[:-dec]
            s = [ch for ch in r]
            f = ['00000000']
            q = f + p + s

            t = ''.join(q)
        else:
            p = ['00000000']
            r = h.replace(h[:8], "")
            s = [ch for ch in r]
            f = ['00000000']
            q = f + p + s

            t = ''.join(q)

        value[rc] = str(int(t, 2))

def typeC(x):
    opcode = x[:5]

    b = x[10:13]
    c = x[13:16]

    rb = reg[b]
    rc = reg[c]

    if opcode == C['mov']:
        value[rc] = value[rb]
        if int(value['FLAGS']) > 0:
            value['FLAGS'] = '0'
    elif opcode == C['div']:
        if int(value['FLAGS']) > 0:
            value['FLAGS'] = '0'
        value['R0'] = str((int(value[rb])) // (int(value[rc])))
        value['R1'] = str((int(value[rb])) % (int(value[rc])))
    elif opcode == C['not']:
        if int(value['FLAGS']) > 0:
            value['FLAGS'] = '0'
        bi = bin(int(value[rb])).replace("0b","")
        y = [ch for ch in bi]
        s = []
        for i in range(16-len(y)):
            s.append('0')
        y = s + y
        for i in range(len(y)):
            if y[i] == '0':
                y[i] = '1'
            else:
                y[i] = '0'
        t = ''.join(y)
        value[rc] = str(int(t, 2))
    elif opcode == C['cmp']:
        if value['FLAGS'] == '8':
            value['FLAGS'] = '0'
        if int(value[rb]) < int(value[rc]):
            value['FLAGS'] = '4'
        elif int(value[rb]) > int(value[rc]):
            value['FLAGS'] = '2'
        elif int(value[rb]) == int(value[rc]):
            value['FLAGS'] = '1'

def typeD(x):
    if int(value['FLAGS']) > 0:
        value['FLAGS'] = '0'
    opcode = x[:5]

    c = x[5:8]

    rc = reg[c]

    if opcode == D['ld']:

        ld = x[8:16]
        dec = int(ld, 2)
        place = dec - n

        index = p.index(place)

        value[rc] = var_bin[index]
    elif opcode == D['st']:

        st = x[8:16]
        dec = int(st, 2)
        place = dec - n

        index = p.index(place)

        var_bin[index] = value[rc]

def typeE(x, line):
    opcode = x[:5]

    add = x[8:16]

    r = 0
    if opcode == E['jmp']:
        r += int(add, 2)
    elif opcode == E['jlt']:
        if value['FLAGS'] == '4':
            r += int(add, 2)      
            value['FLAGS'] = '0'
        else:
            r += line+1
            value['FLAGS'] = '0'
    elif opcode == E['jgt']:
        if value['FLAGS'] == '2':
            r += int(add, 2)      
            value['FLAGS'] = '0'
        else:
            r += line+1
            value['FLAGS'] = '0'
    elif opcode == E['je']:
        if value['FLAGS'] == '1':
            r += int(add, 2)      
            value['FLAGS'] = '0'
        else:
            r += line+1
            value['FLAGS'] = '0'
    s.append(r)
    return r

def typeF(x):
    if int(value['FLAGS']) > 0:
        value['FLAGS'] = '0'

listofreg = []


i = 0
while i<n:
    s = []
    if l1[i][:5] in A2:
        typeA(l1[i])
        listperline = []
        line = dectobin(i)
        listperline.append(line)
        for j in range(7):
            listperline.append(dectobinno(int(value['R'+str(j)])))
        listperline.append(dectobinno(int(value['FLAGS'])))
        listofreg.append(listperline)
        i += 1
    elif l1[i][:5] in B2:
        typeB(l1[i])
        listperline = []
        line = dectobin(i)
        listperline.append(line)
        for j in range(7):
            listperline.append(dectobinno(int(value['R'+str(j)])))
        listperline.append(dectobinno(int(value['FLAGS'])))
        listofreg.append(listperline)
        i += 1
    elif l1[i][:5] in C2:
        typeC(l1[i])
        listperline = []
        line = dectobin(i)
        listperline.append(line)
        for j in range(7):
            listperline.append(dectobinno(int(value['R'+str(j)])))
        listperline.append(dectobinno(int(value['FLAGS'])))
        listofreg.append(listperline) 
        i += 1
    elif l1[i][:5] in D2:
        typeD(l1[i])
        listperline = []
        line = dectobin(i)
        listperline.append(line)
        for j in range(7):
            listperline.append(dectobinno(int(value['R'+str(j)])))
        listperline.append(dectobinno(int(value['FLAGS'])))
        listofreg.append(listperline) 
        i += 1
    elif l1[i][:5] in E2:
        typeE(l1[i], i)
        listperline = []
        line = dectobin(i)
        listperline.append(line)
        for j in range(7):
            listperline.append(dectobinno(int(value['R'+str(j)])))
        listperline.append(dectobinno(int(value['FLAGS'])))
        listofreg.append(listperline)
        i = s[0]
    elif l1[i][:5] in F2:
        typeF(l1[i])
        listperline = []
        line = dectobin(i)
        listperline.append(line)
        for j in range(7):
            listperline.append(dectobinno(int(value['R'+str(j)])))
        listperline.append(dectobinno(int(value['FLAGS'])))
        listofreg.append(listperline) 
        i += 1






last = []
for i in range(len(var_bin)):
    last.append(dectobinno(int(var_bin[i])))

for i in listofreg:
    h = ' '.join(i)
    print(h)

for i in l1:
    print(i)

for i in last:
    print(i)

r = '0000000000000000'
g = 256 - (len(l1) + len(last))
for i in range(g):
    print(r)

