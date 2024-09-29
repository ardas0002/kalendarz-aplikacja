import requests
from flask import Flask, jsonify, send_from_directory, request
from datetime import datetime, timedelta
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


API_URL = 'https://rekrutacja.teamwsuws.pl/events/'
API_KEY = 'e92650386f8307c9abaee4d19785bdb8'


@app.route('/api/events')
def get_events():
    headers = {'api-key': API_KEY}
    response = requests.get(API_URL, headers=headers)

    month = request.args.get('month', default=datetime.now().month, type=int)
    year = request.args.get('year', default=datetime.now().year, type=int)

    if response.status_code == 200:
        events_data = response.json()

        events = []
        
        for event in events_data:
            start_time = event['start_time'].split("T")[0]
            event_date = datetime.strptime(start_time, '%Y-%m-%d')

            if event_date.month == month and event_date.year == year:
                end_time = start_time
                if event['duration'] > 1:
                    end_time = (event_date + timedelta(days=event['duration'] - 1)).strftime('%Y-%m-%d')

                events.append({
                    'id': event['id'],
                    'title': event['name'],
                    'start': start_time,
                    'end': end_time,
                    'description': event['short_description']
                })
        
        return jsonify(events)
    else:
        return jsonify({'error': 'Unable to fetch events'}), 500

@app.route('/api/events/<int:event_id>')
def get_event(event_id):
    headers = {'api-key': API_KEY}
    response = requests.get(f"{API_URL}{event_id}", headers=headers)

    if response.status_code == 200:
        event_data = response.json()
        return jsonify(event_data)
    else:
        return jsonify({'error': 'Unable to fetch event details'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
