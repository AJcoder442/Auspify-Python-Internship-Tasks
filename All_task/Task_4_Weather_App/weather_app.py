import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import requests
import json
import os
import random

# Color Palette for consistent modern dark look
BG_COLOR = "#121212"          # Dark screen background
CARD_BG = "#1e1e1e"           # Card frame background
ACCENT_COLOR = "#00adb5"      # Cool cyan/teal
TEXT_COLOR = "#eeeeee"        # Bright text
MUTED_TEXT = "#888888"        # Gray text
ERROR_COLOR = "#cf6679"       # Soft red for errors
SUCCESS_COLOR = "#4caf50"     # Green for success status

# WMO Weather Code Mapping to Condition Names and Descriptions
WMO_CODES = {
    0: ("Clear", "Clear blue sky"),
    1: ("Mainly Clear", "Mainly clear skies"),
    2: ("Partly Cloudy", "Partly cloudy skies"),
    3: ("Overcast", "Overcast overcast sky"),
    45: ("Foggy", "Dense fog conditions"),
    48: ("Foggy", "Depositing rime fog"),
    51: ("Drizzle", "Light intensity drizzle"),
    53: ("Drizzle", "Moderate intensity drizzle"),
    55: ("Drizzle", "Dense intensity drizzle"),
    56: ("Freezing Drizzle", "Light freezing drizzle"),
    57: ("Freezing Drizzle", "Dense freezing drizzle"),
    61: ("Rain", "Slight rain showers"),
    63: ("Rain", "Moderate rain shower"),
    65: ("Rain", "Heavy rain intensity"),
    66: ("Freezing Rain", "Light freezing rain"),
    67: ("Freezing Rain", "Heavy freezing rain"),
    71: ("Snowfall", "Slight snow fall"),
    73: ("Snowfall", "Moderate snow fall"),
    75: ("Snowfall", "Heavy snow fall"),
    77: ("Snow grains", "Light snow grains"),
    80: ("Rain Showers", "Slight rain showers"),
    81: ("Rain Showers", "Moderate rain showers"),
    82: ("Rain Showers", "Violent rain showers"),
    85: ("Snow Showers", "Slight snow showers"),
    86: ("Snow Showers", "Heavy snow showers"),
    95: ("Thunderstorm", "Slight or moderate thunderstorm"),
    96: ("Thunderstorm", "Thunderstorm with slight hail"),
    99: ("Thunderstorm", "Thunderstorm with heavy hail")
}

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auspify - Premium Weather App")
        self.root.geometry("450x600")
        self.root.configure(bg=BG_COLOR)
        self.root.minsize(400, 550)

        # Build UI layout
        self.create_header()
        self.create_search_bar()
        self.create_weather_card()
        self.create_status_bar()

        # Load a default city on startup
        self.fetch_weather("London", is_startup=True)

    def create_header(self):
        """Creates the header section."""
        header = tk.Frame(self.root, bg=BG_COLOR)
        header.pack(fill="x", padx=25, pady=(25, 10))

        title = tk.Label(
            header,
            text="AUSPIFY WEATHER APP",
            font=("Segoe UI", 16, "bold"),
            bg=BG_COLOR,
            fg=ACCENT_COLOR
        )
        title.pack(anchor="w")

        subtitle = tk.Label(
            header,
            text="Get real-time global weather conditions instantly.",
            font=("Segoe UI", 10),
            bg=BG_COLOR,
            fg=MUTED_TEXT
        )
        subtitle.pack(anchor="w", pady=(2, 0))

    def create_search_bar(self):
        """Creates the input field for searching cities."""
        search_frame = tk.Frame(self.root, bg=BG_COLOR)
        search_frame.pack(fill="x", padx=25, pady=10)

        # Custom text entry container
        entry_container = tk.Frame(search_frame, bg=CARD_BG, bd=1, relief="flat")
        entry_container.pack(side="left", fill="x", expand=True, ipady=4)

        self.city_entry = tk.Entry(
            entry_container,
            font=("Segoe UI", 11),
            bg=CARD_BG,
            fg=TEXT_COLOR,
            insertbackground=TEXT_COLOR,
            bd=0,
            highlightthickness=0
        )
        self.city_entry.pack(side="left", fill="x", expand=True, padx=10)
        self.city_entry.insert(0, "London")
        self.city_entry.bind("<Return>", lambda e: self.on_search())

        # Search Button
        self.search_btn = tk.Button(
            search_frame,
            text="Search",
            font=("Segoe UI", 10, "bold"),
            bg=ACCENT_COLOR,
            fg=BG_COLOR,
            activebackground="#008b91",
            activeforeground=BG_COLOR,
            bd=0,
            cursor="hand2",
            padx=15,
            command=self.on_search
        )
        self.search_btn.pack(side="right", padx=(10, 0), ipady=5)

        # Hover effects
        self.search_btn.bind("<Enter>", lambda e: self.search_btn.configure(bg="#00d8e2"))
        self.search_btn.bind("<Leave>", lambda e: self.search_btn.configure(bg=ACCENT_COLOR))

    def create_weather_card(self):
        """Creates the main weather display card."""
        self.weather_card = tk.Frame(self.root, bg=CARD_BG)
        self.weather_card.pack(fill="both", expand=True, padx=25, pady=15)

        # City Name Label
        self.city_lbl = tk.Label(
            self.weather_card,
            text="Loading...",
            font=("Segoe UI", 18, "bold"),
            bg=CARD_BG,
            fg=TEXT_COLOR
        )
        self.city_lbl.pack(pady=(25, 5))

        # Condition Banner Label
        self.cond_lbl = tk.Label(
            self.weather_card,
            text="--",
            font=("Segoe UI", 12, "bold"),
            bg=CARD_BG,
            fg=ACCENT_COLOR
        )
        self.cond_lbl.pack()

        # Temp Label
        self.temp_lbl = tk.Label(
            self.weather_card,
            text="--°C",
            font=("Segoe UI", 48, "bold"),
            bg=CARD_BG,
            fg=TEXT_COLOR
        )
        self.temp_lbl.pack(pady=(15, 10))

        # Detailed Description
        self.desc_lbl = tk.Label(
            self.weather_card,
            text="--",
            font=("Segoe UI", 10, "italic"),
            bg=CARD_BG,
            fg=MUTED_TEXT
        )
        self.desc_lbl.pack(pady=(0, 20))

        # Horizontal separator
        separator = tk.Frame(self.weather_card, bg=BG_COLOR, height=1)
        separator.pack(fill="x", padx=30, pady=10)

        # Stats grid frame (Humidity, Wind, Pressure)
        grid_frame = tk.Frame(self.weather_card, bg=CARD_BG)
        grid_frame.pack(fill="x", padx=30, pady=10)

        # Configure columns equally
        grid_frame.grid_columnconfigure(0, weight=1)
        grid_frame.grid_columnconfigure(1, weight=1)
        grid_frame.grid_columnconfigure(2, weight=1)

        # Humidity Column
        tk.Label(grid_frame, text="Humidity", font=("Segoe UI", 9), bg=CARD_BG, fg=MUTED_TEXT).grid(row=0, column=0)
        self.humid_val = tk.Label(grid_frame, text="--", font=("Segoe UI", 12, "bold"), bg=CARD_BG, fg=TEXT_COLOR)
        self.humid_val.grid(row=1, column=0, pady=(2, 0))

        # Wind Speed Column
        tk.Label(grid_frame, text="Wind", font=("Segoe UI", 9), bg=CARD_BG, fg=MUTED_TEXT).grid(row=0, column=1)
        self.wind_val = tk.Label(grid_frame, text="--", font=("Segoe UI", 12, "bold"), bg=CARD_BG, fg=TEXT_COLOR)
        self.wind_val.grid(row=1, column=1, pady=(2, 0))

        # Pressure Column
        tk.Label(grid_frame, text="Pressure", font=("Segoe UI", 9), bg=CARD_BG, fg=MUTED_TEXT).grid(row=0, column=2)
        self.press_val = tk.Label(grid_frame, text="--", font=("Segoe UI", 12, "bold"), bg=CARD_BG, fg=TEXT_COLOR)
        self.press_val.grid(row=1, column=2, pady=(2, 0))

    def create_status_bar(self):
        """Creates the bottom info bar."""
        footer = tk.Frame(self.root, bg=CARD_BG)
        footer.pack(fill="x", side="bottom", ipady=8)

        self.status_lbl = tk.Label(
            footer,
            text="Connecting...",
            font=("Segoe UI", 9, "bold"),
            bg=CARD_BG,
            fg=TEXT_COLOR
        )
        self.status_lbl.pack(side="left", padx=25)

        brand = tk.Label(
            footer,
            text="Auspify Technologies",
            font=("Segoe UI", 8, "italic"),
            bg=CARD_BG,
            fg=MUTED_TEXT
        )
        brand.pack(side="right", padx=25)

    def on_search(self):
        """Triggered on clicking search or pressing Enter."""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Empty Search", "Please type a city name.")
            return
        self.fetch_weather(city)

    def fetch_weather(self, city, is_startup=False):
        """Queries Open-Meteo free API or generates mock data if offline."""
        self.status_lbl.configure(text="Updating...", fg=TEXT_COLOR)
        
        # 1. Geocode City Name to Latitude/Longitude using Open-Meteo Geocoding API (Free, No Key)
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
        
        try:
            geo_response = requests.get(geo_url, timeout=5)
            if geo_response.status_code == 200:
                geo_data = geo_response.json()
                results = geo_data.get("results")
                
                if results and len(results) > 0:
                    location = results[0]
                    lat = location["latitude"]
                    lon = location["longitude"]
                    city_name = location["name"]
                    country_code = location.get("country_code", "LOC")

                    # 2. Fetch real weather data from Open-Meteo Forecast API
                    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,rain,showers,snowfall,weather_code,pressure_msl,wind_speed_10m&wind_speed_unit=ms&timezone=auto"
                    
                    weather_response = requests.get(weather_url, timeout=5)
                    if weather_response.status_code == 200:
                        weather_data = weather_response.json()
                        current = weather_data["current"]
                        wmo_code = current.get("weather_code", 0)
                        
                        # Map weather code to text
                        cond_name, cond_desc = WMO_CODES.get(wmo_code, ("Clear", "Clear sky"))

                        self.update_weather_ui(
                            city=city_name,
                            country=country_code,
                            temp=current["temperature_2m"],
                            condition=cond_name,
                            desc=cond_desc.capitalize(),
                            humidity=current["relative_humidity_2m"],
                            wind=current["wind_speed_10m"],
                            pressure=current["pressure_msl"],
                            is_mock=False
                        )
                        return
                    else:
                        self.generate_mock_weather(city, f"Forecast API error {weather_response.status_code}")
                else:
                    # City not found - show error, don't mock unless startup
                    if is_startup:
                        self.generate_mock_weather(city, "City not found on startup")
                    else:
                        self.status_lbl.configure(text=f"City '{city}' not found.", fg=ERROR_COLOR)
                        messagebox.showerror("Not Found", f"Could not find coordinates for city '{city}'. Check spelling.")
            else:
                self.generate_mock_weather(city, f"Geocoding API error {geo_response.status_code}")
        except requests.exceptions.RequestException:
            # Network failure - fallback to offline simulation mode
            self.generate_mock_weather(city, "Offline Mode - displaying offline weather simulation")

    def update_weather_ui(self, city, country, temp, condition, desc, humidity, wind, pressure, is_mock=False):
        """Refreshes the GUI elements with weather data."""
        self.city_lbl.configure(text=f"{city}, {country}")
        self.temp_lbl.configure(text=f"{round(temp)}°C")
        self.cond_lbl.configure(text=condition.upper())
        self.desc_lbl.configure(text=desc)
        self.humid_val.configure(text=f"{humidity}%")
        self.wind_val.configure(text=f"{wind} m/s")
        self.press_val.configure(text=f"{round(pressure)} hPa")

        # Color the condition text based on severity
        cond = condition.lower()
        if "rain" in cond or "drizzle" in cond:
            self.cond_lbl.configure(fg="#5c97ff") # blue
        elif "cloud" in cond or "overcast" in cond:
            self.cond_lbl.configure(fg="#b0bec5") # grey
        elif "clear" in cond or "sun" in cond:
            self.cond_lbl.configure(fg="#ffd54f") # yellow
        elif "snow" in cond:
            self.cond_lbl.configure(fg="#e0f7fa") # icy blue
        else:
            self.cond_lbl.configure(fg=ACCENT_COLOR)

        # Set status message
        if is_mock:
            self.status_lbl.configure(text="⚡ Demo Mode (Simulated Data)", fg=ACCENT_COLOR)
        else:
            self.status_lbl.configure(text="🌐 Live Real Weather Active", fg=SUCCESS_COLOR)

    def generate_mock_weather(self, city, log_msg):
        """Generates realistic dummy weather values for robust demonstration when offline."""
        print(f"[WeatherApp Fallback] {log_msg}")
        
        # Smart templates for known global cities
        city_templates = {
            "london": {"country": "GB", "temp": 15, "cond": "Clouds", "desc": "Scattered overcast sky", "humid": 82, "wind": 4.1, "press": 1012},
            "new york": {"country": "US", "temp": 22, "cond": "Clear", "desc": "Sunny clear skies", "humid": 55, "wind": 3.6, "press": 1016},
            "tokyo": {"country": "JP", "temp": 26, "cond": "Rain", "desc": "Moderate intensity rain", "humid": 90, "wind": 5.2, "press": 1008},
            "delhi": {"country": "IN", "temp": 35, "cond": "Clear", "desc": "Haze and intense heat", "humid": 45, "wind": 2.1, "press": 1002},
            "paris": {"country": "FR", "temp": 19, "cond": "Clouds", "desc": "Partly cloudy skies", "humid": 70, "wind": 3.0, "press": 1014},
            "sydney": {"country": "AU", "temp": 17, "cond": "Clear", "desc": "Cool and pleasant clear wind", "humid": 60, "wind": 4.8, "press": 1020}
        }
        
        normalized = city.lower().strip()
        if normalized in city_templates:
            template = city_templates[normalized]
        else:
            # Generate random but logical weather data
            conditions = [
                ("Clear", "Clear blue sky", "#ffd54f", 18, 38, 30, 60),
                ("Clouds", "Overcast clouds", "#b0bec5", 10, 25, 60, 85),
                ("Rain", "Moderate rainfall", "#5c97ff", 8, 20, 75, 95),
                ("Snow", "Light snow flurry", "#e0f7fa", -5, 3, 80, 95)
            ]
            cond_data = random.choice(conditions)
            template = {
                "country": "LOC",
                "temp": round(random.uniform(cond_data[3], cond_data[4]), 1),
                "cond": cond_data[0],
                "desc": cond_data[1],
                "humid": random.randint(cond_data[5], cond_data[6]),
                "wind": round(random.uniform(1.0, 8.5), 1),
                "press": random.randint(995, 1025)
            }

        self.update_weather_ui(
            city=city.title(),
            country=template["country"],
            temp=template["temp"],
            condition=template["cond"],
            desc=template["desc"],
            humidity=template["humid"],
            wind=template["wind"],
            pressure=template["press"],
            is_mock=True
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
