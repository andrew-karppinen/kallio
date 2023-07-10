import socket
import zlib
from src import *
import sys



# Todo check the correctness of the message





class Server:
    def __init__(self,port:int,connection_timeout:int = 2):#constructor
        self.socket_ = socket.socket()  # create socket object
        self.port_ = port
        self.error_mesage_ = ""

        self.socket_.settimeout(connection_timeout)
        self.connected_ = False


        try:
            self.socket_.bind(('', port))
            print("socket binded to %s" % (port))  # set port
            self.socket_.listen(1)
            print("socket is listening")

            try:
                self.client_, self.addr_ = self.socket_.accept()  # waiting for someone to connect
                self.connected_ = True
                self.client_.settimeout(0.1)
            except Exception as message:
                self.error_mesage_ = message
                self.connected_ = False

        except Exception as message:
            self.error_mesage_ = message




        self.data_ = None #received messages
        self.data_type_ = None
        self.points_collected_ = 0 #if message is map
        self.full_map_ = False #if message is map
        self.position_ = (0,0) #if message is map

        #data_type_: "map","readytostart","gameexit","restartlevel",None, "other"

        #data_:
        #map = str
        #points_collected_ = int
        #readytostart = str
        #gameexit = None
        #restartlevel = None
        #other = str
        #None = None


    def SetTimeout(self,timeout):
        self.client_.settimeout(timeout)  # set new timeout

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

                    index = data.find(":", 5) +1 #find points collected
                    self.points_collected_ = int(data[4:index-1])  #points collected

                    index2 = data.find(":", index) +1 #find is full_map boolean
                    self.full_map_ = eval(data[index:index2-1])

                    index3 = data.find(":",index2) +1 #find position
                    self.position_ = data[index2:index3-1].split(',')

                    self.position_[0] = int(self.position_[0])  # convert str to int
                    self.position_[1] = int(self.position_[1])

                    self.data_type_ = "map"
                    self.data_ = data[index3:] #read the rest of message


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


    def SendMap(self,maplist:list,points_collected:int,send_full_map:bool = True,position:tuple=None):

        #position = (y,x)

        # sends the player's position and adjacent tiles
        if send_full_map == False:

            sendlist = [None,None, None, None, None]

            sendlist[0] = maplist[position[0]][position[1]]  # player
            sendlist[1] = maplist[position[0]][position[1] + 1]  # right
            sendlist[2] = maplist[position[0] + 1][position[1]]  # down
            sendlist[3] = maplist[position[0]][position[1] - 1]  # right
            sendlist[4] = maplist[position[0] - 1][position[1]]  # up

            mapstr = ObjectToStr(sendlist[0])
            for i in range(1,len(sendlist)):
                mapstr += "," + ObjectToStr(sendlist[i])  # convert obejcts to mapsymbol
            print(mapstr)
        else:
            sendlist = maplist
            mapstr = MapListToStr(sendlist)  # convert maplist to mapsymbols

        if position == None:
            position = (0, 0)


        message = f"map:{str(points_collected)}:{send_full_map}:{position[0]},{position[1]}:{mapstr}"
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

        try:
            self.socket_.connect((ipaddress, port))  #connect to server
            self.connected_ = True
            self.socket_.settimeout(0.1)
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


    def SetTimeout(self,timeout):
        self.socket_.settimeout(timeout)  # set new timeout


    def Read(self):
        #read socket message
        try:
            data = self.socket_.recv(10000) #read socket
            data = zlib.decompress(data).decode() #decompress and decode

            #exmine message data type and set data
            if data[0:4] == "map:":  # if message is map

                index = data.find(":", 5) + 1  # find points collected
                self.points_collected_ = int(data[4:index - 1])  # points collected

                index2 = data.find(":", index) + 1  # find is full_map boolean
                self.full_map_ = eval(data[index:index2 - 1]) #convert str to boolean

                index3 = data.find(":", index2) + 1  # find position
                self.position_ = data[index2:index3 - 1].split(',') #position

                self.position_[0] = int(self.position_[0]) #convert str to int
                self.position_[1] = int(self.position_[1])

                self.data_type_ = "map"
                self.data_ = data[index3:]  # read the rest of message


            elif data[0:10] == "startinfo:": #if message is startinfo
                y_x_list = data[10:].split(',') #set map size
                map_height = int(y_x_list[0])  #map size y
                map_width = int(y_x_list[1])  #map size x
                required_score = int(y_x_list[2]) #required_score

                self.data_ = (map_height,map_width,required_score)
                self.data_type_ = "startinfo"

            elif data[0:9] == "gameexit:": #if message is gameexit
                self.data_type_ = "gameexit"
                self.data_ = eval(data[9:]) #string to boolean

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



    def SendMap(self,maplist:list,points_collected:int,send_full_map:bool = True,position:tuple=None):


        #position = (y,x)

        # sends the player's position and adjacent tiles
        if send_full_map == False:

            sendlist = [None, None, None, None, None]

            sendlist[0] = maplist[position[0]][position[1]]  # player
            sendlist[1] = maplist[position[0]][position[1] + 1]  # right
            sendlist[2] = maplist[position[0] + 1][position[1]]  # down
            sendlist[3] = maplist[position[0]][position[1] - 1]  # right
            sendlist[4] = maplist[position[0] - 1][position[1]]  # up

            mapstr = ObjectToStr(sendlist[0])
            print(mapstr)
            for i in range(1,len(sendlist)):
                mapstr += "," + ObjectToStr(sendlist[i])  # convert obejcts to mapsymbol

        else:
            sendlist = maplist
            mapstr = MapListToStr(sendlist)  # convert maplist to mapsymbols

        if position == None:
            position = (0, 0)


        message = f"map:{str(points_collected)}:{send_full_map}:{position[0]},{position[1]}:{mapstr}"
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