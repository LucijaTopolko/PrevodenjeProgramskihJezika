import sys

lines = []

for line in sys.stdin:
    lines.append(line.rstrip())

for i in range(len(lines)):
    lines[i] = lines[i].strip()

i = 0
a = 0
varijable = [{}]


def p():
    global i, varijable, a
    if i < len(lines):
        if lines[i].startswith("OP_PLUS") or lines[i].startswith("OP_MINUS"):
            i += 1
            if lines[i] == "<P>":
                i += 1
                p()
        elif lines[i].startswith("L_ZAGRADA"):
            i += 1
            if lines[i] == "<E>":
                i += 1
                e()
            if lines[i].startswith("D_ZAGRADA"):
                i += 1
        elif lines[i].startswith("BROJ"):
            i += 1
        elif lines[i].startswith("IDN"):
            var = lines[i].split(" ")[2]
            whatline = -1
            for l in reversed(varijable):
                for key in l.keys():  # keys
                    if var == key:
                        whatline = max(whatline, int(l[key]))
                        if whatline != lines[i].split(" ")[1]:
                            break
                        else:
                            whatline = -1
            if whatline != -1 and whatline != int(lines[i].split(" ")[1]):
                print(lines[i].split(" ")[1] + " " + str(whatline) + " " + var)
            else:
                print("err" + " " + lines[i].split(" ")[1] + " " + var)
                exit(0)
            i += 1

def t_lista():  # ista stvar kao e lista
    global i
    if i < len(lines):
        if lines[i].startswith("OP_PUTA") or lines[i].startswith("OP_PODIJELI"):
            i += 1
            if lines[i] == "<T>":
                i += 1
                t()
        elif lines[i] == "$":
            i += 1


def e_lista():  # ako ovdje treba IDN i zagrade, ja to nisam stavila lol
    global i
    if i < len(lines):
        if lines[i].startswith("OP_PLUS") or lines[i].startswith("OP_MINUS"):
            i += 1
            if lines[i] == "<E>":
                i += 1
                e()
        elif lines[i] == "$":
            i += 1


def t():
    global i
    if i < len(lines):
        if lines[i] == "<P>":
            i += 1
            p()
            if lines[i] == "<T_lista>":
                i += 1
                t_lista()


def e():
    global i
    if i < len(lines):
        if lines[i] == "<T>":
            i += 1
            t()
            if lines[i] == "<E_lista>":
                i += 1
                e_lista()


def za_petlja():
    global i, a, varijable
    a += 1
    varijable.append({})
    if i < len(lines):
        if lines[i].startswith("KR_ZA"):
            i += 1
            if lines[i].startswith("IDN"):
                linija = lines[i].split(" ")
                varijable[a][linija[2]] = linija[1]
                i += 1
                if lines[i].startswith("KR_OD"):
                    i += 1
                    if lines[i] == "<E>":
                        i += 1
                        e()
                        if lines[i].startswith("KR_DO"):
                            i += 1
                            if lines[i] == "<E>":
                                i += 1
                                e()
                                if lines[i] == "<lista_naredbi>":
                                    i += 1
                                    lista_naredbi()
                                    if lines[i].startswith("KR_AZ"):
                                        i += 1
    varijable.pop()
    a -= 1


def naredba_pridruzivanja():
    global i, a, varijable
    if i < len(lines):
        used = 0
        if lines[i].startswith("IDN"):
            linija = lines[i].split(" ")
            for l in reversed(varijable):  # list je dictionary
                for key in l.keys():
                    if linija[2] == key:
                        used = 1
            if not used:
                varijable[a][linija[2]] = linija[1]
            i += 1
            if lines[i].startswith("OP_PRIDRUZI"):
                i += 1
                if lines[i] == "<E>":
                    i += 1
                    e()


# [{x:1, y:3}, {k:4}]

def naredba():
    global i
    if i < len(lines):
        if lines[i] == "<naredba_pridruzivanja>":
            i += 1
            naredba_pridruzivanja()
        elif lines[i] == "<za_petlja>":
            i += 1
            za_petlja()


def lista_naredbi():
    global i
    if i < len(lines):
        if lines[i] == "<naredba>":
            i += 1
            naredba()
            if lines[i] == "<lista_naredbi>":
                i += 1
                lista_naredbi()
        elif lines[i] == "$":
            i += 1
        # else:
        #    i += 1
        #    varijable.popitem()


def program():
    global i
    if i < len(lines):
        if lines[i] == "<lista_naredbi>":
            i += 1
            lista_naredbi()


if lines[i] == "<program>":
    i += 1
    program()
