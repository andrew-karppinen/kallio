

mapsymbols = {
    "0":{"name":"empty","command":"None", "command2": None},
    "1":{"name":"local player","command":"gamedata.local_player_","command2": None},
    "2":{"name":"remote player","command":"gamedata.remote_player_", "command2":"gamedata.remote_player_.image_number_ = 0"},
    "2 1":{"name":"remote player image 0","command":"gamedata.remote_player_", "command2":"gamedata.remote_player_.image_number_ = 0"},
    "2 2":{"name":"remote player image 1","command":"gamedata.remote_player_","command2":"gamedata.remote_player_.image_number_ = 1"},
    "2 3":{"name":"remote player image 2","command":"gamedata.remote_player_","command2":"gamedata.remote_player_.image_number_ = 2"},
    "2 4":{"name":"remote player image 3","command":"gamedata.remote_player_","command2":"gamedata.remote_player_.image_number_ = 3"},
    "2 5":{"name":"remote player image 4","command":"gamedata.remote_player_","command2":"gamedata.remote_player_.image_number_ = 4"},
    "3":{"name":"DefaultTile","command":"DefaultTile()","command2": None},
    "4":{"name":"Brick","command":"Brick()","command2": None},
    "5":{"name":"Bedrock","command":"Bedrock()","command2": None},
    "7":{"name":"Goal","command":"Goal()","command2": None},
    "8":{"name":"not falling tnt","command":"Tnt(False)","command2": None},
    "9":{"name":"falling tnt","command":"Tnt(True)","command2": None},

    "10":{"name":"not falling stone","command":"Stone(False)","command2": None},
    "10 1":{"name":"not falling stone direction 1","command":"Stone(False,1)","command2": None},
    "10 2":{"name":"not falling stone direction 2","command":"Stone(False,2)","command2": None},
    "10 3":{"name":"not falling stone direction 3","command":"Stone(False,3)","command2": None},
    "10 4":{"name":"not falling stone direction 4","command":"Stone(False,4)","command2": None},
    "11":{"name":"falling stone","command":"Stone(True)","command2": None},
    "11 1":{"name":"falling stone direction 1","command":"Stone(True,1)","command2": None},
    "11 2":{"name":"falling stone direction 2","command":"Stone(True,2)","command2": None},
    "11 3":{"name":"falling stone direction 3","command":"Stone(True,3)","command2": None},
    "11 4":{"name":"falling stone direction 4","command":"Stone(True,4)","command2": None},

    "14":{"name":"monster which goes to right","command":"Monster(1)","command2": None},
    "15":{"name":"monster which goes to right","command":"Monster(2)","command2": None},
    "16":{"name":"monster which goes to right","command":"Monster(3)","command2": None},
    "17":{"name":"monster which goes to right","command":"Monster(4)","command2": None},

    "18":{"name":"not a falling diamond","command":"Diamond(False)","command2": None},
    "18 1":{"name":"not a falling diamond direction 1","command":"Diamond(False,1)","command2": None},
    "18 2":{"name":"not a falling diamond direction 2","command":"Diamond(False,2)","command2": None},
    "18 3":{"name":"not a falling diamond direction 3","command":"Diamond(False,3)","command2": None},
    "18 4":{"name":"not a falling diamond direction 4","command":"Diamond(False,4)","command2": None},

    "19 1":{"name":"falling diamond direction 1","command":"Diamond(True,1)","command2": None},
    "19 2":{"name":"falling diamond direction 2","command":"Diamond(True,2)","command2": None},
    "19 3":{"name":"falling diamond direction 3","command":"Diamond(True,3)","command2": None},
    "19 4":{"name":"falling diamond direction 4","command":"Diamond(True,4)","command2": None},

    "19":{"name":"falling diamond","command":"Diamond(True)","command2": None},
    "20":{"name":"Door up","command":"Door(1)","command2": None},
    "21":{"name":"Door right","command":"Door(2)","command2": None},
    "22":{"name":"Door down","command":"Door(3)","command2": None},
    "23":{"name":"Door left","command":"Door(4)","command2": None}
}
