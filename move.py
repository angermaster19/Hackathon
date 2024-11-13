import pyautogui
import time

def move_cursor_loop():
    # Set the amount of pixels to move left and right
    move_distance = 100

    while True:
        # Move cursor left
        current_position = pyautogui.position()
        pyautogui.moveTo(current_position.x - move_distance, current_position.y)
        time.sleep(60)  # Wait for 1 minute

        # Move cursor right
        current_position = pyautogui.position()
        pyautogui.moveTo(current_position.x + move_distance, current_position.y)
        time.sleep(60)  # Wait for 1 minute

# Start the cursor movement loop
move_cursor_loop()
