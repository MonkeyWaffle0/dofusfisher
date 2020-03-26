# dofusfisher

## What it does
Dofusfisher allows you to record a path to automaticaly harvest in Dofus.

## What is required
* python 3
```python
pip install pyautogui
```

## How to use it
#### Record you map
* Start map_recorderGUI.py
* In dofus, go to the first map you wish to record, put the game in windowed full-screen.
* Click **New map** then click **New point**
* Put the cursor over the point you wish to save, then press **d** on your keyboard, the point's coordinates should appear below the map in the GUI.
* Repeat for every points you want to save on the current map.
* Click **New exit**
* Put your cursor over the exit you want to use, press **d** on your keyboard to save it.
* In dofus, go to the next map, and repeat the steps until you've done a loop (exit of your last map should lead to the very first map you saved).
* Click **Save** and give a name to your path.

#### Harvest time
* In dofus, go to the first map you saved.
* Start harvester.py
* Enter the name of your path.
* Go back to Dofus.
* Wait and see.

#### What to do if I encounter a monster ?
* You can close the bot, the bot saved the current point you were in a file called **save.pickle**.
* Once you won the fight, start the bot again, and load the **save** file.
* The bot now keeps going where you were before your fight ! (If you closed the bot before it started clicking on the next points)
