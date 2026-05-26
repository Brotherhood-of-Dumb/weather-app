# These were static methods in the WeatherApp class. Moved them to be more modular

# The 700 range needs work. We won't get volcanic ash with that there.
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


def temp_conversion(temp):
    return (temp - 273.15) * 1.8 + 32


def speed_conversion(ms):
    return ms * 2.237


def distance_conversion(meter):
    return meter / 1609


def atmo_convers(hpa):
    return hpa * 0.02953


def first_letter_upper(desc):
    first = desc[0:1].upper()
    rest = desc[1:]
    return first + rest