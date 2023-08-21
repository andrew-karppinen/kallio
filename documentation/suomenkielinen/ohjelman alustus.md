


# Pelin alustus:

Ennen kuin peli pyörii se vaatii alustamista:

importtaa src kansio:
>> from src import *

ohjelman joka importta tämän on oltava src kansion ylähakemistossa
(eli se missä on media,src,maps kansiot)




luo gamedata olio:
>> gamedata = Gamedata(moninpeli:bool,server:bool):

lue kartan tiedot:
>> mapstr, gamedata.map_height_, gamedata.map_width_,gamedata.required_score_,gamedata.level_timelimit_ = ReadMapFile(map_file_path) #moninpelissä client saa nämä tiedot socketin kautta

aseta mapstr gamedata olioon:
>> SetMap(gamedata, mapstr) #muuttaa merkkijonon pelin kartaksi ja asettaa sen gamedata olioon


luo pygame ikkuna:
>>  screen = pygame.display.set_mode(resolution:tuple) #create screen

tätä samaa ikkunaa voidaan käytää esim valikossa

aseta näyttö gamedata olioon:

>> gamedata.InitDisplay(screen)

tämä alustaa näyttöön liittyviä tietoja
HUOM!, tämä pitää tehdä aina kartan asettamisen jälkeen, koska se tarvitsee kartan tietoja



huomaa että itse peli ei sulje tätä ikkunaa koskaan vaan sen voi tehdä halutessaan itse kun pelistä on poistuttu:
>> pygame.display.quit() #close screen






tämän jälkeen pelin alustus on valmis ja se voidaan aloittaa mikäli se on yksinpeli:
>> Run(gamedata:object,connection:object = None)



# Moninpeli:


## CLIENT:

luo client olion ja yrittää yhdistää serveriin:
>> connection = Client(ip-osoite,portti,viestien_pakkaus)  #create connection object


jos yhteys luotu onnistuneesti
voi tarkistaa näin:
>> if connection.connected_: #if the connection was successful

client lähettää viestin että on valmis aloittamaan pelin ja lähettää liittymis tunnuksen:
>> connection.SendReadyToStart(gameid)



serveri vastaa tähän lähettämällä aloitusinfon, odotetaan näitä

joten sockettia pitää lukea:

>> connection.read()

varmista että pakeetti on aloitusinfo ja lue se:
>> if connection.data_type_ == "startinfo":  #if start info
>
> gamedata.map_height_, gamedata.map_width_,gamedata.required_score_,gamedata.level_timelimit_ = connection.data_ 

kun viestin tyyppi ja sisältö on luettu pitää puskurin ensimäinen viesti poistaa jotta seuraava viesti päästään lukemaan:

>> connection.BufferNext() 


heti tämän perään lue kartta
>> connection.Read()  # read messages
> 
>> if connection.data_type_ == "map":  #if message is map

aseta kartta:
>> SetMap(gamedata, connection.data_,True)  #set map
>
>> connection.BufferNext() 

tämän jälkeen pitää pelin sujuvuuden takia asettaa uusi timeout socketille:
>> connection.SetTimeout(0.001) #set new timeout

on tärkeää että serverillä ja clientillä on sama timeout 

ota viestien pakkaus pois käytöstä:
>> connection.compress_messages_ = False


Pelinalustus on valmis, käynnistä se:
>> Run(gamedata:object,connection:object = None)


## SERVER:
lataa kartta

luo Server olio:
ja odottaa aikakatkaisun verran yhdistääkö joku:

>> connection = Server(port,timeout,viestien_pakkaus) #create connection object

tarkista yhdistikö joku:
>> if connection.connected_: #if someone connected


jos yhdisti lue viesti:
 >> connection.Read()  # read messages

tarkista viestin tyyppi ja tarkista liittymistunnus:

>> if connection.data_type_ == "readytostart":  # if client ready to start the game 
> 
>> if connection.data_ == join_id:
>
>> connection.BufferNext() 

lähetä clientille kartan koko, vaadittavat pisteet, kartan aikaraja:

>> connection.SendStartInfo(map_height,map_width,required_score,timelimit)  # send start info

tämän jälkeen pittää lähettää kartta clientille:
>> connection.SendMap(mapstr)  #send map



soccketille pitää asettaa uusi timeout:
>> connection.SetTimeout(0.001) #set new timeout


ota viestine pakkaus pois käytöstä:
>> connection.compress_messages_ = False


Pelin alustus on valmis, käynnistä se:
>> Run(gamedata:object,connection:object = None)


# Run() funktio

>> Run(gamedata:object,connection:object = None)

funktio on itse pelin pääfunktio ja paluattaa True/False riippuen päästinkö kartta läpi














