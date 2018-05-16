import json
from calculator import Calculator
from consts import OPERATOR_DICT
from collections import namedtuple
from state_input_pair import StateInputPair


class StateManager(object):

    @staticmethod
    def is_digit_or_fraction(input):
        if str.isdigit(input):
            return True
        else:
            values = input.split('/')
            return len(values) == 2 and all(i.isdigit() for i in values)

    @staticmethod
    def process_request(state_input_pair_json):

        state_key_pair = StateInputPair(state_input_pair_json['state'], state_input_pair_json['input'])
        return StateManager.calculate_next_state(state_key_pair.state, state_key_pair.input)

    @staticmethod
    def calculate_next_state(json_state, input):
        if json_state is None and StateManager.is_digit_or_fraction(input):
            stack = []
            stack.append(input)
            json_state = Calculator(stack)

        elif json_state is None and not StateManager.is_digit_or_fraction(input):
            json_state = Calculator()
            json_state.is_invalid_input = True

        elif (not json_state.stack and not StateManager.is_digit_or_fraction(input)) or\
                (len(json_state.stack) > 0 and not StateManager.is_digit_or_fraction(json_state.stack[-1]) and not StateManager.is_digit_or_fraction(input)):
            json_state.is_invalid_input = True

        elif (not StateManager.is_digit_or_fraction(input) and not input in OPERATOR_DICT and not input == '='):
            json_state.is_invalid_input = True

        elif StateManager.is_digit_or_fraction(input) and not json_state.is_stack_head_a_result:
            json_state.stack.append(input)

        elif StateManager.is_digit_or_fraction(input) and json_state.is_stack_head_a_result:
            json_state.stack.clear()
            json_state.stack.append(input)
            json_state.is_stack_head_a_result = False

        elif input in OPERATOR_DICT.keys() and not json_state.is_operator_in_stack:
            json_state.stack.append(input)
            json_state.is_stack_head_a_result = False
            json_state.is_operator_in_stack = True

        elif input in OPERATOR_DICT.keys() and json_state.is_operator_in_stack:
            json_state.evaluate()
            json_state.stack.append(input)

        elif input == '=' and not json_state.is_operator_in_stack:
            json_state.is_invalid_input = True

        elif input == '=':
            json_state.evaluate()
            json_state.is_stack_head_a_result = True
            json_state.is_operator_in_stack = False

        json_state.update_display()
        return json_state.to_JSON()


def main():
    s = None

    s = StateManager.calculate_next_state(s, '+')
    obj = json.loads(s)
    print(obj['display'])
    # s = calculate_next_state(s, '2')
    # print(s.display)
    # s = calculate_next_state(s, '+')
    # print(s.display)
    # s = calculate_next_state(s, '4')
    # print(s.display)
    # s = calculate_next_state(s, '3')
    # print(s.display)
    # s = calculate_next_state(s, '=')
    # print(s.display)
    # s = calculate_next_state(s, '+')
    # print(s.display)
    # s = calculate_next_state(s, '1')
    # print(s.display)
    # s = calculate_next_state(s, '=')
    # print(s.display)
    # s = calculate_next_state(s, '5')
    # print(s.display)
    # s = calculate_next_state(s, '/')
    # print(s.display)
    # s = calculate_next_state(s, '0')
    # print(s.display)
    # s = calculate_next_state(s, '=')
    # print(s.display)
    # s = calculate_next_state(s, '2')
    # print(s.display)
    # s = calculate_next_state(s, '+')
    # print(s.display)
    # s = calculate_next_state(s, '4')
    # print(s.display)
    # s = calculate_next_state(s, '3')
    # print(s.display)
    # s = calculate_next_state(s, '=')
    # print(s.display)

if __name__ == '__main__':
    main()