import os
import io
import requests
from flask import Flask, render_template, request, send_file, jsonify
from flask_cors import CORS
from ics import Calendar, Event
from datetime import datetime, timedelta

app = Flask(__name__, template_folder='../templates')
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_google_events')
def fetch_google_events():
    ical_url = request.args.get('url')
    if not ical_url:
        return jsonify({"events": []})
    try:
        headers = {'User-Agent': 'Mozilla/5.0 LunaApp/1.0'}
        response = requests.get(ical_url, headers=headers, timeout=10)
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch Google Calendar"}), 400
            
        g_calendar = Calendar(response.text)
        google_events = []
        for event in g_calendar.events:
            google_events.append({
                'title': event.name or "Event",
                'start': event.begin.isoformat(),
                'end': event.end.isoformat() if event.end else event.begin.isoformat(),
                'backgroundColor': '#3d3d3d',
                'borderColor': '#555',
                'allDay': event.all_day
            })
        return jsonify({"events": google_events})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate_ics')
def generate_ics():
    start_str = request.args.get('start')
    cycle = int(request.args.get('cycle', 28))
    if not start_str: return "Error", 400
    
    start_date = datetime.strptime(start_str, '%Y-%m-%d')
    c = Calendar()
    for i in range(12):
        p_start = start_date + timedelta(days=i * cycle)
        e = Event(name="🌙 Luna Cycle", begin=p_start, duration=timedelta(days=5))
        c.events.add(e)
    
    f = io.BytesIO()
    f.write(str(c).encode('utf-8'))
    f.seek(0)
    return send_file(f, mimetype='text/calendar', as_attachment=True, download_name='luna.ics')
