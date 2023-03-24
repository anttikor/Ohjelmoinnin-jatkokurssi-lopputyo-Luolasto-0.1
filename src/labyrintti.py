#tällä luodaan kenttä
import random

def luo_labyrintti(width, height):
    #luodaan lista täytetään nollilla, eli seinää vaan täyteen koko kenttä
    labyrintti = [[0 for x in range(width)] for y in range(height)] 
    #arvotaan aloitus alimmalta riviltä
    start_x = random.randint(5, width - 10)
    labyrintti[height-1][start_x] = 2 #alku 
    
    #ja loppu ylimälle riville
    end_x = random.randint(5, width - 10)
    labyrintti[0][end_x] = 3 #loppu       
    
    #kutsutaan rekursiivista funktiota, mikä "kaivaa" tien läpi seinillä täytetyn kentän
    luo_tie(labyrintti, start_x, 0)
    
    for y in range(width-1):
        labyrintti[0][y] = 0
        labyrintti[height-1][y] = 0    
    
    #laitetaan kentän ympärys ei muokattavaksi
    for i in range(height):
        labyrintti[i][0] = 4
        labyrintti[i][width-1] = 4
        for j in range(width):
            labyrintti[0][j] = 4
            labyrintti[height-1][j] = 4

    
    #tehdään vielä lopusta vähän isompi
    #enemmän luolan sisäänkäynnin/uloskäynnin omainen
    labyrintti[1][end_x-1] = labyrintti[1][end_x] = labyrintti[1][end_x+1] = 1 #tietä
    labyrintti[0][end_x]  = 3 #loppu

    #ulkoasun testaamiseen, ei virallista toiminnallisuutta
    """
    vihollisia = 6 # kuinka monta vihollista kenttään arvotaan
    while vihollisia != 0:        
        x = random.randint(0, width-1)
        y = random.randint(0, height-5)
        if labyrintti[y][x] == 1:
           labyrintti[y][x] = 3
           vihollisia -= 1 
    """
    
    
    return (labyrintti, start_x)

def luo_tie(labyrintti, x, y):
    suunnat = ["ylos", "vasen", "alas", "oikealle"]
    #arvotaan suunnat listan sisältö uudestaan
    #tämä on tärkeää koska tätä funktiota käytetään rekursiivisesti
    #jos ei oikeaa tulosta löydy kutsutaan funktiota uudestaan
    #ja arvotaan suunnat uudestaan
    random.shuffle(suunnat)
    
    for suunta in suunnat:
        if suunta == "ylos":
            if y - 2 <= 0:
                continue
            if labyrintti[y - 2][x] != 0:
                continue
            labyrintti[y - 1][x] = 1
            labyrintti[y - 2][x] = 1
            luo_tie(labyrintti, x, y - 2)
        if suunta == "vasen":
            if x + 2 >= len(labyrintti[0]) - 1:
                continue
            if labyrintti[y][x + 2] != 0:
                continue
            labyrintti[y][x + 1] = 1
            labyrintti[y][x + 2] = 1
            luo_tie(labyrintti, x + 2, y)
        if suunta == "alas":
            if y + 2 >= len(labyrintti) - 1:
                continue
            if labyrintti[y + 2][x] != 0:
                continue
            labyrintti[y + 1][x] = 1
            labyrintti[y + 2][x] = 1
            luo_tie(labyrintti, x, y + 2)
        if suunta == "oikealle":
            if x - 2 <= 0:
                continue
            if labyrintti[y][x - 2] != 0:
                continue
            labyrintti[y][x - 1] = 1
            labyrintti[y][x - 2] = 1
            luo_tie(labyrintti, x - 2, y)

if __name__ == "__main__":
    laby = (luo_labyrintti(64, 48))
    with open("labyrintti.txt", "w") as f:
        f.write(str(laby))     