import sys

s = sys.stdin.read()
line = s.split("\n")
l1 = []
for i in line:                         
    x  = i.split()
    if len(x) != 0:
        l1.append(x)

A = {'add' : '10000', 'sub' : '10001', 'mul' : '10110', 'xor' : '11010', 'or' : '11011', 'and' : '11100'}
B = {'mov' : '10010', 'ls' : '11001', 'rs' : '11000'}
C = {'mov' : '10011', 'div' : '10111', 'not' : '11101', 'cmp' : '11110'}
D = {'ld' : '10100', 'st' : '10101'}                                                                                  
E = {'jmp' : '11111', 'jlt' : '01100', 'jgt' : '01101', 'je' : '01111'}
F = {'hlt' : '01010'}
reg = {'R0' : '000', 'R1' : '001', 'R2' : '010', 'R3' : '011', 'R4' : '100', 'R5' : '101', 'R6' : '110', 'FLAGS' : '111'}

if len(l1) == 0:
    print("No instruction found")       
    quit()

final = []

variable = []
for i in l1:
    if i[0] == 'var':
        variable.append(i)
    else:
        break

label = []
for i in l1:
    if ':' in i[0]:
        label.append([i[0], l1.index(i) - len(variable)])

def binary(a, line):
    l = []
    x = ''.join(filter(str.isdigit, str(a)))
    y = int(x)
    if(y > 255):
        print("SyntaxError: value out of bounds in line", line)
        quit()
    binary = format(y, 'b')
    z = str(binary)
    n = 8 - len(z)
    for i in range(n):
        l.append('0')
    w = ''.join(l)
    w = w+z
    return w

def memory(a, line):
    n = len(l1) - len(variable)
    for i in range(len(variable)):
        if(variable[i][1] == a):
            return n + i
    for i in range(len(variable)):
        if (i == len(variable) - 1 and a not in variable[i]):
            print("SyntaxError: use of undeclared variable in line", line)
            quit()

def typeA(opcode, reg1, reg2, reg3, line):
    array = []
    array.append(A.get(opcode))
    array.append('00')
    if(reg1 in reg and reg2 in reg and reg3 in reg):
        array.append(reg.get(reg1))
        array.append(reg.get(reg2))
        array.append(reg.get(reg3))
    else:
        print("SyntaxError: Invalid register used in line", line)
        quit()
    x = ''.join(array)
    final.append(x)

def typeB(opcode, reg1, imm, line):
    array = []
    array.append(B.get(opcode))
    if(reg1 in reg):
        array.append(reg.get(reg1))
    else:
        print("SyntaxError: Invalid register used in line", line)
        quit()
    if('$' in imm):
        array.append(binary(imm, line))
    else:
        print("SyntaxError: Invalid immediate value syntax used in line", line)
        quit()
    x = ''.join(array)
    final.append(x)

def typeC(opcode, reg1, reg2, line):
    array = []
    array.append(C.get(opcode))
    array.append('00000')
    if(reg1 in reg and reg2 in reg):
        array.append(reg.get(reg1))
        array.append(reg.get(reg2))
    else:
        print("SyntaxError: Invalid register used in line", line)
        quit()
    x = ''.join(array)
    final.append(x)

def typeD(opcode, reg1, mem, line):
    array = []
    array.append(D.get(opcode))
    if(reg1 in reg):
        array.append(reg.get(reg1))
    else:
        print("SyntaxError: Invalid register used in line", line)
        quit()
    array.append(binary(memory(mem, line), line))
    x = ''.join(array)
    final.append(x)
    
def typeE(opcode, mem, line):
    array = []
    array.append(E.get(opcode))
    array.append('000')
    for i in label:
        if (i[0] == mem+':'):
            array.append(binary(i[1], line))
            x = ''.join(array)
            final.append(x)
            break

def typeF(opcode, line):
    final.append(F.get(opcode)+'00000000000')

def parameter(x, len, line):
    if (x == 'A'):
        if (len not in [4, 5]):
            print("SyntaxError: Invalid number of parameters in line", line)
            quit()
    elif (x == 'B' or x == 'C' or x == 'D'):
        if (len not in [3, 4]):
            print("SyntaxError: Invalid number of parameters in line", line)
            quit()
    elif (x == 'E'):
        if (len not in [2, 3]):
            print("SyntaxError: Invalid number of parameters in line", line)
            quit()
    else:
        if (len not in [1, 2]):
            print("SyntaxError: Invalid number of parameters in line", line)
            quit()
        else:
            if(len == 1 and line != len(l1)):
                print("SyntaxError: Hlt found before the end of program in line", line)
                quit()

for i in l1:
    if i[0] == 'var':
        continue
    elif ':' in i[0]:
        if i[1] in A:
            parameter('A', len(i), l1.index(i) + 1)
            typeA(i[1], i[2], i[3], i[4], l1.index(i) + 1)
        elif i[1] in B:
            parameter('B', len(i), l1.index(i) + 1)
            typeB(i[1], i[2], i[3], l1.index(i) + 1)
        elif i[1] in C:
            parameter('C', len(i), l1.index(i) + 1)
            typeC(i[1], i[2], i[3], l1.index(i) + 1)
        elif i[1] in D:
            parameter('D', len(i), l1.index(i) + 1)
            typeD(i[1], i[2], i[3], l1.index(i) + 1)
        elif i[1] in F:
            parameter('F', len(i), l1.index(i) + 1)
            typeF(i[1], l1.index(i) + 1)
        else:
            print("SyntaxError: Invalid use of label in line", l1.index(i) + 1)
            quit()
    else:
        if i[0] in A:
            parameter('A', len(i), l1.index(i) + 1)
            typeA(i[0], i[1], i[2], i[3], l1.index(i) + 1)
        elif i[0] in B:
            parameter('B', len(i), l1.index(i) + 1)
            typeB(i[0], i[1], i[2], l1.index(i) + 1)
        elif i[0] in C:
            parameter('C', len(i), l1.index(i) + 1)
            typeC(i[0], i[1], i[2], l1.index(i) + 1)
        elif i[0] in D:
            parameter('D', len(i), l1.index(i) + 1)
            typeD(i[0], i[1], i[2], l1.index(i) + 1)
        elif i[0] in E:
            parameter('E', len(i), l1.index(i) + 1)
            typeE(i[0], i[1], l1.index(i) + 1)
        elif i[0] in F:
            parameter('F', len(i), l1.index(i) + 1)
            typeF(i[0], l1.index(i) + 1)
        else:
            print("SyntaxError: Invalid instruction used in line", l1.index(i) + 1)
            quit()

for i in final:
    print(i)

    
