import sys
import requests
import datetime

def load_file():
    stdin = sys.stdin.read()
    return stdin

def get_iss_location():
    url = "http://api.open-notify.org/iss-now.json"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data

def format_coordinates(lat, lon):
    lat_direction = "north" if lat >= 0 else "south"
    lon_direction = "east" if lon >= 0 else "west"
    return f"{abs(lat):.2f}° {lat_direction} latitude and {abs(lon):.2f}° {lon_direction} longitude"

def main():
    data = get_iss_location()
    if data.get("message") != "success":
        print("Failed to retrieve ISS location.")
        return

    position = data.get("iss_position", {})
    lat = float(position.get("latitude", 0))
    lon = float(position.get("longitude", 0))
    timestamp = data.get("timestamp", 0)
    readable_time = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    
    coordinates_description = format_coordinates(lat, lon)
    print(f"At {readable_time}, the International Space Station is currently at {coordinates_description}.")

if __name__ == "__main__":
    main()