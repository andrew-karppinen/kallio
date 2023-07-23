import pygame
import pygame_menu
import random
from src import *
import os


import time




pygame.init() #init pygame module


def ReturnMaps(multiplayer:bool):
    '''
    return map file path

    return files from

     /maps/sigleplayer
     or
    /maps/multiplayer

    return maps file path
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

    def __init__(self,surface:object=None,menu:object = None) -> None: #constructor

        #MENUDATA
        self.surface_ = surface
        self.menu_ = menu #pygame_menu object


        #GAME START DATA
        self.server_ip_ = "localhost"  #client
        self.port_ = 1234 #client and server default port
        self.gameid_ = "" #server or client
        self.timeout_ = 10 #server, socket timeout

        self.fullscreen_ = False
        self.resolution_ = (1600,900) #deafult resolution
        self.resolution_index_ = 0

        self.map_file_path_ = ""  #mapfile path  #if server or singleplayer

    def SetIpaddress(self, ip: str):
        self.server_ip_ = ip


    def SetPort(self,port):
        try:
            self.port_ = int(port)
        except:
            pass
    def SetGameid(self,id:str = ""):


        if id == "":
            self.gameid_ = ""
            for i in range(5): #generate random gameid
                self.gameid_ += str(random.randint(0, 9))
        else:
            self.gameid_ = id


    def SetTimeout(self,timeout):
        try:
            self.timeout_ = int(timeout)
        except:
            pass
    def SetResolution(self,index,resolution:tuple = (1280,720)):
        self.resolution_ = resolution
        self.resolution_index_ = index[1]

    def SetFullscreen(self,fullscreen:bool):
        self.fullscreen_ = fullscreen

    def SetMapFilepath(self,useless_argument,path:str):
        self.map_file_path_ = path





    def ServerMenu(self):

        def StartServer(self):
            gamedata = GameData(True,True)  # create gamedata
            gamedata.server_ = True
            gamedata.menudata_ = self #save menudata for the duration of the game
            mapstr, gamedata.map_height_, gamedata.map_width_,map_is_multiplayer, gamedata.required_score_, gamedata.level_timelimit_ = ReadMapFile(self.map_file_path_)  # read map file


            connection = Server(self.port_,self.timeout_) #create connection object

            if connection.connected_: #if someone connected

                connection.Read()  # read messages
                if connection.data_type_ == "readytostart":  # if client ready to start the game
                    if connection.data_ == self.gameid_:
                        connection.SendStartInfo(gamedata.map_height_, gamedata.map_width_, gamedata.required_score_, gamedata.level_timelimit_)  # send start info


                        connection.SendMap(mapstr)  #and send map
                        SetMap(gamedata, mapstr, True)  # set map(local) convert str to map list

                        gamedata.SetScreenSize(self.resolution_)  #set local screen size
                        if self.fullscreen_:  #if fullscreen
                            pygame.display.toggle_fullscreen()  #set fullscreen
                        gamedata.SetDrawarea()
                        connection.SetTimeout(0.001) #set new timeout

                        Run(gamedata, connection) #start game
                        self.BackToMenu()


            #if the connection failed
            self.menu_.clear()
            self.menu_.add.label(connection.error_mesage_)
            self.menu_.add.label(f"server ip:{socket.gethostbyname(socket.gethostname())}")  # print ip address
            self.menu_.add.label(f"join nubmer: {self.gameid_}") #print gameid
            self.menu_.add.label(f"port: {connection.port_}")  # print port
            self.menu_.add.button("try again",StartServer,self)
            self.menu_.add.button("back to main menu",self.MainMenu)



        self.menu_.clear() #clear menu
        if self.gameid_ == "": #if join id is not exist
            self.SetGameid() #generate random join id

        self.menu_.add.label(f"your ip address:")
        self.menu_.add.label(socket.gethostbyname(socket.gethostname()))  # print ip address
        self.menu_.add.selector("map:", ReturnMaps(True), onchange=self.SetMapFilepath,default=1) #select map
        self.menu_.add.text_input('port:', default=f"{str(self.port_)}",onchange=self.SetPort)
        self.menu_.add.text_input('join number:', default= self.gameid_,onchange=self.SetGameid)
        self.menu_.add.text_input('timeout:', default="10", onchange=self.SetTimeout)
        self.menu_.add.button("start server", StartServer,self)
        self.menu_.add.button("back", self.MainMenu)



    def ClientMenu(self):
        def StartClient(self):
            #try connect to server

            gamedata = GameData(True,False) #create gamedata
            connection = Client(self.server_ip_, self.port_)  #create connection object
            gamedata.menudata_ = self #save menudata for the duration of the game

            if connection.connected_: #if the connection was successful
                connection.SendReadyToStart(self.gameid_)
                connection.Read()  # read messages
                if connection.data_type_ == "startinfo":  #if start info

                    gamedata.map_height_, gamedata.map_width_,gamedata.required_score_,gamedata.level_timelimit_ = connection.data_ #set map size and required_score


                    connection.Read()  # read messages
                    if connection.data_type_ == "map":  #if message is map
                        SetMap(gamedata, connection.data_,True)  #set map
                        gamedata.SetScreenSize(self.resolution_)  # set screen size
                        if self.fullscreen_:  # if fullscreen
                            pygame.display.toggle_fullscreen()  # set fullscreen
                        gamedata.SetDrawarea()

                        connection.SetTimeout(0.001) #set new timeout

                        Run(gamedata, connection)  # start game
                        self.BackToMenu()



            #if the connection failed
            self.menu_.clear()
            self.menu_.add.label(connection.error_mesage_)
            self.menu_.add.button("try again",StartClient,self)
            self.menu_.add.button("back to main menu",self.MainMenu)



        self.menu_.clear()
        self.menu_.add.text_input('server ip:', default=self.server_ip_, onchange=self.SetIpaddress)
        self.menu_.add.text_input('port:', default='1234', onchange=self.SetPort)
        self.menu_.add.text_input('Join number:', default=self.gameid_, onchange=self.SetGameid)
        self.menu_.add.button("Connect",StartClient,self)
        self.menu_.add.button("Back", self.MainMenu)


    def SinglePlayerMenu(self):

        def StartSingleplayer(self):
            gamedata = GameData(False,False)  # create gamedata
            gamedata.menudata_ = self #save menudata for the duration of the game
            gamedata.SetScreenSize(self.resolution_)  #set screen size


            if self.fullscreen_: #if fullscreen
                pygame.display.toggle_fullscreen() #set fullscreen

            mapstr, gamedata.map_height_, gamedata.map_width_,map_is_multiplayer, gamedata.required_score_, gamedata.level_timelimit_ = ReadMapFile(self.map_file_path_)  # read map file
            SetMap(gamedata, mapstr,True)  # convert str to map list
            gamedata.SetDrawarea()
            Run(gamedata) #start game
            self.BackToMenu()



        self.menu_.clear()
        self.menu_.add.button("Play",StartSingleplayer,self)
        self.menu_.add.selector("map:", ReturnMaps(False), onchange=self.SetMapFilepath,default=1) #map select
        self.menu_.add.button("Back",self.MainMenu)




    def SettingsMenu(self):
        self.menu_.clear()
        self.menu_.add.toggle_switch("full screen",onchange= self.SetFullscreen,default=self.fullscreen_)
        self.menu_.add.selector('Screen size:', [('1600x900',(1600,900)),('1920x1080',(1920,1080)),('1056x594',(1056,594)),('1280x720', (1280,720))],default = self.resolution_index_, onchange=self.SetResolution)
        self.menu_.add.button("back",self.MainMenu)


    def MainMenu(self):
        self.menu_.clear()
        self.menu_.add.button('Singleplayer', self.SinglePlayerMenu)
        self.menu_.add.button('Join game', self.ClientMenu)
        self.menu_.add.button('Server', self.ServerMenu)
        self.menu_.add.button("settings",self.SettingsMenu)

        self.menu_.add.button('Quit', pygame_menu.events.EXIT)
        self.menu_.mainloop(self.surface_)


    def BackToMenu(self): #This is used when returning to the menu from the game.
        pygame.QUIT #close all pygame windows
        self.surface_ = pygame.display.set_mode((600, 500))  # create screen
        self.menu_ = pygame_menu.Menu('py boulderdash', 600, 500, theme=mytheme)  # create menu object
        self.MainMenu()


if __name__ == "__main__":

    #create menu theme
    font8bit = pygame_menu.font.FONT_8BIT
    font = pygame_menu.font.FONT_FRANCHISE
    mytheme = pygame_menu.Theme(background_color=(0,0,0),title_background_color=(178, 29, 29),widget_font_color=(255,255,255),widget_padding=6,widget_font_size = 38,title_font=font,title_font_size=65)


    surface = pygame.display.set_mode((600, 500)) #create screen
    pygame_menu_object = pygame_menu.Menu('py boulderdash', 600, 500, theme=mytheme)  #create menu object

    menudata = Menu(surface,pygame_menu_object)

    menudata.MainMenu()