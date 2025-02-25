from PyQt5.QtWidgets import (QApplication, QLabel, QWidget, QLineEdit, QPushButton, QVBoxLayout)
import sys
import requests
from PyQt5.QtCore import Qt
from datetime import datetime
import pytz
from PyQt5.QtGui import QIcon


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowIcon(QIcon("weather.png"))

        self.city_label = QLabel("Enter City Name:", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel( self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel( self)

       
        self.initUI()
     
    
        
        




    def initUI(self):
        self.setWindowTitle("Weather App")
        self.setGeometry(100, 100, 300, 200)

       
        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

       
        self.city_label.setAlignment(Qt.AlignCenter)
        self.get_weather_button.setMinimumHeight(30)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)


        self.city_label.setObjectName("city_lable")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.emoji_label.setObjectName("emoji_label")
        self.temperature_label.setObjectName("temperature_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
        QLable ,QPushButton{
            font-family: calibri;
        }
        QLabel#city_lable{
            font-size:40px;
            font-style:Times New Roman;
            font-weight: bold;
        }
        QLineEdit#city_input{
        font-size:30px;
        }
        QPushButton#get_weather_button{
        font-size:30px;
        font-weight:bold;
        }
        QLabel#temperature_label{
        font-size:75px;
        }
        QLabel#emoji_label{
        font-size:100px;
        font-family:Segoe UI emoji;
        }
        QLabel#description_label
        {
        font-size:50px;
        }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key="Your API"
        city=self.city_input.text()
        url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        
        try:
            response=requests.get(url)
            response.raise_for_status()
            data=response.json()
         
        

            if data["cod"]==200:
              self.display_weather(data)
        except requests.exceptions.HTTPError as http_error :
            match response.status_code:
                case 400:
                    self.display_error("Bad requset:\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized:\nInvalid API Key")
                case 403:
                   self.display_error("Forbidden:\nAccess is dendied")
                case 404:
                    self.display_error("Not found:\nCity not found")
                case 500:
                    self.display_error("Internal Server Error:\nPlease try again later")
            
                case 502:
                    self.display_error("Bad Gatway:\nInvalied response from the server")
                case 503:
                    self.display_error("Service  Unavailable:\nServer is down")                   
                case 504:
                    self.display_error("Gatway Timeout:\nNo resonse from the server")
                case _: 
                   self.display_error(f"HTTP Error occured:\n{http_error}")


        except requests.exceptions.ConnectionError :
            print("Connection Error:\nCheck your internet connection")   
        except requests.exceptions.Timeout :
            print("Timeoout Error:\nThe request timed out")
        except requests.exceptions.TooManyRedirects :    
             print("Too many Redirects:\nCheck the URL")
        except requests.exceptions.RequestException as req_error :    
            print(f"Request Error: \n{req_error}")


    def display_error(self,message):
        self.temperature_label.setStyleSheet("font-size:30px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()





    def display_weather(self,data):
        self.temperature_label.setStyleSheet("font-size:75px;")
        temperature_k=data["main"]["temp"]
        temperature_c=temperature_k-273.15
        weather_description=data["weather"][0]["description"]
        weather_id=data["weather"][0]["id"]

        timezone_offset = data["timezone"] 
        sunrise = data["sys"]["sunrise"] + timezone_offset
        sunset = data["sys"]["sunset"] + timezone_offset
        current_utc = datetime.utcnow().timestamp()
        is_daytime = sunrise <= current_utc <= sunset




        self.temperature_label.setText(f"{temperature_c:.1f}°C")
        self.emoji_label.setText(self.weather_emoji(weather_id,is_daytime))
        self.description_label.setText(weather_description)

    @staticmethod
    def weather_emoji(weather_id,is_daytime):
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
             return "🌦️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
             return "❄️"
        elif 701 <= weather_id <= 781:
          return "🌫️"
        elif weather_id == 800:
            return "☀️" if is_daytime else "🌙"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
              return "❓"




if __name__ == "__main__":
    app = QApplication(sys.argv)
    Weather_App = WeatherApp()
    Weather_App.show()
    sys.exit(app.exec_())