import tkinter as tk
import auto_clicker as ac
import re
import pyautogui

window = tk.Tk()
window.title("auto-clicker")
window.geometry("650x350")
window.minsize(650, 350)
window.maxsize(650, 350)
validation_regex = r"(?P<time>[\d]+)"  # only capture numbers


def handle_start_stop_press():
    if (ac.Autoclicker.get_state() == ac.STATE.STOPPED):
        ac.Autoclicker.start_clicking()
        start_stop_text.set("STOP")
        start_stop_button.configure(bg="red")
        update_status()
    else:
        ac.Autoclicker.stop_clicking()
        start_stop_text.set("START")
        start_stop_button.configure(bg="green")


def set_click_time():
    """
    Set the click time to a custom value.
    Ignores negative values
    """

    interval_time = get_validated_interval(set_time.get())

    if interval_time != -1 and interval_time > 0:
        ac.Autoclicker.clicking_time = interval_time
        set_time.delete(0, tk.END)
        # remove blinking cursor by focusing on set time button
        set_time_button.focus()
        update_status()
    else:
        set_time.delete(0, tk.END)
        status_label_msg.set("No change made to interval")


def set_click_location():
    """
    Sets the click location (x,y coordinate). Requires both x and y be set.
    """

    # we can re-use validation function for int
    x = get_validated_interval(set_x.get())
    y = get_validated_interval(set_y.get())

    if x != -1 and y != -1:
        # we have a good coordinate
        ac.Autoclicker.set_x_location(x)
        ac.Autoclicker.set_y_location(y)
        ac.Autoclicker.custom_position = True
        set_x.delete(0, tk.END)
        set_y.delete(0, tk.END)
        update_status()
    else:
        status_label_msg.set("No change made to location")


def get_validated_interval(value) -> int:
    """
    takes the raw input from the interval time text field
    returns -1 for invalid input or the validated value to be set
    """

    time = re.search(validation_regex, value)
    if time is not None:
        return int(time.group())  # cast to int

    return -1  # anything that is not a positive int is invalid


def reset_var() -> str:
    """
    Reset click interval and x,y location.
    Display status message in the window.
    Default values: x, y = None
    clicking_time = 5
    """

    ac.Autoclicker.x = None
    ac.Autoclicker.y = None
    ac.Autoclicker.clicking_time = 5
    ac.Autoclicker.custom_position = False
    update_status()


def update_status():
    """
    Catch all function to update the
    information to status label
    """
    # TODO 1: update cursor position in real time
    #   1 partially done, now real time but need to hold down key
    #   2: add message to handle invalid positions

    status_label_msg.set(f"[Interval: {ac.Autoclicker.clicking_time} sec.]"
                         f"[Click position: {check_custom_pos()}]")


def check_custom_pos() -> str:
    """
    Depending on the state of
    Autoclicker.custom_position, return
    the correct string to show on the status label
    """
    if ac.Autoclicker.custom_position is True:
        return f"{ac.Autoclicker.x}, {ac.Autoclicker.y}"

    else:
        return f"cursor"


def assisted_location(event: tk.Event):
    """
    Allow for easy finding of cursor location.
    While holding down (or single press of) c,
    the coordinates are displayed and entered into
    the custom fields. Could use lambda function
    to get rid of event param. Window must be
    focused.
    """

    set_x.delete(0, tk.END)
    set_y.delete(0, tk.END)
    set_x.insert(0, pyautogui.position().x)
    set_y.insert(0, pyautogui.position().y)


# create start / stop button
frame1 = tk.Frame()
frame1.pack(side="top", fill="x")
start_stop_text = tk.StringVar()
start_stop_text.set("START")
start_stop_button = tk.Button(
    frame1,
    textvariable=start_stop_text,
    command=handle_start_stop_press,
    bg="green")
start_stop_button.pack(fill=tk.X, padx=5, pady=5, ipadx=20, ipady=20)

"""
Create interval 
"""
frame2 = tk.Frame()
frame2.pack(side="top", fill="x")
time_label = tk.Label(frame2, text="Autoclick interval: ")
time_label.pack(side=tk.LEFT)
set_time = tk.Entry(frame2, width=5, bg="white")
set_time.pack(side=tk.LEFT, padx=5, pady=5, ipadx=18, ipady=5)
set_time_button = tk.Button(
    frame2, text="Set interval", command=set_click_time, bg="green")
set_time_button.pack(side=tk.RIGHT,
                     fill=tk.X, padx=5, pady=5, ipadx=70, ipady=5)
set_time.bind("<Button-1>", lambda x: set_time.delete(0, tk.END))  # on left click, delete textbox contents
"""
End create interval
"""

# create custom x + y location text
frame3 = tk.Frame()
frame3.pack(side="top", fill="x")
x_label = tk.Label(frame3, text="X:")
x_label.pack(side=tk.LEFT)
set_x = tk.Entry(frame3, width=5, bg="white")
set_x.pack(side=tk.LEFT, padx=5, pady=5, ipadx=18, ipady=5)
y_label = tk.Label(frame3, text="Y:")
y_label.pack(side=tk.LEFT)
set_y = tk.Entry(frame3, width=5, bg="white")
set_y.pack(side=tk.LEFT, padx=5, pady=5, ipadx=18, ipady=5)
set_xy_button = tk.Button(frame3,
                          text="Set click location",
                          command=set_click_location, bg="green")
set_xy_button.pack(side=tk.RIGHT, fill=tk.X, padx=5, pady=5, ipadx=70, ipady=5)
window.bind("c", assisted_location)

"""
Status label
"""
frame4 = tk.Frame()
frame4.pack(side="top", fill="x")
status_label_msg = tk.StringVar()
update_status()
status_label = tk.Label(frame4, textvariable=status_label_msg)
status_label.pack(side=tk.LEFT, fill=tk.X)
reset_button = tk.Button(frame4, width=5, text="Reset", command=reset_var, bg="green")
reset_button.pack(side=tk.RIGHT, fill=tk.X, padx=5, pady=5, ipadx=20, ipady=5)
"""
End status label
"""

window.mainloop()
