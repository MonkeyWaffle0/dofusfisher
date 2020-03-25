import pickle


with open("map.pickle", "rb") as file:
    map = pickle.load(file)

print(map)
for x in map:
    print(x)