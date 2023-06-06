
import pygame
from src import *

class GameData:
    '''
    game data
    '''


    def __init__(self,local_player:object,multiplayer:bool = False,server:bool = False,remote_player:object = None,screen:pygame.surface = None):


        self.screen_ = screen #pygame window
        self.tile_size_ = 50 #tilesize y*x
        self.draw_area_x_ = 32 #default drawing area size
        self.draw_area_y_ = 18

        self.margin_x = 0
        self.margin_y = 0


        self.multiplayer_ = multiplayer
        self.server_ = server #False = client, True = server
        self.local_player_ = local_player

        self.local_player_position_x_= None
        self.local_player_position_y_ = None


        self.remote_player_ = remote_player



        self.required_score_ = 0
        self.points_collected_ = 0 #local player Points collected
        self.total_points_collected_ = 0

        self.collision_objects_ = [Player,Stone,Tnt,Bedrock,Brick,Door]
        self.pushing_objects_ = [Stone, Tnt]
        self.gravity_objects_ = [Stone,Tnt,Diamond]
        self.gravity_objects_2_ = [Brick,Stone,Diamond]  #a stone and diamond will not stay on top of these if there is an empty one next to it
        self.explosive_ = [Tnt,Monster,Player] #causing new explosion if explose


        self.pushing_right_ = 0
        self.pushing_left_ = 0

        self.map_width_ = 0 #x
        self.map_height_ = 0 #y

        self.original_mapstr_ = ""

        self.previous_map_ = []
        self.current_map_ = []


        self.menudata_ = None


    def SetDrawarea(self,draw_area_x:int = 32,draw_area_y = 18):

        self.draw_area_x_ = draw_area_x #set draw area
        self.draw_area_y_ = draw_area_y


        if self.map_width_ < self.draw_area_x_: #if map size < drawing area size
            self.draw_area_x_ = self.map_width_ #set drawing area size to map size

            x, y = self.screen_.get_size()
            margin_x = self.map_width_ * self.tile_size_
            margin_x = x //2 - margin_x //2
            self.margin_x = margin_x


        if self.map_height_ < self.draw_area_y_: #if map size < drawing area size
            self.draw_area_y_ = self.map_height_ #set drawing area size to map size

            x, y = self.screen_.get_size()
            margin_y = self.map_height_ * self.tile_size_
            margin_y = y // 2 - margin_y //2
            self.margin_y = margin_y



    def ReturnResolutions(self):

        x = 16
        y = 9
        resolutions = []

        for i in range(200):
            if x % self.draw_area_x_ == 0:
                if y % self.draw_area_y_ == 0:
                    resolutions.append((x,y))
            y += 9
            x += 16


        return(resolutions)

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
            for i in [Goal,Diamond,Tnt,Stone,Door,DefaultTile,Explosion,Brick,Bedrock]:
                i.SetImage(pygame.transform.scale(i.image,(tile_size,tile_size)))

            #scale player image size
            self.local_player_.image_ = pygame.transform.scale(self.local_player_.image_,(tile_size,tile_size))
            if self.remote_player_ != None:
                self.remote_player_.image_ = pygame.transform.scale(self.remote_player_.image_,(tile_size,tile_size))

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
        self.screen_.fill((0, 0, 0))  #set backcolor




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
                            self.screen_.blit(self.current_map_[i][j].image_,(x*self.tile_size_+self.margin_x,y*self.tile_size_+self.margin_y)) #draw tiles





        pygame.display.flip() #update screen