from flask import Flask, request, jsonify, send_from_directory
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS to allow requests from your Framer site or other origins

def get_uv_index(city_name, api_key):
    base_url = "http://api.weatherbit.io/v2.0/current"
    params = {
        "city": city_name,
        "key": api_key
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    if response.status_code == 200 and 'data' in data and len(data['data']) > 0:
        uv_index = data['data'][0]['uv']
        return uv_index
    else:
        raise Exception("City not found or other error: " + str(data))

@app.route('/')
def index():
    return send_from_directory('', 'index.html')

@app.route('/uv-index')
def uv_index():
    city = request.args.get('city')
    api_key = "40b6256ad97b4e10be8bca1d97deb873"  # Replace with your actual API key
    try:
        uv_index = get_uv_index(city, api_key)
        return jsonify({'uv_index': uv_index})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
