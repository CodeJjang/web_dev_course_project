from flask import Flask, request, abort
from state_manager import StateManager

app = Flask(__name__)
@app.route('/calculate', methods=['POST'])
def calc():
    try:
        print('Server received ' + str(request.json))
        resp = StateManager.process_request(request.json)
        print('Server returned ' + str(resp))
        return resp
    except Exception as e:
        print(e)
        abort(500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
