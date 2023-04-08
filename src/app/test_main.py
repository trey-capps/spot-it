import requests

BASE = "http://127.0.0.1:5000/"
END = "/userPlaylists/<name>"

response = requests.post(BASE + END, {"name": "trey.capps"})
res_json = response.json()
MF_uri = res_json['data']['MindFuzz']

res_2 = requests.post

print(response.json())