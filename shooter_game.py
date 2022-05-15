#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timerc
window = display.set_mode((700, 500))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))

font.init()

font1 = font.Font(None, 36)

lost = 0

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()

clock = time.Clock()
FPS = 60
class Game_sprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(Game_sprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= 10
        if keys_pressed[K_d] and self.rect.x < 632:
            self.rect.x += 10
    def fire(self):
        bullet = Bullet("bullet.png",self.rect.centerx, self.rect.top, 10, 10, 30)
        bullets.add(bullet)

class Bullet(Game_sprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()
        
class Ast(Game_sprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(0, 650)
    

class Enemy(Game_sprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            global lost
            lost += 1
            self.rect.y = 0
            self.rect.x = randint(0, 650)

monsters = sprite.Group()
for i in range(5):
    enemy = Enemy('ufo.png', randint(10, 650), 10, randint(1, 2), 65, 65)
    monsters.add(enemy)

asteroids = sprite.Group()
for i in range(2):
    aster = Ast('asteroid.png', randint(10, 650), 10, randint(1, 2), 65, 65)
    asteroids.add(aster)
hero = Player('rocket.png', 100, 420, 10, 65, 65)
bullets = sprite.Group()
game = True
finish = False
score = 0
font = font.Font(None, 90)
win = font.render('You win!', True, (250, 215, 0))
lose = font.render('You lose', True, (250, 215, 0))
num_fire = 0
rel_time = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5:
                    hero.fire()
                    num_fire += 1
                else:
                    rel_time = True
                    cur_time = timer()

    if finish != True:
        window.blit(background, (0, 0))
        hero.reset()
        hero.update()
        monsters.draw(window)
        monsters.update()
        asteroids.draw(window)
        asteroids.update()
        bullets.draw(window)
        bullets.update()
        text_lose = font1.render('Пропущено:' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 10))
        text_score = font1.render('Счёт:' + str(score), 1, (255, 255, 255))
        window.blit(text_score, (10, 50))
        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        if rel_time == True:
            new_time = timer()
            if new_time - cur_time >= 3:
                num_fire = 0
                rel_time = False
            else:
                text_reload = font1.render('Перезарядка, подождите', 1, (255, 0, 50))
                window.blit(text_reload, (300, 450))
        for i in sprites_list:
            score += 1
            enemy = Enemy('ufo.png', randint(10, 650), 10, randint(2, 5), 65, 65)
            monsters.add(enemy)
        if score >= 10:
            finish = True
            window.blit(win, (200, 200))
        if sprite.spritecollide(hero, monsters, False) or lost >= 5 or sprite.spritecollide(hero, asteroids, False):
            finish = True
            window.blit(lose, (200, 200))




    display.update()
    clock.tick(FPS)