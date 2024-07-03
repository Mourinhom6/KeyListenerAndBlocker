# Keyboard Listener AND Monitoring

Script to Monitor and Detect Predefined Words

## Table of Contents

- [Description](#description)
- [Features](#Features)
- [Installation](#Installation)
- [Setup](#Setup)
- [Customization](#Customization)
- [License](#License)

## Description

This Python script monitors keyboard input, clipboard content, and running applications for predefined words. If any predefined words are detected, a simulated shutdown is triggered. This script can be customized to suit various needs and is designed to run continuously.

 <!-- Include a relevant image if available -->

## Features

1. **Monitors keyboard input for predefined words**

2. **Monitors clipboard content for predefined words**

3. **Monitors running applications for predefined words**

4. **Logs detected words and simulates a shutdown (currently a placeholder for real shutdown functionality)**

5. **Resets monitoring if 150 words are processed without a trigger**

## Installation

- **Prerequisites**

- **Python 3.x**

- **pyperclip library**

- **pynput library**

- **psutil library**

------------

You can install the required libraries using pip:

 ```sh
   pip install pyperclip pynput psutil
   ```

## Setup

- Clone the repository or download the script file.

- Ensure the script has the necessary permissions to run (especially for clipboard and process monitoring).

- Running the Script

**Run the code manually:**

 ```sh
   python path/to/your_script.py
   ```

**Continuous Running Setup:**

**Windows**

1. Create a batch file named run_script.bat with the following content:

 ```sh
   @echo off
   python path\to\your_script.py
   pause
   ```

2. Copy the batch file to the startup folder:

Press **'Win + R'**, type **'shell:startup'**, and press Enter.

Paste your **'run_script.bat'** file in the startup folder.

**Linux**

1. Create a shell script named **'run_script.bat'** with the following content:

 ```sh
    #!/bin/bash
   python path/to/your_script.py
   ```

2. Make the script executable:

 ```sh
   chmod +x run_script.sh
   ```

3. Add the script to your startup applications:

Use the **'Startup Applications'** GUI tool or add it to **'~/.config/autostart'**.

Optionally, create a systemd service for reliability.

**MacOS**

1. Create a shell script named **'run_script.sh'**:

 ```sh
   #!/bin/bash
   python3 /path/to/your_script.pyy
   ```

2. Add the script to your startup items:

Go to **'System Preferences > Users & Groups > Login Items'**.

Click the **'+'** button and add your script.

## Customization

**Predefined Words:** Modify the **'predefined_words'** list in the script to add or remove words to be detected.

**Monitored Applications:** Modify the **'monitored_apps'** list to add or remove applications to be monitored.

**Simulated Shutdown:** Customize the **'shutdown_computer'** function to implement real shutdown functionality.

**Logging**

The script logs detected words with timestamps to shutdown_test.log. You can change the log file name or location by modifying the on_word_detected function.

**Debugging**

The script includes debug print statements to help with troubleshooting. Remove or comment out these print statements in a production environment.

## Licença

[MIT](https://choosealicense.com/licenses/mit/)