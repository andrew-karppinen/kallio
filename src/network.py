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

        self.compress_messages_ = False #compress sent message and decompress incoming messages


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


        #data_type_: "map","readytostart","gameexit","restartlevel",None,action, "other"

        #data_:
        #map = str
        #action = str
        #points:int
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
            if self.compress_messages_ == True:
                data = zlib.decompress(data).decode()  # decompress and decode
            else:
                data = data.decode()  # only decode

            if len(data) == 0: #if no message or message is empty
                self.data_ = None
                self.data_type_ = None
            else:
                # exmine message data type and set data
                if data[0:7] == "action:":
                    self.data_type_ = "action"
                    self.data_ = data[7:] #read the rest of message

                elif data[0:7] == "points:":
                    self.data_type_ = "points"
                    self.data_ = int(data[7:]) #read the rest of message

                elif data[0:4] == "map:":  # if message is map
                    self.data_type_ = "map"
                    self.data_ = data[4:] #read the rest of message


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

    def __SendMessage(self, message:str):  # private method

        if self.compress_messages_ == True:
            self.client_.send(zlib.compress(message.encode()))  # compress and send message
        else:
            self.client_.send(message.encode())  # send message without compress

    def SendMap(self,mapstr:str):
        #send full map

        maplist = mapstr.split(",") #convert str to list

        find_1 = maplist.index("1") #find local player position
        find_2 = maplist.index("2") #find remoteplayer position

        #change local player --> remote player
        #and remote player --> local player
        maplist[find_1] = "2"
        maplist[find_2] = "1"


        mapstr = ",".join(maplist) #connvert list to str

        message = f"map:{mapstr}"
        self.__SendMessage(message) #send message


    def SendMove(self,right:bool,left:bool,up:bool,down:bool,door:bool=False):
        '''
        send action:
        a player's moves
        '''

        if right == True:
            message = f"action:moveright:{int(door)}"
        elif down == True:
            message = f"action:movedown:{int(door)}"
        elif left == True:
            message = f"action:moveleft:{int(door)}"
        elif up == True:
            message = f"action:moveup:{int(door)}"

        self.__SendMessage(message) #send message


    def SendPush(self,right:bool,left:bool):
        '''
        send action:
        push object
        '''
        if right == True:
            message = "action:pushright"
        elif left == True:
            message = "action:pushleft"

        self.__SendMessage(message) #send message


    def SendRemove(self,right:bool,left:bool,up:bool,down:bool):
        '''
        send  action:
        remove next to player
        '''
        if right == True:
            message = "action:removeright"
        elif down == True:
            message = "action:removedown"
        elif left == True:
            message = "action:removeleft"
        elif up == True:
            message = "action:removeup"

        self.__SendMessage(message) #send message

    def SendCollectedPoints(self,points_collected):

        message=f"points:{points_collected}"
        self.__SendMessage(message) #send message



    def SendStartInfo(self,map_height:int,map_width:int,required_score:int=0):
        '''
        a message about the start of the game
        send map size y,z and required_score
        '''

        message = f"startinfo:{str(map_height)},{str(map_width)},{str(required_score)}"

        self.__SendMessage(message) #send message


    def SendGameExit(self,win:bool = False): #if game exit
        #win False = game over, True = level complete
        message = "gameexit:" + str(win)
        self.__SendMessage(message) #send message

    def SendRestartLevel(self):
        message = "restartlevel"
        self.__SendMessage(message) #send message

    def CloseSocket(self):
        self.socket_.close()






class Client:
    def __init__(self,ipaddress:str,port:int):
        self.socket_ = socket.socket()  # create socket object
        self.socket_.settimeout(5)
        self.ipaddress_ = ipaddress
        self.port_ = port
        self.error_mesage_ = ""

        self.compress_messages_ = False #compress sent message and decompress incoming messages

        try: #try connect to server
            self.socket_.connect((ipaddress, port))
            self.connected_ = True
            self.socket_.settimeout(0.1)
        except Exception as message:
            self.error_mesage_ = message
            self.connected_ = False


        self.data_ = None #received messages
        self.data_type_ = None

        #data_type_: "map","startinfo","gameexit","restartlevel",None,action, "other"

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

            if self.compress_messages_ == True:
                data = zlib.decompress(data).decode() #decompress and decode
            else:
                data = data.decode() #only decode

            #exmine message data type and set data

            if data[0:7] == "action:":
                self.data_type_ = "action"
                self.data_ = data[7:]  # read the rest of message

            elif data[0:7] == "points:":
                self.data_type_ = "points"
                self.data_ = int(data[7:])  # read the rest of message

            elif data[0:4] == "map:":  # if message is map
                self.data_type_ = "map"
                self.data_ = data[4:]  # read the rest of message



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


    def __SendMessage(self,message:str): #private method

        if self.compress_messages_ == True:
            self.socket_.send(zlib.compress(message.encode()))  # compress and send message
        else:
            self.socket_.send(message.encode())  #send message without compress

    def SendReadyToStart(self,check_number:str):
        message = f"readytostart:{check_number}"

        self.__SendMessage(message) #send message


    def SendMove(self,right:bool,left:bool,up:bool,down:bool,door:bool=False):
        '''
        send action:
        a player's moves
        '''

        if right == True:
            message = f"action:moveright:{int(door)}"
        elif down == True:
            message = f"action:movedown:{int(door)}"
        elif left == True:
            message = f"action:moveleft:{int(door)}"
        elif up == True:
            message = f"action:moveup:{int(door)}"

        self.__SendMessage(message)  # send message
    def SendPush(self,right:bool,left:bool):
        '''
        send action:
        push object
        '''

        if right == True:
            message = "action:pushright"
        elif left == True:
            message = "action:pushleft"

        self.__SendMessage(message)  # send message

    def SendRemove(self,right:bool,left:bool,up:bool,down:bool):
        '''
        send action:
        remove next to player
        '''

        if right == True:
            message = "action:removeright"
        elif down == True:
            message = "action:removedown"
        elif left == True:
            message = "action:removeleft"
        elif up == True:
            message = "action:removeup"

        self.__SendMessage(message)  # send message

    def SendCollectedPoints(self,points_collected):
        message=f"points:{points_collected}"
        self.__SendMessage(message)  # send message


    def SendGameExit(self,win:bool = False): #if game exit
        #win False = game over, True = level complete
        message = "gameexit:" + str(win)
        self.__SendMessage(message)  # send message


    def SendRestartLevel(self):
        message = "restartlevel"
        self.__SendMessage(message)  # send message


    def CloseSocket(self):
        self.socket_.close()