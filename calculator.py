import json
from consts import INVALID_OP_STRING, OPERATOR_DICT


class Calculator(object):

    def __init__(self, stack=[], display='', is_operator_in_stack=False, is_stack_head_a_result=False, is_invalid_input=False):
        self.stack = stack
        self.display = display
        self.is_operator_in_stack = is_operator_in_stack
        self.is_stack_head_a_result = is_stack_head_a_result
        self.is_invalid_input = is_invalid_input

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def update_display(self):
        if self.is_invalid_input:
            self.display = INVALID_OP_STRING
            self.__reset_json()
        else:
            display_string = ''
            for index, item in enumerate(self.stack):
                if item in OPERATOR_DICT.keys() and not index == len(self.stack) - 1:
                    display_string = ''
                elif item not in OPERATOR_DICT.keys():
                    display_string += item
            self.display = display_string

    def evaluate(self):
        a, b, operator = self.__extract_arguments()
        self.stack.clear()
        try:
            self.stack.append(str(OPERATOR_DICT[operator](a, b)))
        except Exception:
            self.is_invalid_input = True

    def __reset_json(self):
        self.stack = []
        self.is_stack_head_a_result = False
        self.is_operator_in_stack = False
        self.is_invalid_input = False

    def __extract_arguments(self):
        a, b = '', ''
        operator = None
        for item in self.stack:
            if item in OPERATOR_DICT.keys():
                operator = item
                break
            else:
                a = a + item
        for item in reversed(self.stack):
            if item in OPERATOR_DICT.keys():
                break
            else:
                b = item + b
        return int(a), int(b), operator