from src.map import ReadMapFile
from src.gamedata import GameData
from src.objects import *
import pygame



hiekkakuva = pygame.image.load("media/hiekka.png")
ukkeli = pygame.image.load("media/ukkeli.png")

local_player = Player(ukkeli)

local_data = GameData(local_player)

print(ReadMapFile(local_data,"testmap.txt"))