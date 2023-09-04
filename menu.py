import pygame
import pygame_menu
import random
import os
import json

from src import * #import py-boulderdash



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

    if  multiplayer == True: #multiplayer maps
        path += "/maps/multiplayer"
        for i in os.listdir(path):
            maplist.append((str(i), f"maps/multiplayer/{i}"))



    elif multiplayer == False: #singleplayer maps
        path += "/maps/singleplayer"
        for i in os.listdir(path):
            maplist.append((str(i), f"maps/singleplayer/{i}"))



    return(maplist)  # return maps



class Menu:


    def __init__(self) -> None: #constructor

        #MENUDATA
        self.screen_ =  pygame.display.set_mode((1600, 900)) #create window
        pygame.display.set_caption('py-boulderdash') #rename window


        # create menu theme

        #find any font file from /media/font/ and load it:
        self.font_ = f"media/font/{os.listdir('media/font')[0]}"


        self.menu_theme_ = pygame_menu.Theme(background_color=(0, 0, 0), title_background_color=(178, 29, 29),
                                    widget_font_color=(255, 255, 255), widget_padding=6,title_font = self.font_,
                                    title_font_size=52,widget_font = self.font_,widget_font_size=38)




        self.menu_ = pygame_menu.Menu('PY-BOULDERDASH', 700, 590,surface=self.screen_, theme=self.menu_theme_)  #create pygame_menu object





        #game return values:
        self.level_completed_ = False
        self.connection_lost_ = False


        #settings temp variables:
        self.temp_resolution_ = 0
        self.temp_resolution_index_ = 0
        self.temp_fullscreen_ = False
        self.temp_sfx_is_on_ = False


        #GAME START DATA
        self.server_ip_ = "localhost"  #client
        self.port_ = 1234 #client and server default port
        self.join_id_ = "" #server or client
        self.timeout_ = 10 #server, socket timeout
        self.map_file_path_ = ""  #mapfile path  #if server or singleplayer


        self.resolutions_ = [('1600x900',(1600,900)),('1920x1080',(1920,1080)),('1056x594',(1056,594)),('1280x720', (1280,720))] #resolutions list

        #default settings:
        self.resolution_ = [1600,900]
        self.resolution_index_ = 0
        self.fullscreen_ = False
        self.sfx_is_on_ = True #sound effects is on

        self.ReadSettings() #read settings from json file

    def ReadSettings(self):
        '''
        read settings from save/settings.json
        '''

        try:
            f = open("save/settings.json", "r")  #read json file
            settings = json.load(f)["settings"]  #read settings
            f.close()  #close file

            self.resolution_index_ = settings["resolution index"]
            self.resolution_ = settings["resolutions"][settings["resolution index"]] #set resolution
            self.sfx_is_on_ = settings["sfx is on"]

            if settings["fullscreen"] == True:
                self.fullscreen_ = True
                self.screen_ = pygame.display.set_mode(self.resolution_, pygame.FULLSCREEN)  # crete fullscreen window
            else:
                self.fullscreen_ = False
                self.screen_ = pygame.display.set_mode(self.resolution_, pygame.WINDOWMOVED)  # crete normal window

            self.menu_ = pygame_menu.Menu('PY-BOULDERDASH', 700, 590, surface=self.screen_,theme=self.menu_theme_)  # create menu object
        except: #invalid json file
            self.SaveSettings() #save default settings to json file
            self.ReadSettings()

    def SaveSettings(self):
        '''
        save current settings to json file
        save/settings.json
        '''


        settings = {
            "settings":{
                "fullscreen":self.fullscreen_,
                "resolution index":self.resolution_index_,
                "resolutions":[[1600,900],[1920,1080],[1056,594],[1280,720]],
                "sfx is on":self.sfx_is_on_
            }
        }

        jsonstr = json.dumps(settings) #dictionary to str

        f = open("save/settings.json", "w")  #open file
        f.write(jsonstr) #write dictionary data to json file
        f.close()  # close file

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

            #Todo check map cortness before sending it

            gamedata = GameData(True,True,self.font_, self.sfx_is_on_)  # create gamedata
            gamedata.server_ = True
            mapstr, gamedata.map_height_, gamedata.map_width_,map_is_multiplayer, gamedata.required_score_, gamedata.level_timelimit_ = ReadMapFile(self.map_file_path_)  # read map file


            connection = Server(self.port_,self.timeout_,True) #create connection object
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
                        connection.compress_messages_ = False #disable message compression

                        self.level_completed_, self.connection_lost_ = Run(gamedata, connection)  # start game

                        del gamedata  # delete gamedata object from memory
                        del connection  # delete connection object from memory

                        self.BackToMenu()


            #if the connection failed
            connection.CloseSocket() #close socket
            self.menu_.clear()
            self.menu_.add.label(connection.error_message_,max_char=30)
            self.menu_.add.label(f"Server ip:{socket.gethostbyname(socket.gethostname())}")  # print ip address
            self.menu_.add.label(f"Join number: {self.join_id_}") #print gameid
            self.menu_.add.label(f"Port: {connection.port_}")  # print port
            self.menu_.add.button("Try again",StartServer,self)
            self.menu_.add.button("Back",self.ServerMenu)



        self.menu_.clear() #clear menu
        if self.join_id_ == "": #if join id is not exist
            self.SetJoinid() #generate random join id

        self.menu_.add.label(f"your ip address:")
        self.menu_.add.label(socket.gethostbyname(socket.gethostname()))  # print ip address
        self.menu_.add.selector("Map: ", ReturnMaps(True), onchange=self.SetMapFilepath,default=1) #select map
        self.menu_.add.text_input('Port:', default=f"{str(self.port_)}",onchange=self.SetPort)  #set port
        self.menu_.add.text_input('Join number:', default= self.join_id_, onchange=self.SetJoinid) #set join id
        self.menu_.add.text_input('Timeout:', default="10", onchange=self.SetTimeout) #set socket timeout
        self.menu_.add.button("Start server", StartServer,self)
        self.menu_.add.button("Back", self.MultiPlayerMenu)



    def ClientMenu(self):
        def StartClient(self):
            #try connect to server


            gamedata = GameData(True,False,self.font_, self.sfx_is_on_) #create gamedata
            connection = Client(self.server_ip_, self.port_,True)  #create connection object

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
                        connection.compress_messages_ = False #disable message compression

                        self.level_completed_, self.connection_lost_ = Run(gamedata, connection)  # start game

                        del gamedata  # delete gamedata object from memory
                        del connection  # delete connection object from memory

                        self.BackToMenu()



            #if the connection failed
            connection.CloseSocket() #close socket
            self.menu_.clear()

            self.menu_.add.label(connection.error_message_,max_char = 30)

            self.menu_.add.button("Try again",StartClient,self)
            self.menu_.add.button("Back ",self.ClientMenu)



        self.menu_.clear()
        self.menu_.add.text_input('Server ip:', default=self.server_ip_, onchange=self.SetIpaddress) #set server ip
        self.menu_.add.text_input('Port:', default='1234', onchange=self.SetPort) #set port
        self.menu_.add.text_input('Join number:', default=self.join_id_, onchange=self.SetJoinid) #set join id
        self.menu_.add.button("Connect",StartClient,self)
        self.menu_.add.button("Back", self.MultiPlayerMenu)


    def SinglePlayerMenu(self):

        def StartSingleplayer(self):
            gamedata = GameData(False, False, self.font_, self.sfx_is_on_)  # create gamedata
            try:
                mapstr, gamedata.map_height_, gamedata.map_width_,map_is_multiplayer, gamedata.required_score_, gamedata.level_timelimit_ = ReadMapFile(self.map_file_path_)  # read map file
                SetMap(gamedata, mapstr,True)  # convert str to map list
            except: #if incorrect map file

                self.menu_.clear()#clear menu
                self.menu_.add.label("Incorrect map file!")
                self.menu_.add.button("Play", StartSingleplayer, self)
                self.menu_.add.selector("Map: ", ReturnMaps(False), onchange=self.SetMapFilepath,default=1)  # map select
                self.menu_.add.button("Back", self.MainMenu)

            else: #no error
                gamedata.InitDisplay(self.screen_)  #set window to gamedata object

                self.level_completed_,self.connection_lost_ = Run(gamedata) #start game

                del gamedata #delete gamedata object from memory

                self.BackToMenu()


        self.menu_.clear()#clear menu
        self.menu_.add.button("Play",StartSingleplayer,self)
        self.menu_.add.selector("Map: ", ReturnMaps(False), onchange=self.SetMapFilepath,default=1) #map select
        self.menu_.add.button("Back",self.MainMenu)


    def InfoMenu(self):
        self.menu_.clear() #clear menu

        self.menu_.add.label("Controls:")
        self.menu_.add.label("Move:")
        self.menu_.add.label("arrow keys")
        self.menu_.add.label("")
        self.menu_.add.label("Delete next to player:")
        self.menu_.add.label("space + arrow keys")
        self.menu_.add.label("")

        self.menu_.add.button("Back to main menu",self.MainMenu)


    def SettingsMenu(self):


        self.temp_fullscreen_ = self.fullscreen_
        self.temp_resolution_ = self.resolution_
        self.temp_resolution_index_ = self.resolution_index_
        self.temp_sfx_is_on_ = self.sfx_is_on_

        def SetTempResolution(index:int,resolution:tuple):
            self.temp_resolution_index_ = index[1]
            self.temp_resolution_ = resolution

        def SetTempFullscreen(fullscreen:bool):
            self.temp_fullscreen_ = fullscreen

        def SetTempSFX(sfx:bool):
            self.temp_sfx_is_on_ = sfx

        def ApplySettings():
            #apply settings
            self.resolution_ = self.temp_resolution_
            self.resolution_index_ = self.temp_resolution_index_
            self.fullscreen_ =  self.temp_fullscreen_
            self.sfx_is_on_ = self.temp_sfx_is_on_

            #update window
            if self.fullscreen_ == True:
                self.screen_ = pygame.display.set_mode(self.resolution_,pygame.FULLSCREEN) #crete fullscreen window
            else:
                self.screen_ = pygame.display.set_mode(self.resolution_,pygame.WINDOWMOVED) #create noremal window

            self.SaveSettings() #save settings to json file

            # update menu object:
            self.menu_ = pygame_menu.Menu('PY-BOULDERDASH', 600, 500, surface=self.screen_,theme=self.menu_theme_)  # create menu object

            self.MainMenu() #back to mainmenu

        self.menu_.clear() #clear menu
        self.menu_.add.toggle_switch("Full screen:",onchange=SetTempFullscreen,default=self.temp_fullscreen_) #change window mode
        self.menu_.add.selector('Resolution: ', self.resolutions_,default = self.temp_resolution_index_, onchange=SetTempResolution) #change resolution
        self.menu_.add.toggle_switch('Sound:', default=self.temp_sfx_is_on_, onchange=SetTempSFX)
        self.menu_.add.button("Apply",action=ApplySettings)
        self.menu_.add.button("Back",self.MainMenu)


    def MultiPlayerMenu(self):
        self.menu_.clear() #clear menu

        self.menu_.add.button('Join game', self.ClientMenu)
        self.menu_.add.button('Server', self.ServerMenu)
        self.menu_.add.button('Back', self.MainMenu)



    def MainMenu(self):
        self.menu_.clear() #clear menu
        self.menu_.add.button('Singleplayer', self.SinglePlayerMenu)
        self.menu_.add.button('Multiplayer', self.MultiPlayerMenu)
        self.menu_.add.button("Info",self.InfoMenu)
        self.menu_.add.button("Settings",self.SettingsMenu)
        self.menu_.add.button('Quit', pygame_menu.events.EXIT) #exit program
        self.menu_.mainloop(self.screen_)


    def BackToMenu(self):
        '''
        This is used when returning to the menu from the game.
        '''
        self.menu_.clear()
        pygame.display.set_caption('py-boulderdash') #rename window


        if self.connection_lost_ == True:
            self.menu_.add.label("Connection lost!")

        else:

            if self.level_completed_ == True:
                self.menu_.add.label("Level completed!")
            else:
                self.menu_.add.label("Level failed!")


        self.menu_.add.button("Main menu",self.MainMenu)
        self.menu_.mainloop(self.screen_)


if __name__ == "__main__":

    #start menu:
    menudata = Menu()
    menudata.MainMenu()


