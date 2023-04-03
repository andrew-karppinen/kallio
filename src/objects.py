


class Player:
    def __init__(self, image,local_player:bool = True):
        self.image_ = image
        self.local_player_ = local_player



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


    @property
    def image_(self):
        return (Stone.image)


class Tnt:
    image = None
    def __init__(self,drop:bool=False):
        self.drop_ = drop  # if currently dropping



    @property
    def image_(self):
        return (Tnt.image)



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