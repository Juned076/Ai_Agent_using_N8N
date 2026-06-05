import requests

user_message = "can you tell me the conversion of INR to USD?"

request_message = {"message": user_message}

url = "http://localhost:5678/webhook-test/1b87af39-c011-4706-802c-cc37cf1d5819"

response = requests.post(url, json=request_message)

print(response.status_code)
print(response.text)
# print(response.json()[0]['output'])