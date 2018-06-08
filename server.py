from flask import Flask, request, abort
from state_manager import StateManager
app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calc():
    try:
        return StateManager.process_request(request.json)
    except:
        abort(500)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
