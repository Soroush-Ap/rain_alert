import requests
from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OWM_API_KEY")
MY_LAT = os.getenv("MY_LAT")
MY_LNG = os.getenv("MY_LNG")

# TWILIO
account_sid = os.getenv("ACCOUNT_SID")
auth_token = os.getenv("AUTH_TOKEN")

# api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API key}
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"   # https://
weather_params = {
    "lat":MY_LAT,
    "lon":MY_LNG,
    "appid": API_KEY,
    "cnt": 4
}

response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()


will_rain = False
for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]['id']
    if int(condition_code) < 700:
        will_rain = True


if will_rain:

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="It's going to rain today. Remember to Bring an ☔",
        from_=f"whatsapp:{os.getenv("v_sim")}",
        to=f"whatsapp:{os.getenv("my_sim")}"
    )
    print(message.sid)
    print(message.status)

