from flask import Flask, render_template, request, jsonify
import phonenumbers
from phonenumbers import geocoder as phone_geocoder
from opencage.geocoder import OpenCageGeocode
from datetime import datetime
import pytz  # Import pytz for timezone handling

app = Flask(__name__)
Key = "6d6f969fd9024ac8afde957f0c86a5ba"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/track', methods=['POST'])
def track():
    number = request.form['phone_number']
    try:
        check_number = phonenumbers.parse(number)
        number_location = phone_geocoder.description_for_number(check_number, "en")
        if number_location:
            opencage_geocoder = OpenCageGeocode(Key)
            results = opencage_geocoder.geocode(number_location)
            if results:
                lat = results[0]['geometry']['lat']
                lng = results[0]['geometry']['lng']
                location_details = results[0]['formatted']

                # Set the timezone to your desired one, for example, 'Asia/Kolkata'
                timezone = pytz.timezone('Asia/Kolkata')
                now = datetime.now(timezone)
                current_time = now.strftime("%Y-%m-%d %H:%M:%S")

                return jsonify({
                    'location': number_location,
                    'lat': lat,
                    'lng': lng,
                    'details': location_details,
                    'time': current_time
                })
            else:
                return jsonify({'error': 'Location could not be found.'}), 400
        else:
            return jsonify({'error': 'Invalid phone number.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/live_update', methods=['GET'])
def live_update():
    # For demonstration, we're using static data. Replace this with actual API or logic.
    lat = 20.5937  # Static example latitude
    lng = 78.9629  # Static example longitude
    location_details = "Updated Location Information"

    # Set the timezone to your desired one, for example, 'Asia/Kolkata'
    timezone = pytz.timezone('Asia/Kolkata')
    now = datetime.now(timezone)
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    return jsonify({
        'lat': lat,
        'lng': lng,
        'location': 'Current Location',
        'details': location_details,
        'time': current_time
    })


if __name__ == '__main__':
    app.run(debug=True)
