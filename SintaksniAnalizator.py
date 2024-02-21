import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip())


for i in range(len(lines)):
    lines[i] = lines[i].split(" ")

a = 0  # broj razmaka
i = 0  # mjesto u lines
rjesenje = "<program>\n"


def p():
    global a, i, rjesenje
    rjesenje += a * " " + "<P>\n"
    a += 1
    if i < len(lines):
        if lines[i][0] in ["IDN", "BROJ"]:
            rjesenje += a * " " + " ".join(lines[i]) + "\n"
            i += 1
        elif lines[i][0] in ["OP_PLUS", "OP_MINUS"]:
            rjesenje += a * " " + " ".join(lines[i]) + "\n"
            i += 1
            p()
        elif lines[i][0] == "L_ZAGRADA":
            rjesenje += a * " " + " ".join(lines[i]) + "\n"
            i += 1
            e()
            if lines[i][0] == "D_ZAGRADA":
                rjesenje += a * " " + " ".join(lines[i]) + "\n"
                i += 1
            else:
                print("err " + " ".join(lines[i]))
                exit(0)
        else:
            print("err " + " ".join(lines[i]))
            exit(0)
    else:
        print("err kraj")
        exit(0)
    a -= 1


def t_lista():
    global a, i, rjesenje
    rjesenje += a * " " + "<T_lista>\n"
    a += 1
    if i < len(lines):
        if lines[i][0] in [
            "IDN",
            "OP_PLUS",
            "OP_MINUS",
            "D_ZAGRADA",
            "KR_ZA",
            "KR_DO",
            "KR_AZ",
        ]:
            rjesenje += a * " " + "$\n"
        elif lines[i][0] in ["OP_PUTA", "OP_DIJELI"]:
            rjesenje += a * " " + " ".join(lines[i]) + "\n"
            i += 1
            t()
            a -= 1
        else:
            print("err " + " ".join(lines[i]))
            exit(0)
    else:
        rjesenje += a * " " + "$\n"


def e_lista():
    global a, i, rjesenje
    rjesenje += a * " " + "<E_lista>\n"
    a += 1
    if i < len(lines):
        if lines[i][0] in ["IDN", "D_ZAGRADA", "KR_ZA", "KR_DO", "KR_AZ"]:
            rjesenje += a * " " + "$\n"
        elif lines[i][0] in ["OP_PLUS", "OP_MINUS"]:
            rjesenje += a * " " + " ".join(lines[i]) + "\n"
            i += 1
            e()
        else:
            print("err " + " ".join(lines[i]))
            exit(0)
    else:
        rjesenje += a * " " + "$\n"
    a -= 1


def t():
    global a, i, rjesenje
    rjesenje += a * " " + "<T>\n"
    a += 1
    if i < len(lines):
        if lines[i][0] in ["IDN", "BROJ", "OP_PLUS", "OP_MINUS", "L_ZAGRADA"]:
            p()
            t_lista()
        else:
            print("err " + " ".join(lines[i]))
            exit(0)
    else:
        print("err kraj")
        exit(0)
    a -= 1


def e():
    global a, i, rjesenje
    rjesenje += a * " " + "<E>\n"
    a += 1
    if i < len(lines):
        if lines[i][0] in ["IDN", "BROJ", "OP_PLUS", "OP_MINUS", "L_ZAGRADA"]:
            t()
            a -= 1
            e_lista()
        else:
            print("err " + " ".join(lines[i]))
            exit(0)
    else:
        print("err kraj")
        exit(0)
    a -= 1


def za_petlja():
    global a, i, rjesenje
    a += 1
    rjesenje += a * " " + "<za_petlja>\n"
    if i < len(lines):
        if lines[i][0] == "KR_ZA":
            a += 1
            rjesenje += a * " " + " ".join(lines[i]) + "\n"
            i += 1
            if i < len(lines):
                if lines[i][0] == "IDN":
                    rjesenje += a * " " + " ".join(lines[i]) + "\n"
                    i += 1
                    if i < len(lines) and lines[i][0] == "KR_OD":
                        rjesenje += a * " " + " ".join(lines[i]) + "\n"
                        i += 1
                    else:
                        print("err " + " ".join(lines[i]))
                        exit(0)
                else:
                    print("err " + " ".join(lines[i]))
                    exit(0)
            else:
                print("err " + " kraj")
                exit(0)
            e()
            if i < len(lines):
                if lines[i][0] == "KR_DO":
                    rjesenje += a * " " + " ".join(lines[i]) + "\n"
                    i += 1
                else:
                    print("err " + " ".join(lines[i]))
                    exit(0)
            else:
                print("err " + " kraj")
                exit(0)
            e()
            a -= 1
            lista_naredbi()
            if i < len(lines):
                if lines[i][0] == "KR_AZ":
                    rjesenje += a * " " + " ".join(lines[i]) + "\n"
                    i += 1
                    a -= 1
                else:
                    print("err " + " ".join(lines[i]))
                    exit(0)
            else:
                print("err " + " kraj")
                exit(0)
        else:
            print("err " + " ".join(lines[i]))
            exit(0)
    else:
        print("err kraj")
        exit(0)
    a -= 1


def naredba_pridruzivanja():
    global a, i, rjesenje
    a += 1
    rjesenje += a * " " + "<naredba_pridruzivanja>\n"
    if i < len(lines):
        if lines[i][0] == "IDN":
            a += 1
            rjesenje += a * " " + " ".join(lines[i]) + "\n"
            i += 1
            if i < len(lines):
                if lines[i][0] == "OP_PRIDRUZI":
                    rjesenje += a * " " + " ".join(lines[i]) + "\n"
                    i += 1
                else:
                    print("err " + " ".join(lines[i]))
                    exit(0)
            else:
                print("err kraj")
                exit(0)
            e()
            a -= 1
        else:
            print("err " + " ".join(lines[i]))
            exit(0)
    else:
        print("err kraj")
        exit(0)
    a -= 1


def naredba():
    global a, i, rjesenje
    a += 1
    rjesenje += a * " " + "<naredba>\n"
    if i < len(lines):
        if lines[i][0] == "IDN":
            naredba_pridruzivanja()
        elif lines[i][0] == "KR_ZA":
            za_petlja()
        else:
            print("err " + " ".join(lines[i]))
            exit(0)
    else:
        print("err kraj")
        exit(0)
    a -= 1


def lista_naredbi():
    global a, i, rjesenje
    a += 1
    rjesenje += a * " " + "<lista_naredbi>\n"
    if i < len(lines):
        if lines[i][0] == "IDN" or lines[i][0] == "KR_ZA":
            naredba()
            lista_naredbi()
        elif lines[i][0] == "KR_AZ":
            a += 1
            rjesenje += a * " " + "$\n"
        else:
            print("err " + " ".join(lines[i]))
            exit(0)
    else:
        a += 1
        rjesenje += a * " " + "$\n"
    a -= 1


def program():
    global a, i, rjesenje
    if i < len(lines):
        if lines[i][0] == "IDN" or lines[i][0] == "KR_ZA":
            lista_naredbi()
        else:
            print("err " + " ".join(lines[i]))
            exit(0)
    else:
        lista_naredbi()


program()
print(rjesenje, end="")
