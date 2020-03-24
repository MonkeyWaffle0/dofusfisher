import pyautogui
import win32api

import pickle
import os.path


def check_map():
    """Check if the map file already exists, create it if it doenst"""
    if not os.path.isfile("map.pickle"):
        map = {}
        with open("map.pickle", "wb") as file:
            pickle.dump(map, file)


def get_pos():
    """Return a tuple (x, y) of the mouse position"""
    pos = pyautogui.position()
    tuple_pos = (pos[0], pos[1])
    return tuple_pos


def get_state():
    """Returns 0 or 1 if left mouse button is up, returns -127 or -128 if mouse button is down."""
    return win32api.GetKeyState(0x01)


def wait_for_click():
    """Wait for mouse button to be down."""
    state = get_state()
    while state >= 0:
        state = get_state()


def save_map(id, map):
    """Save the map in the pickle file."""
    with open("map.pickle", "rb") as file:
        data = pickle.load(file)
    with open("map.pickle", "wb") as file:
        data[id] = map
        pickle.dump(data, file)


def record():
    """Runs a loop, ask the player what he wants to save, then wait for a mouse click to save the pos."""
    # Ask the map ID to the user (first is 1, then 2...) so the bot can navigate through the maps
    id = input("What is the map's ID ?\n")
    map = {
        "exit": {},
        "point": {}
           }
    a = ""  # user input
    i = 1   # index of the point of interest
    e = 1   # index of the exit point
    while a != "q":
        a = input("What do you want to add to the current map ? (i = point of interest, e = exit, q to quit and save)\n")
        if a == "i":
            wait_for_click()
            map["point"][i] = get_pos()
            print(f"Saved point of interest at pos {get_pos()}\n\n")
            i += 1
        elif a == "e":
            wait_for_click()
            map["exit"][e] = get_pos()
            print(f"Saved exit point at pos {get_pos()}\n\n")
            e += 1
        elif a != "q":
            print("Wrong input\n")
            continue

    return id, map


check_map()
id, map = record()
save_map(id, map)