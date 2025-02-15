import sys
import requests

def load_file():
    stdin = sys.stdin.read()
    return stdin

def convert_coordinate(value, pos_label, neg_label):
    if value >= 0:
        return f"{abs(value)}° {pos_label}"
    else:
        return f"{abs(value)}° {neg_label}"

def get_iss_location():
    url = "http://api.open-notify.org/iss-now.json"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    position = data["iss_position"]
    latitude = float(position["latitude"])
    longitude = float(position["longitude"])
    lat_text = convert_coordinate(latitude, "North", "South")
    lon_text = convert_coordinate(longitude, "East", "West")
    return lat_text, lon_text

def main():
    try:
        lat_text, lon_text = get_iss_location()
        print(f"The International Space Station is currently located at {lat_text} latitude and {lon_text} longitude.")
    except Exception as e:
        print("An error occurred while retrieving the ISS location:", e)

if __name__ == "__main__":
    main()