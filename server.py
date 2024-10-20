from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
socketio = SocketIO(app)

slider_value = 50
state = "Probouzím se..."

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html', state=state)

@app.route('/update-slider', methods=['POST'])
def update_slider():
    global slider_value
    data = request.get_json()
    slider_value = data.get('slider_value')
    print(f"Slider Value: {slider_value}")
    os.system(f'amixer -M sset Master {slider_value}%')
    return jsonify({'value': slider_value})

# @app.route('/update', methods=['POST'])
# def update():
#     global paragraph_content
#     data = request.get_json()
#     paragraph_content = data['content']
#     return 200

@app.route('/updatestate', methods=['POST'])
def update_state():
    global state
    data = request.get_json()
    state = data['content']
    socketio.emit('update_state', {'new_state': state})
    return jsonify({'message': 200})

if __name__ == '__main__':
    socketio.run(app, debug=True)
