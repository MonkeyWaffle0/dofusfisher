import pickle
from time import sleep

import pyautogui


OFFSET = 50  # Offset (in pixel) so the mouse can click on the action button as well
TIME_BETWEEN_HARVEST = 23
TIME_EXIT = 8


def load_map():
    """Load the map."""
    name = input("Name of the map you want to load :\n")
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
            print(f"Clicked point {point[0], point[1]} in map {id}.")
            sleep(0.5)
            pyautogui.click(point[0] + OFFSET, point[1] + OFFSET)
            sleep(TIME_BETWEEN_HARVEST)
            pyautogui.press('enter')
        try:
            pyautogui.click(exit[0])
            print(f"Clicked exit {n} in map {id}.")
            sleep(TIME_EXIT)
            id += 1
        except KeyError:
            print("No exit in this map.\n")


map = load_map()
sleep(5)
fish(map)