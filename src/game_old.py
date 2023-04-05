import pygame

from random import randint


from objects import * #import classes

from network import Network



class Game:
    def __init__(self,map:list): #constructor
        ukkelikuva = pygame.image.load("media/ukkeli.png") #load images
        palikkakuva = pygame.image.load("media/hiekka.png")
        kivikuva = pygame.image.load("media/kivi.png")

        #set image
        DefaultTile.image = palikkakuva
        Stone.image_ = kivikuva

        self.player_position_y_ = 0
        self.player_position_x_ = 0
        self.player1_ = Player(ukkelikuva) #create Player
        self.player2_ = Player(ukkelikuva,False) #create remote player
        self.collision_list_ = [Player]

        self.map_size_ = [0,0] #y,x
        self.CreateMap(map)
        #not visible here
        #self.map_

        

        self.screen = pygame.display.set_mode((1000, 700)) #create screen
        pygame.display.set_caption("pygame") #named screen




    def CreateMap(self,map):

        '''
        Crete map

        example:
        1,1,1,1,1,2,2,1,1
        1,1,1,1,1,1,1,1,1
        1,1,1,1,1,1,1,1,2
        1,1,1,1,1,2,2,1,1
        1,1,1,1,1,1,1,1,1
        1,1,1,1,1,1,1,1,2

        1 = default tile
        2 = Stone
        3 = player 1
        4 = remote player
        '''


        self.map_size_[0] = len(map) #map size
        self.map_size_[1] = len(map[1])

        self.map_ = [[None for i in range(self.map_size_[1])] for j in range(self.map_size_[0])]  #create lis



        for i in range(len(self.map_)): #create map
            for j in range(len(self.map_[i])):
                #i = y, j = x

                if map[i][j] == 1:
                    self.map_[i][j] = DefaultTile()
                elif map[i][j] == 2: #stone
                    self.map_[i][j] = Stone()
                elif map[i][j] == 3: #if player 1
                    self.map_[i][j] = self.player1_
                    self.player_position_x_,self.player_position_y_ = j,i
                elif map[i][j] == 4:  # if remote player
                    self.map_[i][j] = self.player2_







    def Draw(self):
        self.screen.fill((0,0,0)) #fill screen in black

        for i in range(len(self.map_)):
            for j in range(len(self.map_[i])):

                if self.map_[i][j] != None:
                    self.screen.blit(self.map_[i][j].image_, (j * 50, i * 50))

        pygame.display.flip() #update screen

    def CollisionCheck(self,position_y,position_x):
        #return True = Collision, False = no collision

        if type(self.map_[position_y][position_x]) in self.collision_list_:
            return True #collision
        else:
            return  False #no collision




    def Move(self,direction):
        #direction 1= right, 2 = left 3 = up 4 = down
        
        if direction == 1: #move right
            if self.player_position_x_ + 1 < len(self.map_[1]):#if map not end

                if not self.CollisionCheck(self.player_position_y_,self.player_position_x_+1): #collision check

                    #if there is a stone next to it
                    if type((self.map_[self.player_position_y_][self.player_position_x_ +1])) == Stone:

                        if len(self.map_[1]) > self.player_position_x_+2: #if map not end
                            if self.map_[self.player_position_y_][self.player_position_x_ +2] == None: #if empty next to the stone
                                self.map_[self.player_position_y_][self.player_position_x_ + 2] = Stone() #push stone
                            else:
                                return #exit method
                        else:
                            return #exit method


                    self.map_[self.player_position_y_][self.player_position_x_] = None
                    self.player_position_x_ += 1
                    self.map_[self.player_position_y_][self.player_position_x_] = self.player1_

        elif direction == 2: #move left
            if self.player_position_x_ - 1 >= 0:#if map not end


                #if there is a stone next to it
                if type((self.map_[self.player_position_y_][self.player_position_x_ -1])) == Stone:
                    if self.player_position_x_-2 >= 0: #if map not end
                        if self.map_[self.player_position_y_][self.player_position_x_ -2] == None: #if empty next to the stone
                            self.map_[self.player_position_y_][self.player_position_x_ - 2] = Stone() #push stone
                        else:
                            return #exit method
                    else:
                        return #exit method

                self.map_[self.player_position_y_][self.player_position_x_] = None
                self.player_position_x_ -= 1
                self.map_[self.player_position_y_][self.player_position_x_] = self.player1_


        elif direction == 3: #move up
            if self.player_position_y_ - 1 >=  0: #if map not end

                if type(self.map_[self.player_position_y_ - 1][self.player_position_x_]) not in [Stone]: #if not collision


                    self.map_[self.player_position_y_][self.player_position_x_] = None
                    self.player_position_y_ -= 1
                    self.map_[self.player_position_y_][self.player_position_x_] = self.player1_

        elif direction == 4: #move down
            if self.player_position_y_ + 1 <  len(self.map_):#if map not end
                if type(self.map_[self.player_position_y_ + 1][self.player_position_x_]) not in [Stone]: #if not collision

                    self.map_[self.player_position_y_][self.player_position_x_] = None
                    self.player_position_y_ += 1
                    self.map_[self.player_position_y_][self.player_position_x_] = self.player1_




    def StoneGravity(self):

        for i in range(len(self.map_)-1,0,-1):
            for j in range(len(self.map_[i])-1,0,-1):
                #i = y, j = x

                if type(self.map_[i][j]) == Stone:

                    if len(self.map_) > i + 1:  # if map not end
                        if self.map_[i][j].drop_ == True:

                            if type(self.map_[i+1][j]) == Player:
                                print("PÖÖÖ!!!")
                                exit()




                        if self.map_[i+1][j] == None: #if nothing in under the stone

                            self.map_[i][j].drop_ = True
                            self.map_[i+1][j] = self.map_[i][j]
                            self.map_[i][j] = None
                            continue
                        else:
                            self.map_[i][j].drop_ = False
                    else:
                        self.map_[i][j].drop_ = False



    def Run(self):

        fpslimit = pygame.time.Clock() #fps limit
        movelimit = 0

        #moving variables
        left = False
        right = False
        up = False
        down = False

        while True: #main loop
        #event loop
            for event in pygame.event.get():
                #read keys
                if event.type == pygame.KEYDOWN:
                    if event.key  == pygame.K_UP:
                        up = True
                    if event.key == pygame.K_DOWN:
                        down = True
                    if event.key == pygame.K_LEFT:
                        left = True
                    if event.key == pygame.K_RIGHT:
                        right = True


                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        left = False
                    if event.key == pygame.K_RIGHT:
                        right = False
                    if event.key == pygame.K_UP:
                        up = False
                    if event.key == pygame.K_DOWN:
                        down = False

                if event.type == pygame.QUIT:
                    exit() #close program


            #stone gravity
            if pygame.time.get_ticks() > movelimit + 95:
                movelimit = pygame.time.get_ticks()
                self.StoneGravity()


            #can only move in one direction at a time
            movecheck = [down,up,left,right]
            if movecheck.count(True) == 1:

                if right:
                    self.Move(1)
                if left:
                    self.Move(2)
                if up:
                    self.Move(3)
                if down:
                    self.Move(4)



            self.Draw()
            fpslimit.tick(12)



if __name__ == "__main__":


    map = [
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,4,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,3,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]




    yhteys = Network("a")



    peli = Game(map)


    yhteys.Send(peli.map_)

    #peli.Run()






