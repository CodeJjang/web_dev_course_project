import os
import sys
import unittest

# operators = ['+', '-', '*', '/']

operators_dict = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a / b if b != 0 else exec('raise(Exception(\'can not divide by zero\'))')
}


class JsonState:
    def __init__(self, stack, is_operator_in_stack=False, is_stack_head_a_result=False):
        self.stack = stack
        self.display = ''
        self.is_operator_in_stack = is_operator_in_stack
        self.is_stack_head_a_result = is_stack_head_a_result

    def update_display(self):
        if self.display != 'can not divide by zero':
            display_string = ''
            for index, item in enumerate(self.stack):
                if item in operators_dict.keys() and not index + 1 == len(self.stack):
                    display_string = ''
                elif item not in operators_dict.keys():
                    display_string += item
            self.display = display_string

    def evaluate(self):
        a, b, operator = self.__extract_arguments()
        self.stack.clear()
        try:
            self.stack.append(str(operators_dict[operator](a, b)))
        except Exception as e:
            self.__reset_json()
            self.display = e.args[0]

    def __reset_json(self):
        self.stack = []
        self.is_stack_head_a_result = False
        self.is_operator_in_stack = False

    def __extract_arguments(self):
        a, b = '', ''
        operator = None
        for item in self.stack:
            if item in operators_dict.keys():
                operator = item
                break
            else:
                a = a + item
        for item in reversed(self.stack):
            if item in operators_dict.keys():
                break
            else:
                b = item + b
        return int(a), int(b), operator


def calculate_next_state(json_state, input):
    if json_state is None and str.isdigit(input):
        stack = []
        stack.append(input)
        json_state = JsonState(stack)

    elif json_state is None and not str.isdigit(input):
        raise Exception('received = or an operator as first argument')

    elif str.isdigit(input) and not json_state.is_stack_head_a_result:
        json_state.stack.append(input)

    elif str.isdigit(input) and json_state.is_stack_head_a_result:
        json_state.stack.clear()
        json_state.stack.append(input)
        json_state.is_stack_head_a_result = False

    elif input in operators_dict.keys() and not json_state.is_operator_in_stack:
        json_state.stack.append(input)
        json_state.is_stack_head_a_result = False

    elif input in operators_dict.keys() and json_state.is_operator_in_stack:
        json_state.evaluate()
        json_state.stack.append(input)

    elif input == '=' and json_state.stack[-1] in operators_dict.keys():
        json_state.stack.append('0')
        json_state.evaluate()
        json_state.is_stack_head_a_result = True

    elif input == '=':
        json_state.evaluate()
        json_state.is_stack_head_a_result = True


    json_state.update_display()
    return json_state


def main():

    s = calculate_next_state(None, '1')
    print(s.display)
    s = calculate_next_state(s, '2')
    print(s.display)
    s = calculate_next_state(s, '+')
    print(s.display)
    s = calculate_next_state(s, '4')
    print(s.display)
    s = calculate_next_state(s, '3')
    print(s.display)
    s = calculate_next_state(s, '=')
    print(s.display)
    s = calculate_next_state(s, '+')
    print(s.display)
    s = calculate_next_state(s, '1')
    print(s.display)
    s = calculate_next_state(s, '=')
    print(s.display)
    s = calculate_next_state(s, '5')
    print(s.display)
    s = calculate_next_state(s, '/')
    print(s.display)
    s = calculate_next_state(s, '0')
    print(s.display)
    s = calculate_next_state(s, '=')
    print(s.display)
    s = calculate_next_state(s, '2')
    print(s.display)
    s = calculate_next_state(s, '+')
    print(s.display)
    s = calculate_next_state(s, '4')
    print(s.display)
    s = calculate_next_state(s, '3')
    print(s.display)
    s = calculate_next_state(s, '=')
    print(s.display)

if __name__ == '__main__':
    main()