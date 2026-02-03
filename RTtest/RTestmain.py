import requests
import json

url = "https://auth.openai.com/oauth/token"

payload = json.dumps({
  "client_id": "app_WXrF1LSkiTtfYqiL6XtjygvX",
  "grant_type": "refresh_token",
  "redirect_uri": "com.openai.chat://auth0.openai.com/ios/com.openai.chat/callback",
#   "refresh_token": "rt_xxxxxxx, 购买的新版RT"
   "refresh_token": "rt_vTusgETDzeviga9r5yO02GhjRvGCWtbnb0soyf05Msk.e2Z5tMijsvv3BqhfYv1IObcMpgA5YyoEKleH3aN0d1Y"

})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
