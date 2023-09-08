


# Pelin alustus:

Ennen kuin peli pyörii se vaatii alustamista:

Importtaa src kansio:
>> from src import *

Ohjelman joka importta tämän on oltava src kansion ylähakemistossa
(eli se missä on media,src,maps kansiot)




Luo gamedata olio:
>> gamedata = Gamedata(moninpeli:bool,server:bool,font_file_path:str,sfx_is_on:bool):

Jos font_file_path on tyhjä käytetään järjestelmän oletusfonttia, ei suositella.
sfx_is_on merkitsee sitä onko ääni efektit päällä vai pois päältä


Lue kartan tiedot:
>> mapstr, gamedata.map_height_, gamedata.map_width_,gamedata.required_score_,gamedata.level_timelimit_ = ReadMapFile(map_file_path) #moninpelissä client saa nämä tiedot socketin kautta

Aseta mapstr gamedata olioon:
>> SetMap(gamedata, mapstr) #muuttaa merkkijonon pelin kartaksi ja asettaa sen gamedata olioon


Luo pygame ikkuna:
>>  screen = pygame.display.set_mode(resolution:tuple) #create screen

Tätä samaa ikkunaa voidaan käytää esim valikossa

Aseta näyttö gamedata olioon:

>> gamedata.InitDisplay(screen)

Tämä alustaa näyttöön liittyviä tietoja
HUOM!, tämä pitää tehdä aina kartan asettamisen jälkeen, koska se tarvitsee kartan tietoja



Huomaa että itse peli ei sulje tätä ikkunaa koskaan vaan sen voi tehdä halutessaan itse kun pelistä on poistuttu:
>> pygame.display.quit() #close screen






Tämän jälkeen pelin alustus on valmis ja se voidaan aloittaa mikäli se on yksinpeli:
>> Run(gamedata:object,connection:object = None)



# Moninpeli:


## CLIENT:

Luo client olion ja yrittää yhdistää serveriin:
>> connection = Client(ip-osoite,portti,viestien_pakkaus)  #create connection object


Jos yhteys luotu onnistuneesti
voi tarkistaa näin:
>> if connection.connected_: #if the connection was successful

Client lähettää viestin että on valmis aloittamaan pelin ja lähettää liittymis tunnuksen:
>> connection.SendReadyToStart(gameid)



Serveri vastaa tähän lähettämällä aloitusinfon, odotetaan näitä

Joten sockettia pitää lukea:

>> connection.read()

Varmista että pakeetti on aloitusinfo ja lue se:
>> if connection.data_type_ == "startinfo":  #if start info
>
> gamedata.map_height_, gamedata.map_width_,gamedata.required_score_,gamedata.level_timelimit_ = connection.data_ 

Kun viestin tyyppi ja sisältö on luettu pitää puskurin ensimäinen viesti poistaa jotta seuraava viesti päästään lukemaan:

>> connection.BufferNext() 


Heti tämän perään lue kartta
>> connection.Read()  # read messages
> 
>> if connection.data_type_ == "map":  #if message is map

Aseta kartta:
>> SetMap(gamedata, connection.data_)  #set map
>
>> connection.BufferNext() 

Tämän jälkeen pitää pelin sujuvuuden takia asettaa uusi timeout socketille:
>> connection.SetTimeout(0.001) #set new timeout

On tärkeää että serverillä ja clientillä on sama timeout 

Ota viestien pakkaus pois käytöstä:
>> connection.compress_messages_ = False


Pelinalustus on valmis, käynnistä se:
>> Run(gamedata:object,connection:object = None)


## SERVER:
Lataa kartta

Luo Server olio:
Ja odottaa aikakatkaisun verran yhdistääkö joku:

>> connection = Server(port,timeout,viestien_pakkaus) #create connection object

Tarkista yhdistikö joku:
>> if connection.connected_: #if someone connected


Jos yhdisti lue viesti:
 >> connection.Read()  # read messages

Tarkista viestin tyyppi ja tarkista liittymistunnus:

>> if connection.data_type_ == "readytostart":  # if client ready to start the game 
> 
>> if connection.data_ == join_id:
>
>> connection.BufferNext() 

Lähetä clientille kartan koko, vaadittavat pisteet, kartan aikaraja:

>> connection.SendStartInfo(map_height,map_width,required_score,timelimit)  # send start info

Tämän jälkeen pittää lähettää kartta clientille:
>> connection.SendMap(mapstr)  #send map



Soccketille pitää asettaa uusi timeout:
>> connection.SetTimeout(0.001) #set new timeout


Ota viestine pakkaus pois käytöstä:
>> connection.compress_messages_ = False


Pelin alustus on valmis, käynnistä se:
>> Run(gamedata:object,connection:object = None)




# Huomioitavaa
Jos yhteys katkeaa serverin eikä client olioiden Read() metodi eikä viestien lähetys aiheuta virheitä
mutta connected_ atribuutti muutta False muotoon



# Run() funktio

>> Run(gamedata:object,connection:object = None)

Funktio on itse pelin pääfunktio ja paluattaa kaksi bool tyyppistä muuttujaa, ensimmäinen kertoo päästiinkö kartta läpi, ja toinen katkesiko yhteys(singelplayerissä aina False)














