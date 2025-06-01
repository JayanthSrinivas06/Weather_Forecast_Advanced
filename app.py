from flask import Flask, render_template, request, redirect, Response
import requests
import os
from dotenv import load_dotenv
from datetime import datetime
from weather_db import init_db, save_current_weather, save_forecast_weather,get_all_weather, update_weather_record, delete_weather_record
import csv


init_db()
load_dotenv()

app = Flask(__name__)
API_KEY = os.getenv('WEATHER_API_KEY')

@app.template_filter('datetimeformat')
def datetimeformat(value, format='%a, %b %d'):
    """Format datetime string to given format (default: Wed, May 28)."""
    try:
        dt = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        return dt.strftime(format)
    except Exception:
        return value

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def get_forecast(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if not check_api_key():
        return redirect('/update-api')

    current_time = datetime.now().strftime("%A, %d %B %Y | %I:%M:%S %p")
    weather, forecast, filtered_forecast = None, None, []
    error = None

    if request.method == 'POST':
        city = request.form.get('city')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        if city:
            weather = get_weather(city)
            forecast = get_forecast(city)

            if weather and forecast:
                try:
                    if not start_date or not end_date:
                        error = "Please provide both start and end dates."
                    else:
                        start = datetime.strptime(start_date, '%Y-%m-%d').date()
                        end = datetime.strptime(end_date, '%Y-%m-%d').date()

                        if start > end:
                            error = "Start date cannot be after end date."
                        else:
                            # Group forecast data by date and pick the 12:00 PM entry if available
                            forecast_by_day = {}

                        for entry in forecast.get('list', []):
                            entry_time = datetime.strptime(entry['dt_txt'], '%Y-%m-%d %H:%M:%S')
                            entry_date = entry_time.date()

                            if start <= entry_date <= end:
                                time_str = entry_time.strftime('%H:%M:%S')
                                if entry_date not in forecast_by_day:
                                    forecast_by_day[entry_date] = []

                                forecast_by_day[entry_date].append((entry_time, entry))

                        # From each date, pick the one closest to 12:00 PM
                        for day_entries in forecast_by_day.values():
                            closest_entry = min(day_entries, key=lambda x: abs(x[0].hour - 12))
                            filtered_forecast.append(closest_entry[1])

                        if 'save_to_db' in request.form:
                            if weather:
                                save_current_weather(
                                    city=weather['name'],
                                    date=datetime.now().strftime('%Y-%m-%d'),
                                    temp=weather['main']['temp'],
                                    description=weather['weather'][0]['description']
                                )

                            if filtered_forecast:
                                forecast_data = [{
                                    'city': weather['name'],
                                    'date': f['dt_txt'].split(' ')[0],
                                    'temp': f['main']['temp'],
                                    'description': f['weather'][0]['description']
                                } for f in filtered_forecast]

                                save_forecast_weather(forecast_data)


                except Exception as e:
                    error = f"Date parsing error: {str(e)}"
            else:
                error = "Could not fetch weather data. Check the city name."
        else:
            error = "Please enter a city name."

    return render_template(
        'index.html',
        current_time=current_time,
        weather=weather,
        forecast=filtered_forecast,
        error=error
    )

@app.route('/dashboard')
def dashboard():
    data = get_all_weather()
    return render_template('dashboard.html', data=data)

@app.route('/update', methods=['POST'])
def update():
    record_id = request.form.get('id')
    temp = request.form.get('temp')
    description = request.form.get('description')
    update_weather_record(record_id, temp, description)
    return redirect('/dashboard')

@app.route('/delete/<int:record_id>', methods=['POST'])
def delete(record_id):
    delete_weather_record(record_id)
    return redirect('/dashboard')


@app.route('/export')
def export():
    data = get_all_weather()
    def generate():
        yield 'ID,City,Date,Temperature,Description,IsCurrent\n'
        for row in data:
            csv_row = ','.join([str(item) for item in row])
            yield f'{csv_row}\n'
    return Response(generate(), mimetype='text/csv',
                    headers={'Content-Disposition': 'attachment; filename=weather_data.csv'})


def check_api_key():
    try:
        with open('.env', 'r') as f:
            for line in f:
                if line.startswith("WEATHER_API_KEY"):
                    key = line.split('=', 1)[1].strip().strip('"').strip("'")
                    return key != ""
        return False
    except FileNotFoundError:
        return False


@app.route('/update-api', methods=['GET', 'POST'])
def update_api():
    if request.method == 'POST':
        new_key = request.form.get('api_key')
        if new_key and new_key.strip():
            with open('.env', 'w') as f:
                f.write(f'WEATHER_API_KEY="{new_key.strip()}"\n')
            os.environ['WEATHER_API_KEY'] = new_key.strip()
            global API_KEY
            API_KEY = new_key.strip()
            return redirect('/')
        else:
            error = "API key cannot be empty."
            return render_template('update_api.html', error=error, has_api_key=check_api_key())

    return render_template('update_api.html', has_api_key=check_api_key())


if __name__ == '__main__':
    app.run(debug=True)
