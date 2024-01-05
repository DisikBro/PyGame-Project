import csv

import pygame



def load_level(filename):
    filename = "map/" + filename
    with open(filename, encoding="utf8") as mapFile:
        level_map = list(csv.reader(mapFile, delimiter=',', quotechar='"'))
    return level_map


layer = load_level('karta._Слой тайлов 1.csv')
print(layer)
print(layer[9][10])