import requests

def skipSong(token) -> None:
	headers = {
		'Accept': 'application/json',
		'Content-Type': 'application/json',
		'Authorization': f'Bearer {token}',
	}
	
	response = requests.post(
		"https://api.spotify.com/v1/me/player/next", 
		headers=headers
	)

def getCurrentSong(token) -> dict:
	headers = {
		'Accept': 'application/json',
		'Content-Type': 'application/json',
		'Authorization': f'Bearer {token}',
	}
	
	response = requests.get(
		'https://api.spotify.com/v1/me/player/currently-playing', 
		headers=headers
	)
	
	return response.json() if response else {}

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
		except KeyError:
			pass
		sleep(1)
