import pyautogui
import threading
import time
import enum


class STATE(enum.Enum):
    STARTED = 1
    STOPPED = 0


class Autoclicker(object):
    state = STATE.STOPPED
    clicker_thread = None
    stop_event = threading.Event()
    clicking_time = 5
    x = None
    y = None

    @staticmethod
    def start_clicking():
        Autoclicker.clicker_thread = threading.Thread(
            target=Autoclicker.__clicking_thread)
        # make the clicker thread a daemon so it lives and dies
        # with the main application
        Autoclicker.clicker_thread.daemon = True
        Autoclicker.clicker_thread.start()
        Autoclicker.state = STATE.STARTED

    @staticmethod
    def stop_clicking():
        Autoclicker.stop_event.set()
        Autoclicker.state = STATE.STOPPED

    @staticmethod
    def get_state():
        return Autoclicker.state

    @staticmethod
    def __clicking_thread():
        while not Autoclicker.stop_event.is_set():
            time.sleep(Autoclicker.clicking_time)
            if Autoclicker.x is None or Autoclicker.y is None:
                pyautogui.click()
            else:
                # save current cursor position
                (x, y) = pyautogui.position()
                # click
                pyautogui.click(Autoclicker.x, Autoclicker.y)
                # move cursor back
                pyautogui.moveTo(x, y)

        # reset the stop event object
        Autoclicker.stop_event = threading.Event()

    @staticmethod
    def set_x_location(x):
        Autoclicker.x = x

    @staticmethod
    def set_y_location(y):
        Autoclicker.y = y

    @staticmethod
    def reset_x_y_location():
        Autoclicker.x = None
        Autoclicker.y = None
