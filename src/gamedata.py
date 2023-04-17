
import pygame
from src import *

class GameData:
    '''
    game data
    '''


    def __init__(self,local_player:object,multiplayer:bool = False,remote_player:object = None,screen:pygame.surface = None):


        self.screen_ = screen #pygame window

        self.multiplayer_ = multiplayer
        self.server_ = False #False = client, True = server
        self.local_player_ = local_player


        self.remote_player_ = remote_player
        self.tile_size_ = 50 #tilesize y*x

        self.required_score_ = 0
        self.collision_objects_ = [Player,Stone,Tnt]
        self.pushing_objects_ = [Stone, Tnt]
        self.gravity_objects_ = [Stone,Tnt]

        self.pushing_right_ = 0
        self.pushing_left_ = 0

        self.map_width_ = 0 #x
        self.map_height_ = 0 #y

        self.previous_map_ = []
        self.current_map_ = []



    def DrawMap(self):
        #draw current map
        #camera follow player test
        y = -1
        self.screen_.fill((0, 0, 0))  #set backcolor



        left = self.local_player_.position_x_ - 13
        right = self.local_player_.position_x_+ 12

        #set drawing area
        while True:
            if left < 0:
                left += 1
                right += 1

            elif right > self.map_width_:
                right -= 1
                left -= 1

            else:
                break

        up = self.local_player_.position_y_ - 8
        down = self.local_player_.position_y_+9

        #set drawing area
        while True:
            if up < 0:
                up += 1
                down += 1
            elif down > self.map_height_:
                down -= 1
                up -= 1
            else:
                break



        #draw tiles
        for i in range(up,down):
            x = -1
            y += 1
            for j in range(left,right):

                x += 1


                if i >= 0 and j >= 0: #if map not end
                    if i < self.map_height_ and j < self.map_width_: #if map not end

                        if self.current_map_[i][j] == None: #if empty
                            pass
                        else:
                            self.screen_.blit(self.current_map_[i][j].image_,(x*self.tile_size_,y*self.tile_size_))







        pygame.display.flip() #update screen