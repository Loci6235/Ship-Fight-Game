import pygame
import random

def water(win):
    for i in range(50):
        x = random.randint(0, 500)
        y = random.randint(0, 500)
        xe = x
        ye = y+10
        pygame.draw.line(win,"white",(x,y), (xe,ye))
    

class bomb():
    def __init__(self, win, x, y, bomb_img):
        self.bomb_img = bomb_img
        self.win = win
        self.x = x
        self.y = y
        self.bombrect = self.bomb_img.get_rect()
        

    def shoot(self):
        self.bombrect.topleft = (self.x, self.y)
        self.win.blit(self.bomb_img, self.bombrect)
    
    def moveb(self):
        self.y -= 5
    
    def Brect(self):
        return self.bombrect


        

class enemy():
    def __init__(self, win, eimage):
        self.eimage = eimage
        self.win = win
        self.x = random.randint(160, 330)
        self.y = 0
        self.image = random.choice(self.eimage) 
        self.en = self.image.get_rect()

    def cars(self):
        self.en.topleft = (self.x, self.y)
        self.win.blit(self.image , self.en)

    def move(self, K):
        g = 1
        if K:
            self.y += 5
        self.y += 2
        if self.y > 500:
            g = 0
        return g
    
    def enmrect(self):
        return self.en
    
    def rey(self):
        return self.y
    def ecoordinates(self):
        return self.x, self.y
        

class car():
    def __init__(self, win, x, y, ourship):
        self.ourship = ourship
        self.win = win
        self.x = x
        self.y = y - 10
        self.ship_rect = self.ourship.get_rect()
        self.ship_rect.topleft = (self.x, self.y)

    def draw(self):
        self.win.blit(self.ourship, self.ship_rect)

    def carrect(self):
        return self.ship_rect
    
    def coordinates(self):
        return self.x, self.y
    

def right(x, y):
    if not x > 330:
        x += 5
    return x, y

def left(x, y):
    if not x < 160:
        x -= 5
    return x, y 
def up(x, y):
    y += 10

def firstview(win, wait):
    bg = pygame.image.load("first.png")
    startimg = pygame.image.load("start.png")
    start_rect = startimg.get_rect()
    start_rect.topleft = (200,425)
    

    while wait:
        win.blit(bg,(0, 0))
        win.blit(startimg, start_rect)
        mx, my = pygame.mouse.get_pos()
        mouse_rect = pygame.Rect(mx, my, 1, 1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                wait = False
            if event.type == pygame.MOUSEBUTTONDOWN and start_rect.colliderect(mouse_rect):
                run = True
                wait = False
                start(run, win)
        pygame.display.flip()
    pygame.quit



def start(run, win):
    clock = pygame.time.Clock()
    x = 250
    y = 450
    K = False
    fram = 3
    score = 0
    font = pygame.font.SysFont(None, 40)

    ourship = pygame.image.load("ship.png")

    eimage = []
    enemys = []
    enemy_rect = []

    bombss = []
    bombssrect = []
    explod = []
    explodrect = []
    

    for i in range(1, 8):
        eimage.append(pygame.image.load(f"shipE{i}.png"))

    bomb_img = pygame.image.load("bomb.png")

    for i in range(1, 4):
        img = pygame.image.load(f"explosion{i}.png")
        explod.append(img)
        explodrect.append(img.get_rect())

    while run:
        clock.tick(40)
        win.fill("#44dcc3")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        #water creation
        water(win)
        score_text = font.render(f"Score: {score}", True, ("white"))
        win.blit(score_text, (10, 10))

        #enemy ship class creation
        if len(enemys) == 0:
            c = enemy(win, eimage)
            enemys.append(c)
        elif enemys[-1].rey() > 200 and len(enemys) < 10:
            c = enemy(win, eimage)
            enemys.append(c)

        #enemy ship rect
        for i in enemys[:]:
            i.cars()
            k = i.move(K)
            if k != 1:
                enemys.remove(i)

        enemy_rect = []
        for i in enemys:
            enemy_rect.append(i.enmrect())
        
        #primary ship    
        car1 = car(win, x, y, ourship)
        car1.draw()
        cr = car1.carrect()
        #collission
        for t in enemy_rect:
            if t.colliderect(cr):
                run = False
                wait = True
                firstview(win,wait)
                

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            x,y =right(x, y)
        if keys[pygame.K_LEFT]:
            x,y = left(x, y)
        if keys[pygame.K_UP]:
            K = True
        else:
            K = False
        if keys[pygame.K_SPACE]:
            bx, by = car1.coordinates()
            if len(bombss) == 0:
                bomb1 = bomb(win, bx , by, bomb_img)
                bombss.append(bomb1)
            elif bombss[-1].y < 400:
                bomb1 = bomb(win, bx , by, bomb_img)
                bombss.append(bomb1)
            
        if bombss:
            bombssrect = []
            for i in bombss:
                if i.y <= 0:
                    bombss.remove(i)
                else:
                    i.shoot()
                    i.moveb()
                    bombssrect.append(i.Brect())

        for b in bombss[:]:
            for e in enemys[:]:
                if b.Brect().colliderect(e.enmrect()):
                    exx, eyy = e.ecoordinates()
                    bombss.remove(b)
                    enemys.remove(e)
                    fram -= 0.5
                    break

        if fram !=3 and fram > 0:
                curr = int(fram)
                ip = explod[curr].get_rect()
                ip.topleft = (exx, eyy)
                win.blit(explod[curr], ip)
                fram -= 0.2
        elif fram<0:
            score += 1
            fram =3

        pygame.display.flip()
   
if __name__ == "__main__":
    pygame.init()
    win = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("SHIP FiGHT")
    icon = pygame.image.load("anchor.png")
    pygame.display.set_icon(icon)
    wait = True

    firstview(win, wait)

    pygame.quit()