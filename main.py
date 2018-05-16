from flask import Flask, request
from state_manager import StateManager
from state_input_pair import StateInputPair
import json

app = Flask(__name__)

@app.route('/', methods=['POST'])
def calc():
    return StateManager.process_request(request.json)


# if __name__ == '__main__':
#     s1 = '{"input": "", "state": null}'
#     print(StateManager.process_request(s1))




#     s2 = '{"input": "*", "state": {"display": "", "is_invalid_input": false, "is_operator_in_stack": false, "is_stack_head_a_result": false, "stack": []}}'
#     s3 = '{"input": "0", "state": {"display": "", "is_invalid_input": false, "is_operator_in_stack": false, "is_stack_head_a_result": false, "stack": []}}'
#     s4 = '{"input": "=", "state": {"display": "", "is_invalid_input": false, "is_operator_in_stack": false, "is_stack_head_a_result": false, "stack": []}}'
#