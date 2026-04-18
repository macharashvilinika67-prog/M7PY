from random import randint

from pygame import *

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load("galaxy.jpg"),(win_width,win_height))
mixer.init()
clock = time.Clock()
FPS = 40

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, w=65, h=65):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (w,h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 65:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("laser.png", self.rect.centerx, self.rect.top, 10, w=30, h=40)
        bullets.add(bullet)


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

missed = 0
score = 0
class Enemy(GameSprite):
    def update(self):
        global missed
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(100, win_width - 100)
            self.rect.y = 0
            missed += 1

font.init()
font1 = font.SysFont("Arial", 40)

bullets = sprite.Group()
player = Player("spaceship1.png", 300, 425, 10)
monsters = sprite.Group()
asteroids = sprite.Group()


def reset_game():
    global player, monsters, missed, score, finish, result_text
    global num_fire, reload, reload_start_time

    missed = 0
    score = 0
    finish = False
    result_text = font1.render("", True, (255, 255, 255))

    player.rect.x = 300
    player.rect.y = 430

    num_fire = 0
    reload = False
    reload_start_time = 0

    asteroids.empty()
    monsters.empty()
    bullets.empty()
    for i in range(5):
        enemy = Enemy("ufo1.png",randint(0, win_width - 100),randint(-150, 40),2,100,100)
        monsters.add(enemy)

    for i in range(2):
        asteroid = Enemy("asteroid.png",randint(0, win_width - 100),randint(-150, 40),2,100,100)
        asteroids.add(asteroid)

reset_game()
game = True
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE and not finish and not reload:
                mixer.music.load("laser.mp3")
                mixer.music.play()
                player.fire()
                num_fire += 1
                if num_fire >=5:
                    reload = True
                    reload_start_time = time.get_ticks()
            if e.key == K_r and finish:
                reset_game()

            else:
                mixer.music.load("galaxy1.mp3")
                mixer.music.play()




    if not finish:
        player.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        if reload:
            now_time = time.get_ticks()
            if now_time - reload_start_time >= 1500:
                reload = False
                num_fire = 0
        window.blit(background, (0, 0))
        text_score = font1.render("Destroyed: " + str(score), True, (255, 255, 255))
        text_missed = font1.render("Missed: " + str(missed), True, (255, 255, 255))
        window.blit(text_missed,(10,10))
        window.blit(text_score,(10,40))
        if sprite.spritecollide(player, monsters, True) or sprite.spritecollide(player, asteroids, True):
            finish = True
            result_text = font1.render("You Lose!", True, (255, 0, 0))
        hits = sprite.groupcollide(monsters, bullets, True, True)
        for i in hits:
            score += 1
            enemy = Enemy("ufo1.png", randint(0, win_width-100), randint(-150, -40), 2, 100, 100)
            monsters.add(enemy)
        if score >= 10:
            finish = True
            result_text = font1.render("You Win!", True, (255, 255, 255))
        if missed > 2:
            finish = True
            result_text = font1.render("You Lose!", True, (255, 255, 255))

        player.reset()
        player.update()
        monsters.update()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

    if finish:
        window.blit(result_text, (win_width / 2 -80, win_height / 2))
        restart_text = font1.render("Press R Restart", True, (255, 255, 255))
        window.blit(restart_text, (win_width / 2 -110, win_height / 2 +40))
    if reload:
        text_reload = font1.render("Reloading", True, (255, 0, 0))
        window.blit(text_reload, (280, 450))
    clock.tick(FPS)
    display.update()
