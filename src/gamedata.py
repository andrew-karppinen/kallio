

class GameData:
    '''
    local computer data

    '''


    def __init__(self,local_player:object,remote_player:object = None):

        self.local_player_ = local_player
        self.remote_player_ = remote_player