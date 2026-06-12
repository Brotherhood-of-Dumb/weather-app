import math
import sys
import requests
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QTabWidget, \
    QStyleOption, QStyle
from PyQt5.QtCore import Qt, QSize
from methods import *


def get_current_weather(city, success, error):
    api_key = "d15ceeb9e59ddbaa73b6e22779d856ee"
    # TODO: This is for current forecast. We need a link for future forecast.
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if response.status_code == 200:
            success(data)
    except requests.exceptions.HTTPError as e:
        match response.status_code:
            case 400:
                error("Bad Request\nCheck your city name")
            case _:
                error({e})
            # add 401,403,404,500,502,503,504
    except requests.exceptions.ConnectionError:
        error("Connection Error\nCheck your internet connection")
    except requests.exceptions.Timeout:
        error("Timeout Error")
    except requests.exceptions.TooManyRedirects:
        error("TooManyRedirects")
    except requests.exceptions.RequestException as e:
        error(f"RequestException: {e}")