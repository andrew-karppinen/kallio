import pygame
import pygame_menu
import random
from src import * #import py-boulderdash
import os



pygame.init() #init pygame module


def ReturnMaps(multiplayer:bool):
    '''
    return map file path

    return files from:

     /maps/sigleplayer
     or
    /maps/multiplayer

    '''

    path = os.getcwd()
    maplist = []

    if multiplayer == True: #multiplayer maps
        path += "/maps/multiplayer"
        for i in os.listdir(path):
            maplist.append((str(i), f"maps/multiplayer/{i}"))


    elif multiplayer == False: #signleplayer maps
        path += "/maps/singleplayer"
        for i in os.listdir(path):
            maplist.append((str(i), f"maps/singleplayer/{i}"))



    return (maplist)  # return maps



class Menu:


    def __init__(self) -> None: #constructor

        #MENUDATA
        self.screen_ =  pygame.display.set_mode((1600, 900)) #create screen

        # create menu theme
        font8bit = pygame_menu.font.FONT_8BIT
        font = pygame_menu.font.FONT_FRANCHISE
        self.menu_theme_ = pygame_menu.Theme(background_color=(0, 0, 0), title_background_color=(178, 29, 29),
                                    widget_font_color=(255, 255, 255), widget_padding=6, widget_font_size=38,
                                    title_font=font, title_font_size=65)


        self.menu_ = pygame_menu.Menu('py boulderdash', 600, 500,surface=self.screen_, theme=self.menu_theme_)  #create pygame_menu object

        self.level_complete_ = False

        self.resolutions_ = [('1600x900',(1600,900)),('1920x1080',(1920,1080)),('1056x594',(1056,594)),('1280x720', (1280,720))] #resolutions list


        #settings temp variables:
        self.temp_resolution_ = 0
        self.temp_resolution_index_ = 0
        self.temp_fullscreen_ = False


        #GAME START DATA
        self.server_ip_ = "localhost"  #client
        self.port_ = 1234 #client and server default port
        self.join_id_ = "" #server or client
        self.timeout_ = 10 #server, socket timeout
        self.map_file_path_ = ""  #mapfile path  #if server or singleplayer


        #current resolution:
        self.resolution_ = (1600,900)
        self.resolution_index_ = 0
        self.fullscreen_ = False



    def SetIpaddress(self, ip: str):
        self.server_ip_ = ip


    def SetPort(self,port):
        try:
            self.port_ = int(port)
        except:
            pass
    def SetJoinid(self, id:str = ""):

        if id == "": #if id is no given
            self.join_id_ = ""
            for i in range(5): #generate random join id
                self.join_id_ += str(random.randint(0, 9))
        else:
            self.join_id_ = id


    def SetTimeout(self,timeout):
        try:
            self.timeout_ = int(timeout)
        except:
            pass




    def SetMapFilepath(self,useless_argument,path:str):
        self.map_file_path_ = path




    def ServerMenu(self):

        def StartServer(self):
            gamedata = GameData(True,True)  # create gamedata
            gamedata.server_ = True
            mapstr, gamedata.map_height_, gamedata.map_width_,map_is_multiplayer, gamedata.required_score_, gamedata.level_timelimit_ = ReadMapFile(self.map_file_path_)  # read map file


            connection = Server(self.port_,self.timeout_) #create connection object

            if connection.connected_: #if someone connected

                connection.Read()  # read messages
                if connection.data_type_ == "readytostart":  # if client ready to start the game
                    if connection.data_ == self.join_id_:
                        connection.BufferNext() #delete first message from buffer
                        connection.SendStartInfo(gamedata.map_height_, gamedata.map_width_, gamedata.required_score_, gamedata.level_timelimit_)  # send start info


                        connection.SendMap(mapstr)  #and send map to client
                        SetMap(gamedata, mapstr, True)  # set map(local) convert str to map list

                        gamedata.InitDisplay(self.screen_)  # set window to gamedata object

                        connection.SetTimeout(0.001) #set new timeout
                        self.level_complete_ =  Run(gamedata, connection) #start game
                        self.BackToMenu()


            #if the connection failed
            self.menu_.clear()
            self.menu_.add.label(connection.error_mesage_)
            self.menu_.add.label(f"server ip:{socket.gethostbyname(socket.gethostname())}")  # print ip address
            self.menu_.add.label(f"join nubmer: {self.join_id_}") #print gameid
            self.menu_.add.label(f"port: {connection.port_}")  # print port
            self.menu_.add.button("try again",StartServer,self)
            self.menu_.add.button("back to main menu",self.MainMenu)



        self.menu_.clear() #clear menu
        if self.join_id_ == "": #if join id is not exist
            self.SetJoinid() #generate random join id

        self.menu_.add.label(f"your ip address:")
        self.menu_.add.label(socket.gethostbyname(socket.gethostname()))  # print ip address
        self.menu_.add.selector("map:", ReturnMaps(True), onchange=self.SetMapFilepath,default=1) #select map
        self.menu_.add.text_input('port:', default=f"{str(self.port_)}",onchange=self.SetPort)  #set port
        self.menu_.add.text_input('join number:', default= self.join_id_, onchange=self.SetJoinid) #set join id
        self.menu_.add.text_input('timeout:', default="10", onchange=self.SetTimeout) #set socket timeout
        self.menu_.add.button("start server", StartServer,self)
        self.menu_.add.button("back", self.MainMenu)



    def ClientMenu(self):
        def StartClient(self):
            #try connect to server

            gamedata = GameData(True,False) #create gamedata
            connection = Client(self.server_ip_, self.port_)  #create connection object

            if connection.connected_: #if the connection was successful
                connection.SendReadyToStart(self.join_id_)
                connection.Read()  # read messages
                if connection.data_type_ == "startinfo":  #if start info

                    gamedata.map_height_, gamedata.map_width_,gamedata.required_score_,gamedata.level_timelimit_ = connection.data_ #set map size, required_score and level timelimit
                    connection.BufferNext()  #delete first message from buffer

                    connection.Read()  # read messages
                    if connection.data_type_ == "map":  #if message is map
                        SetMap(gamedata, connection.data_,True)  #set map
                        connection.BufferNext() #delete first message from buffer

                        gamedata.InitDisplay(self.screen_)  # set window to gamedata object

                        connection.SetTimeout(0.001) #set new timeout
                        self.level_complete_ = Run(gamedata, connection)  # start game
                        self.BackToMenu()



            #if the connection failed
            self.menu_.clear()
            self.menu_.add.label(connection.error_mesage_)
            self.menu_.add.button("try again",StartClient,self)
            self.menu_.add.button("back to main menu",self.MainMenu)



        self.menu_.clear()
        self.menu_.add.text_input('server ip:', default=self.server_ip_, onchange=self.SetIpaddress) #set server ip
        self.menu_.add.text_input('port:', default='1234', onchange=self.SetPort) #set port
        self.menu_.add.text_input('Join number:', default=self.join_id_, onchange=self.SetJoinid) #set join id
        self.menu_.add.button("Connect",StartClient,self)
        self.menu_.add.button("Back", self.MainMenu)


    def SinglePlayerMenu(self):

        def StartSingleplayer(self):
            gamedata = GameData(False,False)  # create gamedata



            mapstr, gamedata.map_height_, gamedata.map_width_,map_is_multiplayer, gamedata.required_score_, gamedata.level_timelimit_ = ReadMapFile(self.map_file_path_)  # read map file
            SetMap(gamedata, mapstr,True)  # convert str to map list

            gamedata.InitDisplay(self.screen_)  #set window to gamedata object

            self.level_complete_ = Run(gamedata) #start game
            self.BackToMenu()



        self.menu_.clear()
        self.menu_.add.button("Play",StartSingleplayer,self)
        self.menu_.add.selector("map:", ReturnMaps(False), onchange=self.SetMapFilepath,default=1) #map select
        self.menu_.add.button("Back",self.MainMenu)




    def SettingsMenu(self):


        self.temp_fullscreen_ = self.fullscreen_
        self.temp_resolution_ = self.resolution_
        self.temp_resolution_index_ = self.resolution_index_

        def SetTempResolution(index:int,resolution:tuple):
            self.temp_resolution_index_ = index[1]
            self.temp_resolution_ = resolution

        def SetTempFullscreen(fullscreen:bool):
            self.temp_fullscreen_ = fullscreen

        def ApplySettings():
            #set temp variables to object
            self.resolution_ = self.temp_resolution_
            self.resolution_index_ = self.temp_resolution_index_
            self.fullscreen_ =  self.temp_fullscreen_


            #update window
            if self.fullscreen_ == True:
                self.screen_ = pygame.display.set_mode(self.resolution_,pygame.FULLSCREEN) #crete fullscreen window
            else:
                self.screen_ = pygame.display.set_mode(self.resolution_,pygame.WINDOWMOVED) #create noremal window

            # update menu object:
            self.menu_ = pygame_menu.Menu('py boulderdash', 600, 500, surface=self.screen_,theme=self.menu_theme_)  # create menu object

            self.MainMenu() #back to mainmenu

        self.menu_.clear()
        self.menu_.add.toggle_switch("full screen",onchange=SetTempFullscreen,default=self.temp_fullscreen_) #change window mode
        self.menu_.add.selector('Screen size:', self.resolutions_,default = self.temp_resolution_index_, onchange=SetTempResolution) #change resolution
        self.menu_.add.button("Apply",action=ApplySettings)
        self.menu_.add.button("back",self.MainMenu)




    def MainMenu(self):
        self.menu_.clear()
        self.menu_.add.button('Singleplayer', self.SinglePlayerMenu)
        self.menu_.add.button('Join game', self.ClientMenu)
        self.menu_.add.button('Server', self.ServerMenu)
        self.menu_.add.button("settings",self.SettingsMenu)

        self.menu_.add.button('Quit', pygame_menu.events.EXIT) #exit program
        self.menu_.mainloop(self.screen_)


    def BackToMenu(self):
        '''
        This is used when returning to the menu from the game.
        '''
        self.menu_.clear()

        if self.level_complete_ == True:
            self.menu_.add.label("level completed!")
        else:
            self.menu_.add.label("level fail!")


        self.menu_.add.button("next",self.MainMenu)
        self.menu_.mainloop(self.screen_)


if __name__ == "__main__":

    #start menu:
    menudata = Menu()
    menudata.MainMenu()


