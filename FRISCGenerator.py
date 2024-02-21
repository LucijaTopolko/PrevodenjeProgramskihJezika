import sys

file = open("a.frisc", "w", encoding="utf-8")

lines = []

for line in sys.stdin:
    lines.append(line.rstrip())

for i in range(len(lines)):
    lines[i] = lines[i].strip()

lines1 = []

for line in lines:
    if not line.startswith("<") and not line.startswith("$"):
        lines1.append(line)

lines = [[] for _ in range(int(lines1[-1].split(" ")[1]))]

for line in lines1:
    line = line.split(" ")
    lines[int(line[1]) - 1].append(line[2])

lines = [' '.join(expr) for expr in lines]

print(lines)


def rpn(line):
    def vaznost(operator):
        if operator == '+' or operator == '-':
            return 1
        elif operator == '*' or operator == '/':
            return 2
        return 0

    def is_operator(char):
        return char in {'+', '-', '*', '/'}

    def vazniji(op1, op2):
        return vaznost(op1) >= vaznost(op2)

    def to_postfix(line):
        stog = []
        postfix = []
        for char in line.split():
            if char.isalnum():
                postfix.append(char)
            elif char == '(':
                stog.append(char)
            elif char == ')':
                while stog and stog[-1] != '(':
                    postfix.append(stog.pop())
                stog.pop()
            elif is_operator(char):
                while stog and vazniji(stog[-1], char):
                    postfix.append(stog.pop())
                stog.append(char)

        while stog:
            postfix.append(stog.pop())

        return postfix

    return to_postfix(line)


def dodaj_razmak(izraz):
    rezultat = ''
    for znak in izraz:
        if znak in ['+', '-', '*', '/']:
            rezultat += ' ' + znak + ' '
        else:
            rezultat += znak
    return rezultat

mul, div = False, False

varijable = ["rez"]
i = 0
curr = ""
counter = []
used = [0]
inkrementi = []
doovi = []

print("\tMOVE 40000, R7", file=file)  # inicijalizacija stoga
print("\tMOVE 3C000, R5", file=file)

for i in range(len(lines)):
    line = lines[i]
    if line.startswith("za"):
        counter.append(used[-1]+1)
        used.append(counter[-1])
        linija = line.split(" ")  # za, i, od, 1, do, n
        if len(linija) != 6:
            line = line.replace(" - ", " -")
            line = line.replace(" + ", "+")
            line = line.replace(" * ", "*")
            line = line.replace(" / ", "/")
            linija = line.split(" ")
        varijable.append(linija[1])
        curr = linija[1]
        od, do = linija[3], linija[5]
        if od.isnumeric():  # pozitivan broj
            print("\tMOVE %D " + od + ", R0", file=file)
            print("\tPUSH R0", file=file)
        elif od[1:].isnumeric():  # negativan broj
            print("\tMOVE %D " + od + ", R0", file=file)
            print("\tPUSH R0", file=file)
        else:  # varijabla
            pos = varijable.index(od)
            print("\tLOAD R0, (V" + str(pos) + ")", file=file)
            print("\tPUSH R0", file=file)
        pos = len(varijable) - 1
        inkrementi.append(varijable[-1])
        doovi.append(do)
        print("\tPOP R0", file=file)
        print("\tSTORE R0, (V" + str(pos) + ")", file=file)
        print("L" + str(counter[-1]) + "   ;", file=file)

    elif line.startswith("az"):
        pos = len(varijable) - 1 - varijable[::-1].index(inkrementi[-1])
        print("\tLOAD R0, (V" + str(pos) + ")", file=file)
        print("\tADD R0, 1, R0", file=file)
        print("\tSTORE R0, (V" + str(pos) + ")", file=file)
        d = doovi[-1]
        doovi.pop()
        print(";"+d, file=file)
        if d.isnumeric():
            print("\tMOVE %D " + d + ", R0", file=file)
            print("\tPUSH R0", file=file)
        elif d[1:].isnumeric():
            print("\tMOVE %D " + d + ", R0", file=file)
            print("\tPUSH R0", file=file)
        else:
            if any(operator in d for operator in ['+', '-', '*', '/']):
                d = dodaj_razmak(d)
                expression = rpn(d)
                for e in expression:
                    if e == " ":
                        continue
                    elif e.isnumeric():
                        print("\tMOVE %D " + e + ", R0", file=file)
                        print("\tPUSH R0", file=file)
                    elif e in "+-*/":
                        if e == "+":
                            print("\tPOP R1", file=file)
                            print("\tPOP R0", file=file)
                            print("\tADD R0, R1, R2", file=file)
                            print("\tPUSH R2", file=file)
                        elif e == "-":
                            print("\tPOP R1", file=file)
                            print("\tPOP R0", file=file)
                            print("\tSUB R0, R1, R2", file=file)
                            print("\tPUSH R2", file=file)
                        elif e == "*":
                            print("\tCALL MUL", file=file)
                            mul = True
                        else:
                            print("\tCALL DIV", file=file)
                            div = True
                    else:
                        if e in inkrementi:
                            pos = len(varijable) - 1 - varijable[::-1].index(e)
                        else:
                            pos = varijable.index(e)
                        print(";"+str(pos), file=file)
                        print("\tLOAD R0, (V" + str(pos) + ")", file=file)
                        print("\tPUSH R0", file=file)
                pos = varijable.index(inkrementi[-1])
            else:
                pos1 = varijable.index(d)
                print("\tLOAD R0, (V" + str(pos1) + ")", file=file)
                print("\tPUSH R0", file=file)
        print("\tLOAD R0, (V" + str(pos) + ")", file=file)
        print("\tPOP R1", file=file)
        print("\tCMP R0, R1", file=file)
        print("\tJP_SLE L" + str(counter[-1]), file=file)
        counter.pop()
        inkrementi.pop()
    else:
        line = line.split(" = ")
        expression = rpn(line[1])
        for e in expression:
            if e == " ":
                continue
            elif e.isnumeric():
                print("\tMOVE %D " + e + ", R0", file=file)
                print("\tPUSH R0", file=file)
            elif e in "+-*/":
                if e == "+":
                    print("\tPOP R1", file=file)
                    print("\tPOP R0", file=file)
                    print("\tADD R0, R1, R2", file=file)
                    print("\tPUSH R2", file=file)
                elif e == "-":
                    print("\tPOP R1", file=file)
                    print("\tPOP R0", file=file)
                    print("\tSUB R0, R1, R2", file=file)
                    print("\tPUSH R2", file=file)
                elif e == "*":
                    print("\tCALL MUL", file=file)
                    mul = True
                else:
                    print("\tCALL DIV", file=file)
                    div = True
            else:
                if e in inkrementi:
                    pos = len(varijable) - 1 - varijable[::-1].index(e)
                else:
                    pos = varijable.index(e)
                print("\tLOAD R0, (V" + str(pos) + ")", file=file)
                print("\tPUSH R0", file=file)
        if line[0] not in varijable:
            varijable.append(line[0])
        pos = varijable.index(line[0])
        print("\tPOP R0", file=file)
        print("\tSTORE R0, (V" + str(pos) + ")", file=file)

print("""\tLOAD R6, (V0)
\tHALT""", file=file)

for index, el in enumerate(varijable):
    print("V" + str(index) + " DW 0", file=file)

if mul or div:
    print("""
MD_SGN MOVE 0, R6
\tXOR R0, 0, R0
\tJP_P MD_TST1
\tXOR R0, -1, R0
\tADD R0, 1, R0
\tMOVE 1, R6
MD_TST1 XOR R1, 0, R1
\tJP_P MD_SGNR
\tXOR R1, -1, R1
\tADD R1, 1, R1
\tXOR R6, 1, R6
MD_SGNR RET
MD_INIT POP R4 ; MD_INIT ret addr
\tPOP R3 ; M/D ret addr
\tPOP R1 ; op2
\tPOP R0 ; op1
\tCALL MD_SGN
\tMOVE 0, R2 ; init rezultata
\tPUSH R4 ; MD_INIT ret addr
\tRET
MD_RET XOR R6, 0, R6 ; predznak?
\tJP_Z MD_RET1
\tXOR R2, -1, R2 ; promijeni predznak
\tADD R2, 1, R2
MD_RET1 POP R4 ; MD_RET ret addr
\tPUSH R2 ; rezultat
\tPUSH R3 ; M/D ret addr
\tPUSH R4 ; MD_RET ret addr
\tRET
MUL CALL MD_INIT
\tXOR R1, 0, R1
\tJP_Z MUL_RET ; op2 == 0
\tSUB R1, 1, R1
MUL_1 ADD R2, R0, R2
\tSUB R1, 1, R1
\tJP_NN MUL_1 ; >= 0?
MUL_RET CALL MD_RET
\tRET
DIV CALL MD_INIT
\tXOR R1, 0, R1
\tJP_Z DIV_RET ; op2 == 0
DIV_1 ADD R2, 1, R2
\tSUB R0, R1, R0
\tJP_NN DIV_1
\tSUB R2, 1, R2
DIV_RET CALL MD_RET
\tRET""", file=file)
