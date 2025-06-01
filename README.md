# 🌦️ Weather Forecast Advanced Web App

A Flask-based web application that provides current weather information and a 5-day forecast for any city using the OpenWeatherMap API. Unlike traditional setups, this application offers a user-friendly interface to input and store your API key, eliminating the need to modify project files for API configuration.

---

## 📁 Project Structure

```
Weather_Forecast_Advanced/
│
├── static/
│   └── imgs/
│       └── background.jpg         # Background image for the app
│
├── templates/
│   ├── index.html                 # Main HTML template
│   └── api_key.html               # Template for API key input
│
├── app.py                         # Main Flask application
├── weather_db.py                  # Module to handle API key storage
├── .env                           # Environment variables (optional)
└── README.md                      # Project documentation
```

---

## ⚙️ Requirements

Ensure you have Python installed. Then, install the required packages:

```bash
pip install flask requests python-dotenv
```

Alternatively, if a `requirements.txt` file is provided:

```text
flask
requests
python-dotenv
```
```bash
pip install -r requirements.txt
```

---

## 🔑 API Key Setup

This application **automatically prompts you** to enter your OpenWeatherMap API key through the web interface **if the `.env` file does not contain one**.

### Initial Setup

1. **Run the application**:

   ```bash
   python app.py
   ```

2. **Automatic API Key Prompt**:

   - If no API key is found in `.env`, the application will **redirect you to the API key input page automatically**.
   - Enter your OpenWeatherMap API key in the form and submit.
   - The key will be securely stored for future use, and you'll be redirected to the homepage.

### Updating the API Key

- If you ever want to change the API key later:
  - Go to the home page ([http://127.0.0.1:5000](http://127.0.0.1:5000))
  - Click the **"Update API Key"** option (available on the home page navigation or interface).
  - Enter the new key and submit.

> ✅ This approach removes the need to manually edit `.env` or project files — everything is handled conveniently through the web interface.

---

## 🚀 Running the App

After setting up your API key:

1. **Start the Flask application**:

   ```bash
   python app.py
   ```

2. **Use the application**:

   - Enter a city name to retrieve current weather data and a 5-day forecast.
   - View temperature, weather conditions, and other relevant information.

---

## 🖼️ Features

- **Dynamic API Key Management**: Input and store your API key through the web interface.
- **Current Weather Data**: Retrieve real-time weather information for any city.
- **5-Day Forecast**: View weather forecasts in 3-hour intervals.
- **Responsive UI**: Enjoy a user-friendly interface with a customizable background image.
- **Modular Codebase**: Organized structure for scalability and maintenance.

---

## 📝 Notes

- Ensure the background image (`background.jpg`) is placed in the `static/imgs/` directory.
- The application uses the `weather_db.py` module to handle API key storage and retrieval.
- Debug mode is enabled by default (`debug=True`). Disable this in production environments.
