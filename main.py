import math
import sys
import requests
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QTabWidget, \
    QStyleOption, QStyle
from PyQt5.QtCore import Qt, QSize
from methods import *
from forecast_component import ForecastTotal
from current_weather_component import CurrentWeather




if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Weather tabs will be what we use in the future. In the interim we're going to replace this with Forecast to better design it
    weather_app = CurrentWeather()
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
