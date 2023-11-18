import pygame
import os

from src import *


class GameData:
    '''
    game data
    '''

    def __init__(self,multiplayer:bool = False,server:bool = False,font_file_path:str="",sfx_is_on:bool=True):


        #window data:
        self.screen_ = None #pygame window

        if font_file_path != "": #if the path to the font file is given
            self.font_ = self.font_ = pygame.font.Font(font_file_path,30) #load font from file, font size 30
            self.big_size_font_ = pygame.font.Font(font_file_path,60) #load font from file, font size 60
        else: #file path is not given, load default sysfont
            self.font_ = pygame.font.SysFont("", 30)  # load sysfont
            self.big_size_font_ = pygame.font.SysFont("", 60)  # load sysfont



        self.tile_size_ = 50 #tilesize y*x
        self.draw_area_x_ = 32 #drawing area size
        self.draw_area_y_ = 16

        self.margin_x_ = 0
        self.margin_y_ = 0

        self.infopanel_height_ = 100

        #create infopanel texts:
        self.infopanel_text_score_ = self.font_.render("Score:",True,(255,255,255))
        self.infopanel_text_needed_ = self.font_.render("Needed:", True, (255, 255, 255))
        self.infopanel_text_time_ = self.font_.render("Time:",True,(255,255,255))


        #gamedata:
        self.multiplayer_ = multiplayer
        self.server_ = server #False = client, True = server

        self.remote_player_position_x_ = None
        self.remote_player_position_y_ = None

        self.local_player_position_x_ = None
        self.local_player_position_y_ = None

        # create players
        self.local_player_ = Player()
        self.remote_player_ = Player(False)


        self.points_collected_ = 0 #points collected by local player
        self.total_points_collected_ = 0 #points collected by local and remote player

        self.local_player_in_goal_ = False #the local player in goal
        self.remote_player_in_goal_ = False #remote player in goal





        self.collision_objects_ = [Player,Stone,Tnt,Bedrock,Brick,Door]
        self.pushing_objects_ = [Stone, Tnt]
        self.gravity_objects_ = [Stone,Tnt,Diamond]
        self.gravity_objects_2_ = [Brick,Stone,Diamond]  #a stone and diamond will not stay on top of these if there is an empty one next to it
        self.explosive_ = [Tnt,Monster] #causing new explosion if explose
        self.explosive2_ = [Tnt,Monster] #explosive if something falls on it
        self.deadlys_objects_ = [Explosion,Monster] #if the player moved to these tiles, it's game over

        self.pushing_right_ = 0 #0,1
        self.pushing_left_ = 0 #0,1

        #level data:
        self.level_timelimit_ = 0 #timelimit in seconds
        self.required_score_ = 0

        self.map_width_ = 0 #x
        self.map_height_ = 0 #y


        #map data
        self.original_mapstr_ = ""
        self.previous_map_ = []
        self.current_map_ = []



        self.SetImages() #set tile images

        #display / map draw data
        self.camera_up_ = 0
        self.camera_left_ = 0
        self.update_camera_ = 0


        self.audio_ = Audio(sfx_is_on) #crate Audio object


        #private variables:
        self.__elapsed_time_ = 0



    def SetImages(self):



        #read tile image paths from json file
        f = open("media/tile images config.json", "r")  # read json file
        json_data = json.load(f)  # read data
        f.close()  # close file

        player_images = json_data["player images"]
        tile_images = json_data["other tile images"]

        #load tile images:
        sandimage = pygame.image.load("media/sand.png")

        player1image1 = pygame.image.load(player_images["player1"][0])
        player1image2 = pygame.image.load(player_images["player1"][1])
        player1image3 = pygame.image.load(player_images["player1"][2])

        player2image1 = pygame.image.load(player_images["player2"][0])
        player2image2 = pygame.image.load(player_images["player2"][1])
        player2image3 = pygame.image.load(player_images["player2"][2])

        monsterimage1 = pygame.image.load(tile_images["Monster"][0])
        monsterimage2 = pygame.image.load(tile_images["Monster"][1])
        stoneimage = pygame.image.load(tile_images["Stone"][0])
        tntimage = pygame.image.load(tile_images["Tnt"][0])

        explosionimage1 = pygame.image.load(tile_images["Explosion"][0])
        explosionimage2 = pygame.image.load(tile_images["Explosion"][1])
        explosionimage3 = pygame.image.load(tile_images["Explosion"][2])
        explosionimage4 = pygame.image.load(tile_images["Explosion"][3])

        diamondimage = pygame.image.load(tile_images["Diamond"][0])

        goal_open_image = pygame.image.load(tile_images["Goal"][0])
        goal_close_image = pygame.image.load(tile_images["Goal"][1])

        bedrockimage = pygame.image.load(tile_images["Bedrock"][0])
        brickimage = pygame.image.load(tile_images["Brick"][0])

        door_right_image = pygame.image.load(tile_images["Door"][0])
        door_down_image = pygame.image.load(tile_images["Door"][1])
        door_left_image = pygame.image.load(tile_images["Door"][2])
        door_up_image = pygame.image.load(tile_images["Door"][3])

        #set images to classes:
        Diamond.SetImage(diamondimage)
        Goal.SetImage(goal_open_image,goal_close_image)
        Explosion.SetImage(explosionimage1,explosionimage2,explosionimage3,explosionimage4)
        Tnt.SetImage(tntimage)
        DefaultTile.SetImage(sandimage)
        Bedrock.SetImage(bedrockimage)
        Brick.SetImage(brickimage)
        Monster.SetImage(monsterimage1,monsterimage2)

        #set images:
        Stone.SetImage(stoneimage)
        Door.SetImage(door_right_image, door_down_image, door_left_image, door_up_image)


        #set players images
        if self.multiplayer_ == True:
            if self.server_ == True: #if server
                self.local_player_.SetImage(player1image1, player1image2, player1image3)
                self.remote_player_.SetImage(player2image1, player2image2, player2image3)

            else: #if client
                self.local_player_.SetImage(player2image1, player2image2, player2image3)
                self.remote_player_.SetImage(player1image1, player1image2, player1image3)

        else: #if singleplayer
            self.local_player_.SetImage(player1image1, player1image2, player1image3)
            self.remote_player_.SetImage(player2image1, player2image2, player2image3)

    def InitTimer(self):
        self.__elapsed_time_ = pygame.time.get_ticks() //1000


    def Timer(self)->int:
        '''
        get game elapsed time in seconds
        '''

        return pygame.time.get_ticks() //1000 - self.__elapsed_time_ #calculate elapsed time and return it




    def InitDisplay(self,screen:pygame.display):
        '''
        set pygame display to gamedata object

        diplay aspect ratio must be 16:9 !!!

        calculate tile size,
        scale tiles images

        example resolution: 1280x720

        #drawing area:
        x = 32
        y = 16
        '''


        self.screen_width_,self.screen_height_ = screen.get_size() #get display size

        self.screen_ = screen #set screen to self object


        if self.draw_area_y_ > self.map_height_: #if map height < draw Area y
            self.draw_area_y_ = self.map_height_ #set draw area si<e to map size


        if self.draw_area_x_ > self.map_width_: #if map width < draw Area x
            self.draw_area_x_ = self.map_width_ #set draw area si<e to map size




        self.tile_size_ = (self.screen_height_ - self.infopanel_height_) // self.draw_area_y_ #calculate tile size


        while self.tile_size_ * self.draw_area_x_ > self.screen_width_: #if the width of the drawing area is greater than the width of the screen
            self.tile_size_ -= 1 #reduce the size of the tile



        #if the width of the drawing area is less than the width of the screen:

        if self.draw_area_x_*self.tile_size_ < self.screen_width_: #margin required in x direction
            self.margin_x_ = abs(self.draw_area_x_*self.tile_size_ - self.screen_width_) //2 #calculate margin x

        if self.draw_area_y_ *self.tile_size_ < self.screen_height_-self.infopanel_height_: #margin required in y direction
            self.margin_y_ = abs(self.draw_area_y_*self.tile_size_ -(self.screen_height_ - self.infopanel_height_))//2 #calculate margin y




        #scale tile images:
        for i in [Goal, Diamond, Tnt, Stone, Door, DefaultTile, Explosion, Brick, Bedrock, Monster]:
            i.ScaleImages(self.tile_size_)

        #scale player image size
        self.local_player_.ScaleImages(self.tile_size_)
        if self.remote_player_ != None:  # if remoteplayer exist
            self.remote_player_.ScaleImages(self.tile_size_)


        #create infopanel texts:
        self.infopanel_text_level_required_score_ = self.font_.render(str(self.required_score_),True,(255,255,255))


        #rename window:
        if self.multiplayer_ == True:
            if self.server_ == True:
                pygame.display.set_caption('server')
            else:
                pygame.display.set_caption('client')
        else:
            pygame.display.set_caption('singleplayer')






        #calculate pause menu texts positions

        #get text size
        self.head_text_size_x_ = self.font_.render('Pause Menu', True, (255, 255, 255)).get_width()

        self.text_1_size_x_ = self.font_.render('Resume game', True, (0, 0, 0)).get_width()
        self.text_1_size_y_ = self.font_.render('Resume game', True, (0, 0, 0)).get_height()

        self.text_2_size_x_ = self.font_.render('Restart level', True, (0, 0, 0)).get_width()
        self.text_2_size_y_ = self.font_.render('Restart level', True, (0, 0, 0)).get_height()

        self.text_3_size_x_ = self.font_.render('Exit level', True, (0, 0, 0)).get_width()
        self.text_3_size_y_ = self.font_.render('Exit level', True, (0, 0, 0)).get_height()


        x, y = self.screen_.get_size() #get window size


        #calculate the text position
        self.text1_position_x_ = x // 2
        self.text1_position_x_ -= self.text_1_size_x_ // 2
        self.text1_position_y_ = y // 2

        self.text2_position_x_ = x // 2
        self.text2_position_x_ -= self.text_2_size_x_ // 2
        self.text2_position_y_ = y // 2 - 50

        self.text3_position_x_ = x // 2
        self.text3_position_x_ -= self.text_3_size_x_ // 2
        self.text3_position_y_ = y // 2 - 100

        self.head_text_position_x_ = x // 2
        self.head_text_position_x_ -= self.head_text_size_x_ // 2
        self.head_text_position_y_ = y // 2 - 190



    def GetPauseMenuButtonNumber(self, mouse_position:tuple):
        '''
        returns the pause menu button number of that the mouse touches
        if the mouse is not touching anything, return None
        '''


        if mouse_position[0] >= self.text1_position_x_ and mouse_position[0] <= self.text1_position_x_ + self.text_1_size_x_:
            if mouse_position[1] >= self.text1_position_y_ and mouse_position[1] <= self.text1_position_y_ + self.text_1_size_y_:
                return 1

        if mouse_position[0] >= self.text2_position_x_ and mouse_position[0] <= self.text2_position_x_ + self.text_2_size_x_:
            if mouse_position[1] >= self.text2_position_y_ and mouse_position[1] <= self.text2_position_y_ + self.text_2_size_y_:
                return 2

        if mouse_position[0] >= self.text3_position_x_ and mouse_position[0] <= self.text3_position_x_ + self.text_3_size_x_:
            if mouse_position[1] >= self.text3_position_y_ and mouse_position[1] <= self.text3_position_y_ + self.text_3_size_y_:
                return 3




    def UpdateCameraHorizontal(self):
        #centre the player horizontal in the middle of the screen
        self.camera_up_ = self.local_player_position_y_ - self.draw_area_y_ // 2


    def UpdateCameraVerticaly(self):
        #centre the player vertically in the middle of the screen
        self.camera_left_ = self.local_player_position_x_ - self.draw_area_x_ // 2


    def DrawMap(self):
        #draw current map
        #camera follow player
        #Drawing area:
        #x = 32
        #y = 16



        #if player are on the edge of the drawing area update the camera:
        if self.camera_left_ >= self.local_player_position_x_-3:
            self.UpdateCameraVerticaly()

        if self.camera_left_+self.draw_area_x_ <= self.local_player_position_x_+3:
            self.UpdateCameraVerticaly()


        if self.camera_up_ >= self.local_player_position_y_-3:
            self.UpdateCameraHorizontal()

        if self.camera_up_ +self.draw_area_y_ <= self.local_player_position_y_+3:
            self.UpdateCameraHorizontal()



        #calculate drawing area from map:
        if self.draw_area_x_ < self.map_width_: #only if draw area x < map width
            left = self.camera_left_
            right = left + self.draw_area_x_
            while True: #move draw area x
                if left < 0:
                    left += 1
                    right += 1

                elif right > self.map_width_:
                    right -= 1
                    left -= 1

                else:
                    break
        else:#draw the whole map vertically
            left = 0
            right = self.map_width_




        if self.draw_area_y_ < self.map_height_: #only if draw area y < map height
            up = self.camera_up_
            down = up + self.draw_area_y_

            while True: #move draw area x
                if up < 0:
                    up += 1
                    down += 1
                elif down > self.map_height_:
                    down -= 1
                    up -= 1
                else:
                    break
        else: #draw the whole map horizontally
            up = 0
            down = self.map_height_







        y = -1
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
                            if not self.current_map_[i][j].movement_going_: #normal tile drawing
                                self.screen_.blit(self.current_map_[i][j].image_, (x * self.tile_size_ + self.margin_x_,y * self.tile_size_ +self.margin_y_)) #draw tiles to surface



                            else:

                                if self.current_map_[i][j].movement_going_left_: #animate tile left
                                    self.screen_.blit(self.current_map_[i][j].image_, ((x+1) * self.tile_size_ + self.margin_x_-self.current_map_[i][j].moved_, y * self.tile_size_ + self.margin_y_)) #draw tiles


                                elif self.current_map_[i][j].movement_going_right_: #animate tile right
                                    self.screen_.blit(self.current_map_[i][j].image_, ((x-1) * self.tile_size_ + self.margin_x_+self.current_map_[i][j].moved_, y * self.tile_size_ + self.margin_y_)) #draw tiles


                                elif self.current_map_[i][j].movement_going_up_: #animate tile up
                                    self.screen_.blit(self.current_map_[i][j].image_, (x * self.tile_size_ + self.margin_x_, (y+1) * self.tile_size_ + self.margin_y_-self.current_map_[i][j].moved_)) #draw tiles



                                elif self.current_map_[i][j].movement_going_down_: #animate tile down
                                    self.screen_.blit(self.current_map_[i][j].image_, (x * self.tile_size_ + self.margin_x_, (y-1) * self.tile_size_ + self.margin_y_+self.current_map_[i][j].moved_)) #draw tiles




                                '''
                                the tile is moved 3 times 1/3 the size of the tile
                                '''

                                if self.current_map_[i][j].moved_counter_ > 2:
                                    self.current_map_[i][j].StopMovementAnimation() #init movement variables
                                else:
                                    self.current_map_[i][j].moved_ += self.tile_size_ / 3
                                    self.current_map_[i][j].moved_counter_ += 1


    def DrawInfoPanel(self):

        #draw info panel:
        screen_size = self.screen_.get_size()
        pygame.draw.rect(self.screen_, (50,50,50), pygame.Rect(0, screen_size[1]-self.infopanel_height_, screen_size[0],self.infopanel_height_))

        #create variable texts:
        time_remaining_text = self.font_.render(str(self.level_timelimit_ - self.Timer()), True, (255, 255, 255)) #calculate remaining time
        points_collected_text = self.font_.render(str(self.total_points_collected_),True,(255,255,255)) #collected points



        #draw texts to infopanel:
        self.screen_.blit(self.infopanel_text_time_,(self.screen_width_//4,self.screen_height_-70)) #draw text to screen
        if self.level_timelimit_ != 0: #if level has timelimit
            self.screen_.blit(time_remaining_text,(self.screen_width_//4+self.infopanel_text_time_.get_width()+20,self.screen_height_-70)) #draw text to screen


        self.screen_.blit(self.infopanel_text_score_,(self.screen_width_//2,self.screen_height_-70))
        self.screen_.blit(points_collected_text,(self.screen_width_//2 + self.infopanel_text_score_.get_width()+20 ,self.screen_height_-70)) #draw text to screen


        self.screen_.blit(self.infopanel_text_needed_, (self.screen_width_ - self.screen_width_ // 4, self.screen_height_ - 70)) #draw text to screen
        self.screen_.blit(self.infopanel_text_level_required_score_,(self.screen_width_ - self.screen_width_ // 4 + self.infopanel_text_needed_.get_width() + 20, self.screen_height_ - 70)) #draw text to screen
