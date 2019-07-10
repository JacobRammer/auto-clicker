import tkinter as tk
import auto_clicker as ac
import re

window = tk.Tk()
window.title("auto-clicker")
window.geometry("400x200")
window.minsize(300, 150)
window.maxsize(400, 200)
validation_regex = r"(?P<time>[\d]+)"  # only capture numbers


def handle_start_stop_press():
    if ((ac.Autoclicker.get_state() == ac.STATE.STOPPED)):
        ac.Autoclicker.start_clicking()
        start_stop_text.set("STOP")
        start_stop_button.configure(bg="red")
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
        set_time.insert(0, f"Interval set")
        # remove blinking cursor by focusing on set time button
        set_time_button.focus()
    else:
        set_time.delete(0, tk.END)
        set_time.insert(0, "No change")


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


def get_validated_interval(value):
    """
    takes the raw input from the interval time text field
    returns -1 for invalid input or the validated value to be set
    """

    time = re.search(validation_regex, value)
    if time is not None:
        return int(time.group())  # cast to int

    return -1  # anything that is not a positive int is invalid


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

# create set time text + button
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
# on left click, delete textbox contents
set_time.bind("<Button-1>", lambda x: set_time.delete(0, tk.END))

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

window.mainloop()
