from pynput import keyboard

# List of predefined words to detect
predefined_words = ['shutdownnow', 'poweroff', 'terminate']

# Buffer to store typed characters
typed_buffer = []



def on_press(key):
    try:
        print(f'Key {key.char} pressed')
    except AttributeError:
        print(f'Special key {key} pressed')

def on_release(key):
    print(f'Key {key} released')
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
from pynput.mouse import Button, Controller

mouse = Controller()

# Move the mouse to the coordinates (100, 100)
mouse.position = (100, 100)
print('Current position:', mouse.position)

# Move the mouse relative to its current position
mouse.move(50, -50)

# Click the left mouse button
mouse.click(Button.left, 1)

# Scroll down
mouse.scroll(0, -2)

from pynput import keyboard



# Function to be called when a predefined word is detected
def on_word_detected(word):
    print(f"Detected word: {word}")
    # Perform any action here
    # Example action: print a message
    if word == 'hello':
        print("Hello there!")
    elif word == 'world':
        print("World detected!")
    elif word == 'test':
        print("Test successful!")

# Function to handle key presses
def on_press(key):
    try:
        if key.char.isalnum():  # Only consider alphanumeric characters
            typed_buffer.append(key.char)
        else:
            typed_buffer.append(' ')
    except AttributeError:
        typed_buffer.append(' ')

    # Check if buffer ends with any predefined word
    current_input = ''.join(typed_buffer).split()
    for word in predefined_words:
        if word in current_input:
            on_word_detected(word)
            # Clear the buffer to prevent multiple detections
            typed_buffer.clear()

# Function to handle key releases (not used here)
def on_release(key):
    pass

# Setting up the listener
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()