import requests

URL = "https://notify-api.line.me/api/notify"
TOKEN_NOTIFY = "HkQ4LrBKcLrtqXHHrON0TjVjoWMEoMBOnGOzu3dnUhb"

headers = {"Authorization": f"Bearer {TOKEN_NOTIFY}"}
data = {"message": "11022125廖先信"}

try:
       rd = requests.post(URL, headers=headers, data=data)
       rd.raise_for_status()
except requests.exceptions.HTTPError as err:
       print(f"HTTP error occurred: {err}")
except Exception as err:
       print(f"An error occurred: {err}")