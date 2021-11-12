import requests
from time import sleep

file = open("spotify history.txt", "a")

OAuthToken = "OAuthToken goes here"

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {OAuthToken}',
}

params = (
    ('market', 'ES'),
    ('additional_types', 'episode'),
)

history = [None]
currently_listening = False

while True:
	response = requests.get('https://api.spotify.com/v1/me/player/currently-playing', \
							headers=headers, params=params)
	if response.status_code == 200:
		cur = (response.json()["item"]["name"], response.json()["item"]["album"]["name"], response.json()["item"]["album"]["artists"][0]["name"])
		currently_listening = True
		if cur != history[-1]:
			print(*cur, sep=" - ")
			file = open("spotify history.txt", "a")
			file.write(cur[0] + " - " + cur[1] + " - " + cur[2] + "\n")
			history += [cur]
	elif currently_listening:
		print("Stopped listening")
		currently_listening = False
	sleep(5)
