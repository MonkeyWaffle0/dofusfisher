import pyautogui
import win32api

import pickle
import os.path


def check_map():
    if not os.path.isfile("map.pickle"):
        map = {}
        with open("map.pickle", "wb") as file:
            pickle.dump(map, file)


def get_pos():
    pos = pyautogui.position()
    tuple_pos = (pos[0], pos[1])
    return tuple_pos


def get_state():
    return win32api.GetKeyState(0x01)


def wait_for_click():
    state = get_state()
    while state >= 0:
        state = get_state()


def save_map(id, map):
    with open("map.pickle", "rb") as file:
        data = pickle.load(file)
    with open("map.pickle", "wb") as file:
        data[id] = map
        pickle.dump(data, file)


def record():
    id = input("What is the map's ID ?\n")
    map = {
        "exit": {},
        "point": {}
           }
    a = ""
    i = 1
    e = 1
    while a != "q":
        a = input("What do you want to add to the current map ? (i = point of interest, e = exit)\n")
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