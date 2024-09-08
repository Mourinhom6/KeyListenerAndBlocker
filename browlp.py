from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Path to your chromedriver
CHROMEDRIVER_PATH = '/path/to/chromedriver'

options = Options()
options.add_argument('--start-maximized')

service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

# Open the browser and navigate to the page with the search input
driver.get('https://example.com')  # Replace with your actual URL

import logging
from pynput import keyboard
import pyperclip
import threading

logging.basicConfig(filename='browser_log.txt', level=logging.INFO)

# Global variable to keep track of the current input value
current_value = ""

def log_event(event_type, value):
    logging.info(f"Type: {event_type}, Value: {value}")

def on_press(key):
    global current_value
    try:
        if key.char:
            current_value += key.char
            log_event('keypress', current_value)
    except AttributeError:
        if key == keyboard.Key.backspace:
            current_value = current_value[:-1]
            log_event('backspace', current_value)
        elif key == keyboard.Key.delete:
            # Assuming deleting a character from the cursor position
            current_value = current_value[:-1]  # Simplification
            log_event('delete', current_value)

def on_release(key):
    # Check for clipboard content on paste (Ctrl+V)
    if key == keyboard.Key.ctrl_l:
        clipboard_content = pyperclip.paste()
        log_event('paste', clipboard_content)

# Start the keyboard listener in a separate thread
def start_listener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

listener_thread = threading.Thread(target=start_listener)
listener_thread.start()

# Keep the script running to capture events
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Logging stopped")
