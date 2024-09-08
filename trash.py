
from datetime import datetime
import os
import sys
import time
import platform
import threading
from pynput import keyboard
from pynput.keyboard import Key
import pyperclip
import psutil
from difflib import SequenceMatcher

# Add the custom path to the system path if it exists
custom_path = os.getenv('PYTHONSCRIPTPATH')
if custom_path and custom_path not in sys.path:
    sys.path.append(custom_path)

# Variables defined
predefined_words = ['shutdownnow', 'poweroff', 'terminate']  # List of predefined words to detect
predefined_words = [word.lower() for word in predefined_words]
monitored_apps = ['Facebook', 'Messenger']  # List of applications to monitor (without '.exe')
monitored_apps = [app.lower() for app in monitored_apps]
typed_buffer = []  # Buffer to store typed characters and word count
word_count = 0
tmpword = ""  # Temporary variable to accumulate characters
initial_apps = set(p.info['name'].replace('.exe', '').lower() for p in psutil.process_iter(['name']))

# Function to simulate shutdown (for testing)
def shutdown_computer():
    print("Shutting down computer...")
    system = platform.system()
    if system == 'Windows':
        os.system('shutdown /s /f /t 0')  # /s for shutdown, /f for force, /t 0 for immediate shutdown
    elif system == 'Linux' or system == 'Darwin':  # Linux and macOS
        os.system('sudo shutdown -h now')  # -h for halt, now for immediate shutdown
    else:
        print(f"Shutdown not supported on {system}.")

# Function to be called when a predefined word is detected
def on_word_detected(word):
    print(f"Detected word: {word}")
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"{current_datetime} - Shutdown command detected and simulated. Triggered by: {word}\n"
    log_file_path = 'C:\\Users\\Utilizador\\Desktop\\codePY\\KeyListenerAndBlocker\\shutdown_test.log'  # Trigger log file
    with open(log_file_path, 'a') as file:
        file.write(message)
    print("Shutdown command detected and simulated.")
    shutdown_computer()

# Function to handle key presses
def on_press(key):
    global word_count
    global tmpword
    print(f"Key pressed: {key}")
    try:
        if hasattr(key, 'char'):  # Only consider keys that have a character attribute
            char = key.char
            if char.isalnum() or char in ['-', '_', 'á', 'é', 'í', 'ó', 'ú', 'à', 'è', 'ì', 'ò', 'ù']:
                tmpword += char
                print("TMPWORD_IF_IF", tmpword)
            elif key == Key.backspace:
                tmpword = tmpword[:-1]
                print("TMPWORD_IF_ELIF", tmpword)
            else:
                if key in [Key.shift, Key.caps_lock]:  # Allow Shift and Caps Lock
                    print("TMPWORD_IF_ELSE_IF", tmpword)
                else:
                    print("TMPWORD_IF_ELSE_ELSE", tmpword)
                    if tmpword:
                        tmpword = tmpword.lower()  # Convert accumulated word to lowercase
                        typed_buffer.append(tmpword)
                        tmpword = ""
                        word_count += 1
        else:
            if key in [Key.shift, Key.caps_lock]:  # Allow Shift and Caps Lock
                print("TMPWORD_ELSE_IF", tmpword)
            elif key == Key.backspace:
                tmpword = tmpword[:-1]
                print("TMPWORD_IF_ELIF", tmpword)
            else:
                print("TMPWORD_ELSE_ELSE", tmpword)
                if tmpword:
                    tmpword = tmpword.lower()  # Convert accumulated word to lowercase
                    typed_buffer.append(tmpword)
                    tmpword = ""
                    word_count += 1
    except AttributeError:
        pass  # Handle special keys as needed, currently ignored in this example
    print("BUFFER AFT_TMP", typed_buffer)
    check_buffer(typed_buffer)  # Check buffer for predefined words

    if word_count >= 150:
        print("Reached 150 words without trigger. Clearing buffer.")
        typed_buffer.clear()
        word_count = 0
    print(word_count)

# Function to calculate the similarity ratio between two words
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

# Function to check buffer for predefined words or near matches
def check_buffer(current_input):
    global word_count  # Declare word_count as global to modify it
    for word in predefined_words + monitored_apps:
        for input_word in current_input:
            if word in input_word or similar(word, input_word) > 0.8:
                on_word_detected(word)
                typed_buffer.clear()
                word_count = 0
                return True
    return False

# Function to monitor clipboard for predefined words
def monitor_clipboard():
    global word_count
    previous_text = ""
    while True:
        current_text = pyperclip.paste().lower()  # Convert clipboard content to lowercase
        if current_text != previous_text:
            previous_text = current_text
            print(f"Clipboard content: {current_text}")
            current_input = current_text.split()
            if not check_buffer(current_input):
                typed_buffer.extend(current_input)
                word_count += len(current_input)
        time.sleep(1)  # Check the clipboard every second

# Function to monitor running applications
def monitor_applications():
    global word_count
    global initial_apps
    print("APPMON COUNT", word_count)
    while True:
        new_apps = set(p.info['name'].replace('.exe', '').lower() for p in psutil.process_iter(['name']))
        for wordo in new_apps:
            if wordo not in initial_apps:
                if not check_buffer([wordo]):
                    print("NEW WORD", wordo)
                    typed_buffer.append(wordo)
                    word_count += 1
        time.sleep(1)  # Check running applications every second

# Initial setup: Add clipboard and running apps to buffer and check for predefined words
def initial_setup():
    global word_count
    global initial_apps
    print("First round of logs")
    clipboard_content = pyperclip.paste().lower()
    clipboard_words = clipboard_content.split()
    print("IN  CLIPBOARD")
    print(clipboard_words)
    print("IN  BUFFER")
    print(typed_buffer)
    print("IN COUNT", word_count)
    typed_buffer.extend(clipboard_words)
    print("BUFFER + CLIPBOARD ST", typed_buffer)
    word_count += len(clipboard_words)
    print("COUNT + CLIPBOARD ST", word_count)

    initial_apps = set(p.info['name'].replace('.exe', '').lower() for p in psutil.process_iter(['name']))
    print("IN  RUNAPPS")
    print(initial_apps)
    typed_buffer.extend(initial_apps)
    print("BUFFER + CLIPBOARD ST + RUNAPPS ST", typed_buffer)
    word_count += len(initial_apps)
    print("COUNT + CLIPBOARD ST + RUNAPPS ST", word_count)

    current_input = ''.join(typed_buffer).split()
    if check_buffer(current_input):
        return
    typed_buffer.clear()
    word_count = 0
    app_monitor_thread = threading.Thread(target=monitor_applications)
    app_monitor_thread.start()
    clipboard_monitor_thread = threading.Thread(target=monitor_clipboard)
    clipboard_monitor_thread.start()

print("Starting listener...")
listener = keyboard.Listener(on_press=on_press, on_release=lambda key: None)
listener.start()
initial_setup()

try:
    listener.join()
except KeyboardInterrupt:
    print("Shutting down...")
