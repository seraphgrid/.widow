
from pynput import keyboard
import subprocess

# Set to keep track of currently pressed keys
current_keys = set()

def on_press(key):
    current_keys.add(key)  # Add the pressed key to the set

    # Check if the key is a modifier
    if key in (keyboard.Key.shift, keyboard.Key.ctrl, keyboard.Key.alt):
        return  # Continue listening without capturing a key

    # Prepare the key combination to send
    key_combination = []
    if keyboard.Key.ctrl in current_keys:
        key_combination.append('ctrl')
    if keyboard.Key.shift in current_keys:
        key_combination.append('shift')
    if keyboard.Key.alt in current_keys:
        key_combination.append('alt')

    # Add the actual key pressed
    try:
        key_combination.append(key.char)  # Get the character of the key pressed
    except AttributeError:
        key_combination.append(str(key))  # Handle special keys

    # Print the key combination
    print(f'You pressed: {" + ".join(key_combination)}')

    # Send the key combination to the active window using xdotool
    subprocess.run(['xdotool', 'key', *key_combination])

    return False  # Stop the listener after capturing the key

def on_release(key):
    current_keys.discard(key)  # Remove the released key from the set

def listen_for_key():
    # Start listening for the next key press
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    print("Listening for the next key press...")
    listen_for_key()
