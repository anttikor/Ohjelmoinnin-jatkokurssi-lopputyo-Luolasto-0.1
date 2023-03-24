import pygame
import kuvat
import labyrintti

class Objekti(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.leveys = self.korkeus = 30
        self.rect = pygame.Rect(x, y, self.leveys, self.korkeus)

    def update(self):
        pass

class Vihollinen(Objekti):
    def __init__(self, x, y):
        super().__init__(x, y)

class Pelaaja(Objekti):
    def __init__(self, x, y):
        super().__init__(x, y)
        
        

    def move(self, dx, dy, seinat):
        
        # Move each axis separately. Note that this checks for collisions both times.
        if dx != 0:
            self.move_single_axis(dx, 0, seinat)
        #if dy != 0:
        #    self.move_single_axis(0, dy, seinat)
    
    def move_single_axis(self, dx, dy, seinat):
        self.x += dx
        self.y += dy

        # If you collide with a wall, move out based on velocity
        for seina in seinat:
            if self.rect.colliderect(seina.rect):
                #print(f"osuu self.rect.right: {self.rect.right}, seina.rect.left: {seina.rect.left}")
                if dx > 0: # Moving right; Hit the left side of the wall
                    #print (self.rect.right)
                    #print (seina.rect.left)
                    self.x = seina.rect.left - 30
                    #if self.rect.right >= seina.rect.left:
                    #self.x = seina.rect.left -25
                if dx < 0: # Moving left; Hit the right side of the wall
                #    print (self.rect.left)
                #    print (seina.rect.right)
                    #if self.rect.left <= seina.rect.right:
                    self.x = seina.rect.right
                    #self.x -= dx
                    pass
                if dy > 0: # Moving down; Hit the top side of the wall
                    #self.y -= dy
                    pass
                if dy < 0: # Moving up; Hit the bottom side of the wall
                    #self.y += dy   
                    pass                                 


    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.leveys, self.korkeus)                                 

class Kolikko(Objekti):
    def __init__(self, x, y):
        super().__init__(x, y)   

class Seina(Objekti):
    def __init__(self, x, y):
        super().__init__(x, y)

class Tie(Objekti):
    def __init__(self, x, y):
        super().__init__(x, y)

class Peli:
    def __init__(self):
        pygame.init()
        self.koko = (1200, 690) #1200, 690
        self.skaala = 30
        self.screen = pygame.display.set_mode((self.koko))
        self.clock = pygame.time.Clock()
        self.viholliset = pygame.sprite.Group()
        self.kolikot = pygame.sprite.Group()
        self.seinat = pygame.sprite.Group()
        self.tiet = pygame.sprite.Group()        
        self.pelaajat = pygame.sprite.Group()
        self.pelaaja = Pelaaja(300, 480)
        self.taso = 10
        self.kartta = []
        self.luo_kentta()
        
        for i in range(self.taso):
            vihollinen = Vihollinen(50 * i, 50)
            self.viholliset.add(vihollinen)
        
        for i in range(10):
            kolikko = Kolikko(100 * i, 100)
            self.kolikot.add(kolikko)



        for y in range(len(self.kartta)):
            for x in range(len(self.kartta[y])):
                seina = Seina(x*self.skaala, y*self.skaala)
                tie = Tie(x*self.skaala, y*self.skaala)                
                if self.kartta[y][x] == 0:
                    self.seinat.add(seina)
                elif self.kartta[y][x] == 1:
                    self.tiet.add(tie)



    def luo_kentta(self):
        # kutsutaan toiseen tiedostoon tehtyä luo_labyrintti-funktiota
        # tein toiseen tiedostoon kun tuli aika pitkä
        # alussa on import labyrintti mikä lisää tämän tiedoston funktiot (ja luokat jos niitä olisi) käyttöön
        palautus = labyrintti.luo_labyrintti(int(self.koko[0]/self.skaala), int(self.koko[1]/self.skaala)-5)
        self.kartta = palautus[0]
        self.player_x = palautus[1]*self.skaala
        self.player_y = self.koko[1]-(self.skaala * 7)


    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.pelaaja.move(0, -5, self.seinat)
                #self.pelaaja.y -= 5
            if keys[pygame.K_DOWN]:
                self.pelaaja.move(0, 5, self.seinat)                
                #self.pelaaja.y += 5
            if keys[pygame.K_LEFT]:
                self.pelaaja.move(-5, 0, self.seinat)
                #self.pelaaja.x -= 5
            if keys[pygame.K_RIGHT]:
                self.pelaaja.move(5, 0, self.seinat)
                #self.pelaaja.x += 5
                    
            self.screen.fill((0, 0, 0))
            
            for seina in self.seinat:
                #pygame.draw.rect(self.screen, (255,0 , 0), (seina.rect))
                #pygame.draw.rect(self.screen, (0, 255, 0), self.seina.rect)
                #"""
                matriisi = kuvat.stone()
                for i in range(len(matriisi)):
                    for j in range(len(matriisi[i])):
                        r, g, b = matriisi[i][j]
                        if r == g == b == 0:
                            pass
                        else:
                            pygame.draw.rect(self.screen, (r, g, b), (seina.x + i*3, seina.y + j*3, 3, 3))
                #"""
            self.pelaaja.update()
            
            for tie in self.tiet:
                matriisi = kuvat.dirt_road()
                for i in range(len(matriisi)):
                    for j in range(len(matriisi[i])):
                        r, g, b = matriisi[i][j]
                        if r == g == b == 0:
                            pass
                        else:
                            pygame.draw.rect(self.screen, (r, g, b), (tie.x + i*3, tie.y + j*3, 3, 3))
            
            for vihollinen in self.viholliset:
                if self.pelaaja.rect.colliderect(vihollinen.rect):
                    self.viholliset.remove(vihollinen)
                #pygame.draw.rect(self.screen, (255, 0, 0), vihollinen.rect)
                matriisi = kuvat.lohikaarme()
                for i in range(len(matriisi)):
                    for j in range(len(matriisi[i])):
                        r, g, b = matriisi[i][j]
                        if r == g == b == 0:
                            pass
                        else:
                            pygame.draw.rect(self.screen, (r, g, b), (vihollinen.x + i*3, vihollinen.y + j*3, 3, 3))                      
                
            for kolikko in self.kolikot:
                if self.pelaaja.rect.colliderect(kolikko.rect):
                    self.kolikot.remove(kolikko)
                #pygame.draw.rect(self.screen, (255, 255, 0), kolikko.rect)
                matriisi = kuvat.coin()
                for i in range(len(matriisi)):
                    for j in range(len(matriisi[i])):
                        r, g, b = matriisi[i][j]
                        if r == g == b == 0:
                            pass
                        else:
                            pygame.draw.rect(self.screen, (r, g, b), (kolikko.x + i*3, kolikko.y + j*3, 3, 3))
                
            for kolikko in self.kolikot:
                if self.pelaaja.rect.colliderect(kolikko.rect):
                    self.kolikot.remove(kolikko)
                #pygame.draw.rect(self.screen, (255, 255, 0), kolikko.rect)
                matriisi = kuvat.coin()
                for i in range(len(matriisi)):
                    for j in range(len(matriisi[i])):
                        r, g, b = matriisi[i][j]
                        if r == g == b == 0:
                            pass
                        else:
                            pygame.draw.rect(self.screen, (r, g, b), (kolikko.x + i*3, kolikko.y + j*3, 3, 3))

            pygame.draw.rect(self.screen, (0, 255, 0), self.pelaaja.rect)
            pygame.display.update()
            self.clock.tick(30)
            
        pygame.quit()
        
if __name__ == "__main__":
    peli = Peli()
    peli.run()
