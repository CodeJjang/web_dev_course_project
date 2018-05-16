import json
from calculator import Calculator

class StateInputPair(object):

    def __init__(self, state, input):
        self.input = input
        if state != None:
            self.state = Calculator(state['stack'], state['display'],
                                    state['is_operator_in_stack'], state['is_stack_head_a_result'], state['is_invalid_input'])
        else:
            self.state = Calculator()