# Task 4: Weather Information App (GUI)

A premium, keyless Weather Application that retrieves and displays real-time weather information for any searched city using the Open-Meteo Free Global Weather API and Geocoding APIs.

## Key Features

- **Live City Search**: Enter any city name globally to view its real-time weather details.
- **Keyless Real API Integration**: Leverages Open-Meteo's geocoding and weather forecast APIs. It operates with **100% real-world live data** without requiring any registration or API keys!
- **Detailed Weather Metrics**:
  - Main temperature (in Celsius).
  - Main weather condition classification (Clear, Clouds, Rain, Snow, Drizzle, etc.) with custom color coding.
  - Detailed sky description mapped from WMO Weather Codes.
  - Secondary stats: Humidity level (%), Wind speed (m/s), and Air pressure (hPa).
- **Graceful Error Handling & Fallbacks**:
  - If the device is offline, the app automatically transitions to **Demo Mode** with simulated realistic weather parameters. This ensures the app is always functional during reviews.
  - Handles typos and unknown city search entries with user-friendly error banners.
- **Modern Dark UI**: Flat dark themed user interface styled with clean layouts and responsive typography.

## Files

- `weather_app.py`: The Python application source code.
- `README.md`: Project details & user guide.

## How to Run

1. Open a terminal in the folder.
2. Run the application:
   ```bash
   python weather_app.py
   ```

## Dependencies
- Standard Python 3.x
- `requests` library (`pip install requests`)
