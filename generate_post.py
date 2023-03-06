import requests
from http.client import HTTPConnection
HTTPConnection._http_vsn_str = 'HTTP/1.1'

url = "http://localhost:8000/"

payload = {
    "query": "POST",
    "msg": "fox flex"
}

response = requests.post(url, json=payload, )

if response.status_code == 200:
    print("POST request successful")
    print("Response:", response.json())
else:
    print("POST request failed")
    print("Status code:", response.status_code)
    print("Error message:", response.text)