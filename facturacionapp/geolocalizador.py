import requests

class CoordenadasNum:
    def __init__(self):
        self.longitud = 0.0
        self.latitud = 0.0

class Geolocalizador:
    def __init__(self, api_key):
        self.api_key = api_key

    def geolocate(self):
        url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={self.api_key}"
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            location = data.get("location", {})
            lat = location.get("lat")
            lng = location.get("lng")
            if lat is not None and lng is not None:
                return lat, lng
            else:
                print("Latitude or Longitude not found in the response.")
                return None, None
        else:
            print(f"Request failed with status code {response.status_code}")
            return None, None