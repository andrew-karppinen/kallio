
import pygame


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


        self.map_width_ = 0 #x
        self.map_height_ = 0 #y

        self.previous_map_ = []
        self.current_map_ = []



    def DrawMap(self):
        #draw current map
        #first version
        self.screen_.fill((0, 0, 0))  #asetetaan taustan väriksi musta
        for y in range(self.map_height_):
            for x in range(self.map_width_):

                if self.current_map_[y][x] == None: #if empty
                    pass
                else:
                    self.screen_.blit(self.current_map_[y][x].image_,(x*self.tile_size_,y*self.tile_size_))


        pygame.display.flip()