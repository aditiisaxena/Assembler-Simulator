import sys

s = sys.stdin.read()
line = s.split("\n")
l1 = []
for i in line:                          #taking indefinite inputs and appending them (list within a list)
    x  = i.split()
    if len(x) != 0:
        l1.append(x)

if len(l1) == 0:
    print("No instruction found")       #error for empty input
    quit()

A = {'add' : '10000', 'sub' : '10001', 'mul' : '10110', 'xor' : '11010', 'or' : '11011', 'and' : '11100'}
B = {'mov' : '10010', 'ls' : '11001', 'rs' : '11000'}
C = {'mov' : '10011', 'div' : '10111', 'not' : '11101', 'cmp' : '11110'}
D = {'ld' : '10100', 'st' : '10101'}                                                                                  #dictionary for ISA types
E = {'jmp' : '11111', 'jlt' : '01100', 'jgt' : '01101', 'je' : '01111'}
F = {'hlt' : '01010'}
float = {'addf' : '00000', 'subf' : '00001', 'movf' : '00010'}
reg = {'R0' : '000', 'R1' : '001', 'R2' : '010', 'R3' : '011', 'R4' : '100', 'R5' : '101', 'R6' : '110', 'FLAGS' : '111'}


variables = []
for i in l1:
    if len(i) == 2:
        if i[0] == 'var':
            variables.append(i[1])                            #storing variables in a list
        else:
            break
    else:
        break

labels = []
for i in l1:
    if len(i) == 5:
        if ':' in i[0]:
            if i[1] in A:
                if i[2] in reg:
                    if i[3] in reg:                           #storing labels in a list
                        if i[4] in reg:
                            labels.append([i[0], (l1.index(i) - len(variables))])
    elif len(i) == 4:
        if ':' in i[0]:
            if i[1] in B:
                if i[2] in reg:
                    if '$' in i[3]:
                        l = []
                        for j in i[3]:
                            if (j.isnumeric()):
                                l.append(j)
                        num = int(''.join(l))
                        if 0<=num<=255:
                            labels.append([i[0], (l1.index(i) - len(variables))])
            elif i[1] in C:
                if i[2] in reg:
                    if i[3] in reg:
                        labels.append([i[0], (l1.index(i) - len(variables))])
            elif i[1] in D:
                if i[2] in reg:
                    if i[3] in variables:
                        labels.append([i[0], (l1.index(i) - len(variables))])
    elif len(i) == 2:
        if ':' in i[0]:
            if i[1] in F:
                labels.append([i[0], (l1.index(i) - len(variables))])



last_list = []

def typeA(list, line):   
    arr = []
    if not(3<len(list)<6):
        print("SyntaxError: Invalid number of parameters for given instruction in line", line)
        quit()
    elif len(list) == 4:
        if list[0] in A:
            arr.append(A[list[0]])
            arr.append('00')
            if list[1] in reg:
                arr.append(reg[list[1]])
                if list[2] in reg:
                    arr.append(reg[list[2]])
                    if list[3] in reg:
                        arr.append(reg[list[3]])
                    else:
                        print("SyntaxError: Invalid register used in line", line)
                        quit()
                else:
                    print("SyntaxError: Invalid register used in line", line)
                    quit()
            else:
                print("SyntaxError: Invalid register used in line", line)
                quit()
        elif list[0] in float:
            arr.append(float[list[0]])
            arr.append('00')
            if list[1] in reg:
                arr.append(reg[list[1]])
                if list[2] in reg:
                    arr.append(reg[list[2]])
                    if list[3] in reg:
                        arr.append(reg[list[3]])
                    else:
                        print("SyntaxError: Invalid register used in line", line)
                        quit()
                else:
                    print("SyntaxError: Invalid register used in line", line)
                    quit()
            else:
                print("SyntaxError: Invalid register used in line", line)
                quit()
        else:
            print("SyntaxError: Invalid placing of instruction in line", line)
            quit()
    else:
        if ':' in list[0]:
            if list[1] in A:
                arr.append(A[list[1]])
                arr.append('00')
                if list[2] in reg:
                    arr.append(reg[list[2]])
                    if list[3] in reg:
                        arr.append(reg[list[3]])
                        if list[4] in reg:
                            arr.append(reg[list[4]])
                        else:
                            print("SyntaxError: Invalid register used in line", line)
                            quit()
                    else:
                        print("SyntaxError: Invalid register used in line", line)
                        quit()
                else:
                    print("SyntaxError: Invalid register used in line", line)
                    quit()
            elif list[1] in float:
                arr.append(float(list[1]))
                arr.append('00')
                if list[2] in reg:
                    arr.append(reg[list[2]])
                    if list[3] in reg:
                        arr.append(reg[list[3]])
                        if list[4] in reg:
                            arr.append(reg[list[4]])
                        else:
                            print("SyntaxError: Invalid register used in line", line)
                            quit()
                    else:
                        print("SyntaxError: Invalid register used in line", line)
                        quit()
                else:
                    print("SyntaxError: Invalid register used in line", line)
                    quit()
            else:
                print("SyntaxError: Invalid placing of instruction in line", line)
                quit()
        else:
            print("SyntaxError: Invalid declaration of label in line", line)
            quit()
    x = ''.join(arr)
    last_list.append(x)


def typeB(list, line):
    arr = []
    if not(2<len(list)<5):
        print("SyntaxError: Invalid number of parameters for given instruction in line", line)
        quit()
    elif len(list) == 3:
        if list[0] in B:
            arr.append(B[list[0]])
            if list[1] in reg:
                arr.append(reg[list[1]])
                if '$' in list[2]:
                    l = []
                    for i in list[2]:
                        if (i.isnumeric()):
                            l.append(i)
                    num = int(''.join(l))
                    if 0<=num<=255:
                        b= []
                        while(num>0):
                            d=num%2
                            b.append(str(d))
                            num=num//2
                        b.reverse()
                        y = ''.join(b)
                        y = [ch for ch in y]
                        count = 0
                        for i in y:
                            count += 1
                        m = []
                        if count < 8:
                            for i in range(8-count):
                                m.append('0')
                        h = m + y
                        binary = ''.join(h)
                        arr.append(binary)
                    else:
                        print("SyntaxError: Imm value exceeding limit in line", line)
                        quit()
                else:
                    print("SyntaxError: Invalid imm syntax in line", line)
                    quit()
            else:
                print("SyntaxError: Invalid register used in line", line)
                quit()
        elif list[0] in float:
            arr.append(float[list[0]])
            if list[1] in reg:
                arr.append(reg[list[1]])
                if '$' in list[2]:
                    l = []
                    for i in list[2]:
                        if (i.isnumeric()):
                            l.append(i)
                    num = int(''.join(l))
                    if 1<=num<=255:
                        b= []
                        while(num>0):
                            d=num%2
                            b.append(str(d))
                            num=num//2
                        b.reverse()
                        y = ''.join(b)
                        y = [ch for ch in y]
                        count = 0
                        for i in y:
                            count += 1
                        m = []
                        if count < 8:
                            for i in range(8-count):
                                m.append('0')
                        h = m + y
                        binary = ''.join(h)
                        arr.append(binary)
                    else:
                        print("SyntaxError: Imm value exceeding limit in line", line)
                        quit()
                else:
                    print("SyntaxError: Invalid imm syntax in line", line)
                    quit()
            else:
                print("SyntaxError: Invalid register used in line", line)
                quit()
        else:
            print("SyntaxError: Invalid placing of instruction in line", line)
            quit()
    else:
        if ':' in list[0]:
            if list[1] in B:
                arr.append(B[list[1]])
                if list[2] in reg:
                    arr.append(reg[list[2]])
                    if '$' in list[3]:
                        l = []
                        for i in list[3]:
                            if (i.isnumeric()):
                                l.append(i)
                        num = int(''.join(l))
                        if 0<=num<=255:
                            b= []
                            while(num>0):
                                d=num%2
                                b.append(str(d))
                                num=num//2
                            b.reverse()
                            y = ''.join(b)
                            y = [ch for ch in y]
                            count = 0
                            for i in y:
                                count += 1
                            m = []
                            if count < 8:
                                for i in range(8-count):
                                    m.append('0')
                            h = m + y
                            binary = ''.join(h)
                            arr.append(binary)
                        else:
                            print("SyntaxError: Imm value exceeding limit in line", line)
                            quit()
                    else:
                        print("SyntaxError: Invalid imm syntax in line", line)
                        quit()
                else:
                    print("SyntaxError: Invalid register used in line", line)
                    quit()
            elif list[1] in float:
                arr.append(float[list[1]])
                if list[2] in reg:
                    arr.append(reg[list[2]])
                    if '$' in list[3]:
                        l = []
                        for i in list[3]:
                            if (i.isnumeric()):
                                l.append(i)
                        num = int(''.join(l))
                        if 1<=num<=255:
                            b= []
                            while(num>0):
                                d=num%2
                                b.append(str(d))
                                num=num//2
                            b.reverse()
                            y = ''.join(b)
                            y = [ch for ch in y]
                            count = 0
                            for i in y:
                                count += 1
                            m = []
                            if count < 8:
                                for i in range(8-count):
                                    m.append('0')
                            h = m + y
                            binary = ''.join(h)
                            arr.append(binary)
                        else:
                            print("SyntaxError: Imm value exceeding limit in line", line)
                            quit()
                    else:
                        print("SyntaxError: Invalid imm syntax in line", line)
                        quit()
                else:
                    print("SyntaxError: Invalid register used in line", line)
                    quit()
            else:
                print("SyntaxError: Invalid placing of instruction in line", line)
                quit()
        else:
            print("SyntaxError: Invalid declaration of label in line", line)
            quit()
    x = ''.join(arr)
    last_list.append(x)


def typeC(list, line):
    arr = []
    if not(2<len(list)<5):
        print("SyntaxError: Invalid number of parameters for given instruction in line", line)
        quit()
    elif len(list) == 3:
        if list[0] in C:
            arr.append(C[list[0]])
            arr.append('00000')
            if list[1] in reg:
                arr.append(reg[list[1]])
                if list[2] in reg:
                    arr.append(reg[list[2]])
                else:
                    print("SyntaxError: Invalid register used in line", line)
                    quit()
            else:
                print("SyntaxError: Invalid register used in line", line)
                quit()
        else:
            print("SyntaxError: Invalid placing of instruction in line", line)
            quit()
    else:
        if ':' in list[0]:
            if list[1] in C:
                arr.append(C[list[1]])
                arr.append('00000')
                if list[2] in reg:
                    arr.append(reg[list[2]])
                    if list[3] in reg:
                        arr.append(reg[list[3]])
                    else:
                        print("SyntaxError: Invalid register in line", line)
                        quit()
                else:
                    print("SyntaxError: Invalid register in line", line)
                    quit()
            else:
                print("SyntaxError: Invalid placing of instruction in line", line)
                quit()
        else:
            print("SyntaxError: Invalid declaration of label in line", line)
            quit()
    x = ''.join(arr)
    last_list.append(x)


def typeD(list, line):
    arr = []
    if not(2<len(list)<5):
        print("SyntaxError: Invalid number of parameters for given instruction in line", line)
        quit()
    elif len(list) == 3:
        if list[0] in D:
            arr.append(D[list[0]])
            if list[1] in reg:
                arr.append(reg[list[1]])
                if list[2] in variables:
                    x = len(l1) - len(variables)
                    count = 0
                    for i in variables:
                        if i != list[2]:
                            count += 1
                        else:
                            count += 1
                            break
                    num = x + count - 1
                    b= []
                    while(num>0):
                        d=num%2
                        b.append(str(d))
                        num=num//2
                    b.reverse()
                    y = ''.join(b)
                    y = [ch for ch in y]
                    count = 0
                    for i in y:
                        count += 1
                    m = []
                    if count < 8:
                        for i in range(8-count):
                            m.append('0')
                    h = m + y
                    binary = ''.join(h)
                    arr.append(binary)
                else:
                    print("SyntaxError: Undefined variable used in line", line) 
                    quit()   
            else:
                print("SyntaxError: Invalid register used in line", line)
                quit()
        else:
            print("SyntaxError: Invalid placing of instruction in line", line)
            quit()
    else:
        if ':' in list[0]:
            if list[1] in D:
                arr.append(D[list[1]])
                if list[2] in reg:
                    arr.append(reg[list[2]])
                    if list[3] in variables:
                        x = len(l1) - len(variables)
                        count = 0
                        for i in variables:
                            if i != list[3]:
                                count += 1
                            else:
                                count += 1
                                break
                        num = x + count - 1
                        b= []
                        while(num>0):
                            d=num%2
                            b.append(str(d))
                            num=num//2
                        b.reverse()
                        y = ''.join(b)
                        y = [ch for ch in y]
                        count = 0
                        for i in y:
                            count += 1
                        m = []
                        if count < 8:
                            for i in range(8-count):
                                m.append('0')
                        h = m + y
                        binary = ''.join(h)
                        arr.append(binary)
                    else:
                        print("SyntaxError: Undefined variable used in line", line)      
                        quit()               
                else:
                    print("SyntaxError: Invalid register used in line", line)
                    quit()
            else:
                print("SyntaxError: Invalid placing of instruction in line", line)
                quit()
        else:
            print("SyntaxError: Invalid declaration of label in line", line)
            quit()
    x = ''.join(arr)
    last_list.append(x)


def typeE(list, line):
    arr = []
    if len(list) == 2:
        if list[0] in E:
            arr.append(E[list[0]])
            arr.append('000')
            for i in labels:
                if list[1]+':' == i[0]:
                    num = i[1]
                    b= []
                    while(num>0):
                        d=num%2
                        b.append(str(d))
                        num=num//2
                    b.reverse()
                    y = ''.join(b)
                    y = [ch for ch in y]
                    count = 0
                    for i in y:
                        count += 1
                    m = []
                    if count < 8:
                        for i in range(8-count):
                            m.append('0')
                    h = m + y
                    binary = ''.join(h)
                    arr.append(binary)
                    break
                else:
                    if i == labels[len(labels)-1] and list[1]+':' != i[0]:
                        print("SyntaxError: Undefined label used in line", line)
                        quit()
                    else:
                        continue
        else:
            print("SyntaxError: Invalid placing of instruction in line", line)
            quit()
    elif len(list) == 3:
        if ':' in list[0]:
            if list[1] in E:
                arr.append(E[list[0]])
                arr.append('000')
                for i in labels:
                    if list[2]+':' == i[0]:
                        num = i[1]
                        b= []
                        while(num>0):
                            d=num%2
                            b.append(str(d))
                            num=num//2
                        b.reverse()
                        y = ''.join(b)
                        y = [ch for ch in y]
                        count = 0
                        for i in y:
                            count += 1
                        m = []
                        if count < 8:
                            for i in range(8-count):
                                m.append('0')
                        h = m + y
                        binary = ''.join(h)
                        arr.append(binary)
                        break
                    else:
                        if i == labels[len(labels)-1] and list[2]+':' != i[0]:
                            print("SyntaxError: Undefined label used in line", line)
                            quit()
                        else:
                            continue
            else:
                print("SyntaxError: Invalid declaration of label in line", line)
                quit()
        else:
            print("SyntaxError: Invalid placing of instruction in line", line)
            quit()
    else:
        print("SyntaxError: Invalid number of parameters for given instruction in line", line)
        quit()
    x = ''.join(arr)
    last_list.append(x)


def typeF(list, line):
    arr = []
    if len(list) == 1:
        if list[0] in F:
            arr.append(F[list[0]])
            if line == len(l1):
                arr.append('00000000000')
            else:
                print("SyntaxError: Hlt found before the end of program in line", line)
                quit()
        else:
            print("SyntaxError: Invalid placing of instruction in line", line)
            quit()
    elif len(list) == 2:
        if ':' in list[0]:
            if list[1] in F:
                arr.append(F[list[1]])
                if line == len(l1):
                    arr.append('00000000000')
                else:
                    print("SyntaxError: Hlt found before the end of program in line", line)
                    quit()
            else:
                print("SyntaxError: Invalid placing of instruction in line", line)
                quit()
        else:
            print("SyntaxError: Invalid declaration of label in line", line)
            quit()
    else:
        print("SyntaxError: Invalid number of parameters for given instruction in line", line)
        quit()
    x = ''.join(arr)
    last_list.append(x)


for i in range(0, len(l1)):
    if i != len(l1)-1:
        if len(l1[i]) == 1:
            if l1[i][0] in F:
                typeF(l1[i], i+1)
            else:
                print("SyntaxError: Invalid command in line", i+1)
                quit()
        elif len(l1[i]) == 2:
            if l1[i][0] == 'var':
                if l1[i][1] in variables:
                    continue
                else:
                    print("SyntaxError: Invalid declaration of variable in line", i+1)
                    quit()
            elif l1[i][0] in E:
                typeE(l1[i], i+1)
            elif l1[i][1] in F:
                typeF(l1[i], i+1)
            else:
                print("SyntaxError: Invalid instruction in line", i+1)
                quit()
        elif 2<len(l1[i])<5 and l1[i][0] not in A:
            if l1[i][0] in B or l1[i][1] in B or l1[i][0] in float or l1[i][1] in float:
                if '$' in l1[i][len(l1[i])-1]:
                    typeB(l1[i], i+1)
                else:
                    typeC(l1[i], i+1)
            elif l1[i][0] in C or l1[i][1] in C:
                typeC(l1[i], i+1)
            elif l1[i][0] in D or l1[i][1] in D:
                typeD(l1[i], i+1)
            else:
                print("SyntaxError: Invalid instruction in line", i+1)
                quit()
        elif 3<len(l1[i])<6:
            if l1[i][0] in A or l1[i][1] in A or l1[i][0] in float or l1[i][1] in float:
                typeA(l1[i], i+1)
            else:
                print("SyntaxError: Invalid instruction in line", i+1)
                quit()
        else:
            print("SyntaxError: Invalid number of parameters in instruction in line", i+1)
            quit()
    else:
        if len(l1[i]) == 1:
            if l1[i][0] in F:
                typeF(l1[i], i+1)
            else:
                print("SyntaxError: Last command is not hlt in line", i+1)
                quit()
        elif len(l1[i]) == 2:
            if l1[i][1] in F:
                typeF(l1[i], i+1)
            else:
                print("SyntaxError: Last command is not hlt in line", i+1)
                quit()
        else:
            print("SyntaxError: Last command is not hlt in line", i+1)
            quit()
    

for i in last_list:
    print(i)