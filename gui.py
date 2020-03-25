from tkinter import *
import pickle

import win32api
import pyautogui


def get_pos():
    """Return a tuple (x, y) of the mouse position"""
    pos = pyautogui.position()
    tuple_pos = (pos[0], pos[1])
    return tuple_pos


class Point():
    def __init__(self, map, map_index, point_type, id, pos, mainWindow):
        self.map = map.map
        self.index = map_index
        self.pos = pos
        self.type = point_type
        self.id = id
        self.mainWindow = mainWindow

        self.button = Button(mainWindow.frame, text=pos, command=lambda: map.new_point(point_type))
        if point_type == "point":
            self.button.grid(row=id + 3, column=map_index * 2)
        elif point_type == "exit":
            self.button.grid(row=id + 3, column=1 + (map_index * 2))


class Map():
    def __init__(self, index, mainWindow):
        self.map = {
            "exit": {},
            "point": {}
        }

        self.p_id = 0
        self.e_id = 0

        self.mainWindow = mainWindow
        self.name = "Map " + str(index)
        self.index = index
        # self.button = Button(mainWindow.frame, text=self.name, command=self.left)
        # self.button.bind("<Button-3>", self.right)
        self.text = Label(mainWindow.frame, text=self.name, font="arial 10 bold").grid(row=1, column=index * 2, padx=1, pady=1)
        self.point_button = Button(mainWindow.frame, text="New point", command=lambda: self.new_point("point"))
        self.exit_button = Button(mainWindow.frame, text="New exit", command=lambda: self.new_point("exit"))

        self.point_button.grid(row=2, column=index * 2)
        self.exit_button.grid(row=2, column=1+(index*2))

        self.point_pressed = False
        self.exit_pressed = False

    def add(self, point_type, id):
        pos = get_pos()
        point = Point(self, self.index, point_type, id, pos, self.mainWindow)
        self.map[point_type][id] = pos

    def new_point(self, point_type):
        self.mainWindow.master.bind('<d>', self.on_key)
        if point_type == "point":
            self.point_pressed = True
            if self.exit_pressed:
                self.exit_pressed = False
        elif point_type == "exit":
            self.exit_pressed = True
            if self.point_pressed:
                self.point_pressed = False

    def on_key(self, event=None, *args):
        if self.point_pressed:
            self.add("point", self.p_id)
            self.p_id += 1
            print(f"got the point at pos {get_pos()}")
            self.point_pressed = False
        elif self.exit_pressed:
            self.add("exit", self.e_id)
            self.e_id += 1
            print(f"got the exit at pos {get_pos()}")
            self.exit_pressed = False

    def right(self):
        self.button.destroy()
        self.mainWindow.maps.remove(self)
        self.mainWindow.update()


class GlobalMap():
    def __init__(self, mainWindow):
        self.global_map = {}
        self.mainWindow = mainWindow

    def __setitem__(self, id, map):
        self.global_map[id] = map

    def add(self, index, map):
        self.global_map[index] = map

    def to_dict(self):
        dic = {}
        for i, map in self.global_map.items():
            dic[i] = {
                "point": {},
                "exit": {}
            }
            for j, point in map.map["point"].items():
                dic[i]["point"][j] = point
            for k, exit in map.map["exit"].items():
                dic[i]["exit"][k] = exit
        return dic


class SaveWindow():
    """Popup window when clicked on the add button."""
    def __init__(self, master):
        top = self.top = Toplevel(master)
        self.label = Label(top, text="Name of your map :")
        self.label.pack()
        self.entry = Entry(top)
        self.entry.pack()
        self.button = Button(top, text="Go", command=self.cleanup)
        self.button.pack()

    def cleanup(self):
        """Get the entry value and close the popup window."""
        self.value = self.entry.get()
        self.top.destroy()


class MainWindow():
    """Main window"""
    def __init__(self, master):
        self.master = master
        self.frame = Frame(master, width=1000, height=600)
        self.frame.pack()

        self.id = 0
        self.global_map = GlobalMap(self)

        # Button to add a new map.
        self.add_button = Button(self.frame, text="New map", command=self.new_map)
        self.add_button.grid(row=0, column=0, padx=1, pady=1)

        # Button to save the current list.
        self.save_button = Button(self.frame, text="Save", command=self.save)
        self.save_button.grid(row=0, column=1)

        #Button to load a saved list.
        self.load_button = Button(self.frame, text="Load", command=self.load)
        self.load_button.grid(row=0, column=2)

        # Setting the minimum size of each column to 150.
        """columnCount, rowCount = self.frame.grid_size()
        for column in range(columnCount):
            self.frame.grid_columnconfigure(column, minsize=150)"""

    def new_map(self):
        map = Map(self.id, self)
        self.global_map.add(self.id, map)
        self.id += 1

    def save(self):
        """Popup window to save the current list."""
        # Creating the window.
        self.window = SaveWindow(self.master)

        # Disable the save button until the popup is closed.
        self.save_button["state"] = "disabled"
        self.master.wait_window(self.window.top)
        self.save_button["state"] = "normal"

        dic = self.global_map.to_dict()
        # Add every task to self.save and dump it to a file.
        with open(self.entryValue() + ".pickle", "wb") as outfile:
            pickle.dump(dic, outfile)

    def load(self):
        """Load the file in the load entry field."""
        self.window = SaveWindow(self.master)

        # Disable the save button until the popup is closed.
        self.load_button["state"] = "disabled"
        self.master.wait_window(self.window.top)
        self.load_button["state"] = "normal"
        try:
            with open(self.entryValue() + ".pickle", "rb") as file:
                dic = pickle.load(file)
                for i, map in dic.items():
                    new_map = Map(i, self)
                    for j, pos in map["point"].items():
                        new_point = Point(new_map, i, "point", j, pos, self)
                    self.global_map[i] = new_map
        except FileNotFoundError:
            # Displays message error if the file does not exist.
            self.noFile = Label(self.frame, text="No such file found !", fg="red", font="arial 10")
            self.noFile.grid(row=1, column=3, padx=1, pady=1)
            self.noFile.after(2500, self.noFile.destroy)

    def entryValue(self):
        """Get the value in the entry field."""
        return self.window.value


if __name__ == "__main__":
    root = Tk()
    root.title("Map recorder")
    root.geometry("1000x600")
    main = MainWindow(root)
    root.mainloop()
