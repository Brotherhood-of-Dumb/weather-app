import math
import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QTabWidget
from PyQt5.QtCore import Qt, QSize


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_name = QLabel("Enter City Name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.city = QLabel("", self)
        self.temperature_label = QLabel("", self)
        self.emoji = QLabel("", self)
        self.description_label = QLabel("", self)
        self.wind_label = QLabel("", self)
        self.humidity_label = QLabel("", self)
        self.feelslike_label = QLabel("", self)
        self.pressure_label = QLabel("", self)
        self.visibility_label = QLabel("", self)
        self.ui()

    def ui(self):
        self.setWindowTitle("Weather App")
        # TODO: Figure out how to add tabs. Have a "current" and a "forecast" option.
        # Follow up: Figure out how to resize/reformat app to better fit things.
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        hbox.addWidget(self.emoji)
        hbox.addWidget(self.temperature_label)
        hbox2.addWidget(self.wind_label)
        hbox2.addWidget(self.pressure_label)
        hbox2.addWidget(self.humidity_label)
        hbox3.addWidget(self.feelslike_label)
        hbox3.addWidget(self.visibility_label)
        vbox.addWidget(self.city_name)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.city)
        temp_widget = QWidget(self)
        air_widget = QWidget(self)
        environ_widget = QWidget(self)
        temp_widget.setLayout(hbox)
        air_widget.setLayout(hbox2)
        environ_widget.setLayout(hbox3)
        vbox.addWidget(temp_widget)
        vbox.addWidget(air_widget)
        vbox.addWidget(environ_widget)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)
        self.city_name.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.city.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignLeft)
        self.emoji.setAlignment(Qt.AlignRight)
        self.description_label.setAlignment(Qt.AlignCenter)
        self.get_weather_button.setFixedSize(QSize(200, 30))
        self.wind_label.setAlignment(Qt.AlignCenter)
        self.pressure_label.setAlignment(Qt.AlignCenter)
        self.visibility_label.setAlignment(Qt.AlignCenter)
        self.humidity_label.setAlignment(Qt.AlignCenter)
        self.feelslike_label.setAlignment(Qt.AlignCenter)

        self.city_name.setObjectName("city_name")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.city.setObjectName("city")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji.setObjectName("emoji")
        self.description_label.setObjectName("description_label")

        # Something is going on with my sizes, idk what
        # Update: I don't understand why, but anything not Qt is messing everything else up
        # My theory is it has to do with specificity, but I'm not sure
        self.setStyleSheet("""
            QLabel, QPushButton {
                font-family: Calibri;
                font-size: 18px;
                color: #484d49;
            }
            QLabel#city_name {
                font-size: 24px;
            }
            QLineEdit#city_input {
                font-size: 18px;
                background-color: rgb(255, 255, 255);
                width: 250px;
            }
            QPushButton#get_weather_button {
                background-color: rgb(255, 255, 255);
                margin-left: 80px;
            }
            QLabel#city {
                font-size: 40px;
                color: #000000;
                margin-top: 15px;
                border-top: 1px solid #484d49;
            }
            QLabel#description_label {
                font-size: 20px;
            }
        """)
        temp_widget.setStyleSheet("""
            QLabel#temperature_label {
                font-size: 30px;
                padding-top: 5px;
            }
            QLabel#emoji {
                font-family: Segoe UI emoji;
                font-size: 30px;
            }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = "d15ceeb9e59ddbaa73b6e22779d856ee"
        city = self.city_input.text()
        # TODO: This is for current forecast. We need a link for future forecast.
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if response.status_code == 200:
                self.display_success(data)
        except requests.exceptions.HTTPError as e:
            match response.status_code:
                case 400:
                    self.display_error("Bad Request\nCheck your city name")
                case _:
                    self.display_error({e})
                # add 401,403,404,500,502,503,504
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error\nCheck your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error")
        except requests.exceptions.TooManyRedirects:
            self.display_error("TooManyRedirects")
        except requests.exceptions.RequestException as e:
            self.display_error(f"RequestException: {e}")

    def display_error(self, message):
        self.temperature_label.setText(message)
        self.emoji.clear()
        self.description_label.clear()

    def display_success(self, data):
        # It is here that we're going to set our widgets to the data
        # print(data)
        # The temp we're getting from API is in Kelvin
        # TODO: give options to see temp in C
        temp = self.temp_conversion(data["main"]["temp"])
        feelslike = self.temp_conversion(data["main"]["feels_like"])
        humidity = data["main"]["humidity"]
        weather_description = self.first_letter_upper(data["weather"][0]["description"])
        icon = data["weather"][0]["id"]
        city = data["name"]
        self.city_input.clear()
        self.city.setText(city)
        self.temperature_label.setText(f"{temp:.0f}°F")
        self.feelslike_label.setText(f"Feels like:\n{feelslike:.0f}°F")
        self.description_label.setText(weather_description)
        self.emoji.setText(self.weather_emoji(icon))
        self.humidity_label.setText(f"Humidity:\n{humidity}%")
        self.wind_label.setText(f"Wind:\n{round(self.speed_conversion(data['wind']['speed']), 2)} mph")
        self.visibility_label.setText(f"Visibility:\n{round(self.distance_conversion(data["visibility"]), 2)} miles")
        self.pressure_label.setText(f"Pressure:\n{round(self.atmo_convers(data['main']['pressure']), 2)} inches")

    # The 700 range needs work. We won't get volcanic ash with that there.
    @staticmethod
    def weather_emoji(id):
        if 200 <= id <= 232:
            return "⛈"
        elif 300 <= id <= 321:
            return "⛅"
        elif 500 <= id <= 531:
            return "🌧"
        elif 600 <= id <= 622:
            return "❄"
        elif 701 <= id <= 781:
            return "🌫"
        elif id == 762:
            return "🌋"
        elif id == 781:
            return "🌪"
        elif id == 800:
            return "🌞"
        elif 801 <= id <= 804:
            return "☁"
        else:
            return ""

    @staticmethod
    def temp_conversion(temp):
        return (temp - 273.15) * 1.8 + 32

    @staticmethod
    def speed_conversion(ms):
        return ms * 2.237

    @staticmethod
    def distance_conversion(meter):
        return meter / 1609

    @staticmethod
    def atmo_convers(hpa):
        return hpa * 0.02953

    @staticmethod
    def first_letter_upper(desc):
        first = desc[0:1].upper()
        rest = desc[1:]
        return first + rest

class WeatherAppTabs(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300,200)
        self.tabs.addTab(self.tab1, "Current Weather")
        self.tabs.addTab(self.tab2, "Forecast")

        # Current Weather
        current_weather = WeatherApp()
        self.tab1.layout = QVBoxLayout(self)
        self.tab1.layout.addWidget(current_weather)
        self.tab1.setLayout(self.tab1.layout)

        # Forecast
        self.tab2.layout = QVBoxLayout(self)
        self.l = QLabel()
        self.l.setText("This is where the forecast is going to go")
        self.tab2.layout.addWidget(self.l)
        self.tab2.setLayout(self.tab2.layout)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    weather_app = WeatherAppTabs()
    weather_app.show()
    app.setStyleSheet("""
    QWidget {
        background-color: #ceeefa;
        width: 300px;
    }
    """)
    # Need a license to use qss apparently.
    # with open("style.qss", "r") as file:
    #     app.setStyleSheet(file.read())
    sys.exit(app.exec_())
