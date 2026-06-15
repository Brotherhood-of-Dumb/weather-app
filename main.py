import sys
from PyQt5.QtWidgets import QApplication
from forecast_component import ForecastTotal
from current_weather_component import CurrentWeather
from tabs_component import WeatherAppTabs

# TODO: potentially create a QMainWindow class here, set title and setGeometry methods in it.
# TODO: to add an icon, need asset folder, import from QtGui QIcon, setWindowIcon and pass in QIcon with file path

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
