# Written by Nicholas Glaze
from math import exp


def add(a, b):
    return a + b


def sub(a, b):
    return a - b


def mult(a, b):
    return a * b


def div(a, b):
    if b == 0:
        return "error: div by 0"
    return a / b


def pow(a, b):
    return a ** b


ops = {"+": add,
       "-": sub,
       "*": mult,
       "/": div,
       "^": pow}


def digit_type(digit):
    if digit in "0123456789":
        return "num"
    if digit in "+-*/^":
        return "op"
    if digit in "(":
        return "("
    if digit in ")":
        return ")"


def operate(first_op, second_op, operator):
    return operator(first_op, second_op)


def postfix(expression):
    """

    :param expression: user input string
    :return: input converted to postfix
    """
    precedence = {"(": -1,
                  "+": 0,
                  "-": 0,
                  "*": 1,
                  "/": 1,
                  "^": 2, }
    opstack = []
    res = []
    infix = list(expression)
    for token in infix:
        if token in "0123456789":           #fix for multi-digit numbers / decimals
            res.append(token)
        elif token == "(":
            opstack.append(token)
        elif token == ")":
            while opstack:
                operator = opstack.pop()
                if operator == "(":
                    break
                res.append(operator)
        elif token in "+-*/^":
            while opstack and precedence[opstack[-1]] >= precedence[token]:
                res.append(opstack.pop())
            opstack.append(token)
    while opstack:
        res.append(opstack.pop())
    return res
def eval(postfix):
    """

    :param postfix: user-input expression converted to postfix
    :return: evaluted expression
    """
    operands = []
    print(postfix)
    for token in postfix:
        if token in "+-*/^":
            if len(operands) < 2:
                return "error: invalid input"
            res = operate(operands.pop(), operands.pop(), ops[token])
            operands.append(res)
    if len(operands) != 1:
        return "error: invalid input"
    return operands[0]

print(eval(postfix("1+1")))