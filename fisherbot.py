import pickle
from time import sleep

import pyautogui


OFFSET = 40  # Offset (in pixel) so the mouse can click on the action button as well
TIME_BETWEEN_HARVEST = 23
TIME_EXIT = 8


def load_map():
    """Load the map."""
    name = input("Name of the map you want to load :\n")
    if name == "save":
        with open(name + ".pickle", "rb") as file:
            data = pickle.load(file)
            map = data["map"]
            id = data["id"]
            p = data["p"]
            return fish(map, id, p)

    with open(name + ".pickle", "rb") as file:
        map = pickle.load(file)
    return map


def save(map, id, p):
    save = {
        "map": map,
        "id": id,
        "p": p
    }
    with open("save.pickle", "wb") as file:
        pickle.dump(save, file)


def get_pos():
    """Return a tuple (x, y) of the mouse position"""
    pos = pyautogui.position()
    tuple_pos = (pos[0], pos[1])
    return tuple_pos


def ghost_click(pos):
    previous_pos = get_pos()
    pyautogui.click(pos)
    pyautogui.click(previous_pos)


def fish(map, id=0, p=0, backup=False):
    """FISHING TIME"""
    sleep(5)
    if p != 0:
        backup = True
    while True:
        try:
            current = map[id]
        except KeyError:
            id = 0
            current = map[id]
        points = current["point"]
        exit = current["exit"]
        for n, point in points.items():
            print(f"n = {n}, p = {p}, backup = {backup}")
            if not backup:
                ghost_click((point[0], point[1]))
                print(f"Clicked point {point[0], point[1]} in map {id}.")
                # sleep(0.5)
                ghost_click((point[0] + OFFSET, point[1] + OFFSET))
                sleep(TIME_BETWEEN_HARVEST)
                pyautogui.press('enter')
            elif backup and n == p:
                ghost_click((point[0], point[1]))
                print(f"Clicked point {point[0], point[1]} in map {id}.")
                sleep(0.5)
                ghost_click((point[0] + OFFSET, point[1] + OFFSET))
                sleep(TIME_BETWEEN_HARVEST)
                pyautogui.press('enter')
                backup = False
            save(map, id, n)
        try:
            ghost_click(exit[0])
            print(f"Clicked exit in map {id}.")
            sleep(TIME_EXIT)
            id += 1
        except KeyError:
            print("No exit in this map.\n")


map = load_map()
sleep(5)
fish(map)
