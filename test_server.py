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
        body = self.generateBody(_state, _input)
        resp = self.postCalculate(self, body)
        self.validateNextStateResponse(resp)
        data = self.getResponseData(resp)
        assert data['display'] == _input
        assert data['stack'][0] == _input

    def test_multi_digit_number(self):
        _state = None
        inputs = ["1", "2", "3"]

        # First request
        body = self.generateBody(_state, inputs[0])
        resp = self.postCalculate(self, body)
        state = self.getResponseData(resp)

        # Second request
        body = self.generateBody(state, inputs[1])
        resp = self.postCalculate(self, body)

        # Validate second request
        self.validateNextStateResponse(resp)
        state = self.getResponseData(resp)
        assert state['display'] == ''.join(inputs[:2])
        assert state['stack'][0] == inputs[0]
        assert state['stack'][1] == inputs[1]

        # Third request
        body = self.generateBody(state, inputs[2])
        resp = self.postCalculate(self, body)

        # Validate third request
        self.validateNextStateResponse(resp)
        state = self.getResponseData(resp)
        assert state['display'] == ''.join(inputs[:3])
        assert state['stack'][0] == inputs[0]
        assert state['stack'][1] == inputs[1]
        assert state['stack'][2] == inputs[2]

    # def test_plus_op(self):
    #     _state = None
    #     _input = "1"
    #     initialStateBody = self.generateBody(_state, _input)
    #     resp = self.postCalculate(self, initialStateBody)
    #
    #
    #     self.validateNextStateResponse(resp)
    #     data = self.getResponseData(resp)
    #     assert data['display'] == _input
    #     assert data['stack'][0] == _input


    def test_should_return_invalid_op_initial_state_input_is_eq(self):
        _state = None
        _input = "="
        body = self.generateBody(_state, _input)
        resp = self.postCalculate(self, body)
        self.validateNextStateResponse(resp)
        data = self.getResponseData(resp)
        assert data['display'] == INVALID_OP_STRING
        assert data['is_invalid_input'] is False
        assert data['is_operator_in_stack'] is False
        assert data['is_stack_head_a_result'] is False
        assert len(data['stack']) == 0

    def test_should_return_invalid_op_initial_state_input_is_mult(self):
        _state = None
        _input = "*"
        body = self.generateBody(_state, _input)
        resp = self.postCalculate(self, body)
        self.validateNextStateResponse(resp)
        data = self.getResponseData(resp)
        assert data['display'] == INVALID_OP_STRING
        assert data['is_invalid_input'] is False
        assert data['is_operator_in_stack'] is False
        assert data['is_stack_head_a_result'] is False
        assert len(data['stack']) == 0

    def test_should_return_invalid_op_initial_state_input_is_plus(self):
        _state = None
        _input = "+"
        body = self.generateBody(_state, _input)
        resp = self.postCalculate(self, body)
        self.validateNextStateResponse(resp)
        data = self.getResponseData(resp)
        assert data['display'] == INVALID_OP_STRING
        assert data['is_invalid_input'] is False
        assert data['is_operator_in_stack'] is False
        assert data['is_stack_head_a_result'] is False
        assert len(data['stack']) == 0

    def test_should_return_invalid_op_initial_state_input_is_minus(self):
        _state = None
        _input = "-"
        body = self.generateBody(_state, _input)
        resp = self.postCalculate(self, body)
        self.validateNextStateResponse(resp)
        data = self.getResponseData(resp)
        assert data['display'] == INVALID_OP_STRING
        assert data['is_invalid_input'] is False
        assert data['is_operator_in_stack'] is False
        assert data['is_stack_head_a_result'] is False
        assert len(data['stack']) == 0

    def test_should_return_invalid_op_initial_state_input_is_unrecognized_char(self):
        _state = None
        _input = "$"
        body = self.generateBody(_state, _input)
        resp = self.postCalculate(self, body)
        self.validateNextStateResponse(resp)
        data = self.getResponseData(resp)
        assert data['display'] == INVALID_OP_STRING
        assert data['is_invalid_input'] is False
        assert data['is_operator_in_stack'] is False
        assert data['is_stack_head_a_result'] is False
        assert len(data['stack']) == 0

    def test_should_return_500_no_calculatorstate_field(self):
        body = dict(
            input="1"
        )
        resp = self.postCalculate(self, body)
        assert resp.status_code == 500

    def test_should_return_500_no_input_field(self):
        body = dict(
            calculaturState=None
        )
        resp = self.postCalculate(self, body)
        assert resp.status_code == 500

    def test_should_return_500_input_is_not_string(self):
        body = dict(
            calculatorState=None,
            input=1
        )
        resp = self.postCalculate(self, body)
        assert resp.status_code == 500


    def test_should_return_500_calculatorstate_is_not_json(self):
        body = dict(
            calculatorState="not_json",
            input=1
        )
        resp = self.postCalculate(self, body)
        assert resp.status_code == 500


    def validateNextStateResponse(self,resp):
        assert resp.status_code == 200
        data = self.getResponseData(resp)
        assert 'display' in data and isinstance(data['display'], str)
        assert 'is_invalid_input' in data and isinstance(data['is_invalid_input'], bool)
        assert 'is_operator_in_stack' in data and isinstance(data['is_operator_in_stack'], bool)
        assert 'is_stack_head_a_result' in data and isinstance(data['is_stack_head_a_result'], bool)
        assert 'stack' in data and isinstance(data['stack'], list)

    def getResponseData(self, resp):
        return json.loads(resp.get_data(as_text=True))

    def generateBody(self, state, _input):
        return dict(
            calculatorState=state,
            input=_input
        )


    def postCalculate(self, instance, body):
        return instance.app.post(
            ServerTestCase.CALCULATE_PATH,
            data=json.dumps(body),
            content_type='application/json')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ServerTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
