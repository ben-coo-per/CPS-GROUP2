import pyautogui
import time


def set_wekinator_model_values(values):
    """
    Required because wekinator does not have a way to programatically set the model values.
    This script will control the mouse and keyboard to set the model values in wekinator.

    Make sure the wekinator app is open and stays in a constant location on the screen so the script can click the first text box.
    """
    time.sleep(2)
    first_input_x, first_input_y = 423, 130

    pyautogui.click(first_input_x, first_input_y)
    pyautogui.click(first_input_x, first_input_y)

    # Type each value and tab to the next input
    for value in values:
        # clear the input
        pyautogui.press("arrow right", presses=8)
        pyautogui.press("backspace", presses=4)

        pyautogui.write(str(value))
        pyautogui.press("enter")

        # press tab 6 times to get to the next input
        pyautogui.press("tab", presses=6)


if __name__ == "__main__":
    test_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
    set_wekinator_model_values(test_values)
