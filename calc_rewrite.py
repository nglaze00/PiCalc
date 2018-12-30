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
digits = "0123456789."

def element_type(element):
    if element[0] in "0123456789.":
        return "num"
    if element[0] in "+-*/^":
        return "op"
    if element[0] in "(":
        return "("
    if element[0] in ")":
        return ")"


def operate(first_op, second_op, operator):
    return operator(first_op, second_op)

def collapse(expression):
    """
    :return: expression, with all multi-digit numbers collapsed down to a single index
    """
    num = ""
    i = 0
    while i < len(expression):
        if expression[i] in digits:
            num += expression[i]
            del(expression[i])
        else:
            if num:
                expression.insert(i, num)
                num = ""
            i += 1
    if num:
        expression.append(num)
    return expression

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
        if token[0] in "0123456789.":           #fix for multi-digit numbers / decimals
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
def eval(str_exp):
    """

    :param postfix: user-input expression converted to postfix
    :return: evaluted expression
    """
    expression = postfix(collapse(str_exp))
    operands = []
    print(postfix)
    for token in postfix:
        if token in "+-*/^":
            if len(operands) < 2:
                return "error: invalid input"
            res = operate(float(operands.pop()), float(operands.pop()), ops[token])
            operands.append(res)
        else:
            operands.append(token)
    print(operands)
    if len(operands) != 1:
        return "error: invalid input"
    return operands[0]

print (eval("1+1"))