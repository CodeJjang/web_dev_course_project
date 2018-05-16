

INVALID_OP_STRING = "Invalid operation, reset"


OPERATOR_DICT = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a / b if b != 0 else exec('raise(Exception(\'can not divide by zero\'))')
}