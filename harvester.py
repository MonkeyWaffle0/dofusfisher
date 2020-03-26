import pickle
from time import sleep

import pyautogui


OFFSET = 40  # Offset (in pixel) so the mouse can click on the action button as well
TIME_BETWEEN_HARVEST = 5
TIME_EXIT = 5


def get_pos():
    """Return a tuple (x, y) of the mouse position"""
    pos = pyautogui.position()
    tuple_pos = (pos[0], pos[1])
    return tuple_pos


def ghost_click(pos):
    previous_pos = get_pos()
    pyautogui.click(pos)
    pyautogui.click(previous_pos)


def save(global_map, id, n):
    save = {
        "global_map": global_map,
        "id": id,
        "p": n
    }
    with open("save.pickle", "wb") as file:
        pickle.dump(save, file)


class Harvester:
    def __init__(self):
        self.backup = False
        name = input("Name of the map you want to load :\n")
        if name == "save":
            self.backup = True
        with open(name + ".pickle", "rb") as file:
            data = pickle.load(file)
            self.global_map = data["global_map"]
            self.id = data["id"]
            self.p = data["p"]

    def ghost_click(self, pos):
        previous_pos = get_pos()
        pyautogui.click(pos)
        pyautogui.moveTo(previous_pos)

    def get_current(self):
        try:
            current = self.global_map[self.id]
        except KeyError:
            self.id = 0
            current = self.global_map[self.id]
        points = current["point"]
        exit = current["exit"][0]
        return points, exit

    def click(self, point):
        ghost_click(point)
        print(f"Clicked point {point} in map {self.id}.")
        sleep(0.5)
        ghost_click((point[0] + OFFSET, point[1] + OFFSET))
        sleep(TIME_BETWEEN_HARVEST)
        pyautogui.press('enter')

    def exit(self, pos):
        ghost_click(pos)
        print(f"Clicked exit in map {self.id}.")
        sleep(TIME_EXIT)
        self.id += 1

    def harvest(self):
        sleep(5)
        while True:
            points, exit = self.get_current()
            for n, point in points.items():
                if self.backup:
                    if n != self.p + 1:
                        continue
                    else:
                        self.backup = False
                save(self.global_map, self.id, n)
                self.click(point)
            self.backup = False
            self.exit(exit)


harvester = Harvester()
harvester.harvest()