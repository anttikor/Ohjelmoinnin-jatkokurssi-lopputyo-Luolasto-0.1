import random
import pygame
import math
import labyrintti # tämän tiedoston alta löytyy labyrintin luova funktio

# kuvat.py sisältää "tyhmiä" funktioita, mitkä palauttaa vain kaksiulotteisen listan mihin olen tehnyt RGB arvot
# spritet.py "ohjelmalla" ja copypastannut arvot spritet.py ohjelman luomista txt-tiedostoista noihin tyhmiin funktioihin
# HUOM!!! et tarvitse spritet.py tämän pelin ajamiseen, mutta jätin sen mukaan jos joku haluaa testailla
# tai perehtyä siihen mitä olen tehnyt tarkemmin
import kuvat 



# perusmuotoinen objekti mitä kopioidaan vähän kaikkeen
class Objekti(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.leveys = self.korkeus = skaala_px
        self.rect = pygame.Rect(x, y, self.leveys, self.korkeus)

class Pelaaja(Objekti):    
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rect = pygame.Rect(x, y, self.leveys, self.korkeus)
    
    def liiku(self, dx, dy):        
        # Liikutaan molemmilla akseleilla erikseen. Seurataan törmäystä molemmilla kerroilla
        if dx != 0:
            self.liiku_yhdella_akselilla(dx, 0)
        if dy != 0:
            self.liiku_yhdella_akselilla(0, dy)
    
    def liiku_yhdella_akselilla(self, dx, dy):        
        # siirretään pelaajaa
        self.rect.x += dx
        self.rect.y += dy

        # Jos törmätään seinään, niin palataan törmätyn seinän törmäyskohtaan
        for seina in seinat:
            if self.rect.colliderect(seina.rect):
                if dx > 0: # Liikutaan oikealle, törmätään seinän vasempaan reunaan
                    self.rect.right = seina.rect.left
                if dx < 0: # Liikutaan vasemmalle, törmätään seinän oikeaan reunaan
                    self.rect.left = seina.rect.right
                if dy > 0: # Liikutaan alas, törmätään seinän ylä reunaan
                    self.rect.bottom = seina.rect.top
                if dy < 0: # Liikutaan ylös, törmätään seinän ala reunaan
                    self.rect.top = seina.rect.bottom

class Seina(Objekti):    
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rect = pygame.Rect(x, y, self.leveys, self.korkeus)

class Loppu(Objekti):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rect = pygame.Rect(x, y, self.leveys, self.korkeus)

class Kolikko(Objekti):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rect = pygame.Rect(x, y, self.leveys, self.korkeus)

class Vihollinen(Objekti):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rect = pygame.Rect(x, y, self.leveys, self.korkeus)
    
    def update(self, pXY): #pXY on pelaajan koordinaatit tuple
        etaisyydet = [] # luodaan tyhjä lista
        for dx in [-1, 0, 1]: #vihollinen voi liikkua x-akselilla -1, 0 tai 1, käydään kaikki läpi
            for dy in [-1, 0, 1]: #vihollinen voi liikkua y-akselilla -1, 0 tai 1, käydään kaikki läpi
                x1, y1 = pXY #pelaajan koordinaatit
                x2, y2 = self.rect.center[0]+dx, self.rect.center[1]+dy #vihollisen koordinaatit
                etaisyys = math.sqrt((x2 - x1)**2 + (y2 - y1)**2) # lasketaan euklidinen etäisyys
                # voisi laskea myös seuraavalla, koodilla mikä olisi selkeämpi, mutta math.dist
                # ei ole pythonin standardi-kirjastoja
                #etaisyys = math.dist((pXY), (self.rect.center[0]+dx, self.rect.center[1]+dy))
                etaisyydet.append((etaisyys, dx, dy)) # laitetaan laskettu etäisyys, sekä koordinaatit tupleen, mikä lisätään listaan
        etaisyydet = sorted(etaisyydet, key=lambda x: x[0]) #järjestetään listan tuplet tuplejen ensimmäisen tiedon,
                                                            #eli euklidisen etäisyyden mukaan
        if etaisyydet[0][0] <= skaala_px * 3: # tarkistetaan onko etäisyys 3 ruutua tai alle
            #jos oli, niin siirretään lohikäärmettä siihen suuntaan mikä on suorin reitti
            self.rect.center = (self.rect.center[0] + etaisyydet[0][1], self.rect.center[1] + etaisyydet[0][2])


# Alustetaan pygamen asioita
pygame.init()
kello = pygame.time.Clock()
pygame.display.set_caption("Luolasto 0.1!")

# pelin muuttujia
kentta = 1
elamat = 3
raha = 0
nopeus = 5
arvottavat_kolikot = 10 # kuinka monta kolikkoa arvotaan jokaisen kentän alussa
skaala_px = 30 # kuinka monta pikseliä* XY on yksi kentän "palikka" #jos tätä muuttaa niin pitää muuallakin pelissä sitten puukottaa koodia
# labyrintin_koko # X * Y # minimi arvot millä toimii: X=15 (silloin jää toisiksi alin teksti piiloon) ja y=14
# jos näitä arvoja alkaa muuttamaan enemmän, niin kannattaa tarkistaa miten pelaajan aloituskohta määrittyy
labyrintin_koko = (20, 20) #aika hyvät arvot tasapainoiseen peliin
running = True

koko = (labyrintin_koko[0]*skaala_px, labyrintin_koko[1]*skaala_px + 3*skaala_px) # tuple mikä on laskettu määritellystä 
naytto = pygame.display.set_mode(koko) # näyttö edellisen muuttujan perusteella

# alustettavat luokat, eli mitä on vain yksi kpl
loppu = Loppu(0, 0)
pelaaja = Pelaaja(0, 0) # luodaan pelaaja

# alustettavat sprite ryhmät, eli ryhmät mihin asetetaan 
kolikot = pygame.sprite.Group()
viholliset = pygame.sprite.Group()
seinat = pygame.sprite.Group()
font = pygame.font.Font(None, 20)

#fog of war/näkökenttä
maski = pygame.Surface((koko[0],koko[1]))
maski.fill((0, 0, 0))
maski.set_colorkey((255, 255, 255))
nakokentta = 120 #oikea aloitusarvo 120
tee_maski = True

#luodaan uusi kenttä
def uusi_kentta():
    # kutsutaan tiedostossa labyrintti.py olevaa funktiota, mikä palauttaa labyrintin ja sen alkukohdan
    labyrintti_palautus = labyrintti.luo_labyrintti(labyrintin_koko[0],labyrintin_koko[1])
    
    
    seinat.empty() # tyhjennetään vanha sprite group, mihin on tallennettu seinät
    # lisätään seinät, seinät sprite grouppiiin
    x = y = 0
    for row in labyrintti_palautus[0]:
        for col in row:
            if col == 0:
                seinat.add(Seina(x, y))                
            if col == 4:
                seinat.add(Seina(x, y))        
            if col == 3:
                loppu.rect.topleft = (x,y)
            x += 30
        y += 30
        x = 0
        
    # määritetään pelaajan aloituspaikka
    pelaaja.rect.x = labyrintti_palautus[1]*30
    pelaaja.rect.y = koko[1]-(30 * 5)

    
    kolikot.empty() # tyhjennetään vanha sprite group, mihin on tallennettu kolikot
    a_kolikot = arvottavat_kolikot
    while a_kolikot != 0:
        x = random.randint(1, (labyrintin_koko[0])-2)
        y = random.randint(1, (labyrintin_koko[1])-3)
        if labyrintti_palautus[0][y][x] == 1:
            kolikko = Kolikko(x * 30, y * 30)
            kolikot.add(kolikko)
            a_kolikot -= 1
    
    viholliset.empty() # tyhjennetään vanha sprite group, mihin on tallennettu viholliset
    arvottavat_viholliset = kentta # arvotaan yhtämonta vihollista kuin missä kentässä ollaan
    while arvottavat_viholliset != 0:
        x = random.randint(1, (labyrintin_koko[0])-2)
        y = random.randint(1, (labyrintin_koko[1])-3)
        if labyrintti_palautus[0][y][x] == 1:
            vihollinen = Vihollinen(x * 30, y * 30)
            viholliset.add(vihollinen)
            arvottavat_viholliset -= 1

uusi_kentta() # viimeinen alustuksen käsky, eli kutsutaan juuri äsken tehtyä funktiota

while running:    
    kello.tick(30)                  
    
    # näppäimistön seuraus kun näppäintä painetaan pohjassa
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        pelaaja.liiku(nopeus*-1, 0)
    if key[pygame.K_RIGHT]:
        pelaaja.liiku(nopeus, 0)
    if key[pygame.K_UP]:
        pelaaja.liiku(0, nopeus*-1)
    if key[pygame.K_DOWN]:
        pelaaja.liiku(0, nopeus)

    # muut seurattavat tapahtumat ja näppäintapahtumat, kuten sulkeminen ja ostamiset
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
            if raha > 0:
                elamat += 1
                raha -= 1  
        if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
            nakokentta += skaala_px
            raha -= 1 
          

    # kun elämät on lopussa, pelaaja kuolee
    if elamat == 0:
        running = False

    # kun pelaajan hahmo osuu maalin oveen suoritetaan
    if pelaaja.rect.colliderect(loppu.rect):
        tee_maski = True # asetetaan lippu, että voidaan renderöidä uusi peittomaski
        kentta += 1 # merkitään kentäksi seuraava        
        uusi_kentta() #kutsutaan uuden kentän luovaa funktiota
    
    # tämä renderöi seinät
    for seina in seinat:
        matriisi = kuvat.stone()
        for i in range(len(matriisi)):
            for j in range(len(matriisi[i])):
                r, g, b = matriisi[i][j]
                if r == g == b == 0:
                    pass
                else:
                    pygame.draw.rect(naytto, (r, g, b), (seina.rect.topleft[0] + i*3, seina.rect.topleft[1] + j*3, 3, 3))       
    
    # tämä renderöi oven, mikä on maali
    matriisi = kuvat.ovi()
    for i in range(len(matriisi)):
        for j in range(len(matriisi[i])):
            r, g, b = matriisi[i][j]
            if r == g == b == 0:
                pass
            else:
                pygame.draw.rect(naytto, (r, g, b), (loppu.rect.left + i*3, loppu.rect.top + j*3, 3, 3))    

    # tämä renderöi kolikot
    for kolikko in kolikot:
        if pelaaja.rect.colliderect(kolikko.rect):
            kolikot.remove(kolikko) 
            raha += 1       
        matriisi = kuvat.coin()
        for i in range(len(matriisi)):
            for j in range(len(matriisi[i])):
                r, g, b = matriisi[i][j]
                if r == g == b == 0:
                    pass
                else:
                    pygame.draw.rect(naytto, (r, g, b), (kolikko.rect.topleft[0] + i*3, kolikko.rect.topleft[1] + j*3, 3, 3))       

    # tämä renderöi viholliset
    for vihollinen in viholliset:
        vihollinen.update(pelaaja.rect.center)
        if pelaaja.rect.colliderect(vihollinen.rect):
            viholliset.remove(vihollinen)
            elamat -= 1
        matriisi = kuvat.lohikaarme()        

        for i in range(len(matriisi)):
            for j in range(len(matriisi[i])):
                r, g, b = matriisi[i][j]
                if r == g == b == 0:
                    pass
                else:
                    pygame.draw.rect(naytto, (r, g, b), (vihollinen.rect.topleft[0] + i*3, vihollinen.rect.topleft[1] + j*3, 3, 3))       

    # tämä renderöi pelaajan
    matriisi = kuvat.hero()
    for i in range(len(matriisi)):
        for j in range(len(matriisi[i])):
            r, g, b = matriisi[i][j]
            if r == g == b == 0:
                pass
            else:
                pygame.draw.rect(naytto, (r, g, b), (pelaaja.rect.left + i*3, pelaaja.rect.top + j*3, 3, 3))

    # tämä määrittää "fog of war, mikä lie olisi suomeksi. Sotasumu?"
    naytto.blit(maski, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    varin_arvo = 100
    sumun_vari = (varin_arvo, varin_arvo, varin_arvo, 128)
    
    # Piirretään sotasumu jos tee maski on true
    # tämä lippu asetetaan true tilaan aina kentän päätyttyä,
    # joten maski piirretään vain ensimmäisessä framessa
    # ja sitä syödään pois kenttää pelatessa
    if tee_maski == True:
        maski.fill((0, 0, 0))
        tee_maski = False

    # piirretään askelittain kirkastuvia ja pienentyviä ympyröitä
    # joiden perusteella katsotaan kuinka paljon musta päästää läpi sen alla olevia
    # muista kerroksia
    # HUOM!!! näiden päälle piirretään vain kentän alussa uusi musta
    # Näin saadaan jo näkökentässä käyneet alueet näkymään
    gradient_sade = nakokentta
    for _ in range(nakokentta - skaala_px):
        pygame.draw.circle(maski, (sumun_vari), pelaaja.rect.center, gradient_sade, 0)
        if varin_arvo != 255:
            varin_arvo += 1
        if gradient_sade != skaala_px:
            gradient_sade -= 1
        sumun_vari = (varin_arvo, varin_arvo, varin_arvo, 128)

    # määritetään tekstit mitä kirjoitetaan alareunaan
    teksti1 = font.render(f"Elämät: {str(elamat).ljust(10)} Raha:  {str(raha).ljust(10)} Kenttä:  {kentta}", True, (255, 255, 255), (0, 0, 0))
    teksti2 = font.render("1 = Osta elämä    2 = Osta isompi näkyvyys", True, (255, 255, 255), (0, 0, 0))
    teksti3 = font.render("Etsi kolikoita ja osta niillä kehityksiä. Koita päästä mahdollisimman korkeaan kenttään", True, (255, 255, 255), (0, 0, 0))
    teksti4 = font.render("Jos elämät loppuvat, peli loppuu.", True, (255, 255, 255), (0, 0, 0))
    # laatikko alareunaan
    pygame.draw.rect(naytto, (255,255,255), (0, koko[1]-90,koko[0],3))
    # renderöidään tekstit
    naytto.blit(teksti1, ((koko[0]-teksti1.get_width())/2,koko[1]-80))
    naytto.blit(teksti2, ((koko[0]-teksti2.get_width())/2,koko[1]-60))
    naytto.blit(teksti3, ((koko[0]-teksti3.get_width())/2,koko[1]-40))
    naytto.blit(teksti4, ((koko[0]-teksti4.get_width())/2,koko[1]-20))

    # päivitetään näyttö
    pygame.display.flip()