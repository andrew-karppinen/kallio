from src.map import *
from src.gamedata import GameData
from src.objects import *
import pygame


naytto = pygame.display.set_mode((800, 800)) #create window


#initialize
hiekkakuva = pygame.image.load("media/hiekka.png")
ukkeli = pygame.image.load("media/ukkeli.png")
kivikuva = pygame.image.load("media/kivi.png")

DefaultTile.image = hiekkakuva
Brick.image = kivikuva


local_player = Player(ukkeli)
data = GameData(local_player,screen=naytto) #create game data

mapstr,data.map_height_,data.map_width_ = ReadMapFile("testmap.txt")

data.current_map_ = SetMap(data,mapstr,data.map_height_,data.map_width_)




while True:

    data.DrawMap()

