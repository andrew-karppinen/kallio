import pygame
import pygame_menu
import socket
import random
from src import *
from threading import Thread
import os


#initialize

#load images
sandimage = pygame.image.load("media/sand.png")
playerimage = pygame.image.load("media/player.png")
playerimage2 = pygame.image.load("media/player2.png")
playerimage3 = pygame.image.load("media/player3.png")
stoneimage = pygame.image.load("media/stone.png")
tntimage = pygame.image.load("media/tnt.png")
explosionimage = pygame.image.load("media/explosion.png")
diamondimage = pygame.image.load("media/diamond.png")
goalimage = pygame.image.load("media/goal.png")
bedrockimage = pygame.image.load("media/bedrock.png")
brickimage = pygame.image.load("media/brick.png")
doorimage = pygame.image.load("media/door.png")

#set images
Diamond.SetImage(diamondimage)
Goal.SetImage(goalimage)
Explosion.SetImage(explosionimage)
Tnt.SetImage(tntimage)
DefaultTile.SetImage(sandimage)
Bedrock.SetImage(bedrockimage)
Brick.SetImage(brickimage)

#set images
Stone.SetImage(stoneimage)
Door.SetImage(doorimage)

#create players
local_player = Player()
remote_player = Player(False)

#set players images
local_player.SetImage(playerimage,playerimage2,playerimage3)
remote_player.SetImage(playerimage,playerimage2,playerimage3)

pygame.init() #inti pygame module


def ReturnMaps():
    # return maps for \maps folder
    # set maps folder path
    path = os.getcwd()
    path += "/maps"

    maplist = []
    for i in os.listdir(path):
        maplist.append((str(i), f"maps/{i}"))

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

        self.map_file_path_ = "maps/testmap.txt"  #mapfile path  #if server or singleplayer

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
            gamedata = GameData(local_player, True,True, remote_player)  # create gamedata
            gamedata.server_ = True
            gamedata.menudata_ = self #save menudata for the duration of the game
            mapstr, gamedata.map_height_, gamedata.map_width_,gamedata.required_score_,map_is_multiplayer = ReadMapFile(self.map_file_path_) #read map file
            SetMap(gamedata, mapstr,True)  # convert str to map list


            connection = Server(self.port_,self.timeout_) #create connection object

            if connection.connected_: #if someone connected

                connection.Read()  # read messages
                if connection.data_type_ == "readytostart":  # if client ready to start the game
                    if connection.data_ == self.gameid_:
                        connection.SendStartInfo(gamedata.map_height_, gamedata.map_width_)  # send start info

                        connection.SendMap(gamedata.current_map_, 0)  #and send map
                        gamedata.SetScreenSize(self.resolution_)  #set local screen size
                        if self.fullscreen_:  #if fullscreen
                            pygame.display.toggle_fullscreen()  #set fullscreen
                        gamedata.SetDrawarea()
                        Run(gamedata, connection) #start game
                        self.BackToMenu()

            #if the connection failed
            self.menu_.clear()
            self.menu_.add.label("no one connected!")
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
        self.menu_.add.selector("map:", ReturnMaps(), onchange=self.SetMapFilepath) #select map
        self.menu_.add.text_input('port:', default=f"{str(self.port_)}",onchange=self.SetPort)
        self.menu_.add.text_input('join number:', default= self.gameid_,onchange=self.SetGameid)
        self.menu_.add.text_input('timeout:', default="10", onchange=self.SetTimeout)
        self.menu_.add.button("start server", StartServer,self)
        self.menu_.add.button("back", self.MainMenu)



    def ClientMenu(self):
        def StartClient(self):
            print(self.gameid_)
            #try connect to server

            gamedata = GameData(local_player, True,False, remote_player) #create gamedata
            connection = Client(self.server_ip_, self.port_)  #create connection object
            gamedata.menudata_ = self #save menudata for the duration of the game

            if connection.connected_: #if the connection was successful
                connection.SendReadyToStart(self.gameid_)
                connection.Read()  # read messages
                print("tässä1", connection.data_)
                if connection.data_type_ == "startinfo":  #if start info

                    gamedata.map_height_, gamedata.map_width_,gamedata.required_score_ = connection.data_ #set map size and required_score

                    connection.Read()  # read messages
                    if connection.data_type_ == "map":  #if message is map
                        SetMap(gamedata, connection.data_,True)  #set map
                        gamedata.SetScreenSize(self.resolution_)  # set screen size
                        if self.fullscreen_:  # if fullscreen
                            pygame.display.toggle_fullscreen()  # set fullscreen
                        gamedata.SetDrawarea()

                        print("käynnistetään client")
                        Run(gamedata, connection)  # start game
                        print("poistuttiin clientistä")
                        self.BackToMenu()



            #if the connection failed
            self.menu_.clear()
            self.menu_.add.label("Connection Failed!")
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
            gamedata = GameData(local_player, False,False, remote_player)  # create gamedata
            gamedata.menudata_ = self #save menudata for the duration of the game
            gamedata.SetScreenSize(self.resolution_)  #set screen size


            if self.fullscreen_: #if fullscreen
                pygame.display.toggle_fullscreen() #set fullscreen

            mapstr, gamedata.map_height_, gamedata.map_width_,gamedata.required_score_,map_is_multiplayer = ReadMapFile(self.map_file_path_) #read map file
            SetMap(gamedata, mapstr,True)  # convert str to map list
            gamedata.SetDrawarea()
            Run(gamedata) #start game
            self.BackToMenu()



        self.menu_.clear()
        self.menu_.add.button("Play",StartSingleplayer,self)
        self.menu_.add.selector("map:", ReturnMaps(), onchange=self.SetMapFilepath,default=1) #map select
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