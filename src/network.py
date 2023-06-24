import socket
import zlib
from src import *
import sys



# Todo check the correctness of the message





def MapListToStr(maplist: list):
    '''
    convert objects to numbers

    data:
    0 = empty
    1 = local player
    2 = remote player
    3 = default tile
    4 = tile that can be destroyed
    5 = tile that cannot be destroyed
    7 = goal
    8 = not a falling tnt
    9 = falling tnt
    10 = not a falling stone
    11 = falling stone
    12 = Explosion
    14 = monster which looking to right
    15 = monster which looking to down
    16 = monster which looking to left
    17 = monster which looking to up
    18 = not a falling diamond
    19 = falling diamond

    20 Door up
    21 Door right
    22 door down
    23 door left
    '''

    sendlist = []


    for i in range(len(maplist)):
        for j in range(len(maplist[i])):
            # i = y j = x

            if maplist[i][j] == None:  # if none
                sendlist.append("0")

            elif type(maplist[i][j]) == Player:  #if player
                if maplist[i][j].local_player_:  #if local player, change to remoteplayer
                    if maplist[i][j].image_number_ == 0:
                        sendlist.append("2 1")
                    elif maplist[i][j].image_number_ == 1:
                        sendlist.append("2 2")
                    elif maplist[i][j].image_number_ == 2:
                        sendlist.append("2 3")
                    elif maplist[i][j].image_number_ == 3:
                        sendlist.append("2 4")
                    elif maplist[i][j].image_number_ == 4:
                        sendlist.append("2 5")
                else:  #if remoteplayer
                    sendlist.append("1")  # change to local player

            elif type(maplist[i][j]) == DefaultTile:  # if default tile
                sendlist.append("3")
            elif type(maplist[i][j]) == Brick:  # can explode tile
                sendlist.append("4")
            elif type(maplist[i][j]) == Bedrock:  # cannot explode tile
                sendlist.append("5")
            elif type(maplist[i][j]) == Goal:
                sendlist.append("7")

            elif type(maplist[i][j]) == Tnt:  # if tnt
                if maplist[i][j].drop_:  # if currently dropping
                    sendlist.append("9")
                else:  #no currently dropping
                    sendlist.append("8")

            elif type(maplist[i][j]) == Stone:  # if stone
                if maplist[i][j].drop_:  #if currently dropping
                    if maplist[i][j].direction_ == 1:
                        sendlist.append("11 1")
                    elif maplist[i][j].direction_ == 2:
                        sendlist.append("11 2")
                    elif maplist[i][j].direction_ == 3:
                        sendlist.append("11 3")
                    elif maplist[i][j].direction_ == 4:
                        sendlist.append("11 4")

                else:  # no currently dropping
                    if maplist[i][j].direction_ == 1:
                        sendlist.append("10 1")
                    elif maplist[i][j].direction_ == 2:
                        sendlist.append("10 2")
                    elif maplist[i][j].direction_ == 3:
                        sendlist.append("10 3")
                    elif maplist[i][j].direction_ == 4:
                        sendlist.append("10 4")

            elif type(maplist[i][j]) == Explosion: #if explosion
                #sendlist.append("12")
                #Todo delete this?
                pass

            elif type(maplist[i][j]) == Monster:  # if monster
                if maplist[i][j].direction_ == 1:  # right
                    sendlist.append("14")
                elif maplist[i][j].direction_ == 2:  # down
                    sendlist.append("15")
                elif maplist[i][j].direction_ == 3:  # left
                    sendlist.append("16")
                elif maplist[i][j].direction_ == 4:  # up
                    sendlist.append("17")

            elif type(maplist[i][j]) == Diamond: #if diamond
                if maplist[i][j].drop_:  # if currently dropping
                    if maplist[i][j].direction_ == 1:
                        sendlist.append("19 1")
                    elif maplist[i][j].direction_ == 2:
                        sendlist.append("19 2")
                    elif maplist[i][j].direction_ == 3:
                        sendlist.append("19 3")
                    elif maplist[i][j].direction_ == 2:
                        sendlist.append("19 4")
                else:# no currently dropping
                    if maplist[i][j].direction_ == 1:
                        sendlist.append("18 1")
                    elif maplist[i][j].direction_ == 2:
                        sendlist.append("18 2")
                    elif maplist[i][j].direction_ == 3:
                        sendlist.append("18 3")
                    elif maplist[i][j].direction_ == 2:
                        sendlist.append("18 4")

            elif type(maplist[i][j]) == Door:  # if door
                if maplist[i][j].direction_ == 1: #up
                    sendlist.append("20")
                elif maplist[i][j].direction_ == 2: #right
                    sendlist.append("21")
                elif maplist[i][j].direction_ == 3: #down
                    sendlist.append("22")
                elif maplist[i][j].direction_ == 4: #left
                    sendlist.append("23")

    sendstr = ",".join(sendlist) #convert list to string

    return (sendstr)


class Server:
    def __init__(self,port:int,connection_timeout:int = 2):#constructor
        self.socket_ = socket.socket()  # create socket object
        self.port_ = port

        self.socket_.settimeout(connection_timeout)

        self.socket_.bind(('', port))
        print("socket binded to %s" % (port))  # set port

        self.socket_.listen(1)
        print("socket is listening")

        try:
            self.client_, self.addr_ = self.socket_.accept()  # waiting for someone to connect
            self.connected_ = True
            self.client_.settimeout(0.1) #set new timeout
        except:
            self.connected_ = False


        self.data_ = None #received messages
        self.data_type_ = None
        self.points_collected_ = 0 #if message is map

        #data_type_: "map","readytostart","gameexit","restartlevel",None, "other"

        #data_:
        #map = str
        #points_collected_ = int
        #readytostart = str
        #gameexit = None
        #restartlevel = None
        #other = str
        #None = None



    def Read(self):
        #read socket message

        try:
            data = self.client_.recv(10000) #read messages
            data = zlib.decompress(data).decode()  # decompress and decode

            if len(data) == 0: #if no message or message is empty
                self.data_ = None
                self.data_type_ = None
            else:
                # exmine message data type and set data
                if data[0:4] == "map:":  # if message is map

                    index = data.find(":", 5) +1
                    self.points_collected_ = int(data[4:index-1])  #points collected
                    self.data_type_ = "map"
                    self.data_ = data[index:] #read the rest of message


                elif data[0:13] == "readytostart:": #if message is "readytostart"
                    self.data_type_ = "readytostart"
                    self.data_ = data[13:] #read check_number

                elif data[0:9] == "gameexit:":  # if message is gameexit
                    self.data_type_ = "gameexit"
                    self.data_ = eval(data[9:])  # string to boolean

                elif data[0:13] == "restartlevel":
                    self.data_type_ = "restartlevel"
                    self.data_ = None


                else: #other
                    self.data_type_ = "other"
                    self.data_ = data


        except TimeoutError:
            self.data_ = None
            self.data_type_ = None

        return self.data_


    def SendMap(self,maplist:list,points_collected:int):
        mapstr = MapListToStr(maplist) #convert maplist to mapstr
        message = f"map:{str(points_collected)}:{mapstr}"
        self.client_.send(zlib.compress(message.encode()))  # compress and send message




    def SendStartInfo(self,map_height:int,map_width:int,required_score:int=0):
        '''
        a message about the start of the game
        send map size y,z and required_score
        '''

        message = f"startinfo:{str(map_height)},{str(map_width)},{str(required_score)}"

        self.client_.send(zlib.compress(message.encode()))  # compress and send message


    def SendGameExit(self,win:bool = False): #if game exit
        #win False = game over, True = level complete
        message = "gameexit:" + str(win)
        self.client_.send(zlib.compress(message.encode()))  # compress and send message

    def SendRestartLevel(self):
        message = "restartlevel"
        self.client_.send(zlib.compress(message.encode()))  # compress and send message

    def CloseSocket(self):
        self.socket_.close()



class Client:
    def __init__(self,ipaddress:str,port:int):
        self.socket_ = socket.socket()  # create socket object
        self.socket_.settimeout(5)
        self.ipaddress_ = ipaddress
        self.port_ = port

        try: #Todo connection timeout not working
            self.socket_.connect((ipaddress, port))  #connect to server
            self.socket_.settimeout(0.1)  #set new timeout
            self.connected_ = True
        except Exception as a:
            print(a)

            self.connected_ = False


        self.data_ = None #received messages
        self.data_type_ = None
        self.points_collected_ = 0 #if message is map

        #data_type_: "map","startinfo","gameexit","restartlevel",None, "other"

        #data_:
        #map = str
        #points_collected_ = int
        #startinfo = tuple (map_height,map_width)
        #gameexit = bool
        #restartlevel = None
        #other = str
        #None = None



    def Read(self):
        #read socket message
        try:
            data = self.socket_.recv(10000) #read socket
            data = zlib.decompress(data).decode() #decompress and decode

            #exmine message data type and set data
            if data[0:4] == "map:": #if message is map

                index = data.find(":", 4) +1
                self.points_collected_ = int(data[4:index-1])  #points_collected_
                self.data_type_ = "map"
                self.data_ = data[index:] #read the rest of message


            elif data[0:10] == "startinfo:": #if message is startinfo
                y_x_list = data[10:].split(',') #set map size
                map_height = int(y_x_list[0])  #map size y
                map_width = int(y_x_list[1])  #map size x
                required_score = int(y_x_list[1]) #required_score

                self.data_ = (map_height,map_width,required_score)
                self.data_type_ = "startinfo"

            elif data[0:9] == "gameexit:": #if message is gameexit
                self.data_type_ = "gameexit"
                self.data_ = eval(data[9:]) #strin to boolean

            elif data[0:13] == "restartlevel":
                self.data_type_ = "restartlevel"
                self.data_ = None

            else:  # other
                self.data_type_ = "other"
                self.data_ = data

        except TimeoutError:
            self.data_ = None
            self.data_type_ = None


        return self.data_


    def SendReadyToStart(self,check_number:str):
        message = f"readytostart:{check_number}"
        self.socket_.send(zlib.compress(message.encode()))  # compress and send message



    def SendMap(self,maplist:list,points_collected:int):

        mapstr = MapListToStr(maplist) #convert maplist to mapstr
        message = f"map:{str(points_collected)}:{mapstr}"

        self.socket_.send(zlib.compress(message.encode()))  # compress and send message

    def SendGameExit(self,win:bool = False): #if game exit
        #win False = game over, True = level complete
        message = "gameexit:" + str(win)
        self.socket_.send(zlib.compress(message.encode()))  # compress and send message


    def SendRestartLevel(self):
        message = "restartlevel"
        self.socket_.send(zlib.compress(message.encode()))  # compress and send message


    def CloseSocket(self):
        self.socket_.close()