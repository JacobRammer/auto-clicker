import tkinter as tk
import sys

window = tk.Tk()

window.title("Hello world!")

state = "stop"

def startClicking() :
    print("Start clicking.")
    return "start"

def stopClicking() :
    print("Stop clicking.")
    return "stop"

# get user input
command = input("Choose from 'start', 'stop', or 'quit'. =>")

while (command != "quit"):
    if (command == state):
        print("Already in that state.")
    
    if (command == "start" and state != "start"):
        state = startClicking()
    elif (command == "stop" and state != "stop"):
        state = stopClicking()
    elif (command != "start" and command != "stop"):
        print("Unknown command.")
    # wait for user input
    command = input("Choose from 'start', 'stop', or 'quit'. => ")

sys.exit()