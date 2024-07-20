import time
import pyautogui
import keyboard
import win32api, win32con, win32gui
import ctypes

def check_coins():
    coin_color = (247, 159, 87)  # Bronze Coins
    screen_width, screen_height = pyautogui.size()
    screenshot = pyautogui.screenshot()
    
    for x in range(0, screen_width, 5):
        for y in range(0, screen_height, 5):
            pixel_color = screenshot.getpixel((x, y))
            if all(abs(a - b) <= 10 for a, b in zip(pixel_color, coin_color)):
                for dx in range(5):
                    if x + dx >= screen_width:
                        break
                    check_color = screenshot.getpixel((x + dx, y))
                    if not all(abs(a - b) <= 10 for a, b in zip(check_color, coin_color)):
                        break
                else:
                    return (x, y)
    return None

def click_method_1(x, y):
    # Direct Input simulation
    ctypes.windll.user32.SetCursorPos(x, y)
    ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # left down
    time.sleep(0.1)
    ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # left up

def click_method_2(x, y):
    # Send input to the window directly
    hwnd = win32gui.GetForegroundWindow()
    lParam = win32api.MAKELONG(x, y)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    time.sleep(0.1)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, lParam)

def click_method_3(x, y):
    # Rapid double-click
    for _ in range(2):
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        time.sleep(0.01)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        time.sleep(0.01)

click_methods = [click_method_1, click_method_2, click_method_3]
current_method = 0

print("Script started. Press 'q' to quit, 'c' to change click method.")
while not keyboard.is_pressed('q'):
    if keyboard.is_pressed('c'):
        current_method = (current_method + 1) % len(click_methods)
        print(f"Switched to click method {current_method + 1}")
        time.sleep(0.5)  # Prevent multiple switches

    coin_coords = check_coins()
    if coin_coords:
        print(f"Coin found at {coin_coords}. Clicking with method {current_method + 1}...")
        click_methods[current_method](*coin_coords)
        print("Click performed.")
        time.sleep(0.5)
    else:
        print("No coins were found in this scan.")
    
    time.sleep(0.1)

print("Script terminated.")