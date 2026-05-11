import os
import io
import requests
from flask import Flask, render_template, request, send_file, jsonify
from ics import Calendar, Event
from datetime import datetime, timedelta

# Настройка путей для Vercel
app = Flask(__name__, template_folder='../templates')

@app.route('/')
def index():
    return render_template('index.html')

# ЭНДПОИНТ 1: Генерация твоих циклов Luna (для скачивания или подписки)
@app.route('/generate_ics')
def generate_ics():
    try:
        # Получаем данные из параметров URL (query params)
        start_date_str = request.args.get('start')
        cycle_length = int(request.args.get('cycle', 28))
        
        if not start_date_str:
            return "Error: Start date required", 400
            
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        c = Calendar()

        # Генерируем на 12 месяцев для солидности
        for i in range(12):
            period_start = start_date + timedelta(days=i * cycle_length)
            e = Event()
            e.name = "🌙 Luna Cycle (Low Energy)"
            e.begin = period_start
            e.duration = timedelta(days=5)
            e.description = "Biorhythm Sync: Focus on recovery. Do hard things, but smart."
            c.events.add(e)

        f = io.BytesIO()
        f.write(str(c).encode('utf-8'))
        f.seek(0)

        return send_file(
            f, 
            mimetype='text/calendar',
            as_attachment=True,
            download_name='luna_sync.ics'
        )
    except Exception as e:
        return f"Error: {str(e)}", 500

# ЭНДПОИНТ 2: Чтение данных ИЗ Google Календаря мамы
@app.route('/fetch_google_events')
def fetch_google_events():
    ical_url = request.args.get('url')
    if not ical_url:
        return jsonify({"events": []})
    
    try:
        # Идем в Google по секретной ссылке мамы
        response = requests.get(ical_url, timeout=10)
        if response.status_code != 200:
            return jsonify({"error": "Could not fetch Google Calendar"}), 400
            
        g_calendar = Calendar(response.text)
        
        google_events = []
        for event in g_calendar.events:
            # Превращаем события из формата ICS в формат для нашего FullCalendar
            google_events.append({
                'title': event.name,
                'start': event.begin.isoformat(),
                'end': event.end.isoformat() if event.end else event.begin.isoformat(),
                'backgroundColor': '#333333', # Темный цвет для обычных дел
                'borderColor': '#444444',
                'allDay': event.all_day
            })
            
        return jsonify({"events": google_events})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Для локальной отладки (Vercel это игнорирует)
if __name__ == '__main__':
    app.run(debug=True)
