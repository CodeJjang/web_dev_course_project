import os
import server
import unittest
import json


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
        _input = 1
        body = self.generateBody(_state, _input)
        resp = self.postCalculate(self, body)
        self.validateNextStateResponse(resp)

    def test_should_return_500_input_is_not_string(self):
        body = dict(
            calculatorState=None,
            input=1
        )
        resp = self.postCalculate(self, body)
        assert resp.status_code == 500

    def validateNextStateResponse(self,resp):
        assert resp.status_code == 200
        data = json.loads(resp.get_data(as_text=True))
        assert 'display' in data and isinstance(data['display'], str)
        assert 'is_invalid_input' in data and isinstance(data['is_invalid_input'], bool)
        assert 'is_operator_in_stack' in data and isinstance(data['is_operator_in_stack'], bool)
        assert 'is_stack_head_a_result' in data and isinstance(data['is_stack_head_a_result'], bool)
        assert 'stack' in data and isinstance(data['stack'], list)


    def generateBody(self, state, _input):
        return dict(
            calculatorState=state,
            input=str(_input)
        )


    def postCalculate(self, instance, body):
        return instance.app.post(
            ServerTestCase.CALCULATE_PATH,
            data=json.dumps(body),
            content_type='application/json')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ServerTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
