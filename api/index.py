from flask import Flask, render_template, request, send_file
from ics import Calendar, Event
from datetime import datetime, timedelta
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    # Получаем данные из формы
    start_date_str = request.form.get('last_period')
    cycle_length = int(request.form.get('cycle_length'))
    
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    c = Calendar()

    # Генерируем события на 6 месяцев вперед
    for i in range(6):
        period_start = start_date + timedelta(days=i * cycle_length)
        
        e = Event()
        e.name = "🌙 Luna: Режим Энергосбережения"
        e.begin = period_start
        e.duration = timedelta(days=5) # Длительность периода
        e.description = "В эти дни лучше не планировать тяжелые нагрузки. Do hard things, but smart."
        c.events.add(e)

    # Создаем файл в памяти
    f = io.BytesIO()
    f.write(str(c).encode('utf-8'))
    f.seek(0)

    return send_file(f, as_attachment=True, download_name='luna_calendar.ics', mimetype='text/calendar')

if __name__ == '__main__':
    app.run(debug=True)
