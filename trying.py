from pynput import keyboard
import os
import platform

# List of predefined words to detect
predefined_words = ['shutdownnow', 'poweroff', 'terminate']

# Buffer to store typed characters
typed_buffer = []

# Function to simulate shutdown (for testing)
def shutdown_computer():
    with open('shutdown_test.log', 'a') as file:
        file.write('Shutdown command detected and simulated.\n')
    print("Shutdown command detected and simulated.")

# Function to be called when a predefined word is detected
def on_word_detected(word):
    print(f"Detected word: {word}")
    shutdown_computer()

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
