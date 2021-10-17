from pynput import keyboard
import pyperclip as clipboard

MESSAGE = "( ͡° ͜ʖ ͡°)|( ° ͜ʖ °)|( ‾ʖ̫‾)| ☞ó ͜つò☞ |(˵ ͡° ͜ʖ ͡°˵)|( ͠° ͟ʖ ͠°)|( ͠° ͟ʖ ͡°)|(ᴗ ͜ʖ ᴗ)"
message_split = MESSAGE.split("|")
global i
i = 0

def main():
	global i
	i = 0
	def on_press(key):
		if key == keyboard.Key.esc: return False
		try: k = key.char
		except: k = key.name
		if k == "v": 
			global i
			clipboard.copy(message_split[i])
			i += 1
			i %= len(message_split)

	listener = keyboard.Listener(on_press=on_press)
	listener.start()
	while listener.join(): pass
	

if __name__ == "__main__":
	main()
