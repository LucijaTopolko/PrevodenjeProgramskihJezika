import sys

lines = []
a = 0
numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
operators = ['+', '-', '*', '/', '=', '(', ')']

for line in sys.stdin:
    lines.append(line.rstrip())

for line in lines:
    a += 1
    i = 0
    while i < len(line):
        if (i + 1) < len(line) and line[i] == '/' and line[i + 1] == '/':
            break
        elif line[i] == '(':
            print("L_ZAGRADA " + str(a) + ' (')
            i += 1
        elif line[i] == ')':
            print("D_ZAGRADA " + str(a) + ' )')
            i += 1
        elif line[i] == '=':
            print("OP_PRIDRUZI " + str(a) + ' =')
            i += 1
        elif line[i] == '+':
            print("OP_PLUS " + str(a) + ' +')
            i += 1
        elif line[i] == '-':
            print("OP_MINUS " + str(a) + ' -')
            i += 1
        elif line[i] == '*':
            print("OP_PUTA " + str(a) + ' *')
            i += 1
        elif line[i] == '/':
            print("OP_DIJELI " + str(a) + ' /')
            i += 1
        elif line[i:i + 2] == 'za' and ((i + 2) == len(line) or line[i + 2] == " "):
            print("KR_ZA " + str(a) + ' za')
            i += 2
        elif line[i:i + 2] == 'az' and ((i + 2) == len(line) or line[i + 2] == " "):
            print("KR_AZ " + str(a) + ' az')
            i += 2
        elif line[i:i + 2] == 'od' and ((i + 2) == len(line) or line[i + 2] == " "):
            print("KR_OD " + str(a) + ' od')
            i += 2
        elif line[i:i + 2] == 'do' and ((i + 2) == len(line) or line[i + 2] == " "):
            print("KR_DO " + str(a) + ' do')
            i += 2
        elif line[i] in numbers:
            p = ' '
            while i < len(line) and (line[i] in numbers or line[i] == '.') and line[i] != ' ':
                p += str(line[i])
                i += 1
            print("BROJ " + str(a) + p)
        elif line[i] != ' ' and line[i] != '\t':
            p = ' '
            while i < len(line) and line[i] != ' ' and line[i] not in operators:
                p += str(line[i])
                i += 1
            print("IDN " + str(a) + p)
        else:
            i += 1
