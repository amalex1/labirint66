from pygame import *
class GameSprite(sprite.Sprite):
    def __init__(self,picture,w,h,x,y):
        super().__init__()
        self.image=transform.scale(image.load(picture),(w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
class Player(GameSprite):
    def __init__(self, picture, w, h, x, y, x_speed, y_speed):
        super().__init__(picture, w, h, x, y)    
        self.x_speed = x_speed
        self.y_speed = y_speed
    def update(self):
        if (self.rect.x <= 620 and self.x_speed > 0) or (self.rect.x >= 0 and self.x_speed < 0):
            self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)

        if (self.rect.y <= 410 and self.y_speed > 0) or (self.rect.y >= 0 and self.y_speed < 0):
            self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0: # идем вниз
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0: # идем вверх
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)
    def fire(self):
        bullet = Bullet('pppp.png', 20, 15, self.rect.right, self.rect.centery, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def __init__(self, picture, w, h, x, y, speed):
        super().__init__(picture, w, h, x, y)
        self.speed = speed
        self.direction = 'left'
    def update(self):
        if self.rect.x <= 420:
            self.direction = 'right'
        if self.rect.x >= 620:
            self.direction = 'left'
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Bullet(GameSprite):
    def __init__(self, picture, w, h, x, y, speed):
        super().__init__(picture, w, h, x, y)
        self.speed = speed
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > 700:
            self.kill()
        


wall_1 = GameSprite('1542_westerwald-krasnyy-gladkiy.jpg', 80, 180, 200, 250)
wall_2 = GameSprite('85d401fa178529b4e680ce5e7cb63953.png', 370, 100, 50, 400)
barriers = sprite.Group()
barriers.add(wall_1)
barriers.add(wall_2)

bullets = sprite.Group()

player = Player('ddd.png', 80, 80, 5, 100, 0, 0)
final_sprite = GameSprite('jjj.jpg', 80, 80, 620, 420)
monstr = Enemy('aaa.jpg', 80, 80, 620, 180, 7)
monsters = sprite.Group()
monsters.add(monstr)
window = display.set_mode((700, 500))
display.set_caption('Game')
picture = transform.scale(image.load('ggg.png'), (700, 500))
run = True
finish = False
while run:
    time.delay(50)
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
           if e.key == K_LEFT:
               player.x_speed = -5
           elif e.key == K_RIGHT:
               player.x_speed = 5
           elif e.key == K_UP:
               player.y_speed = -5
           elif e.key == K_DOWN:
               player.y_speed = 5
           elif e.key == K_SPACE:
               player.fire()
        elif e.type == KEYUP:
           if e.key == K_LEFT:
               player.x_speed = 0
           elif e.key == K_RIGHT:
               player.x_speed = 0
           elif e.key == K_UP:
               player.y_speed = 0
           elif e.key == K_DOWN:
               player.y_speed = 0
    if finish != True:
        window.blit(picture,(0,0))
        player.update()
        monsters.update()
        bullets.update()
        monsters.draw(window)
        final_sprite.reset()
        player.reset()
        barriers.draw(window)
        bullets.draw(window)
        
        sprite.groupcollide(bullets, barriers, True, False)
        sprite.groupcollide(bullets, monsters, True, True)
        if sprite.collide_rect(player, final_sprite):
            finish = True
            font.init()
            win = font.SysFont('Arial', 70).render('Ты выиграл!', True, (0,255,0))
            window.blit( win ,(200,200))
        if sprite.spritecollide(player, monsters, False):
            finish = True
            font.init()
            win = font.SysFont('Arial', 70).render('Ты проиграл!', True, (255,0,0))
            window.blit( win ,(200,200))   
    display.update()        
