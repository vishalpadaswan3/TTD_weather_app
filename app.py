from flask import Flask
from flask import request, jsonify

app = Flask(__name__)


weather_data = {
    'San Francisco': {'temperature': 14, 'weather': 'Cloudy'},
    'New York': {'temperature': 20, 'weather': 'Sunny'},
    'Los Angeles': {'temperature': 24, 'weather': 'Sunny'},
    'Seattle': {'temperature': 10, 'weather': 'Rainy'},
    'Austin': {'temperature': 32, 'weather': 'Hot'},
}

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/weather/<string:city>')
def get_weather(city):
    if city in weather_data:
        return weather_data[city]
    else:
        return {
            'error': f"Weather information not found for city: {city}"
        }, 404


@app.route('/weather', methods=['POST'])
def add_weather():
    data = request.get_json()
    city = data.get('city')
    temperature = data.get('temperature')
    weather = data.get('weather')

    if not city or not temperature or not weather:
        return jsonify(error='Missing required fields'), 400

    weather_data[city] = {'temperature': temperature, 'weather': weather}
    return jsonify(message=f"Weather information added for {city}")

@app.route('/weather/<string:city>', methods=['PUT'])
def update_weather(city):
    if city not in weather_data:
        return jsonify(error=f"Weather information not found for city: {city}"), 404

    data = request.get_json()
    temperature = data.get('temperature')
    weather = data.get('weather')

    if temperature:
        weather_data[city]['temperature'] = temperature
    if weather:
        weather_data[city]['weather'] = weather

    return jsonify(message=f"Weather information updated for {city}")

@app.route('/weather/<string:city>', methods=['DELETE'])
def delete_weather(city):
    if city not in weather_data:
        return jsonify(error=f"Weather information not found for city: {city}"), 404

    del weather_data[city]
    return jsonify(message=f"Weather information deleted for {city}")



