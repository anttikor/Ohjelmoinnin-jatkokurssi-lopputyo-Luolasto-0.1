import os
import random
import pygame
import labyrintti
import kuvat
import math

class Objekti(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        #self.x = x
        #self.y = y
        self.leveys = self.korkeus = 30
        self.rect = pygame.Rect(x, y, self.leveys, self.korkeus)

class Player(object):
    
    def __init__(self, x: int, y: int):
        #self.x = x
        #self.y = y
        self.rect = pygame.Rect(x, y, 30, 30)  
    
    def move(self, dx, dy):
        
        # Move each axis separately. Note that this checks for collisions both times.
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)
    
    def move_single_axis(self, dx, dy):
        
        # Move the rect
        self.rect.x += dx
        self.rect.y += dy

        # If you collide with a wall, move out based on velocity
        for seina in seinat:
            if self.rect.colliderect(seina.rect):
                if dx > 0: # Moving right; Hit the left side of the wall
                    self.rect.right = seina.rect.left
                if dx < 0: # Moving left; Hit the right side of the wall
                    self.rect.left = seina.rect.right
                if dy > 0: # Moving down; Hit the top side of the wall
                    self.rect.bottom = seina.rect.top
                if dy < 0: # Moving up; Hit the bottom side of the wall
                    self.rect.top = seina.rect.bottom

class Wall(Objekti):    
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rect = pygame.Rect(x, y, 30, 30)

class Loppu(Objekti):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rect = pygame.Rect(x, y, 30, 30)

class Kolikko(Objekti):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rect = pygame.Rect(x, y, 30, 30)

class Vihollinen(Objekti):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rect = pygame.Rect(x, y, 30, 30)
    
    def update(self, pXY):
        #print(f"E:{self.rect.center}, V:{pXY}")
        etaisyydet = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                etaisyys = math.dist((pXY), (self.rect.center[0]+dx, self.rect.center[1]+dy))
                etaisyydet.append((etaisyys, dx, dy))
        etaisyydet = sorted(etaisyydet, key=lambda x: x[0])
        #print(f"{self.rect.center[0]:.1f}, {self.rect.center[1]:.1f},{etaisyydet[0][0]:.1f}, {etaisyydet[0][1]}, {etaisyydet[0][2]}")
        if etaisyydet[0][0] <= 30 * 3:
            self.rect.center = (self.rect.center[0] + etaisyydet[0][1], self.rect.center[1] + etaisyydet[0][2])
            #self.x += etaisyydet[0][1]
            #self.y += etaisyydet[0][2]
          
       

# Initialise pygame
pygame.init()


pygame.display.set_caption("Luolasto 0.1!")
koko = (1200, 750)
naytto = pygame.display.set_mode(koko)
clock = pygame.time.Clock()

kentta = 1
elamat = 3
raha = 0
nopeus = 10
labyrintin_koko = (15, 23) #(40, 23) == oikea koko


x = y = player_x = player_y = 0
end_rect = pygame.Rect(0, 0, 0, 0)
player = Player(player_x, player_y) # luodaan pelaaja
kolikot = pygame.sprite.Group()
viholliset = pygame.sprite.Group()
seinat = pygame.sprite.Group()
loppu = Loppu(0, 0)

#luodaan uusi kenttä
def uusi_kentta():
    labyrintti_palautus = labyrintti.luo_labyrintti(labyrintin_koko[0],labyrintin_koko[1])
    x = y = 0
    for row in labyrintti_palautus[0]:
        for col in row:
            if col == 0:
                seinat.add(Wall(x, y))                
            if col == 4:
                seinat.add(Wall(x, y))        
            if col == 3:
                loppu.rect.topleft = (x,y)
            x += 30
        y += 30
        x = 0
        
    player.rect.x = labyrintti_palautus[1]*30
    player.rect.y = koko[1]-(30 * 5)

    kolikot.empty()
    arvottavat_kolikot = 10
    while arvottavat_kolikot != 0:
        x = random.randint(1, (labyrintin_koko[0])-2)
        y = random.randint(1, (labyrintin_koko[1])-3)
        if labyrintti_palautus[0][y][x] == 1:
            kolikko = Kolikko(x * 30, y * 30)
            kolikot.add(kolikko)
            arvottavat_kolikot -= 1
    
    viholliset.empty()
    arvottavat_viholliset = kentta
    while arvottavat_viholliset != 0:
        x = random.randint(1, (labyrintin_koko[0])-2)
        y = random.randint(1, (labyrintin_koko[1])-3)
        if labyrintti_palautus[0][y][x] == 1:
            vihollinen = Vihollinen(x * 30, y * 30)
            viholliset.add(vihollinen)
            arvottavat_viholliset -= 1

uusi_kentta()
running = True
while running:
    
    clock.tick(1000000)
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False
    
    # Move the player if an arrow key is pressed
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        player.move(nopeus*-1, 0)
    if key[pygame.K_RIGHT]:
        player.move(nopeus, 0)
    if key[pygame.K_UP]:
        player.move(0, nopeus*-1)
    if key[pygame.K_DOWN]:
        player.move(0, nopeus)
    
    # Just added this to make it slightly fun ;)
    if player.rect.colliderect(loppu.rect):
        #arvotaan uusi kenttä
        print("You win!")
        kentta += 1
        seinat.empty()
        uusi_kentta()
    
    # Draw the scene
    naytto.fill((0, 0, 0))
    for seina in seinat:
        matriisi = kuvat.stone()
        for i in range(len(matriisi)):
            for j in range(len(matriisi[i])):
                r, g, b = matriisi[i][j]
                if r == g == b == 0:
                    pass
                else:
                    pygame.draw.rect(naytto, (r, g, b), (seina.rect.topleft[0] + i*3, seina.rect.topleft[1] + j*3, 3, 3))       
    pygame.draw.rect(naytto, (255, 0, 0), loppu)



    for kolikko in kolikot:
        if player.rect.colliderect(kolikko.rect):
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

    for vihollinen in viholliset:
        vihollinen.update(player.rect.center)
        if player.rect.colliderect(vihollinen.rect):
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

    print(f"Elämät: {elamat}, Raha: {raha}, Kenttä: {kentta}")

    matriisi = kuvat.hero()
    for i in range(len(matriisi)):
        for j in range(len(matriisi[i])):
            r, g, b = matriisi[i][j]
            if r == g == b == 0:
                pass
            else:
                pygame.draw.rect(naytto, (r, g, b), (player.rect.left + i*3, player.rect.top + j*3, 3, 3))
    #"""                   
    pygame.display.flip()