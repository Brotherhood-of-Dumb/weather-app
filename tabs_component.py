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
        self.tab1.setObjectName("tab1")
        self.tab2.setObjectName("tab2")

        # Current Weather
        current_weather = CurrentWeather()
        self.tab1.layout = QVBoxLayout(self)
        self.tab1.layout.addWidget(current_weather)
        self.tab1.setLayout(self.tab1.layout)

        # Forecast
        forecast = ForecastTotal()
        self.tab2.layout = QVBoxLayout(self)
        self.tab2.layout.addWidget(forecast)
        self.tab2.setLayout(self.tab2.layout)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        self.setStyles()

    def setStyles(self):
        self.setStyleSheet("""
            QLabel, QTabWidget {
                font-family: Calibri;
                font-size: 18px;
                color: #484d49;
            }
            QTabWidget {
                border: 1px solid #C2C7CB;
            }
            QTabBar::tab {
                font-family: Calibri;
                background-color: #5fccf5;
                border-radius: 5px;
                margin-right: 3px;
                padding: 5px;
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
            }
            QTabBar::tab:selected:hover {
                background-color: #ffffff;
                color: #000000;
            }
            QTabBar::tab:hover {
                background-color: #277491;
                color: #ffffff;
            }
        """)