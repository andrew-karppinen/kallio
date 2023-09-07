import pygame


class Player:
    def __init__(self,local_player:bool = True):
        self.images_ = []
        self.local_player_ = local_player
        self.animated_ = False
        self.image_number_ = 0
        #0 = no move,1 left1, 2 = left2, 3 = right1, 4 = right2

    def SetImage(self,nomove,move1 = None,move2 = None):
        '''
        in the pictures the character is moving to the right!

        automatically create a mirror images

        images must be pygame surface object!
        '''

        if move1 != None and move2 != None:
            move3 = pygame.transform.flip(move1,True,False)
            move4 = pygame.transform.flip(move2,True,False)
            self.images_ = [nomove,move1,move2,move3,move4]
            self.animated_ = True
        else:
            self.images_ = [nomove, move1, move2]
            self.animated_ = False
    def ScaleImages(self,tile_size=50):
        self.images_[0] = pygame.transform.scale(self.images_[0],(tile_size,tile_size))

        if self.images_[1] != None:
            self.images_[1] = pygame.transform.scale(self.images_[1], (tile_size, tile_size))
            self.images_[3] = pygame.transform.scale(self.images_[3], (tile_size, tile_size))
        if self.images_[2] != None:
            self.images_[2] = pygame.transform.scale(self.images_[2], (tile_size, tile_size))
            self.images_[4] = pygame.transform.scale(self.images_[4], (tile_size, tile_size))


    def AnimateToRight(self):
        if self.animated_ == True:
            if self.image_number_ == 1:
                self.image_number_ = 2
            else:
                self.image_number_ = 1

    def AnimateToLeft(self):
        if self.animated_ == True:
            if self.image_number_ == 3:
                self.image_number_ = 4
            else:
                self.image_number_ = 3

    def AnimateToHorizontal(self):
        if self.animated_ == True:
            if self.image_number_ == 0 or self.image_number_ == 1 or self.image_number_ == 2:
                self.AnimateToRight()
            else:
                self.AnimateToLeft()


    @property
    def image_(self):

        if self.images_[self.image_number_] != None:
            return(self.images_[self.image_number_])

        else:
            return self.images_[0] #if no animation




class DefaultTile:
    #class variables:
    image = None

    def SetImage(image:pygame.surface):
        DefaultTile.image = image

    def ScaleImages(tile_size:int):
        DefaultTile.image = pygame.transform.scale(DefaultTile.image, (tile_size, tile_size))

    def __init__(self):
        pass

    @property
    def image_(self):
        return (DefaultTile.image)


class Stone:
    #class variables:
    image_left = None
    image_right = None
    image_up = None
    image_down = None

    def SetImage(image:pygame.surface):

        #rotate images
        Stone.image_up = image
        Stone.image_right = pygame.transform.rotate(image,-90)
        Stone.image_left = pygame.transform.rotate(image,90)
        Stone.image_down = pygame.transform.rotate(image,180)

    def ScaleImages(tile_size:int):
        Stone.image_left = pygame.transform.scale(Stone.image_left, (tile_size, tile_size))
        Stone.image_right = pygame.transform.scale(Stone.image_right, (tile_size, tile_size))
        Stone.image_up = pygame.transform.scale(Stone.image_up, (tile_size, tile_size))
        Stone.image_down = pygame.transform.scale(Stone.image_down, (tile_size, tile_size))
    def __init__(self, drop:bool,direction:int = 1):
        self.drop_ = drop
        self.direction_ = direction  # 1 = up, 2 = right, 3 = down, 4 = left


    def Rotate(self,direction:int):
        #direction = 1 or 2
        #1 = clockwise
        #2 = counterclockwise

        if direction == 1:
            if self.direction_ == 4:
                self.direction_ = 1
            else:
                self.direction_ += 1

        elif direction == 2:
            if self.direction_ == 1:
                self.direction_ = 4
            else:
                self.direction_ -= 1


    @property
    def image_(self):
        if self.direction_ == 1:
            return(Stone.image_up)
        elif self.direction_ == 2:
            return(Stone.image_right)
        elif self.direction_ == 3:
            return (Stone.image_down)
        elif self.direction_ == 4:
            return(Stone.image_left)



class Diamond:
    #class variables:
    image_left = None
    image_right = None
    image_up = None
    image_down = None


    def SetImage(image:pygame.surface):
        Diamond.image = image
        #rotate images
        Diamond.image_up =  image
        Diamond.image_right = pygame.transform.rotate(Diamond.image,-90)
        Diamond.image_left = pygame.transform.rotate(Diamond.image,90)
        Diamond.image_down = pygame.transform.rotate(Diamond.image,180)

    def ScaleImages(tile_size:int):
        Diamond.image_left = pygame.transform.scale(Diamond.image_left, (tile_size, tile_size))
        Diamond.image_right = pygame.transform.scale(Diamond.image_right, (tile_size, tile_size))
        Diamond.image_up = pygame.transform.scale(Diamond.image_up, (tile_size, tile_size))
        Diamond.image_down = pygame.transform.scale(Diamond.image_down, (tile_size, tile_size))

    def __init__(self, drop:bool,direction:int = 1):
        self.drop_ = drop
        self.direction_ = direction  # 1 = up, 2 = right, 3 = down, 4 = left


    def Rotate(self,direction:int):
        #direction = 1 or 2
        #1 = clockwise
        #2 = counterclockwise

        if direction == 1:
            if self.direction_ == 4:
                self.direction_ = 1
            else:
                self.direction_ += 1

        if direction == 2:
            if self.direction_ == 1:
                self.direction_ = 4
            else:
                self.direction_ -= 1


    @property
    def image_(self):
        if self.direction_ == 1:
            return(Diamond.image_up)
        elif self.direction_ == 2:
            return(Diamond.image_right)
        elif self.direction_ == 3:
            return (Diamond.image_down)
        elif self.direction_ == 4:
            return(Diamond.image_left)



class Tnt:
    #class variables:
    image = None

    def SetImage(image:pygame.surface):
        Tnt.image = image
    def ScaleImages(tile_size:int):
        Tnt.image = pygame.transform.scale(Tnt.image, (tile_size, tile_size))
    def __init__(self,drop:bool=False):
        self.drop_ = drop  # if currently dropping



    @property
    def image_(self):
        return (Tnt.image)



class Explosion:
    #class variables:
    images = []

    def SetImage(image1,image2,image3,image4):
        Explosion.images = [image1,image2,image3,image4]

    def ScaleImages(tile_size:int):

        for i in range(len(Explosion.images)):
            Explosion.images[i] = pygame.transform.scale(Explosion.images[i], (tile_size, tile_size))
    def __init__(self,counter:int = 0):
        self.counter_ = counter

    @property
    def image_(self):
        return(Explosion.images[self.counter_//4])

class Bedrock:
    #class variables:
    image = None

    def SetImage(image:pygame.surface):
        Bedrock.image = image

    def ScaleImages(tile_size:int):
        Bedrock.image = pygame.transform.scale(Bedrock.image, (tile_size, tile_size))

    def __init__(self):
        pass

    @property
    def image_(self):
        return (Bedrock.image)

class Brick:
    #class variables:
    image = None

    def SetImage(image:pygame.surface):
        Brick.image = image

    def ScaleImages(tile_size:int):
        Brick.image = pygame.transform.scale(Brick.image, (tile_size, tile_size))

    def __init__(self):
        pass

    @property
    def image_(self):
        return (Brick.image)


class Goal:
    #class variables:
    image_open = None
    image_close = None

    goal_is_open = False #if required score have been collected

    def SetImage(goal_open,goal_close):
        Goal.image_open = goal_open
        Goal.image_close = goal_close

    def ScaleImages(tile_size:int):
        Goal.image_open = pygame.transform.scale(Goal.image_open, (tile_size, tile_size))
        Goal.image_close = pygame.transform.scale(Goal.image_close, (tile_size, tile_size))

    def __init__(self):
        pass

    @property
    def image_(self):

        if Goal.goal_is_open == True:
            return (Goal.image_open)
        else:
            return (Goal.image_close)





class Monster:
    #class variables:
    image1 = None
    image2 = None
    def SetImage(image1:pygame.surface,image2:pygame.surface=None):
        Monster.image1 = image1
        Monster.image2 = image2

    def ScaleImages(tile_size:int):
        Monster.image1 = pygame.transform.scale(Monster.image1,(tile_size,tile_size))
        if Monster.image2 != None: #if image 2 is exist
            Monster.image2 = pygame.transform.scale(Monster.image2, (tile_size, tile_size))

    def __init__(self,direction):
        self.direction_ = direction #1 = right, 2 = down, 3 = left, 4= up
        self.image_number_ = 1 #1, 2

        self.moved_during_this_function_call_ = False




    @property
    def image_(self):
        if self.image_number_ == 1:
            return(Monster.image1)
        elif self.image_number_ == 2:
            return (Monster.image2)



class Door:
    image_left = None
    image_right = None
    image_up = None
    image_down = None


    def SetImage(image_right,image_down,image_left,image_up):
        Door.image_right = image_right
        Door.image_up = image_up
        Door.image_left = image_left
        Door.image_down = image_down

    def ScaleImages(tile_size:int):
        Door.image_left = pygame.transform.scale(Door.image_left, (tile_size, tile_size))
        Door.image_right = pygame.transform.scale(Door.image_right, (tile_size, tile_size))
        Door.image_up = pygame.transform.scale(Door.image_up, (tile_size, tile_size))
        Door.image_down = pygame.transform.scale(Door.image_down, (tile_size, tile_size))

    def __init__(self, direction):
        self.direction_ = direction  # 1 = up, 2 = right, 3 = down, 4 = left


    @property
    def image_(self):
        if self.direction_ == 1:
            return(Door.image_up)
        elif self.direction_ == 2:
            return(Door.image_right)
        elif self.direction_ == 3:
            return (Door.image_down)
        elif self.direction_ == 4:
            return(Door.image_left)
