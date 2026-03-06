import customtkinter as ctk
import requests
import threading
import time
from queue import Queue
from typing import List, Dict

API_KEY = "8d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a"
WEATHER_API = "https://api.openweathermap.org/data/2.5/weather"

DEFAULT_CITIES = ["Kathmandu", "Pokhara", "Dharan", "Birgunj", "Biratnagar"]


class WeatherCollector:
    """Fetch weather data"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def fetch_weather(self, city: str) -> Dict:
        """Fetch weather for a city"""
        try:
            params = {"q": city, "appid": self.api_key, "units": "metric"}
            response = requests.get(WEATHER_API, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "city": city,
                    "temp": data["main"]["temp"],
                    "humidity": data["main"]["humidity"],
                    "pressure": data["main"]["pressure"]
                }
            else:
                return {"city": city, "error": "Not found"}
        except:
            return {"city": city, "error": "Error"}
    
    def fetch_sequential(self, cities: List[str]) -> tuple:
        """Sequential fetch"""
        start = time.time()
        results = [self.fetch_weather(city) for city in cities]
        return results, time.time() - start
    
    def fetch_parallel(self, cities: List[str]) -> tuple:
        """Parallel fetch"""
        start = time.time()
        results = []
        
        def worker(city):
            results.append(self.fetch_weather(city))
        
        threads = [threading.Thread(target=worker, args=(city,)) for city in cities]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        return results, time.time() - start


class WeatherApp:
    """Simple GUI"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Collector")
        self.root.geometry("500x600")
        ctk.set_appearance_mode("dark")
        
        self.collector = WeatherCollector(API_KEY)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI"""
        # Title
        title = ctk.CTkLabel(self.root, text="Weather Data Collector", font=("Arial", 18, "bold"))
        title.pack(pady=15)
        
        # Cities input
        ctk.CTkLabel(self.root, text="Cities (comma separated):", font=("Arial", 11)).pack(anchor="w", padx=20, pady=(10, 0))
        self.cities_entry = ctk.CTkEntry(self.root, width=400)
        self.cities_entry.pack(pady=10, padx=20)
        self.cities_entry.insert(0, ", ".join(DEFAULT_CITIES))
        
        # Buttons
        button_frame = ctk.CTkFrame(self.root)
        button_frame.pack(pady=10)
        
        seq_btn = ctk.CTkButton(button_frame, text="Sequential", command=self.fetch_seq, width=150)
        seq_btn.pack(side="left", padx=5)
        
        par_btn = ctk.CTkButton(button_frame, text="Parallel", command=self.fetch_par, width=150)
        par_btn.pack(side="left", padx=5)
        
        # Results
        ctk.CTkLabel(self.root, text="Results:", font=("Arial", 11, "bold")).pack(anchor="w", padx=20, pady=(15, 5))
        
        self.result_text = ctk.CTkTextbox(self.root, height=350, width=450, font=("Courier", 10))
        self.result_text.pack(padx=20, pady=10, fill="both", expand=True)
        self.result_text.insert("0.0", "Click a button to fetch weather...")
    
    def fetch_seq(self):
        """Fetch sequential"""
        cities = [c.strip() for c in self.cities_entry.get().split(",")]
        results, time_taken = self.collector.fetch_sequential(cities)
        self.display_results(results, time_taken, "Sequential")
    
    def fetch_par(self):
        """Fetch parallel"""
        cities = [c.strip() for c in self.cities_entry.get().split(",")]
        results, time_taken = self.collector.fetch_parallel(cities)
        self.display_results(results, time_taken, "Parallel")
    
    def display_results(self, results: List[Dict], elapsed: float, method: str):
        """Display results"""
        output = f"{method} Fetch - Time: {elapsed:.3f}s\n" + "="*40 + "\n\n"
        
        for r in results:
            if "error" in r:
                output += f"{r['city']}: {r['error']}\n"
            else:
                output += f"{r['city']}:\n"
                output += f"  Temp: {r['temp']}°C\n"
                output += f"  Humidity: {r['humidity']}%\n"
                output += f"  Pressure: {r['pressure']} hPa\n\n"
        
        self.result_text.delete("0.0", "end")
        self.result_text.insert("0.0", output)


def main():
    root = ctk.CTk()
    app = WeatherApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

