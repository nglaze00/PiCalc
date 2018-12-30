# Written by Nicholas Glaze
import math
from calc_rewrite.display_manager import Menu
class Evaluator(Menu):
    def __init__(self):
        Menu.__init__([])
        self._answers = []
        self._ops = {"+": self.add,
               "-": self.sub,
               "*": self.mult,
               "/": self.div,
               "^": self.pow,
               "sin": math.sin,
               "cos": math.cos,
               "tan": math.tan,
               "asin": math.asin,
               "acos": math.acos,
               "atan": math.atan}
        self._binary_ops = "+-*/^"
        self._precedence = {"(": -2,
                      "sin": -1,
                      "cos": -1,
                      "tan": -1,
                      "asin": -1,
                      "acos": -1,
                      "atan": -1,
                      "+": 0,
                      "-": 0,
                      "*": 1,
                      "/": 1,
                      "^": 2, }
        self._digits = "0123456789."


    def add(self, a, b):
        return a + b
    def sub(self, a, b):
        return a - b
    def mult(self, a, b):
        return a * b
    def div(self, a, b):
        if b == 0:
            return self.error("div by 0")
        return a / b
    def pow(self, a, b):
        return a ** b

    def element_type(self, element):
        if element[0] in "0123456789.":
            return "num"
        if element[0] in self._ops.keys():
            return "op"
        if element[0] in "(":
            return "("
        if element[0] in ")":
            return ")"

    def error(self, msg):
        return "error: " + msg

    def operate(self, first_op, second_op, operator):
        return operator(first_op, second_op)

    def substitute(self, expression = []):
        i = 0
        while i < len(expression):
            if expression[i] == "a":
                expression = expression[:i] + list(str(self._answers[-expression[i + 1]])) + expression[i + 1:]
    def collapse(self, expression = []):
        """
        :return: expression, with all multi-digit numbers collapsed down to a single index
        """

        num = ""
        i = 0
        while i < len(expression):
            if expression[i] in self._digits:
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

    def add_mult(self, expression = []):
        """

        :param expression: list representing expression
        :return: expression, with * added between e.g. "2(" and ")4"
        """
        i = 0
        while i < len(expression):
            if i > 0 and expression[i] == "(" and expression[i - 1] in self._digits:
                expression.insert(i, "*")
                i += 1
            elif i < len(expression) - 1 and expression[i] == ")" and expression[i + 1] in self._digits:
                expression.insert(i + 1, "*")
                i += 2
            i += 1
        return expression

    def postfix(self, expression = []):
        """

        :param expression: user input string
        :return: input converted to postfix
        """
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
            elif token in self._ops.keys():
                while opstack and self._precedence[opstack[-1]] >= self._precedence[token]:
                    res.append(opstack.pop())
                opstack.append(token)
        while opstack:
            res.append(opstack.pop())
        return res

    def format_input(self, str_exp=""):
        """

        :param str_exp: input expression
        :return: expression, properly formatted for evaluation
        """
        expression = list(str_exp)
        return self.postfix(self.collapse(self.add_mult(expression)))

    def format_output(self, output):
        """

        :param output: result of evaluated expression
        :return: expression formatted to 5 decimal places or 0 if integer
        """
        if output.is_integer():
            return int(output)
        else:
            return "{:.2f}".format(output)

    def eval(self, str_exp):
        """

        :param str_exp: user-input expression string
        :return: result of expression
        """
        expression = self.format_input(str_exp)
        operands = []
        print(expression)
        for token in expression:
            if token in self._binary_ops:
                if len(operands) < 2:
                    return self.error("invalid input")
                num2, num1 = float(operands.pop()), float(operands.pop())
                res = self.operate(num1, num2, self._ops[token])
                operands.append(res)
            elif token in self._ops.keys():   #unary operator
                if not operands:
                    return self._error("invalid input")
            else:
                operands.append(token)
        if len(operands) != 1:
            return self._error("invalid input")
        return operands[0]

    def display(self):
        while True:
            str_exp = input()
            res = eval(str_exp)
            if res[0] != "e":
                print(self.format_output(res))
                self._answers.append(res)
            else:
                print(res)
