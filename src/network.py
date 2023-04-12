import socket
from src.objects import *


def MapListToStr(maplist: list):
    '''
    send map data
    0 = tyhjä
    1 = paikallinen pelaaja
    2 = toisen tietokoneen pelaaja
    3 = perustile
    4 = tile joka voidaan räjäyttää
    5 = tile jota ei voida räjäyttää
    6 = piste
    7 = maali
    8 = tnt joka ei putoamassa
    9 = tnt joka putoamassa
    10 = kivi joka ei putoamassa
    11 = kivi joka putoamassa
    14 =  vihollinen joka katsoo oikealle
    15 = vihollinen joka katsoo alas
    16 = vihollinen joka katsoo vasemmalle
    17 = vihollinen joka katsoo ylös
    '''

    # objects to numbers

    sendlist = []


    for i in range(len(maplist)):
        for j in range(len(maplist[i])):
            # i = y j = x

            if maplist[i][j] == None:  # if none
                sendlist.append("0")

            elif type(maplist[i][j]) == Player:  # if player
                if maplist[i][j].local_player_:  # if local player
                    sendlist.append("2")  # change to remoteplayer
                else:  # if remoteplayer
                    sendlist.append("1")  # change to local player

            elif type(maplist[i][j]) == DefaultTile:  # if default tile
                sendlist.append("3")
            elif type(maplist[i][j]) == Brick:  # can explode tile
                sendlist.append("4")
            elif type(maplist[i][j]) == Bedrock:  # cannot explode tile
                sendlist.append("5")
            elif type(maplist[i][j]) == Diamond:
                sendlist.append("6")
            elif type(maplist[i][j]) == Goal:
                sendlist.append("7")

            elif type(maplist[i][j]) == Tnt:  # if tnt
                if maplist[i][j].drop_:  # if currently dropping
                    sendlist.append("9")
                else:  # no currently dropping
                    sendlist.append("8")

            elif type(maplist[i][j]) == Stone:  # if stone
                if maplist[i][j].drop_:  # if currently dropping
                    sendlist.append("11")

                else:  # no currently dropping
                    sendlist.append("10")

            elif type(maplist[i][j]) == Monster:  # if monster

                if maplist[i][j].direction_ == 1:  # right
                    sendlist.append("14")
                elif maplist[i][j].direction_ == 2:  # down
                    sendlist.append("15")
                elif maplist[i][j].direction_ == 3:  # left
                    sendlist.append("16")
                elif maplist[i][j].direction_ == 4:  # up
                    sendlist.append("17")

    sendstr = ",".join(sendlist) #convert list to string

    return (sendstr)


class Server:
    def __init__(self,port:int):


        self.socket_ = socket.socket()  # create socket object
        self.port_ = port

        self.socket_.settimeout(5)  # timeout 5 second

        self.socket_.bind(('', port))
        print("socket binded to %s" % (port))  # set port

        self.socket_.listen(1)
        print("socket is listening")

        try:
            self.client_, self.addr_ = self.socket_.accept()  # waiting for someone to connect
            self.connected_ = True
            self.client_.settimeout(0.01)
        except:
            self.connected_ = False


        self.data_ = None #received messages
        self.data_type_ = None
        self.round_number_ = 0 #if message is map

        #data_type_: "map","readytostart","gameexit",None, "other"

        #data_:
        #map = str
        #readytostart = str
        #gameexit = None
        #other = str
        #None = None



    def Read(self):

        try:
            data = self.client_.recv(1024).decode() #read messages

            if len(data) == 0: #if no message or message is empty
                self.data_ = None
                self.data_type_ = None
            else:
                # exmine message data type and set data
                if data[0:4] == "map:":  # if message is map

                    index = data.find(":", 5) +1
                    self.round_number_ = data[4:index-1]  # round counter
                    self.data_type_ = "map"
                    self.data_ = data[index:] #read the rest of message


                elif data[0:13] == "readytostart:": #if message is "readytostart"
                    self.data_type_ = "readytostart"
                    self.data_ = data[13:] #read check_number
        except TimeoutError:
            self.data_ = None
            self.data_type_ = None

        return self.data_


    def SendMap(self,maplist:list,round_number:int):
        mapstr = MapListToStr(maplist) #convert maplist to mapstr
        message = f"map:{str(round_number)}:{mapstr}"
        self.client_.send(message.encode())  #send message


    def SendStartInfo(self,map_height:int,map_width:int):

        '''
        a message about the start of the game
        send map size y,z
        '''

        message = "startinfo:" + str(map_height) + "," + str(map_width)

        self.client_.send(message.encode())  # send message


    def SendGameExit(self,win:bool = False): #if game exit
        #win False = game over, True = level complete
        message = "gameexit:" + str(win)
        self.client_.send(message.encode())  # send message

    def CloseSocket(self):
        self.socket_.close()



class Client:
    def __init__(self,ipaddress:str,port:int):
        self.socket_ = socket.socket()  # create socket object
        self.socket_.settimeout(2)
        self.ipaddress_ = ipaddress
        self.port_ = port

        try:
            self.socket_.connect((ipaddress, port))  #connect to server
            self.socket_.settimeout(0.01)  # set new timeout
            self.connected_ = True
        except:
            self.connected_ = False


        self.data_ = None #received messages
        self.data_type_ = None
        self.round_number_ = 0 #if message is map

        #data_type_: "map","startinfo","gameexit",None, "other"

        #data_:
        #map = str
        #startinfo = tuple (map_height,map_width)
        #gameexit = bool
        #other = str
        #None = None


    def Read(self):

        try:
            data = self.socket_.recv(1024).decode() #read socket

            #exmine message data type and set data
            if data[0:4] == "map:": #if message is map

                index = data.find(":", 4) +1
                self.round_number_ = data[4:index-1]  # round counter
                self.data_type_ = "map"
                self.data_ = data[index:] #read the rest of message


            elif data[0:10] == "startinfo:": #if message is startinfo
                y_x_list = data[10:].split(',') #set map size
                map_height = int(y_x_list[0])  #map size y
                map_width = int(y_x_list[1])  #map size x

                self.data_ = (map_height,map_width)
                self.data_type_ = "startinfo"

            elif data[0:9] == "gameexit:": #if message is gameexit
                self.data_type_ = "gameexit"
                self.data_ = eval(data[9:]) #strin to boolean

        except TimeoutError:
            self.data_ = None
            self.data_type_ = None


        return self.data_


    def SendReadyToStart(self,check_number:str):
        message = f"readytostart:{check_number}"
        self.socket_.send(message.encode())  # send message



    def SendMap(self,maplist:list,round_number:int):

        mapstr = MapListToStr(maplist) #convert maplist to mapstr
        message = f"map:{str(round_number)}:{mapstr}"

        self.socket_.send(message.encode())  #send message

    def SenGameExit(self):
        pass


    def CloseSocket(self):
        self.socket_.close()