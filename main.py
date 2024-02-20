import requests
from datetime import datetime
import os

user_input = input("Tell me which exercises you did: ")

nutrition_exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
nutrition_params = {
    "query": user_input,
}
headers = {
    "x-app-id": os.environ["APP_ID"],
    "x-app-key": os.environ["API_KEY"],
}
response = requests.post(url=nutrition_exercise_endpoint, json=nutrition_params, headers=headers)
result = response.json()

sheet_endpoint = os.environ["SHEET_ENDPOINT"]
sheet_headers = {
    "Authorization": os.environ["TOKEN"],
}
today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheet_response = requests.post(url=sheet_endpoint, json=sheet_inputs,headers=sheet_headers)

    print(sheet_response.text)