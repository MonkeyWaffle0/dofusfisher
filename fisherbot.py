import pickle
from time import sleep

import pyautogui


offset = 50


def load_map():
    with open("map.pickle", "rb") as file:
        map = pickle.load(file)
    return map


def fish(map):
    id = 1
    while True:
        try:
            current = map[str(id)]
        except IndexError:
            id = 1
            current = map[str(id)]
        points = current["point"]
        exit = current["exit"]
        for n, point in points.items():
            pyautogui.click(point[0], point[1])
            sleep(0.5)
            pyautogui.click(point[0] + offset, point[1] + offset)
            sleep(23)
        pyautogui.click(exit[1])
        sleep(5)
        id += 1


sleep(5)
map = load_map()
fish(map)