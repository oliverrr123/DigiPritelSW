from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

slider_value = 50

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/update-slider', methods=['POST'])
def update_slider():
    global slider_value
    data = request.get_json()
    slider_value = data.get('slider_value')
    print(f"Slider Value: {slider_value}")
    os.system(f'osascript -e "set volume output volume {slider_value}"')
    return jsonify({'value': slider_value})

# @app.route('/update', methods=['POST'])
# def update():
#     global paragraph_content
#     data = request.get_json()
#     paragraph_content = data['content']
#     return 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)