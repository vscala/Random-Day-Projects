from datetime import datetime, timedelta
from pynput import keyboard
import pyperclip as clipboard

class LeagueClipboard:
	DEFAULT_FORMATTING = "Enemy summoners: {info}"
	def __init__(self, formatting=DEFAULT_FORMATTING):
		self.formatting = formatting 
		self.new()
		
	def new(self):
		self.clear()
		self.gameStart = datetime.now()
		
	def clear(self):
		self.stack = {}
		self.update()
	
	def add(self, cooldown, message):
		time = datetime.now() - self.gameStart + cooldown
		m, s = divmod(time.seconds, 60)
		message = f"{message} ({m}:{str(s).zfill(2)}) "
		self.stack[message] = time
		self.update()
	
	def update(self):
		info = ""
		seen = set()
		for message in self.stack:
			if message[0:3] in seen: continue
			seen.add(message[0:3])
			if self.stack[message] <= (datetime.now() - self.gameStart):
				del self.stack[message]
			info += f"{message}, "
		
		clipboard.copy(self.formatting.replace("{info}", info[:-2]))
		 

keys = {
	'1' : (LeagueClipboard.add, (timedelta(minutes=5), "SUP FLASH")),
	'2' : (LeagueClipboard.add, (timedelta(minutes=5), "AD FLASH")),
	'3' : (LeagueClipboard.add, (timedelta(minutes=5), "JG FLASH")),
	'4' : (LeagueClipboard.add, (timedelta(minutes=5), "TOP FLASH")),
	'5' : (LeagueClipboard.add, (timedelta(minutes=5), "MID FLASH")),
	'`' : (LeagueClipboard.clear, ()),
	'n' : (LeagueClipboard.new, ()),
}

def main():
	lc = LeagueClipboard()

	def on_press(key):
		if key == keyboard.Key.esc: return False
		try: k = key.char
		except: k = key.name
		if k in keys: keys[k][0](lc, *keys[k][1]) 

	listener = keyboard.Listener(on_press=on_press)
	listener.start()
	while listener.join(): pass
	

if __name__ == "__main__":
	main()
		
