import pickle
from time import sleep

import pyautogui


offset = 50  # Offset (in pixel) so the mouse can click on the action button as well


def load_map():
    """Load the map."""
    name = input("How do you want to call your map ?\n")
    with open(name + ".pickle", "rb") as file:
        map = pickle.load(file)
    return map


def fish(map):
    """FISHING TIME"""
    id = 0
    while True:
        try:
            current = map[id]
        except KeyError:
            id = 0
            current = map[id]
        points = current["point"]
        exit = current["exit"]
        for n, point in points.items():
            pyautogui.click(point[0], point[1])
            sleep(0.5)
            pyautogui.click(point[0] + offset, point[1] + offset)
            sleep(23)
            pyautogui.press('enter')
        try:
            pyautogui.click(exit[0])
            sleep(8)
            id += 1
        except KeyError:
            print("No exit in this map.\n")

map = load_map()
sleep(5)
fish(map)