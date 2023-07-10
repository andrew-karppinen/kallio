import pygame
import json
from src import *

class GameData:
    '''
    game data
    '''


    def __init__(self,multiplayer:bool = False,server:bool = False):


        self.screen_ = None #pygame window
        self.font_ = self.font_ = pygame.font.SysFont('', 30) #load font
        self.tile_size_ = 50 #tilesize y*x
        self.draw_area_x_ = 32 #default drawing area size
        self.draw_area_y_ = 18

        self.margin_x_ = 0
        self.margin_y_ = 0


        self.multiplayer_ = multiplayer
        self.server_ = server #False = client, True = server

        self.local_player_position_x_ = None
        self.local_player_position_y_ = None

        # create players
        self.local_player_ = Player()
        self.remote_player_ = Player(False)



        self.required_score_ = 0
        self.points_collected_ = 0 #local player Points collected
        self.total_points_collected_ = 0
        self.level_complete_ = False

        self.collision_objects_ = [Player,Stone,Tnt,Bedrock,Brick,Door]
        self.pushing_objects_ = [Stone, Tnt]
        self.gravity_objects_ = [Stone,Tnt,Diamond]
        self.gravity_objects_2_ = [Brick,Stone,Diamond]  #a stone and diamond will not stay on top of these if there is an empty one next to it
        self.explosive_ = [Tnt,Monster] #causing new explosion if explose
        self.explosive2_ = [Tnt,Player,Monster] #explosive if something falls on it
        self.deadlys_objects_ = [Explosion,Monster] #if the player moved to these tiles, it's game over

        self.pushing_right_ = 0 #0,1
        self.pushing_left_ = 0 #0,1

        self.map_width_ = 0 #x
        self.map_height_ = 0 #y

        #read configs from json file
        f = open("src/config/tile commands config.json", "r")  # read json file
        self.mapsymbols_ = json.load(f)["commands"]  # read mapsymbols
        f.close()  # close file

        #map data
        self.original_mapstr_ = ""
        self.previous_map_ = []
        self.current_map_ = []


        self.menudata_ = None

        self.SetImages() #set tile images






    def SetImages(self):
        # load images and set tile images
        sandimage = pygame.image.load("media/sand.png")
        playerimage = pygame.image.load("media/player.png")
        playerimage2 = pygame.image.load("media/player2.png")
        playerimage3 = pygame.image.load("media/player3.png")
        monsterimage1 = pygame.image.load("media/monster1.png")
        monsterimage2 = pygame.image.load("media/monster2.png")
        stoneimage = pygame.image.load("media/stone.png")
        tntimage = pygame.image.load("media/tnt.png")
        explosionimage = pygame.image.load("media/explosion.png")
        diamondimage = pygame.image.load("media/diamond.png")
        goalimage = pygame.image.load("media/goal.png")
        bedrockimage = pygame.image.load("media/bedrock.png")
        brickimage = pygame.image.load("media/brick.png")

        door_right_image = pygame.image.load("media/door right.png")
        door_down_image = pygame.image.load("media/door down.png")
        door_up_image = pygame.image.load("media/door up.png")
        door_left_image = pygame.image.load("media/door left.png")

        # set images
        Diamond.SetImage(diamondimage)
        Goal.SetImage(goalimage)
        Explosion.SetImage(explosionimage)
        Tnt.SetImage(tntimage)
        DefaultTile.SetImage(sandimage)
        Bedrock.SetImage(bedrockimage)
        Brick.SetImage(brickimage)
        Monster.SetImage(monsterimage1,monsterimage2)

        # set images
        Stone.SetImage(stoneimage)
        Door.SetImage(door_right_image, door_down_image, door_left_image, door_up_image)



        # set players images
        self.local_player_.SetImage(playerimage, playerimage2, playerimage3)
        self.remote_player_.SetImage(playerimage, playerimage2, playerimage3)


    def SetDrawarea(self,draw_area_x:int = 32,draw_area_y = 18):

        self.draw_area_x_ = draw_area_x #set draw area
        self.draw_area_y_ = draw_area_y


        if self.map_width_ < self.draw_area_x_: #if map size < drawing area size
            self.draw_area_x_ = self.map_width_ #set drawing area size to map size
            x, y = self.screen_.get_size()
            margin_x = self.map_width_ * self.tile_size_
            margin_x = x // 2 - margin_x // 2
            self.margin_x_ = margin_x


        if self.map_height_ < self.draw_area_y_: #if map size < drawing area size
            self.draw_area_y_ = self.map_height_ #set drawing area size to map size
            x, y = self.screen_.get_size()
            margin_y = self.map_height_ * self.tile_size_
            margin_y = y // 2 - margin_y //2
            self.margin_y_ = margin_y


    def SetScreenSize(self,resolution:tuple):

        '''
        sets screen size and scales images
        return True/False if resize succesful or unsuccesful
        '''


        width = resolution[0]
        height = resolution[1]

        tile_size = height // self.draw_area_y_

        if width % tile_size != 0:
            raise Exception("invalid screen size")

        else:
            self.tile_size_ = tile_size
            self.screen_ = pygame.display.set_mode((width, height))  #update screen size

            #scale tile images
            for i in [Goal,Diamond,Tnt,Stone,Door,DefaultTile,Explosion,Brick,Bedrock,Monster]:
                i.ScaleImages(tile_size)

            #scale player image size
            self.local_player_.ScaleImages(tile_size)
            if self.remote_player_ != None: #if remoteplayer exist
                self.remote_player_.ScaleImages(tile_size)

            if self.server_:
                name = "server"
            else:
                name = "client"

            pygame.display.set_caption(name) #name window
            return(True)

    def DrawMap(self):
        #draw current map
        #camera follow player


        #Drawing area:
        #x = 32
        #y = 18

        y = -1



        left = self.local_player_position_x_ - self.draw_area_x_ // 2
        right = self.local_player_position_x_+ self.draw_area_x_ // 2


        #move draw area
        while True:
            if left < 0:
                left += 1
                right += 1

            elif right > self.map_width_:
                right -= 1
                left -= 1

            else:
                break



        up = self.local_player_position_y_ - self.draw_area_y_ // 2
        down = self.local_player_position_y_ + self.draw_area_y_ //2

        #move draw area
        while True:
            if up < 0:
                up += 1
                down += 1
            elif down > self.map_height_:
                down -= 1
                up -= 1
            else:
                break



        #draw map
        for i in range(up,down): #y
            x = -1
            y += 1
            for j in range(left,right): #x

                x += 1


                if i >= 0 and j >= 0: #if map not end
                    if i < self.map_height_ and j < self.map_width_: #if map not end

                        if self.current_map_[i][j] == None: #if empty
                            pass
                        else:
                            self.screen_.blit(self.current_map_[i][j].image_, (x * self.tile_size_ + self.margin_x_, y * self.tile_size_ + self.margin_y_)) #draw tiles





