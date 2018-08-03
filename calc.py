# scanning:
# 0: () 
# 1: sqrt ^ sin,log,etc 
# 2: * / 
# 3: + -


# THINGS TO ADD: squared trigs, variable storing?, GRAPHING, INTEGRATION, matrices?, summation, errors
# CURRENTLY WORKING ON: fix derivative log10(x+1), start graphing (table first)


# SETUP
from mpmath import *
import sympy as s
from fractions import Fraction
# from funcGraph import *
import math
import time
import operator
import sys
import os

ops = {'+': operator.add,
       '-': operator.sub,
       '*': operator.mul,
       '/': operator.truediv,
       '^': operator.pow,
       }
trigsP = {'sin(', 'cos(', 'tan(', 'atan(', 'acos(', 'asin('}
trigs = {'sin': math.sin,
         'cos': math.cos,
         'tan': math.tan,
         'atan': math.atan,
         'acos': math.acos,
         'asin': math.asin,
         }

digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

mp.dps = 100


def isfloat(num):
    try:
        mpmathify(num)
    except:
        return False
    return True


def isint(num):
    try:
        num = mpmathify(num)
    except:
        return False
    return math.floor(num) == num


def clearLists():
    global charList
    del charList[:]


def error(msg):  # errors
    clearLists()
    print("Error: " + msg)
    inMain([], 'wait', ['=', 'dlt', 'clear'])


def charIn(lst, inp, digit):
    try:
        if inp == 'ans':
            inp = ansList[len(ansList) - 1]
        elif inp == 'pi':
            inp = 'π'
    except IndexError:
        error("No ans stored")
    save(inp, lst)

    for x in range(0, len(charList) - 1):
        if charList[x] == '':
            del (charList[x])
    time.sleep(.25)


def parenBal(lst):
    balance = 0
    for w in lst:
        if w == '(':
            balance += 1
        if w == ')':
            balance -= 1
    while balance != 0:
        if balance < 0:
            for y in range(len(lst) - 1, -1, -1):
                if lst[y] == ')':
                    del (lst[y])
                    balance += 1
                    break
        if balance > 0:
            lst.append(')')
            balance -= 1
        print('a')

    return lst


def addMult(lst):
    x = 0
    z = len(lst)
    for y in range(z):
    #while y < z:  # split parentheses
        if lst[y] in trigsP or 'log' in str(lst[y]) or lst[y] == 'ln(':
            lst[y] = lst[y][:-1]
            lst.insert(y + 1, '(')
        z = len(lst)
    while x < z - 1:
        if ((lst[x + 1] in trigs) or (lst[x + 1] in {'sqrt', 'ln', '(', 'π', 'e'}) or ('log' in str(lst[x + 1]))) and (
                isfloat(lst[x]) == True or lst[x] in ['π', 'e', ')', '!']):
            print('a')
            print(lst[x])
            print(lst[x + 1])
            lst.insert(x + 1, '*')
            x += 1
        x += 1
        z = len(lst)
    x = 0
    z = len(lst)
    while x < z - 1:
        if (lst[x] == ')') and (lst[x + 1] not in ops and lst[x + 1] not in [')']):
            print('d')
            lst.insert(x + 1, '*')
            x += 1
        x += 1
        z = len(lst)
    if 'x' in lst:
        x = 0
        z = len(lst)
        while x < z - 1:
            if (lst[x] == 'x') and (lst[x + 1] in trigs or lst[x + 1] in ['sqrt', 'ln', '(', 'π', 'e', 'x'] or isfloat(
                    lst[x + 1]) == True):
                print('b')
                lst.insert(x + 1, '*')
                x += 1
            x += 1
            z = len(lst)
        x = 1
        z = len(lst)
        while x < z - 1:
            if (lst[x + 1] == 'x') and (lst[x] in ['π', 'e', ')'] or isfloat(lst[x]) == True):
                print('c')
                lst.insert(x + 1, '*')
                x += 1
            x += 1
            z = len(lst)
        while x < z:

            if 'log' in lst[x]:
                close = False
                for q in range(x, len(lst)):
                    if lst[q] == ')':
                        end = q
                        close = True
                        break
                if close == False:
                    lst.insert(end + 1, ')')
                do = True
                end = len(lst) - 1
                for y in range(x, len(lst)):
                    if lst[y] == ',':
                        do = False
                    if lst[y] == ')':
                        end = y
                        break
                if do == True:
                    lst[x] = 'log'
                    lst.insert(end, '0')
                    lst.insert(end, '1')
                    lst.insert(end, ',')

                z = len(lst)
            x += 1
    for x in range(len(lst)):
        if lst[x] == 'log1':
            lst[x] = 'log'
    return lst


def delMult(strIn):
    lst = []
    for x in strIn:
        lst.append(x)
    x = 0
    z = len(lst)
    while x < z:
        try:
            if lst[x] == '*' and (isfloat(lst[x + 1]) == False or isfloat(lst[x - 1]) == False):
                del (lst[x])
        except:
            del (lst[x])
        z = len(lst)
        x += 1
    string = ''
    for y in lst:
        string += y
    return string  # <-----------


def save(s, lst):
    for y in range(len(lst)):
        if s != '' and lst[y] == '_':
            lst[y] = s
            lst.insert(y + 1, '_')
            break


def decimal(lst, x):  # combine input into decimals
    dec = '0.0'
    try:
        if isint(lst[x + 1]):
            dec = '0.' + str(lst[x + 1])
            del (lst[x + 1])
    except IndexError:
        pass
    if isint(lst[x - 1]) and x > 0:
        dec = mpmathify(lst[x - 1]) + mpmathify(dec)
        del (lst[x - 1])
        lst[x - 1] = dec
    else:
        lst[x] = dec
    if dec == '0.0':
        error('invalid decimal point')
        return (['error'])
    return lst


def negative(lst, x):
    lst = checkNext(lst, x)
    if lst[x + 1] == '(':
        lst = parenth(lst, x + 1)
    del (lst[x])
    lst[x] = mpmathify(lst[x]) * mpmathify(-1)
    return lst


def checkNext(lst, x):
    if x + 1 < len(lst):
        if str(lst[x + 1]) in '(':
            parenth(lst, x + 1)
        if str(lst[x + 1]) in trigs:
            lst = trig(lst, x + 1)
        if str(lst[x + 1]) in 'ln' or 'log' in str(lst[x + 1]):
            lst = logr(lst, x + 1)
        if str(lst[x + 1]) == '-':
            lst = negative(lst, x + 1)
        if str(lst[x + 1]) == 'sqrt':
            lst = sqrt(lst, x + 1)

    return lst

    #####         EVALUATIONS        #####

    ### SPECIAL FUNCTIONS


def sqrt(lst, x):
    lst = checkNext(lst, x)
    del (lst[x])
    lst[x] = mpmathify(lst[x]) ** 0.5
    return lst


def trig(lst, x):
    try:
        u = None
        lst = checkNext(lst, x)
        lst[x] = trigs[lst[x]](mpmathify(lst[x + 1]))
        del (lst[x + 1])
        return lst
    except ValueError:
        error("undefined")
        return ['error']


def fact(lst, x):
    lst = checkNext(lst, x)
    del (lst[x])
    if math.floor(mpmathify(lst[x - 1])) != mpmathify(lst[x - 1]):
        error('Factorial must be integer')
        return ['error']
    total = 1
    for x in range(int(lst[x - 1]), 0, -1):
        total *= x
    lst[x - 1] = total
    return lst


def logBase(lst):
    base = []
    add("logBase: ", '')
    x = inMain(base, 'op', [])
    x = equals(base)
    if x == 'exit':
        upLayer()
        del (lst[-1])
        return ''

    baseNum = ''
    remove("logBase: ")
    for x in base:
        baseNum += x
    if baseNum == '' or baseNum == '10':
        return ''
    return baseNum


def logr(lst, x):  # evaluate log
    lst = checkNext(lst, x)
    if 'log' in lst[x]:
        if len(lst[x]) > 3 and lst[x][3:5] != '10':
            print(lst[x + 1])
            print(lst[x])
            lst[x] = mp.log(lst[x + 1], mpmathify(lst[x][3:]))
        else:
            lst[x] = mp.log(lst[x + 1], 10)
    else:
        emult = False
        for y in range(1, 10):
            if abs(mp.e - mpmathify(lst[x + 1]) ** (1 / y)) < .01:
                emult = True
                lst[x] = y
        if emult == False:
            lst[x] = mp.log(lst[x + 1])

    del (lst[x + 1])
    return lst

    # parenthesis


def parenth(lst, x):
    resultList = []
    for y in range(x + 1, len(lst)):
        if lst[y] == ')':
            end = y
            # print('b')
            break
        else:
            end = 0
    for a in range(x + 1, end):
        resultList.append(lst[a])  # new list for stuff in ()
    for z in range(0, end - x):
        del (lst[x])
    lst[x] = equals(resultList)[0]  # replace () w output of inside
    return lst


def power(lst, x):  # exponents
    if x + 2 < len(lst):
        if lst[x + 2] == '^':
            power(lst, x + 2)
    if lst[x - 1] == 0 and lst[x + 1] == 0:  # 0^0 error
        error("undefined")
        return ['error']
    result = operator.pow(mpmathify(lst[x - 1]), mpmathify(lst[x + 1]))
    lst[x - 1] = result
    del (lst[x])
    del (lst[x])
    return lst


def baseOp(lst, x):  # + - * /
    result = ops[lst[x]](mpmathify(lst[x - 1]), mpmathify(lst[x + 1]))
    lst[x - 1] = str(result)
    del (lst[x])
    del (lst[x])
    return lst


ansList = []


def equals(lst):  # EQUALS **NEED ERROR DETECTION**
    addMult(lst)
    for w in range(len(lst)):
        if lst[w] == 'π':
            lst[w] = math.pi
        elif lst[w] == 'e':
            lst[w] = math.e
        lst[w] = str(lst[w])

    # try:

    # print(lst)
    global ansList
    scanning = -3  # 0-() 1-^ 2-*/ 3-+-
    lst = parenBal(lst)
    z = len(lst)
    while z > 1:
        x = 0
        if z == 2 and lst[len(lst) - 1] in ['fr', 'i']:
            break
        while x < z:
            # print(lst)
            lst = parenBal(lst)
            z = len(lst)
            if isfloat(lst[x]) and x + 1 < z:
                if isfloat(lst[x + 1]):
                    lst[x] = str(lst[x]) + str(lst[x + 1])
                    del (lst[x + 1])
                    z = len(lst)
                    x = -1
            if lst[x] == 'ans':
                lst[x] = ansList[-1]
            if lst[x] == '.' and scanning == -2:  # .
                lst = decimal(lst, x)
                x = -1
            elif lst[x] == '-' and scanning == -1 and (isfloat(lst[x - 1]) == False or x == 0):
                lst = negative(lst, x)
            elif lst[x] == '(' and scanning == 0:  # ()
                lst = parenth(lst, x)
                x = -1
            elif lst[x] == '!' and scanning == 1:
                lst = fact(lst, x)
                x = -1
            elif lst[x] in ['sin', 'cos', 'tan', 'atan', 'acos', 'asin'] and scanning == 1:
                lst = trig(lst, x)
                x = -1
            elif isinstance(lst[x], str) and scanning == 1:
                if 'log' in lst[x] or 'ln' in lst[x]:
                    lst = logr(lst, x)
                    x = -1
            elif lst[x] == '^' and scanning == 2:  # ^
                lst = power(lst, x)
                x = -1
            elif (lst[x] == 'sqrt' and scanning == 2):  # sqrt
                lst = sqrt(lst, x)
                x = -1
            elif scanning == 3 and (lst[x] == '*' or lst[x] == '/'):  # * /
                lst = baseOp(lst, x)
                x = -1
            elif scanning == 4 and (lst[x] == '+' or lst[x] == '-'):  # + -
                lst = baseOp(lst, x)
                x = -1
            elif lst[x] == 'exit':
                return 'exit'
            x += 1
        scanning += 1
        if scanning > 4:
            scanning = -3

    return lst


# except:
# error('Syntax')
# return ['error']
def repeatTest(lst):
    aList = []
    bList = []
    if '(' in str(lst[0]):
        if '+' in str(lst[0]):
            a, b = str(lst[0]).split(' + ')
        else:
            a, b = str(lst[0]).split(' - ')
        aList = repeatTest([a[1:]])
        bList = repeatTest([b[:-1]])
        return aList, bList
    doesRepeat = ''
    repeatStart = -1
    repeatLen = ''
    repeatDigs = ''
    oDec = ''
    integ = ''
    if '.' in str(lst[0]):
        integ, oDec = str(lst[0]).split(".")
    else:
        integ = mpmathify(lst[0])
    if len(str(oDec)) < 9:
        return [lst[0], '', -1, -1, '', '']
    test = ""
    for digLen in range(1, 50):
        for digStart in range(10, -1, -1):
            duplicate = False
            test = ""
            try:
                for y in range(digStart, digStart + digLen):
                    test += oDec[y]
            except IndexError:
                break
            repeats = False
            repeats = 0
            for num in range(2, 10):
                if test == str(oDec)[(digLen) * (num - 1) + digStart:(digLen) * num + digStart]:
                    repeats += 1
                if repeats == 8:
                    repeatStart = digStart
                    repeatDigs = test[:len(test)]
    dec = oDec[repeatStart:]
    repeaters = []
    for length in range(1, int(len(repeatDigs))):
        lenRepeats = True
        for iterate in range(1, int(len(repeatDigs) / 4)):
            if dec[0:length] != dec[length * (iterate - 1):length * iterate]:
                lenRepeats = False
        if lenRepeats == True:
            repeaters.append(repeatDigs[0:length])
    for x in range(len(repeaters) - 1, -1, -1):
        if repeaters[x] == dec[len(repeaters[x]):2 * len(repeaters[x])] == dec[
                                                                           2 * len(repeaters[x]):3 * len(repeaters[x])]:
            repeatDigs = repeaters[x]
    if repeatStart == 0 or repeatDigs == '':
        r = repeatDigs
    else:
        r = "(" + repeatDigs + ")"
    if repeatStart != -1:
        doesRepeat = True
    final = str(int(integ)) + "." + oDec[:repeatStart] + r
    if repeatDigs == '9':
        final = str(round(mpf(final), repeatStart))
        return [final, '', '', '', '']
    if 'j' in str(lst[0]):
        if mpf(lst[0][:-1]) < 0:
            final = '-' + final + 'j'
    elif mpf(lst[0]) < 0:
        final = '-' + final
    if final == '0.0':
        return [lst[0], '', '', '', '']
    repeatLen = len(repeatDigs)
    if doesRepeat == True:
        lst[0] = str(lst[0])
        if repeatDigs not in str(
                lst[0][repeatLen * (int(100 / repeatLen) - 5) + 2:repeatLen * (int(100 / repeatLen) - 4) + 2]):
            return [lst[0], '', '', '', '']

    return [lst[0], final, repeatStart, repeatLen, repeatDigs,
            doesRepeat]  # original, final, start, length of repeating, digits that repeat, repeats?


def fracOut(lst, x):
    rList = repeatTest(lst)
    orig = lst[0]
    dec = mpmathify(orig) - math.floor(mpmathify(orig))
    if rList[5] == True:
        num = ((mpmathify(rList[0]) * mpmathify(10 ** rList[3])) - mpmathify(dec))
        denom = (10 ** rList[3]) - 1
        a, b = str(num).split('.')
        for x in range(1, len(b) + 1):
            if b[len(b) - x] == '0':
                b = b[:x - 1] + b[x + 1:]
            else:
                break
        num *= 10 ** len(b)
        denom *= 10 ** len(b)
        num, d = str(num).split('.')
        num = int(num)
        frac = str(Fraction(num, denom))
        num, denom = frac.split("/")
        return (num + " / " + denom)


    else:
        if len(str(orig)) > 20:
            error("overflow")
            return (round(mpmathify(orig), 8))

        frac = str(Fraction(str(orig)))
        if '/' not in frac:
            return (frac)
        num, denom = frac.split("/")
        if num == denom:
            return ('1')
        elif num == 0:
            return ('0')
        else:
            return (num + " / " + denom)


class Funcs:
    def printList(lst):
        for z in range(len(lst)):
            print(str(lst[z]), end='')

    def special(lst, mode):
        clr()

        add('1: sin', '\n')
        add('2: cos', '\n')
        add('3: tan', '\n')
        add('4: arcsin', '\n')
        add('5: arccos', '\n')
        add('6: arctan', '\n')
        add('7: log', '\n')
        add('8: ln', '\n')
        add('9: !', '\n')
        x = inMain([], 'digs', digits[1:])
        if x != '7':
            upLayer()
        if x == '1':
            return 'sin('
        if x == '2':
            return 'cos('
        if x == '3':
            return 'tan('
        if x == '4':
            return 'asin('
        if x == '5':
            return 'acos('
        if x == '6':
            return 'atan('
        if x == '7':
            base = ''
            if mode != 'func':
                base = logBase(lst)
            upLayer()
            if base != '':
                return 'log' + base + '('
            return 'log('
        if x == '8':
            return 'ln('
        if x == '9':
            return '!'
        if x == 'exit':
            return 'exit'

    def funcIn():
        global active
        global funcList
        for num, y in enumerate(funcList):
            if y != []:
                active = num
        Funcs.printAll()
        while True:
            done = inMain(funcList[active], 'func', [])
            y = 0
            for x in funcList[active]:
                if x == '(':
                    y += 1
                if x == ')':
                    y -= 1
            for z in range(y, 0, -1):
                funcList[active].append(')')
            clr()
            if done == 'exit':
                return
            elif done == 'done' and active < 9:
                active += 1
            Funcs.printAll()
            if isfloat(done[1]) and done[1] >= 0 and done[1] <= 9:
                lst = done[0]
                active = done[1]

    def printAll():
        clr()
        for y in range(10):
            add(str(y + 1) + ":  y = ", "")
            for z in funcList[y]:
                add(z, '')
            add('', '\n')

    def printActive():
        clr()
        for y in range(10):
            if funcList[y] != []:
                add(str(y + 1) + ":  y = ", "")
                for z in funcList[y]:
                    add(z, '')
                add('', '\n')

    def printFunc(num):
        global funcList
        clr()
        add('y = ', '')
        for z in funcList[num - 1]:
            add(z, '')
        add('', '\n')

    def fSpec(fmode):
        global funcList
        empty = True
        for x in funcList:
            if x != []:
                empty = False
                break
        if empty == True:
            print('No functions entered. Press = to return.')
            inMain([], 'wait', ['=', 'dlt', 'clear'])
            return
        done = False
        while done == False:
            done2 = False

            clr()
            Funcs.printActive()
            add('Function: ', '')
            c = inMain([], 'digs', digits[1:len(funcList) + 1])
            try:
                c = int(c)
            except:
                done = True
                done2 = True
                if c == 'exit':
                    return
            while done2 == False:
                Funcs.printActive()
                if fmode == 'value':  ###funcval
                    xVal = []
                    yVal = []
                    add(' x = ', '')
                    x = inMain(xVal, 'op', [])
                    if x == 'exit':
                        return
                    x = equals(xVal)[0]
                    add(x, '')
                    funcChoice = funcList[c - 1][:]
                    z = len(funcChoice)
                    y = 0
                    funcChoice = addMult(funcChoice)
                    for num, a in enumerate(funcChoice):
                        if a == 'x':
                            funcChoice[num] = x
                    print(funcChoice)
                    yVal = equals(funcChoice)
                    add('; y = ' + format(mpmathify(yVal[0])), '\n')
                elif fmode == 'deriv':  # derivative
                    xVal = []
                    dVal = []
                    function = ''
                    derivPrint = ''
                    funcChoice = parenBal(addMult(funcList[c - 1][:]))
                    for y in funcChoice:
                        function += y
                    print(function)
                    deriv = str(s.diff(function, 'x'))
                    length = len(deriv)
                    z = 0
                    while z < length:
                        if deriv[z] == ' ':
                            deriv = deriv[:z] + deriv[z + 1:]
                        if deriv[z] == '*' == deriv[z + 1]:
                            deriv = deriv[:z] + '^' + deriv[z + 2:]
                        if deriv[z] == 'l' and deriv[z + 1] == 'o':
                            deriv = deriv[:z] + 'ln' + deriv[z + 3:]
                        z += 1
                        length = len(deriv)
                    derivPrint = delMult(deriv)

                    add('f\'(x) = ' + derivPrint + ' | x = ', "")

                    x = inMain(xVal, 'op', [])
                    if x == 'exit':
                        return

                    x = equals(xVal)[0]

                    funcDiv = []
                    z = 0
                    while z < len(deriv):
                        if deriv[z] == 'l':
                            if deriv[z + 1] == 'n':
                                if deriv[z + 3] == 'e' and deriv[z + 4] == ')':
                                    if deriv[z - 1] in ['*', '/']:
                                        del (funcDiv[-1])
                                    if deriv[z + 5] in ['*', '/']:
                                        z += 1
                                    z += 4
                                else:
                                    funcDiv.append('ln')
                                    z += 1
                            if deriv[z + 1] == 'o':
                                funcDiv.append('log10')
                                z += 4
                        elif deriv[z] == 'a':
                            if deriv[z + 1] == 's':
                                funcDiv.append('arcsin')
                                z += 3
                            elif deriv[z + 1] == 'c':
                                funcDiv.append('arccos')
                                z += 3
                            elif deriv[z + 1] == 't':
                                funcDiv.append('arctan')
                                z += 3
                        elif deriv[z] == 's':
                            if deriv[z + 1] == 'i':
                                funcDiv.append('sin')
                                z += 2
                            elif deriv[z + 1] == 'q':
                                funcDiv.append('sqrt')
                                z += 3
                        elif deriv[z] == 'c':
                            funcDiv.append('cos')
                            z += 2
                        elif deriv[z] == 't':
                            funcDiv.append('tan')
                            z += 2
                        if deriv[z] not in ['l', 'n', 'o', 'g', 's', 'i', 'c', 't', 'a', 'r', 'q']:
                            funcDiv.append(deriv[z])
                        z += 1

                    for z in range(len(funcDiv)):
                        try:
                            if funcDiv[z] == 'x':
                                funcDiv[z] = x
                        except:
                            pass
                    funcDiv = parenBal(funcDiv)
                    print(funcDiv)
                    dVal = equals(funcDiv)[0]
                    remove('f\'(x) = ' + derivPrint + ' | x = ')
                    add('f\'(x) = ' + derivPrint + ' | f\'(' + format(x) + ') = ' + format(dVal), '\n')
                re([], 'wait')
                while True:
                    if inMain([], 'wait', ['=', 'exit']) == '=':
                        break
                    else:
                        done2 == True
                        break


def inMain(lst, mode, rnge):
    global pos
    global charList
    global current
    done = False
    while done == False:
        if mode == 'calc':
            current = []
        if mode not in ['wait']:
            if '_' not in lst:
                lst.append('_')
            re(lst, mode)
        x = input()
        if x == 'off':
            standby()
        if x == 'left':
            lst = left(lst)
        if x == 'right':
            lst = right(lst)
        if x == 'up':
            return up(lst, mode)
        if x == 'down':
            return down(lst, mode)
        if mode == 'digs':
            if x in rnge:
                print(x)
                return x
            if x == 'exit':
                del_(lst)
                upLayer()
                return 'exit'
        if mode in ['calc', 'func', 'op']:
            if x in digits:
                charIn(lst, str(int(x) % 10), True)
            if x == 'pi':
                charIn(lst, 'pi', False)
            if x == 'e':
                charIn(lst, 'e', False)
            if x == '.':
                charIn(lst, '.', False)
            if x == '(':
                charIn(lst, '(', False)
            if x == ')':
                charIn(lst, ')', False)
            if x == '^':
                charIn(lst, '^', False)
            if x == 'spec':
                inp = Funcs.special(lst, mode)
                if inp != 'exit':
                    charIn(lst, inp, False)
                del_(lst)
            if x == '/':
                charIn(lst, '/', False)
            if x == '*':
                charIn(lst, '*', False)
            if x == '-':
                charIn(lst, '-', False)
            if x == '+':
                charIn(lst, '+', False)
            if x == 'sqrt':
                charIn(lst, 'sqrt', False)
                charIn(lst, '(', False)
            if x == '=':
                del_(lst)
                done = True
                return 'done'
            if x == 'dlt':
                dlt(lst)
            if x == 'clear':
                if len(lst) == 0:
                    upLayer()
                    return 'exit'
                else:
                    clear(lst)
            if x == 'exit':
                upLayer()
                del_(lst)
                return 'exit'
            if mode in ['calc', 'func']:
                if x == 'funcVal':
                    del_(lst)
                    Funcs.fSpec('value')
                if x == 'deriv':
                    del_(lst)
                    Funcs.fSpec('deriv')
            if mode == 'calc':
                if x == 'fr':
                    charIn(lst, 'fr', False)
                if x == 'ans':
                    charIn(lst, 'ans', False)
                if x == 'funcIn':
                    del_(lst)
                    Funcs.funcIn()
            if mode == 'func':
                if x == 'x':
                    charIn(lst, 'x', False)
        if mode == 'wait':
            time.sleep(.25)
            # if x in rnge:
            return x
        x = ''


def left(lst):  # cursor left
    for x in range(len(lst)):
        if x > 0 and lst[x] == '_':
            lst[x], lst[x - 1] = lst[x - 1], lst[x]
            break
    return lst


def right(lst):  # cursor right
    for x in range(len(lst)):
        if x < len(lst) - 1 and lst[x] == '_':
            lst[x], lst[x + 1] = lst[x + 1], lst[x]
            break
    return lst


def up(lst, mode):  # shift cursor up
    global funcList
    if mode == 'func':
        for num, x in enumerate(funcList):
            for y in x:
                if y == '_':
                    del_(lst)
                    return lst, num - 1


def down(lst, mode):
    global funcList
    if mode == 'func':
        for num, x in enumerate(funcList):
            for y in x:
                if y == '_':
                    del_(lst)
                    return lst, num + 1


def del_(lst):  # deletes the cursor when done with a list

    for w, a in enumerate(lst):
        if a == '_':
            del (lst[w])
            break


def add(text, new):  ##add text to scree
    global lastTxt
    current.append(text)
    current.append(new)
    if new == '\n':
        lastTxt = ''


def remove(text):  ##delete text from screen
    global lastTxt
    for x in range(len(current)):
        if current[x] == text:
            del (current[x], current[x])
            break


def dlt(lst):  # delete last input character from active list
    for x in range(len(lst)):
        if lst[x] == '_' and x > 0:
            del (lst[x - 1])
            break


def re(lst, mode):
    os.system('clear')  ##Change to 'clear' for linux, 'clear' windows
    if mode == 'func':
        clr()
        Funcs.printAll()
    for y in range(0, len(current), 2):
        print(current[y], end=current[y + 1])
    if mode == 'calc':
        for y in range(1, len(ansList), 2):
            print(ansList[y])
    if mode != 'func':
        Funcs.printList(lst)


def clear(lst):  # calculator clear function
    del lst[:]
    os.system('clear')
    for y in range(0, len(current), 2):
        print(current[y], end=current[y + 1])


def clr():  # clears screen
    global old
    global current
    if current != []:
        old.append(current)
    current = []
    os.system('clear')


def upLayer():  # prints whatever was on the screen before u left
    global old
    global current
    if len(old) > 0:
        if old[-1] != []:
            current = old[-1]
            del (old[-1])
            #####         MAIN         #####


charList = []
shift = 0
oList = []
funcList = [[], [], [], [], [], [], [], [], [], []]
current = []
old = []
active = 0


def standby():  # 'off'
    # TURN SCREEN OFF (or complete shutdown?)
    x = inMain([], 'wait', ['on'])
    # TURN SCREEN ON
    return


def format(output):  # format an mpf
    output = str(output)
    if str(output) == str(mpmathify(mp.pi))[:100]:
        return 'π'
    elif str(output) == str(mpmathify(mp.e))[:100]:
        return 'e'
    output = str(mpmathify(output))
    if str(output)[-2:] == '.0':
        if mpmathify(output) == 0 and output[0] == '-':
            return '0'
        return str(output)[:-2]
    else:

        return str(round(mpf(output), 8))


while True:  # run calculator!
    # try: ERROR
    inMain(charList, 'calc', [])

    charList = equals(charList)

    if charList not in [[], ['error']]:
        output = mpmathify(charList[0])

        ansList.append(output)
        if len(charList) == 1:

            oList = repeatTest(
                charList)  # [original, repeating format, start, length of repeating, digits that repeat]              UNCOMMENT WHEN FIXED

            if isinstance(oList[0], list):
                out = ''
                real = oList[0]
                comp = oList[1]
                r = format(real[0])
                c = format(comp[0][:-1]) + 'i'
                if real[4] not in ['']:
                    r = real[1] + '\u0305'
                if r != '0':
                    out = r + ' + '
                if comp[4] not in ['']:
                    c = comp[1] + '\u0305i'
                if c in ['0i', '0.0i']:
                    out = out.replace(' + ', '')
                elif c in '1i':
                    out += 'i'
                else:
                    out += c
                ansList.append(out)


            else:
                if oList[4] != '':
                    ansList.append(str(oList[1]) + '\u0305')
                else:
                    ansList.append(format(output))
            pass
        elif charList[-1] == 'fr':
            ansList.append(fracOut(charList, 1))
    clearLists()
# except: ERROR
# error('Syntax error')
G.cleanup()
