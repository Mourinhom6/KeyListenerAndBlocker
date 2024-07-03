import pyperclip
import time
from pynput import keyboard
import os
import platform
from datetime import datetime
import threading
import psutil

#Variables defenied
predefined_words = ['shutdownnow', 'poweroff', 'terminate']# List of predefined words to detect
typed_buffer = []# Buffer to store typed characters and word count
monitored_apps = ['Facebook', 'Messenger']# List of applications to monitor (without '.exe')
word_count = 0

initial_apps = set(p.info['name'].replace('.exe', '') for p in psutil.process_iter(['name']))

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
        
    check_buffer(typed_buffer)    # # Count words based on spaces
    # if len(typed_buffer) > 1 and typed_buffer[-1] == ' ' and typed_buffer[-2] != ' ':
    #     word_count += 1
    # Check if we reached 150 words without a trigger
    if word_count >= 150:
        print("Reached 150 words without trigger. Clearing buffer.")
        typed_buffer.clear()
        word_count = 0
    print(word_count)

# Function to check buffer for predefined words
def check_buffer(current_input):
    for word in predefined_words + monitored_apps:
        if word in current_input:
            on_word_detected(word)
            typed_buffer.clear()
            word_count = 0
            return True
    return False
# Function to monitor clipboard for predefined words
def monitor_clipboard():
    global word_count
    print("CLIPMON COUNT",word_count)
    previous_text = ""
    while True:
        current_text = pyperclip.paste()
        if current_text != previous_text:
            previous_text = current_text
            print(f"Clipboard content: {current_text}")  # Debug print
            print(word_count)
            current_input = current_text.split()
            print("BUFFER CLIMON ",typed_buffer)
            if not check_buffer(current_input):
                # Add clipboard words to the buffer and count them
                typed_buffer.extend(current_input)
                print("BUFFER CLIMON ND",typed_buffer)
                word_count += len(current_input)
            # Check if we reached 150 words without a trigger

        time.sleep(1)  # Check the clipboard every second

# Function to monitor running applications
def monitor_applications():
    global word_count
    global initial_apps
    print("APPMON COUNT",word_count)
    print("APPMON INITILaPPS",initial_apps)
    while True:
        new_apps  = set(p.info['name'].replace('.exe', '') for p in psutil.process_iter(['name']))
        # print("BUFFER APPMON ",typed_buffer)
        for wordo in new_apps:
            if wordo not in initial_apps:
                if not check_buffer(wordo):
                    print("NEW WORD",wordo)
                    # Add new running apps to the buffer and count them
                    typed_buffer.extend(wordo)
                    # print("BUFFER APPMON ND",typed_buffer)
                    word_count += 1
                    # Check if we reached 150 words without a trigger
        time.sleep(1)  # Check running applications every second
# Initial setup: Add clipboard and running apps to buffer and check for predefined words
def initial_setup():
    global word_count
    print("First round of logs")
    # Add clipboard content
    clipboard_content = pyperclip.paste()
    clipboard_words = clipboard_content.split()
    print("IN  CLIPBOARD")
    print(clipboard_words)
    print("IN  BUFFER")
    print(typed_buffer)
    print("IN COUNT",word_count)
    typed_buffer.extend(clipboard_words)
    print("BUFFER + CLIPBOARD ST",typed_buffer)
    word_count += len(clipboard_words)
    print("COUNT + CLIPBOARD ST",word_count)

    # Add running applications
    running_apps = set(p.info['name'].replace('.exe', '') for p in psutil.process_iter(['name']))
    print("IN  RUNAPPS")
    print(running_apps)
    typed_buffer.extend(running_apps)
    print("BUFFER + CLIPBOARD ST + RUNAPPS ST",typed_buffer)
    word_count += len(running_apps)
    print("COUNT + CLIPBOARD ST + RUNAPPS ST",word_count)

    # Check for predefined words
    current_input = ''.join(typed_buffer).split()
    if check_buffer(current_input):
        return
    # Clear buffer and word count if no predefined words are detected
    typed_buffer.clear()
    word_count = 0
    print("ND  BUFFER")
    print(typed_buffer)
    print("ND COUNT",word_count)
    # Start application monitoring in a separate thread
    app_monitor_thread = threading.Thread(target=monitor_applications)
    app_monitor_thread.start()

    # Start clipboard monitoring in a separate thread
    clipboard_monitor_thread = threading.Thread(target=monitor_clipboard)
    clipboard_monitor_thread.start()
# Setting up the keyboard listener
print("Starting listener...")  # Debug print
listener = keyboard.Listener(on_press=on_press, on_release=lambda key: None)
listener.start()
# Run initial setup
initial_setup()

# Main loop to keep the script running
try:
    listener.join()
except KeyboardInterrupt:
    print("Shutting down...")
