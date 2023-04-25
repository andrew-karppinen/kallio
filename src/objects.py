import pygame


class Player:
    def __init__(self, image,local_player:bool = True):
        self.image_ = image
        self.local_player_ = local_player

        self.position_y_ = None
        self.position_x_ = None


class DefaultTile:
    image = None

    def __init__(self):
        pass

    @property
    def image_(self):
        return (DefaultTile.image)


class Stone:
    image = None

    def __init__(self,drop:bool=False):
        self.drop_ = drop  # if currently dropping
        self.angle_ = 0

    @property
    def image_(self):

        return pygame.transform.rotate(Stone.image,self.angle_) #Rotate the image and return it



    def Rotate(self,direction:int):
        #direction = 1 or 2
        #1 = clockwise
        #2 = counterclockwise

        if direction == 1:
            self.angle_ -= 90
        if direction == 2:
            self.angle_ += 90




class Tnt:
    image = None
    def __init__(self,drop:bool=False):
        self.drop_ = drop  # if currently dropping



    @property
    def image_(self):
        return (Tnt.image)



class Explosion:
    image = None

    def __init__(self,counter:int = 0):
        self.counter_ = counter #1,2

    @property
    def image_(self):
        return (Explosion.image)

class Bedrock:
    image = None

    def __init__(self):
        pass

    @property
    def image_(self):
        return (Bedrock.image)

class Brick:
    image = None



    def __init__(self):
        pass

    @property
    def image_(self):
        return (Brick.image)


class Goal:
    image = None

    def __init__(self):
        pass

    @property
    def image_(self):
        return (Goal.image)

class Diamond:
    image = None

    def __init__(self):
        pass


    @property
    def image_(self):
        return (Diamond.image)



class Monster:
    image = None

    def __init__(self,direction):
        self.direction_ = direction #1 = right, 2 = down,  3 = left, 4 = up


    @property
    def image_(self):
        return (Monster.image)