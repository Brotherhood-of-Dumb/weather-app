from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import  QWidget, QLineEdit, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, \
    QStyleOption, QStyle
from PyQt5.QtCore import Qt, QSize, QThread
from methods import *
from services import GetCurrentWeather

class CurrentWeather(QWidget):
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

        self.get_weather_button.clicked.connect(self.get_current_weather)

    def get_current_weather(self):
        # This is going to be new and experimental; don't know if it will work, we will see.
        # Update: it works. Just need to replicate this in other components
        self.thread = QThread()
        self.worker = GetCurrentWeather(self.city_input.text())

        self.worker.moveToThread(self.thread)
        # The call we want to use.
        self.thread.started.connect(self.worker.get_current_weather)
        # these are built in our components
        self.worker.finished.connect(self.display_success)
        self.worker.error.connect(self.display_error)
        # These are, as far as I understand it, like our unsubscribe. Just removed from memory after use.
        self.worker.finished.connect(self.thread.quit)
        self.worker.error.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.error.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def display_error(self, message):
        self.temperature_label.setText(message)
        self.emoji.clear()
        self.description_label.clear()

    def display_success(self, data):
        # It is here that we're going to set our widgets to the data
        # print(data)
        # The temp we're getting from API is in Kelvin
        # TODO: give options to see temp in C
        temp = temp_conversion(data["main"]["temp"])
        feelslike = temp_conversion(data["main"]["feels_like"])
        humidity = data["main"]["humidity"]
        weather_description = first_letter_upper(data["weather"][0]["description"])
        icon = data["weather"][0]["id"]
        city = data["name"]
        self.city_input.clear()
        self.city.setText(city)
        self.temperature_label.setText(f"{temp:.0f}°F")
        self.feelslike_label.setText(f"Feels like:\n{feelslike:.0f}°F")
        self.description_label.setText(weather_description)
        self.emoji.setText(weather_emoji(icon))
        self.humidity_label.setText(f"Humidity:\n{humidity}%")
        self.wind_label.setText(f"Wind:\n{round(speed_conversion(data['wind']['speed']), 2)} mph")
        self.visibility_label.setText(f"Visibility:\n{round(distance_conversion(data["visibility"]), 2)} miles")
        self.pressure_label.setText(f"Pressure:\n{round(atmo_convers(data['main']['pressure']), 2)} inches")