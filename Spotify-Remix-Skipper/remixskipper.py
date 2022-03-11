import requests

def skipSong(token):
	headers = {
		'Accept': 'application/json',
		'Content-Type': 'application/json',
		'Authorization': f'Bearer {token}',
	}
	
	response = requests.post(
		"https://api.spotify.com/v1/me/player/next", headers=headers
	)

def getCurrentSong(token):
	headers = {
		'Accept': 'application/json',
		'Content-Type': 'application/json',
		'Authorization': f'Bearer {token}',
	}

	params = (
		('market', 'ES'),
		('additional_types', 'episode'),
	)
	response = requests.get('https://api.spotify.com/v1/me/player/currently-playing', \
							headers=headers, params=params)
	if response: response_json = response.json()
	else: return {}
	return response_json

if __name__ == "__main__":
	from time import sleep
	import os
	
	token = os.environ.get('spotify-os-token')
	if token == None:
		print("No authentication token set, please enter your token")
		token = input().strip()
		os.environ['spotify-os-token'] = token
	
	while True:
		song = getCurrentSong(token)
		try:
			if "mix" in song["item"]["name"].lower():
				print(f"[{song['item']['name']}] is a remix, skipping")
				skipSong(token)
		except TypeError:
			pass
		sleep(1)