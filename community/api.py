from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Replace with your actual Tune Studio API endpoint
TUNE_API_ENDPOINT = 'https://api.tune.app/your-endpoint'

# Replace with your Tune Studio API key or authentication token if required
TUNE_API_KEY = 'YOUR_TUNE_API_KEY'

# Replace with your weather data provider API key
WEATHER_API_KEY = 'YOUR_WEATHER_API_KEY'

@app.route('/weather', methods=['GET'])
def get_weather():
    # Get latitude and longitude from query parameters
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if not lat or not lon:
        return jsonify({'error': 'Please provide latitude and longitude parameters.'}), 400

    try:
        # Call the weather API to get weather data
        weather_url = (
            f'https://api.openweathermap.org/data/2.5/weather'
            f'?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric'
        )
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()

        if weather_response.status_code != 200:
            return jsonify({'error': weather_data.get('message', 'Error fetching weather data.')}), weather_response.status_code

        # Prepare data to send to Tune Studio API
        tune_payload = {
            'latitude': lat,
            'longitude': lon,
            'weather': weather_data
        }

        # Headers for the request to Tune Studio
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {TUNE_API_KEY}'
        }

        # Call the Tune Studio API
        tune_response = requests.post(TUNE_API_ENDPOINT, json=tune_payload, headers=headers)
        tune_data = tune_response.json()

        if tune_response.status_code != 200:
            return jsonify({'error': tune_data.get('message', 'Error processing data with Tune Studio.')}), tune_response.status_code

        # Return the processed data
        return jsonify(tune_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
