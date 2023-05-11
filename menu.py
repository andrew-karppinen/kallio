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
stoneimage = pygame.image.load("media/stone.png")
tntimage = pygame.image.load("media/tnt.png")
explosionimage = pygame.image.load("media/explosion.png")
diamondimage = pygame.image.load("media/diamond.png")
goalimage = pygame.image.load("media/goal.png")
bedrockimage = pygame.image.load("media/bedrock.png")
brickimage = pygame.image.load("media/brick.png")
doorimage = pygame.image.load("media/door.png")

#set images
Goal.image = goalimage
Diamond.image = diamondimage
Explosion.image = explosionimage
Tnt.image = tntimage
DefaultTile.image = sandimage
Stone.image = stoneimage
Bedrock.image = bedrockimage
Brick.image = brickimage
Door.Setimage(doorimage)

#create players
local_player = Player(playerimage)
remote_player = Player(playerimage2, False)



pygame.init()



class StartData:

    def __init__(self) -> None:
        self.server_ip_ = ""  #client
        self.port_ = 1234 #client adn server default port
        self.gameid_ = "" #server or client
        self.timeout_ = 10 #server, socket timeout

        self.fullscreen_ = False
        self.resolution_ = (1600,900) #deafult resolution

        self.map_file_path_ = "maps/testmap.txt"  #mapfile path  #if server or singleplayer

    def SetIpaddress(self, ip: str):
        self.server_ip_ = ip


    def SetPort(self,port):
        try:
            self.port_ = int(port)
        except:
            pass
    def SetGameid(self,id:str = ""):
        self.gameid_ = ""

        if id == "":
            for i in range(5): #generate random gameid
                self.gameid_ += str(random.randint(0, 9))
        else:
            self.gameid_ = id


    def SetTimeout(self,timeout):
        try:
            self.timeout_ = int(timeout)
        except:
            pass
    def SetResolution(self,useless_argument=None,resolution:tuple = (1280,720)):
        self.resolution_ = resolution

    def SetFullscreen(self,fullscreen:bool):
        self.fullscreen_ = fullscreen

    def SetMapFilepath(self,useless_argument,path:str):
        self.map_file_path_ = path


def ReturnMaps():
    #return maps for \maps folder
    #set maps folder path
    path = os.getcwd()
    path += "/maps"


    maplist = []
    for i in  os.listdir(path):
        maplist.append((str(i),f"maps/{i}"))

    return(maplist) #return maps

def ServerMenu(startdata):

    def StartServer(startdata):
        gamedata = GameData(local_player, True,True, remote_player)  # create gamedata
        gamedata.server_ = True
        connection = Server(startdata.port_,startdata.timeout_) #create connection object 12 sec timeout

        mapstr, gamedata.map_height_, gamedata.map_width_,gamedata.required_score_,map_is_multiplayer = ReadMapFile(startdata.map_file_path_) #read map file
        SetMap(gamedata, mapstr)  # convert str to map list

        if connection.connected_: #if someone connected

            connection.Read()  # read messages
            if connection.data_type_ == "readytostart":  # if client ready to start the game
                if connection.data_ == startdata.gameid_:
                    connection.SendStartInfo(gamedata.map_height_, gamedata.map_width_)  # send start info

                    connection.SendMap(gamedata.current_map_, 0)  # and send map
                    gamedata.SetScreenSize(startdata.resolution_)  # set screen size
                    if startdata.fullscreen_:  # if fullscreen
                        pygame.display.toggle_fullscreen()  # set fullscreen
                    gamedata.SetDrawarea()
                    Run(gamedata, connection) #start game

        #if the connection failed
        menu.clear()
        menu.add.label("no one connected!")
        menu.add.label(f"server ip:{socket.gethostbyname(socket.gethostname())}")  # print ip address
        menu.add.label(f"join nubmer: {startdata.gameid_}") #print gameid
        menu.add.label(f"port: {connection.port_}")  # print port
        menu.add.button("try again",StartServer,startdata)
        menu.add.button("back to main menu",MainMenu)



    menu.clear() #clear menu
    startdata.SetGameid()#generate random gameid
    menu.add.label(f"your ip address:")
    menu.add.label(socket.gethostbyname(socket.gethostname()))  # print ip address
    menu.add.selector("map:", ReturnMaps(), onchange=startdata.SetMapFilepath) #select map
    menu.add.text_input('port:', default=f"{str(startdata.port_)}",onchange=startdata.SetPort)
    menu.add.text_input('join number:', default= startdata.gameid_,onchange=startdata.SetGameid)
    menu.add.text_input('timeout:', default="10", onchange=startdata.SetTimeout)
    menu.add.button("start server", StartServer,startdata)
    menu.add.button("back", MainMenu)



def ClientMenu(startdata):
    def StartClient(startdata):
        #try connect to server

        gamedata = GameData(local_player, True,False, remote_player, screen=None) #create gamedata
        connection = Client(startdata.server_ip_, startdata.port_)  #create connection object


        if connection.connected_: #iif the connection was successful
            connection.SendReadyToStart(startdata.gameid_)
            connection.Read()  # read messages
            print("tässä1", connection.data_)
            if connection.data_type_ == "startinfo":  #if start info

                gamedata.map_height_, gamedata.map_width_,gamedata.required_score_ = connection.data_ #set map size and required_score

                connection.Read()  # read messages
                print("tässä2", connection.data_)
                if connection.data_type_ == "map":  #if message is map
                    SetMap(gamedata, connection.data_)  #set map
                    gamedata.SetScreenSize(startdata.resolution_)  # set screen size
                    if startdata.fullscreen_:  # if fullscreen
                        pygame.display.toggle_fullscreen()  # set fullscreen
                    gamedata.SetDrawarea()
                    Run(gamedata, connection)  # start game
                    print("tässä3", connection.data_)

        #if the connection failed
        menu.clear()
        menu.add.label("Connection Failed!")
        menu.add.button("try again",StartClient,startdata)
        menu.add.button("back to main menu",MainMenu)



    menu.clear()
    menu.add.text_input('server ip:', default='localhost', onchange=startdata.SetIpaddress)
    menu.add.text_input('port:', default='1234', onchange=startdata.SetPort)
    menu.add.text_input('Join number:', default='', onchange=startdata.SetGameid)
    menu.add.button("Connect",StartClient,startdata)
    menu.add.button("Back", MainMenu)


def SinglePlayerMenu(startdata):

    def StartSingleplayer(startdata):
        gamedata = GameData(local_player, False,False, remote_player)  # create gamedata
        gamedata.SetScreenSize(startdata.resolution_)  #set screen size


        if startdata.fullscreen_: #if fullscreen
            pygame.display.toggle_fullscreen() #set fullscreen

        mapstr, gamedata.map_height_, gamedata.map_width_,gamedata.required_score_,map_is_multiplayer = ReadMapFile(startdata.map_file_path_) #read map file
        SetMap(gamedata, mapstr)  # convert str to map list
        gamedata.SetDrawarea()
        Run(gamedata) #start game



    menu.clear()
    menu.add.button("Play",StartSingleplayer,startdata)
    menu.add.selector("map:", ReturnMaps(), onchange=startdata.SetMapFilepath,default=1) #map select
    menu.add.button("Back", MainMenu)





def SettingsMenu(stratdata):
    menu.clear()
    menu.add.toggle_switch("full screen",onchange= startdata.SetFullscreen)
    menu.add.selector('Screen size:', [('1600x900',(1600,900)),('1920x1080',(1920,1080)),('1056x594',(1056,594)),('1280x720', (1280,720))], onchange=startdata.SetResolution)
    menu.add.button("back",MainMenu)


def MainMenu():
    menu.clear()
    menu.add.button('Singleplayer', SinglePlayerMenu, startdata)
    menu.add.button('Join game', ClientMenu, startdata)
    menu.add.button('Server', ServerMenu, startdata)
    menu.add.button("settings",SettingsMenu,startdata)

    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(surface)



#GLOBAL SCOPE
#create menu theme
font8bit = pygame_menu.font.FONT_8BIT
font = pygame_menu.font.FONT_FRANCHISE
mytheme = pygame_menu.Theme(background_color=(0,0,0),title_background_color=(178, 29, 29),widget_font_color=(255,255,255),widget_padding=6,widget_font_size = 38,title_font=font,title_font_size=65)


startdata = StartData()  # create data obeject
surface = pygame.display.set_mode((600, 500)) #create screen
menu = pygame_menu.Menu('py boulderdash', 600, 500, theme=mytheme)  #create menu object

MainMenu() #star menu