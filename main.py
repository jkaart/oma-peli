import pygame
import random

class Peli:
    def __init__(self):
        pygame.init()

        nayton_leveys, nayton_korkeus = 640, 480
        self.naytto = pygame.display.set_mode((nayton_leveys, nayton_korkeus))
        self.kello = pygame.time.Clock()
        self.nayton_tausta = 225, 225, 225

        self.fontti = pygame.font.SysFont("Arial", 24)

        self.uusi_peli()

    def silmukka(self):
        while True:
            self.tutki_tapahtumat()
            self.piirra_naytto()
            self.kello.tick(60)

    def tutki_tapahtumat(self):
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.QUIT:
                exit()

            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_LEFT:
                    self.__vasemmalle = True
                if tapahtuma.key == pygame.K_RIGHT:
                    self.__oikealle = True
                if tapahtuma.key == pygame.K_UP:
                    self.__ylos = True
                if tapahtuma.key == pygame.K_DOWN:
                    self.__alas = True
                if tapahtuma.key == pygame.K_F2:
                    self.uusi_peli()
                if tapahtuma.key == pygame.K_ESCAPE:
                    exit()

            if tapahtuma.type == pygame.KEYUP:
                if tapahtuma.key == pygame.K_LEFT:
                    self.__vasemmalle = False
                if tapahtuma.key == pygame.K_RIGHT:
                    self.__oikealle = False
                if tapahtuma.key == pygame.K_UP:
                    self.__ylos = False
                if tapahtuma.key == pygame.K_DOWN:
                    self.__alas = False
        
        if self.__vasemmalle:
            if self.__pelaaja.hae_sijainti[0] >= 0:
                self.__pelaaja.liiku_vasemmalle
        
        if self.__oikealle:
            if self.__pelaaja.hae_sijainti[0] <= self.naytto.get_width()-self.__pelaaja.leveys:
                self.__pelaaja.liiku_oikealle

        if self.__ylos:
            if self.__pelaaja.hae_sijainti[1] >= 0:
                self.__pelaaja.liiku_ylos
        
        if self.__alas:
            if self.__pelaaja.hae_sijainti[1] <= self.naytto.get_height()-self.__pelaaja.korkeus:
                self.__pelaaja.liiku_alas

    def uusi_peli(self):
        self.__oikealle = False
        self.__vasemmalle = False
        self.__ylos = False
        self.__alas = False

        self.__pelaaja = Pelaaja(self.nayton_koko)
        self.__hirviot = [Hirvio(self.nayton_koko) for i in range(5)]
        self.__kolikot = [Kolikko(self.nayton_koko, self.__pelaaja) for i in range(20)]

        self.silmukka()

    @property
    def nayton_koko(self):
        return self.naytto.get_width(),self.naytto.get_height()

    def peli_paattyi(self, voitto: bool):
        while True:
            self.tutki_tapahtumat()
            self.naytto.fill(self.nayton_tausta)
            if voitto:
                teksti = self.fontti.render("Voitit!", True, (0,0,0))
                
            else:
                teksti = self.fontti.render("Hävisit", True, (0,0,0))

            self.naytto.blit(teksti, (self.nayton_koko[0]//2 - teksti.get_width()//2, 20))

            teksti = self.fontti.render(f"Pisteet: {self.__pelaaja.pisteet}", True, (0,0,0))
            self.naytto.blit(teksti, (self.nayton_koko[0]//2 - teksti.get_width()//2, 44))

            teksti = self.fontti.render("Uuusi peli = F2", True, (0,0,0))
            self.naytto.blit(teksti, (self.nayton_koko[0]//2 - teksti.get_width()//2, 100))

            teksti = self.fontti.render("Lopeta peli = ESC", True, (0,0,0))
            self.naytto.blit(teksti, (self.nayton_koko[0]//2 - teksti.get_width()//2, 120))
            pygame.display.flip()

    def piirra_naytto(self):
        self.naytto.fill(self.nayton_tausta)
        self.naytto.blit(self.__pelaaja.kuva, self.__pelaaja.hae_sijainti)
        teksti = self.fontti.render("Uusi_peli = F2, Lopeta = ESC", True, (0,0,0))
        self.naytto.blit(teksti, (0, 0))
        teksti = self.fontti.render(f"Pisteet: {self.__pelaaja.pisteet}", True, (0,0,0))
        self.naytto.blit(teksti, (self.nayton_koko[0] - teksti.get_width(), 0))

        for kolikko in self.__kolikot:
            self.naytto.blit(kolikko.kuva, kolikko.hae_sijainti)
            if kolikko.hae_sijainti.colliderect(self.__pelaaja.hae_sijainti):
                self.__kolikot.remove(kolikko)
                self.__pelaaja.lisaa_piste
        
        #liikutetaan kutakin hirviötä
        for hirvio in self.__hirviot:
            hirvio.liiku
            self.naytto.blit(hirvio.kuva, hirvio.hae_sijainti)
            if hirvio.hae_sijainti.colliderect(self.__pelaaja.hae_sijainti):
                self.peli_paattyi(False)
        
        #Jos kaikki kolikot kerätty: voitit pelin!
        if len(self.__kolikot) == 0:
            self.peli_paattyi(True)

        pygame.display.flip()

class Pelaaja:
    def __init__(self, nayton_koko: tuple):
        self.__nayton_koko = nayton_koko
        self.__kuva = pygame.image.load("robo.png")
        self.__hahmo = self.__kuva.get_rect()
        self.__hahmo.x = self.__nayton_koko[0]/2 - self.__hahmo.right/2
        self.__hahmo.y = self.__nayton_koko[1]/2 - self.__hahmo.bottom/2
        self.__pisteet = 0

    @property
    def kuva(self):
        return self.__kuva

    @property
    def liiku_oikealle(self):
        self.__hahmo.x += 2

    @property
    def liiku_vasemmalle(self):
        self.__hahmo.x -= 2

    @property
    def liiku_ylos(self):
        self.__hahmo.y -= 2

    @property
    def liiku_alas(self):
        self.__hahmo.y += 2

    @property
    def lisaa_piste(self):
        self.__pisteet += 1

    @property
    def pisteet(self):
        return self.__pisteet
    
    @property
    def nollaa_pisteet(self):
        self.__pisteet = 0

    @property
    def hae_sijainti(self):
        return self.__hahmo
    
    @property
    def leveys(self):
        return self.__hahmo[2]
    
    @property
    def korkeus(self):
        return self.__hahmo[3]

class Hirvio:
    def __init__(self, nayton_koko: tuple):
        self.__nayton_koko = nayton_koko
        self.__kuva = pygame.image.load("hirvio.png")
        self.__hahmo = self.__kuva.get_rect()

        #Aloitus sijainti satunaisesta kentän nurkasta
        self.__hahmo.x, self.__hahmo.y = random.choice([(0,0),nayton_koko,(0,nayton_koko[1]),(nayton_koko[0],0)])

        #arvotaan ensimmäinen kohde minne mennään
        self.__suunta = self.satunainen_sijainti

    @property
    def kuva(self):
        return self.__kuva

    @property
    def liiku(self):
        #Liikutetaan hirvio kohti kohdetta tai arvotaan uusi kohde, jos olllaan jo kohteeessa
        if self.__suunta[0] == self.__hahmo.x and self.suunta[1] == self.__hahmo.y:
            self.__suunta = self.satunainen_sijainti
        else:
            if self.__hahmo.x < self.__suunta[0]:
                self.__hahmo.x += 1
            if self.__hahmo.x > self.__suunta[0]:
                self.__hahmo.x -= 1
            
            if self.__hahmo.y < self.__suunta[1]:
                self.__hahmo.y += 1
            if self.__hahmo.y > self.suunta[1]:
                self.__hahmo.y -= 1

    @property
    def hae_sijainti(self):
        return self.__hahmo

    @property
    def satunainen_sijainti(self):
        return random.randint(0,self.__nayton_koko[0]),random.randint(0,self.__nayton_koko[1])
    
    @property
    def suunta(self):
        return self.__suunta
    
class Kolikko:
    def __init__(self, nayton_koko: tuple, pelaaja: "Pelaaja"):
        pelaajan_sijainti = pelaaja.hae_sijainti
        self.__nayton_koko = nayton_koko
        self.__kuva = pygame.image.load("kolikko.png")
        self.__kuva = pygame.transform.scale(self.__kuva, (25,25))
        self.__kolikko = self.__kuva.get_rect()
        paikat = [x for x in range(0,self.__nayton_koko[0]) if x < pelaajan_sijainti[0] or x > pelaajan_sijainti[0] + pelaajan_sijainti[2]],[y for y in range(0,self.__nayton_koko[1]) if y < pelaajan_sijainti[1] or y > pelaajan_sijainti[1] + pelaajan_sijainti[3]]
        self.__kolikko.x = random.choice(paikat[0])
        self.__kolikko.y = random.choice(paikat[1])

    @property
    def kuva(self):
        return self.__kuva
    
    @property
    def hae_sijainti(self):
        return self.__kolikko

if __name__ == "__main__":
    Peli()
