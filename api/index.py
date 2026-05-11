import os
import io
from flask import Flask, render_template, request, send_file
from ics import Calendar, Event
from datetime import datetime, timedelta

# Указываем Flask, что шаблоны (index.html) лежат папкой выше в 'templates'
app = Flask(__name__, template_folder='../templates')

@app.route('/')
def index():
    # Vercel иногда капризничает с путями, поэтому проверяем наличие файла
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Получаем данные из формы
        start_date_str = request.form.get('last_period')
        cycle_length_str = request.form.get('cycle_length')
        
        # Проверка на пустые данные
        if not start_date_str or not cycle_length_str:
            return "Ошибка: заполни все поля!", 400
            
        cycle_length = int(cycle_length_str)
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        
        c = Calendar()

        # Генерируем события на 6 месяцев вперед
        for i in range(6):
            period_start = start_date + timedelta(days=i * cycle_length)
            
            e = Event()
            e.name = "🌙 Luna: Режим Энергосбережения"
            e.begin = period_start
            e.duration = timedelta(days=5) # Длительность
            e.description = "В эти дни лучше снизить нагрузку. Принцип: Do hard things, but smart."
            c.events.add(e)

        # Создаем файл в оперативной памяти
        f = io.BytesIO()
        f.write(str(c).encode('utf-8'))
        f.seek(0)

        return send_file(
            f, 
            as_attachment=True, 
            download_name='luna_calendar.ics', 
            mimetype='text/calendar'
        )
    except Exception as e:
        return f"Произошла ошибка: {str(e)}", 500

# ВАЖНО: Для Vercel НЕ НУЖНО писать app.run(). 
# Просто оставляем объект app для сервера.
