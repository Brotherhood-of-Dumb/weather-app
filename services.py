import requests
from PyQt5.QtCore import QObject, pyqtSignal

# Keep creating classes for each call; that way we aren't importing a million services in our components
class GetCurrentWeather(QObject):
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    def __init__(self, city_input):
        super().__init__()
        self.city = city_input

    def get_current_weather(self):
        api_key = "d15ceeb9e59ddbaa73b6e22779d856ee"
        # TODO: This is for current forecast. We need a link for future forecast.
        url = f"https://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={api_key}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if response.status_code == 200:
                self.finished.emit(data)
        except requests.exceptions.HTTPError as e:
            match response.status_code:
                case 400:
                    self.error.emit("Bad Request\nCheck your city name")
                case _:
                    self.error.emit({e})
                # add 401,403,404,500,502,503,504
        except requests.exceptions.ConnectionError:
            self.error.emit("Connection Error\nCheck your internet connection")
        except requests.exceptions.Timeout:
            self.error.emit("Timeout Error")
        except requests.exceptions.TooManyRedirects:
            self.error.emit("TooManyRedirects")
        except requests.exceptions.RequestException as e:
            self.error.emit(f"RequestException: {e}")

