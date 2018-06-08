import os
import server
import unittest
import json
from consts import INVALID_OP_STRING

class ServerTestCase(unittest.TestCase):
    CALCULATE_PATH = '/calculate'

    def setUp(self):
        server.app.testing = True
        server.app.debug = True
        self.app = server.app.test_client()

    def tearDown(self):
        pass

    def test_initial_state_calculatorstate_null(self):
        _state = None
        _input = "1"
        body = self.generate_body(_state, _input)
        resp = self.post_calculate(self, body)
        self.validate_next_state_response(resp)
        data = self.get_response_data(resp)
        self.validate_display(data, _input)
        self.validate_stack(data, [_input])

    def test_multi_digit_number(self):
        _state = None
        inputs = ["1", "2", "3"]

        # First request
        body = self.generate_body(_state, inputs[0])
        resp = self.post_calculate(self, body)
        state = self.get_response_data(resp)

        # Second request
        body = self.generate_body(state, inputs[1])
        resp = self.post_calculate(self, body)

        # Validate second request
        self.validate_next_state_response(resp)
        state = self.get_response_data(resp)
        self.validate_display(state, ''.join(inputs[:2]))
        self.validate_stack(state, inputs[:2])

        # Third request
        body = self.generate_body(state, inputs[2])
        resp = self.post_calculate(self, body)

        # Validate third request
        self.validate_next_state_response(resp)
        state = self.get_response_data(resp)
        self.validate_display(state, ''.join(inputs[:3]))
        self.validate_stack(state, inputs[:3])

    def test_plus_op(self):
        _state = None
        inputs = ["1", "+", "2", "="]
        expected_output = "3"

        # First request
        body = self.generate_body(_state, inputs[0])
        resp = self.post_calculate(self, body)
        state = self.get_response_data(resp)

        # Second request
        body = self.generate_body(state, inputs[1])
        resp = self.post_calculate(self, body)

        # Validate second request
        self.validate_next_state_response(resp)
        state = self.get_response_data(resp)
        self.validate_display(state, inputs[0])
        self.validate_stack(state, inputs[:2])

        # Third request
        body = self.generate_body(state, inputs[2])
        resp = self.post_calculate(self, body)

        # Validate third request
        self.validate_next_state_response(resp)
        state = self.get_response_data(resp)
        self.validate_display(state, inputs[2])
        self.validate_stack(state, inputs[:3])

        # Fourth request
        body = self.generate_body(state, inputs[3])
        resp = self.post_calculate(self, body)

        # Validate fourth request
        self.validate_next_state_response(resp)
        state = self.get_response_data(resp)
        self.validate_display(state, expected_output)
        self.validate_stack(state, [expected_output])


    def test_should_return_invalid_op_initial_state_input_is_eq(self):
        _state = None
        _input = "="
        body = self.generate_body(_state, _input)
        resp = self.post_calculate(self, body)
        self.validate_next_state_response(resp)
        data = self.get_response_data(resp)
        self.validate_invalid_op(data)

    def test_should_return_invalid_op_initial_state_input_is_mult(self):
        _state = None
        _input = "*"
        body = self.generate_body(_state, _input)
        resp = self.post_calculate(self, body)
        self.validate_next_state_response(resp)
        data = self.get_response_data(resp)
        self.validate_invalid_op(data)

    def test_should_return_invalid_op_initial_state_input_is_plus(self):
        _state = None
        _input = "+"
        body = self.generate_body(_state, _input)
        resp = self.post_calculate(self, body)
        self.validate_next_state_response(resp)
        data = self.get_response_data(resp)
        self.validate_invalid_op(data)

    def test_should_return_invalid_op_initial_state_input_is_minus(self):
        _state = None
        _input = "-"
        body = self.generate_body(_state, _input)
        resp = self.post_calculate(self, body)
        self.validate_next_state_response(resp)
        data = self.get_response_data(resp)
        self.validate_invalid_op(data)

    def test_should_return_invalid_op_initial_state_input_is_unrecognized_char(self):
        _state = None
        _input = "$"
        body = self.generate_body(_state, _input)
        resp = self.post_calculate(self, body)
        self.validate_next_state_response(resp)
        data = self.get_response_data(resp)
        self.validate_invalid_op(data)

    def test_should_return_500_no_calculatorstate_field(self):
        body = dict(
            input="1"
        )
        resp = self.post_calculate(self, body)
        assert resp.status_code == 500

    def test_should_return_500_no_input_field(self):
        body = dict(
            calculaturState=None
        )
        resp = self.post_calculate(self, body)
        assert resp.status_code == 500

    def test_should_return_500_input_is_not_string(self):
        body = dict(
            calculatorState=None,
            input=1
        )
        resp = self.post_calculate(self, body)
        assert resp.status_code == 500


    def test_should_return_500_calculatorstate_is_not_json(self):
        body = dict(
            calculatorState="not_json",
            input=1
        )
        resp = self.post_calculate(self, body)
        assert resp.status_code == 500


    def validate_display(self, data, value):
        assert data['display'] == value

    def validate_stack(self, data, value):
        assert data['stack'] == value

    def validate_invalid_op(self, data):
        assert data['display'] == INVALID_OP_STRING
        assert data['is_invalid_input'] is False
        assert data['is_operator_in_stack'] is False
        assert data['is_stack_head_a_result'] is False
        assert len(data['stack']) == 0

    def validate_next_state_response(self,resp):
        assert resp.status_code == 200
        data = self.get_response_data(resp)
        assert 'display' in data and isinstance(data['display'], str)
        assert 'is_invalid_input' in data and isinstance(data['is_invalid_input'], bool)
        assert 'is_operator_in_stack' in data and isinstance(data['is_operator_in_stack'], bool)
        assert 'is_stack_head_a_result' in data and isinstance(data['is_stack_head_a_result'], bool)
        assert 'stack' in data and isinstance(data['stack'], list)

    def get_response_data(self, resp):
        return json.loads(resp.get_data(as_text=True))

    def generate_body(self, state, _input):
        return dict(
            calculatorState=state,
            input=_input
        )


    def post_calculate(self, instance, body):
        return instance.app.post(
            ServerTestCase.CALCULATE_PATH,
            data=json.dumps(body),
            content_type='application/json')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ServerTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
