import pyperclip
import time
from pynput import keyboard
import os
import platform
from datetime import datetime
import threading
import psutil

# List of predefined words to detect
predefined_words = ['shutdownnow', 'poweroff', 'terminate']

# Buffer to store typed characters and word count
typed_buffer = []
word_count = 0

# List of applications to monitor
monitored_apps = ['Facebook.exe', 'Messenger.exe']

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
    global word_count

    # Debug print
    print(f"Key pressed: {key}")
    try:
        if hasattr(key, 'char') and key.char.isalnum():  # Only consider alphanumeric characters
            typed_buffer.append(key.char)
        else:
            typed_buffer.append(' ')
    except AttributeError:
        print(f"Special key pressed: {key}")  # Debug print
        typed_buffer.append(' ')

    # Count words based on spaces
    if len(typed_buffer) > 1 and typed_buffer[-1] == ' ' and typed_buffer[-2] != ' ':
        word_count += 1

    # Check if buffer ends with any predefined word
    current_input = ''.join(typed_buffer).split()
    print(f"Current input buffer: {current_input}")  # Debug print
    print(word_count)
    # Check if we reached 150 words without a trigger
    if word_count >= 150:
        print("Reached 150 words without trigger. Clearing buffer.")
        typed_buffer.clear()
        word_count = 0
    else:
        for word in predefined_words:
            if word in current_input:
                on_word_detected(word)
                typed_buffer.clear()
                word_count = 0
                break

# Function to handle key releases (not used here)
def on_release(key):
    pass

# Function to monitor clipboard for predefined words
def monitor_clipboard():
    global word_count
    previous_text = ""
    while True:
        current_text = pyperclip.paste()
        if current_text != previous_text:
            previous_text = current_text
            print(f"Clipboard content: {current_text}")  # Debug print
            print(word_count)
            current_input = current_text.split()
            for word in current_input:
                if word in predefined_words:
                    on_word_detected(word)
                    typed_buffer.clear()
                    word_count = 0
                    break
            else:
                # Add clipboard words to the buffer and count them
                typed_buffer.extend(current_input)
                word_count += len(current_input)

                for word in current_input:
                    typed_buffer.append(word)
                    typed_buffer.append(' ')
                word_count += len(current_input)
                # Check if we reached 150 words without a trigger
                if word_count >= 150:
                    print("Reached 150 words without trigger. Clearing buffer.")
                    typed_buffer.clear()
                    word_count = 0
            print(f"Updated input buffer: {''.join(typed_buffer).split()}")  # Debug print
            print(word_count)
        time.sleep(1)  # Check the clipboard every second

# Function to monitor running applications
def monitor_applications():
    while True:
        running_apps = [p.info['name'] for p in psutil.process_iter(['name'])]
        for app in monitored_apps:
            if app in running_apps:
                on_word_detected(app)
        time.sleep(1)  # Check running applications every second
# Start application monitoring in a separate thread
app_monitor_thread = threading.Thread(target=monitor_applications)
app_monitor_thread.start()

# Start clipboard monitoring in a separate thread
clipboard_monitor_thread = threading.Thread(target=monitor_clipboard)
clipboard_monitor_thread.start()

# Setting up the keyboard listener
print("Starting listener...")  # Debug print
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

# Main loop to keep the script running
try:
    listener.join()
except KeyboardInterrupt:
    print("Shutting down...")
