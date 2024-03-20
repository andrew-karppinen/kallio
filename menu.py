import pygame
import pygame_menu
import random
import os
import json

from src import * #import py-boulderdash


pygame.init() #init pygame module



PROGRAM_VERSION = "0.0.13"





def ReturnMaps(multiplayer:bool):
    '''
    return map files path from:

    /maps/sigleplayer
     or
    /maps/multiplayer

    reads the map files to be used and their order from the json file

    syntax of the list to be returned:
    [("map number: map name","map file path")]

    if level set is incorect return None
    '''

    maplist = []

    if multiplayer == True: #multiplayer maps
        try:
            with open("maps/multiplayer/level set config.json") as multiplayer_maps: #reads the map files to be used and their order from the json file
                multiplayer_maps = json.load(multiplayer_maps)
                for i in range(1,multiplayer_maps["map count"]+1):
                    if os.path.isfile(multiplayer_maps["maps"][str(i)][0]) == False: #check if file is exist
                        raise
                    maplist.append((f"{i}: {multiplayer_maps['maps'][str(i)][1]}",multiplayer_maps["maps"][str(i)][0])) #append: ("map number: map name","map file path")
        except: #if error
            return (None)

    elif multiplayer == False: #singleplayer maps
        try:
            with open("maps/singleplayer/level set config.json") as singleplayer_maps: #reads the map files to be used and their order from the json file
                singleplayer_maps = json.load(singleplayer_maps)
                for i in range(1,singleplayer_maps["map count"]+1):
                    if os.path.isfile(singleplayer_maps["maps"][str(i)][0]) == False: #check if file is exist
                        raise
                    maplist.append((f"{i}: {singleplayer_maps['maps'][str(i)][1]}",singleplayer_maps["maps"][str(i)][0])) #append: ("map number: map name","map file path")
        except: #if error
            return(None)


    return(maplist)  #return maps



class Menu:


    def __init__(self) -> None: #constructor


        with open("media/font/font config.json") as json_data: #read font file path from json file
            self.font_ = json.load(json_data)["font file path"]




        #create menu theme:
        self.menu_theme_ = pygame_menu.Theme(background_color=(0, 0, 0), title_background_color=(178, 29, 29),
                                    widget_font_color=(255, 255, 255), widget_padding=6,title_font = self.font_,
                                    title_font_size=52,widget_font = self.font_,widget_font_size=38,title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE) #create menu theme


        #game return values:
        self.level_completed_ = False
        self.connection_lost_ = False

        self.music_ = Music()  # create music object

        #GAME START DATA
        self.server_ip_ = "localhost"  #client
        self.port_ = 1234 #client and server default port
        self.join_id_ = "" #server or client
        self.timeout_ = 10 #server, socket timeout
        self.map_file_path_ = ""  #mapfile path  #if server or singleplayer

        self.resolutions_ = [['1600x900',[1600,900]],['1920x1080',[1920,1080]],['2560x1440',[2560,1440]],['1056x594',[1056,594]],['1280x720', [1280,720]]] #resolutions 16:9 list

        #remove resolutions higher than the screen resolution from the list
        info = pygame.display.Info() #get screen resolution
        self.display_resolution_ = (info.current_w,info.current_h) #get screen resolution

        for i in range(len(self.resolutions_)-1,0,-1):
            if self.resolutions_[i][1][0] > self.display_resolution_[0] or self.resolutions_[i][1][1] > self.display_resolution_[1]:
                self.resolutions_.pop(i)


        #settings temp variables:
        self.temp_resolution_ = 0
        self.temp_resolution_index_ = 0
        self.temp_fullscreen_ = False
        self.temp_sfx_is_on_ = False #sound effects is on
        self.temp_volume_ = 0
        self.temp_music_is_on_ = False
        self.temp_music_volume_ = False

        #default settings:
        self.resolution_ = [1600,900]
        self.fullscreen_ = False
        self.sfx_is_on_ = True #sound effects is on
        self.sfx_volume_ = 0.5
        self.music_is_on_ = True
        self.music_volume_ = 0.5


        self.ReadSettings() #read settings from json file, create screen, menu object


    def ReadSettings(self):
        '''
        read settings from save/settings.json
        create menu object and window
        '''

        try:
            f = open("save/settings.json", "r")  #read json file
            settings = json.load(f)["settings"]  #read settings
            f.close()  #close file


            self.sfx_is_on_ = settings["sfx is on"]
            self.sfx_volume_ = settings["volume"]

            self.music_is_on_ = settings["music is on"]
            self.music_volume_ = settings["music volume"]


            self.music_.SetVolume(settings["music volume"])
            if self.music_is_on_ == True:
                self.music_.PlayMusic() #play music


            resolution = settings["resolution"] #saved resolution

            if resolution[0] > self.display_resolution_[0] and resolution[1] > self.display_resolution_[1]: #if saved resolution > screen resolution
                raise
            else: #no error
                 self.resolution_ = resolution


            if settings["fullscreen"] == True:
                self.fullscreen_ = True
                self.screen_ = pygame.display.set_mode(self.resolution_, pygame.FULLSCREEN)  # crete fullscreen window
            else:
                self.fullscreen_ = False
                self.screen_ = pygame.display.set_mode(self.resolution_, pygame.WINDOWMOVED)  # crete normal window

            self.menu_ = pygame_menu.Menu('KALLIO', 700, 590, surface=self.screen_,theme=self.menu_theme_)  #create menu object
            pygame.display.set_caption('KALLIO') #rename window

        except Exception: #invalid json file or file not exist
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
                "resolution":self.resolution_,
                "sfx is on":self.sfx_is_on_,
                "volume":self.sfx_volume_,
                "music is on": self.music_is_on_,
                "music volume":self.music_volume_

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

    def GenerateJoinid(self):
        #generate random join id
        self.join_id_ = ""
        for i in range(5): #generate random join id
            self.join_id_ += str(random.randint(0, 9))
        return self.join_id_
    def SetJoinid(self,id:str):
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

            gamedata = GameData(True, True, self.font_, self.sfx_is_on_, self.sfx_volume_)  # create gamedata
            gamedata.server_ = True
            mapstr, gamedata.map_height_, gamedata.map_width_,map_is_multiplayer, gamedata.required_score_, gamedata.level_timelimit_ = ReadMapFile(self.map_file_path_)  # read map file


            connection = Server(self.port_,self.timeout_,True) #create connection object
            if connection.connected_: #if someone connected

                connection.Read()  # read messages
                if connection.data_type_ == "readytostart":  # if client ready to start the game

                    if connection.data_[1] == PROGRAM_VERSION: #check program version
                        pass

                        if connection.data_[0] == self.join_id_: #chec join id

                            connection.BufferNext() #delete first message from buffer
                            connection.SendStartInfo(gamedata.map_height_, gamedata.map_width_, gamedata.required_score_, gamedata.level_timelimit_)  # send start info


                            connection.SendMap(mapstr)  #and send map to client
                            SetMap(gamedata, mapstr)  # set map(local) convert str to map list

                            gamedata.InitDisplay(self.screen_)  # set window to gamedata object
                            connection.compress_messages_ = False #disable message compression

                            self.level_completed_, self.connection_lost_ = Run(gamedata, connection)  # start game

                            del gamedata  # delete gamedata object from memory
                            del connection  # delete connection object from memory

                            self.BackToMenu()


                    else: #if incorrect version
                        connection.SendWrongVersion()


            #if the connection failed
            connection.CloseSocket() #close socket
            self.menu_.clear()
            self.menu_.add.label(connection.error_message_,max_char=30)
            self.menu_.add.label(f"Server ip:{socket.gethostbyname(socket.gethostname())}")  # print ip address
            self.menu_.add.label(f"Join id: {self.join_id_}") #print join id
            self.menu_.add.label(f"Port: {connection.port_}")  # print port
            self.menu_.add.button("Try again",StartServer,self)
            self.menu_.add.button("Back",self.ServerMenu)



        #error check:
        maps_list = ReturnMaps(True)
        if maps_list == None: #if level set is incorrect
            pass

        else:
            self.map_file_path_ = maps_list[0][1] # set default map file path, due to a bug in the pygame menu!

            self.menu_.clear() #clear menu
            if self.join_id_ == "": #if join id is not exist
                self.GenerateJoinid()#generate random join id

            self.menu_.add.label(f"your ip address:")
            self.menu_.add.label(socket.gethostbyname(socket.gethostname()))  # print ip address
            self.menu_.add.label(f"Join id: {self.join_id_}")
            self.menu_.add.selector("Map: ", maps_list, onchange=self.SetMapFilepath) #select map
            self.menu_.add.text_input('Port:', default=f"{str(self.port_)}",onchange=self.SetPort)  #set port
            self.menu_.add.text_input('Timeout:', default="10", onchange=self.SetTimeout) #set socket timeout
            self.menu_.add.button("Start server", StartServer,self)
            self.menu_.add.button("Back", self.MultiPlayerMenu)



    def ClientMenu(self):
        def StartClient(self):


            error_message = ""
            self.menu_.clear() #clear menu

            if len(self.join_id_) == 5:

                #try connect to server

                gamedata = GameData(True, False, self.font_, self.sfx_is_on_, self.sfx_volume_) #create gamedata
                connection = Client(self.server_ip_, self.port_,True)  #create connection object

                if connection.connected_: #if the connection was successful
                    connection.SendReadyToStart(self.join_id_,PROGRAM_VERSION)
                    connection.Read()  # read messages
                    if connection.data_type_ == "startinfo":  #if start info

                        gamedata.map_height_, gamedata.map_width_,gamedata.required_score_,gamedata.level_timelimit_ = connection.data_ #set map size, required_score and level timelimit
                        connection.BufferNext()  #delete first message from buffer

                        connection.Read()  # read messages
                        if connection.data_type_ == "map":  #if message is map
                            SetMap(gamedata, connection.data_)  #set map
                            connection.BufferNext() #delete first message from buffer

                            gamedata.InitDisplay(self.screen_)  # set window to gamedata object
                            connection.compress_messages_ = False #disable message compression
                            self.level_completed_, self.connection_lost_ = Run(gamedata, connection)  # start game

                            del gamedata  # delete gamedata object from memory
                            del connection  # delete connection object from memory

                            self.BackToMenu()

                    elif connection.data_type_ == "wrongversion" : #if the program version differs from the server version
                         error_message = "The version of the program is different from the host!"
                else: #if the connection failed
                    error_message = connection.error_message_
                    connection.CloseSocket() #close socket
            else:
                error_message = "joind id must be 5 characters long"


            self.menu_.add.label(error_message,max_char = 30) #show error message
            self.menu_.add.button("Try again",StartClient,self)
            self.menu_.add.button("Back ",self.ClientMenu)



        self.menu_.clear()
        self.menu_.add.text_input('Server ip:', default=self.server_ip_, onchange=self.SetIpaddress) #set server ip
        self.menu_.add.text_input('Port:', default='1234', onchange=self.SetPort) #set port
        self.menu_.add.text_input('Join number:', default=self.join_id_, onchange=self.SetJoinid,maxchar=5) #set join id
        self.menu_.add.button("Connect",StartClient,self)
        self.menu_.add.button("Back", self.MultiPlayerMenu)


    def SinglePlayerMenu(self):

        def StartSingleplayer(self):
            gamedata = GameData(False, False, self.font_, self.sfx_is_on_, self.sfx_volume_)  # create gamedata
            try:
                mapstr, gamedata.map_height_, gamedata.map_width_,map_is_multiplayer, gamedata.required_score_, gamedata.level_timelimit_ = ReadMapFile(self.map_file_path_)  # read map file
                SetMap(gamedata, mapstr)  # convert str to map list
            except: #if incorrect map file

                self.menu_.clear() #clear menu
                self.menu_.add.label("Incorrect map file!")
                self.menu_.add.button("Ok", self.SinglePlayerMenu)


            else: #no error
                gamedata.InitDisplay(self.screen_)  #set window to gamedata object


                self.level_completed_,self.connection_lost_ = Run(gamedata) #start game

                del gamedata #delete gamedata object from memory

                self.BackToMenu()


        #error check:
        maps_list = ReturnMaps(False)
        if maps_list == None: #if level set is incorrect
            pass

        else:
            self.map_file_path_ = maps_list[0][1] # set default map file path, due to a bug in the pygame menu!
            self.menu_.clear() #clear menu
            self.menu_.add.button("Play",StartSingleplayer,self)
            self.menu_.add.selector("Map: ", ReturnMaps(False), onchange=self.SetMapFilepath) #map select

            self.menu_.add.button("Back",self.MainMenu)


    def MultiPlayerMenu(self):

        def InternetMenu():
            self.menu_.clear()  # clear menu
            self.menu_.add.label("This feature coming!")
            self.menu_.add.label("In the meantime, play on the local network!",max_char=24)
            self.menu_.add.button('Back', self.MultiPlayerMenu)


        def LanMenu():
            self.menu_.clear()  # clear menu
            self.menu_.add.button('Join game', self.ClientMenu)
            self.menu_.add.button('Server', self.ServerMenu)
            self.menu_.add.button('Back', self.MultiPlayerMenu)



        self.menu_.clear()  # clear menu
        self.menu_.add.button('Local area network', LanMenu)

        self.menu_.add.button('Internet', InternetMenu)
        self.menu_.add.button('Back', self.MainMenu)




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

        self.temp_music_is_on_ = self.music_is_on_
        self.temp_music_volume_ = self.music_volume_

        self.temp_fullscreen_ = self.fullscreen_
        self.temp_resolution_ = self.resolution_
        self.temp_sfx_is_on_ = self.sfx_is_on_
        self.temp_volume_ = self.sfx_volume_

        def SetTempResolution(index:int,resolution:tuple):
            self.temp_resolution_ = resolution

        def SetTempFullscreen(fullscreen:bool):
            self.temp_fullscreen_ = fullscreen

        def SetTempSFX(sfx:bool):
            self.temp_sfx_is_on_ = sfx

        def SetTempVolume(volume:float):
            self.temp_volume_ = volume /10

        def SetTempMusicVolume(volume:float):
            self.temp_music_volume_ = volume /10

        def SetTempMusic(on:bool):
            self.temp_music_is_on_ = on

        def ApplySettings():
            '''
            Save changes

            set temp variable -->
            '''

            if self.temp_resolution_ == [1056,594]: #prevent setting full screen if the resolution is too low
                self.temp_fullscreen_ = False



            #apply settings
            self.sfx_is_on_ = self.temp_sfx_is_on_
            self.sfx_volume_ = self.temp_volume_
            self.music_is_on_ =  self.temp_music_is_on_
            self.music_volume_ = self.temp_music_volume_

            self.music_.SetVolume(self.music_volume_)#set music volume

            if self.music_is_on_ == True:
                self.music_.PlayMusic()
            else:
                self.music_.StopMusic()

            if self.temp_fullscreen_ != self.fullscreen_ or self.temp_resolution_ != self.resolution_: #if the screen settings has been changed
                self.resolution_ = self.temp_resolution_
                self.fullscreen_ = self.temp_fullscreen_
                self.SaveSettings()  # save settings to json file
                #update menu object:
                self.ReadSettings()


            self.SaveSettings() #save settings to json file

            self.SettingsMenu()
            self.menu_.mainloop(self.screen_)


        def FindReslutionIndex(resolution, resoluutions_list):
            for index, item in enumerate(resoluutions_list):
                if resolution == item[1]:
                    return index
            return -1  #Resolution not found in the list




        #settings menu:
        self.menu_.clear() #clear menu


        self.menu_.add.toggle_switch("Full screen:",onchange=SetTempFullscreen,default=self.temp_fullscreen_) #change window mode
        self.menu_.add.selector('Resolution: ', self.resolutions_,default=FindReslutionIndex(self.resolution_,self.resolutions_), onchange=SetTempResolution) #change resolution
        self.menu_.add.toggle_switch('Sound:', default=self.temp_sfx_is_on_, onchange=SetTempSFX)

        self.menu_.add.range_slider(title="Volume: ", default=int(self.sfx_volume_ * 10), range_values=(0, 10), increment=1, onchange=SetTempVolume) #set volume
        self.menu_.add.toggle_switch(title="Music: ",onchange=SetTempMusic,default=self.temp_music_is_on_) #turn music on/off

        self.menu_.add.range_slider(title="Music volume: ", default=int(self.temp_music_volume_ * 10), range_values=(0, 10), increment=1, onchange=SetTempMusicVolume) #set volume
        self.menu_.add.button("Apply",action=ApplySettings)
        self.menu_.add.button("Back",self.MainMenu)





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
        pygame.display.set_caption('KALLIO') #rename window


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


