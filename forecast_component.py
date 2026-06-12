import math
import sys
import requests
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QTabWidget, \
    QStyleOption, QStyle
from PyQt5.QtCore import Qt, QSize
from methods import *

class ForecastTotal(QWidget):
    def __init__(self):
        super().__init__()
        self.city_name = QLabel("Enter City Name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.city = QLabel("City", self)
        self.forecast = []
        # Potentially cut off the amount of data we're feeding into the array
        # 16 days is excessive; can create an option later for people to adjust how much they want.
        for data in range(0, 16):
            day = ForecastDay()
            if len(self.forecast) <= 7:
                self.forecast.append(day)
        self.ui()

    def ui(self):
            self.setWindowTitle("Weather App")
            vbox = QVBoxLayout()
            hbox = QHBoxLayout()
            hbox2 = QHBoxLayout()
            hbox3 = QHBoxLayout()
            hbox4 = QHBoxLayout()
            for day in self.forecast:
                if self.forecast.index(day) <= 3:
                    hbox.addWidget(day)
                elif self.forecast.index(day) <= 7:
                    hbox2.addWidget(day)
                elif self.forecast.index(day) <= 11:
                    hbox3.addWidget(day)
                else:
                    hbox4.addWidget(day)
            # hbox.addWidget(self.emoji)
            # hbox.addWidget(self.low_label)
            # hbox.addWidget(self.high_label)
            # hbox2.addWidget(self.precip_percent)
            # hbox2.addWidget(self.precip_amount)
            # hbox3.addWidget(self.feelslike_label)
            # hbox3.addWidget(self.visibility_label)
            # these four need to be common; put in master class and pass everything else into individual comps
            vbox.addWidget(self.city_name)
            vbox.addWidget(self.city_input)
            vbox.addWidget(self.get_weather_button)
            vbox.addWidget(self.city)
            #
            # vbox.addWidget(self.day)
            # vbox.addWidget(self.emoji)
            # vbox.addWidget(self.description_label)

            forecast_widget1 = QWidget(self)
            forecast_widget2 = QWidget(self)
            forecast_widget3 = QWidget(self)
            forecast_widget4 = QWidget(self)
            # precep_widget = QWidget(self)
            # environ_widget = QWidget(self)
            forecast_widget1.setLayout(hbox)
            forecast_widget2.setLayout(hbox2)
            forecast_widget3.setLayout(hbox3)
            forecast_widget4.setLayout(hbox4)
            # precep_widget.setLayout(hbox2)
            # environ_widget.setLayout(hbox3)
            vbox.addWidget(forecast_widget1)
            vbox.addWidget(forecast_widget2)
            vbox.addWidget(forecast_widget3)
            vbox.addWidget(forecast_widget4)

            self.setLayout(vbox)
            # WHY CAN I NOT PROPERLY SET A WIDTH ON THESE AND HAVE THEM CENTERED!!!
            # self.city_input.setFixedWidth(250)
            # self.get_weather_button.setFixedWidth(250)
            self.city_name.setAlignment(Qt.AlignCenter)
            self.city_input.setAlignment(Qt.AlignCenter)
            self.city.setAlignment(Qt.AlignCenter)
            # self.temperature_label.setAlignment(Qt.AlignLeft)
            # self.day.setAlignment(Qt.AlignCenter)
            # self.emoji.setAlignment(Qt.AlignCenter)
            # self.description_label.setAlignment(Qt.AlignCenter)
            # self.get_weather_button.setFixedSize(QSize(200, 30))
            # self.low_label.setAlignment(Qt.AlignCenter)
            # self.high_label.setAlignment(Qt.AlignCenter)
            # self.precip_percent.setAlignment(Qt.AlignCenter)
            # self.precip_amount.setAlignment(Qt.AlignCenter)

            self.city_name.setObjectName("city_name")
            self.city_input.setObjectName("city_input")
            self.get_weather_button.setObjectName("get_weather_button")
            self.city.setObjectName("city")

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
            # temp_widget.setStyleSheet("""
            #             QLabel#temperature_label {
            #                 font-size: 30px;
            #                 padding-top: 5px;
            #             }
            #             QLabel#emoji {
            #                 font-family: Segoe UI emoji;
            #                 font-size: 30px;
            #             }
            #         """)

            # self.get_weather_button.clicked.connect(self.get_weather)

class ForecastDay(QWidget):
    def __init__(self):
        super().__init__()
        self.day = QLabel("The Day", self)
        self.emoji = QLabel("<UNC>", self)
        self.low_label = QLabel("Low\n 70", self)
        self.high_label = QLabel("High\n 80", self)
        self.description_label = QLabel("it rainin'", self)
        self.precip_percent = QLabel("90% chance", self)
        self.precip_amount = QLabel("3 inches", self)
        self.ui()

    def ui(self):
            self.setWindowTitle("Weather App")
            vbox = QVBoxLayout()
            hbox = QHBoxLayout()
            hbox2 = QHBoxLayout()
            hbox.addWidget(self.low_label)
            hbox.addWidget(self.high_label)
            hbox2.addWidget(self.precip_percent)
            hbox2.addWidget(self.precip_amount)

            vbox.addWidget(self.day)
            vbox.addWidget(self.emoji)
            vbox.addWidget(self.description_label)

            temp_widget = QWidget(self)
            precep_widget = QWidget(self)
            # environ_widget = QWidget(self)
            temp_widget.setLayout(hbox)
            precep_widget.setLayout(hbox2)
            # environ_widget.setLayout(hbox3)
            vbox.addWidget(temp_widget)
            vbox.addWidget(precep_widget)
            # vbox.addWidget(environ_widget)

            self.setLayout(vbox)
            # self.city_name.setAlignment(Qt.AlignCenter)
            # self.city_input.setAlignment(Qt.AlignCenter)
            # self.city.setAlignment(Qt.AlignCenter)
            # self.temperature_label.setAlignment(Qt.AlignLeft)
            self.day.setAlignment(Qt.AlignCenter)
            self.emoji.setAlignment(Qt.AlignCenter)
            self.description_label.setAlignment(Qt.AlignCenter)
            # self.get_weather_button.setFixedSize(QSize(200, 30))
            self.low_label.setAlignment(Qt.AlignCenter)
            self.high_label.setAlignment(Qt.AlignCenter)
            self.precip_percent.setAlignment(Qt.AlignCenter)
            self.precip_amount.setAlignment(Qt.AlignCenter)

            # self.city_name.setObjectName("city_name")
            # self.city_input.setObjectName("city_input")
            # self.get_weather_button.setObjectName("get_weather_button")
            # self.city.setObjectName("city")
            self.day.setObjectName("day")
            self.emoji.setObjectName("emoji")
            # self.description_label.setObjectName("description_label")

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
                        ForecastDay {
                            border: 1px solid #484d49;
                        }
                    """)


            # self.get_weather_button.clicked.connect(self.get_weather)

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)