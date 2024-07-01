from pynput import keyboard
import os
import platform
from datetime import datetime


# List of predefined words to detect
predefined_words = ['shutdownnow', 'poweroff', 'terminate']

# Buffer to store typed characters
typed_buffer = []

# Function to simulate shutdown (for testing)
def shutdown_computer():
    print("On hold for real version.")

# Function to be called when a predefined word is detected
def on_word_detected(word):
    print(f"Detected word: {word}")
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"{current_datetime} - Shutdown command detected and simulated. Triggered by: {word}\n"
    with open('shutdown_test.log', 'a') as file:
        file.write(message)
    print("Shutdown command detected and simulated.")
    shutdown_computer()

# Function to handle key presses
def on_press(key):
    print(f"Key pressed: {key}")  # Debug print
    try:
        if hasattr(key, 'char') and key.char.isalnum():  # Only consider alphanumeric characters
            typed_buffer.append(key.char)
        else:
            typed_buffer.append(' ')
    except AttributeError:
        print(f"Special key pressed: {key}")  # Debug print
        typed_buffer.append(' ')

    # Check if buffer ends with any predefined word
    current_input = ''.join(typed_buffer).split()
    print(f"Current input buffer: {current_input}")  # Debug print
    for word in predefined_words:
        if word in current_input:
            on_word_detected(word)
            # Clear the buffer to prevent multiple detections
            typed_buffer.clear()

# Function to handle key releases (not used here)
def on_release(key):
    pass

# Setting up the listener
print("Starting listener...")  # Debug print
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
print("Listener stopped.")  # Debug print
