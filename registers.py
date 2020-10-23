# 1.2.13

COM = b'00000000000000'
OP1 = b'00000000000000'
ACC = b'00000000000000'


R1 = b'10101010101010'
R2 = b'01010101010101'
R3 = b'11111110000000'
R4 = b'00000001111111'

SIGN = b'00000000000000'
COUNTER = b'00000000000000'
TACT = b'00000000000000'


def parse(command):
    global COM, OP1, TACT
    COM = bytes(command[0:1], encoding='utf-8') + COM[1:14]

    if len(command) == 15:
        COM = COM[0:1] + b'0' + COM[2:]
        OP1 = bytes(command[1:15], encoding='utf-8')
    else:
        COM = COM[0:1] + b'1' + COM[2:]
        OP1 = bytes('000000000000' + command[1:3], encoding='utf-8')


def mov():
    global COM, OP1, ACC, R1, R2, R3, R4

    if int(COM[2:3], 2):
        if OP1[12:14] == b'00':
            ACC = R1
        elif OP1[12:14] == b'01':
            ACC = R2
        elif OP1[12:14] == b'10':
            ACC = R3
        else:
            ACC = R4
    else:
        ACC = OP1


def mine():
    global COM, OP1, ACC, TACT, SIGN

    summ = 0
    for i in range(len(ACC)):
        summ += int(ACC[i:i+1], 2)

    to_count = b''
    if int(COM[1:2], 2):
        if OP1[12:14] == b'00':
            to_count += R1[0:1]
        elif OP1[12:14] == b'01':
            to_count += R2[0:1]
        elif OP1[12:14] == b'10':
            to_count += R3[0:1]
        else:
            to_count += R4[0:1]
    else:
        to_count += OP1[13:14]



    if to_count == b'1':
        ACC = bytes(format(summ, "014b"), encoding='utf-8')
    else:
        ACC = bytes(format(14-summ, "014b"), encoding='utf-8')


def act():
    global COM
    if int(COM[0:1], 2):
        mine()
    else:
        mov()



def output():
    global COM, OP1, ACC, R1, R2, R3, R4, SIGN, COUNTER, TACT

    if int(chr(COM[0])):
        print('mine(', end='')
    else:
        print('mov(', end='')
    if int(chr(COM[1])):
        print(f'R{int(OP1[12:14], 2)+1}', end='')
    else:
        print(int(OP1, 2), end='')
    print(')')

    print(f'COM     {str(COM)[2:-1]} {int(chr(COM[0]))+1}')
    print(f'OP1     {str(OP1)[2:-1]} {int(OP1, 2)}')
    print(f'ACC     {str(ACC)[2:-1]} {int(ACC, 2)}')
    print(f'R1      {str(R1)[2:-1]} {int(R1, 2)}')
    print(f'R2      {str(R2)[2:-1]} {int(R2, 2)}')
    print(f'R3      {str(R3)[2:-1]} {int(R3, 2)}')
    print(f'R4      {str(R4)[2:-1]} {int(R4, 2)}')
    print(f'SIGN    {str(SIGN)[2:-1]} {chr(43+int(chr(SIGN[0]))*2)}')
    print(f'COUNTER {format(int(COUNTER, 2), "014b")} {int(COUNTER, 2)}')
    print(f'TACT    {str(TACT)[2:-1]} {int(TACT[12:14], 2)+1}')


def main():
    global TACT, COUNTER, SIGN

    with open('program.txt', 'r') as prog:
        for line in prog:
            input('Press Enter to continue')
            TACT = TACT[0:13] + b'0'
            COUNTER = bin(int(COUNTER, 2)+1)
            parse(line[0:-1])
            output()
            input('Press Enter to continue')
            TACT = TACT[0:13] + b'1'
            act()
            SIGN = SIGN[0:13] + ACC[0:1]
            output()


main()