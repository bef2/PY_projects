# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3
# Art from Kenney.nl

import pygame, random
from os import path


img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'sound')
font_name = pygame.font.match_font('jetbrains mono')

WIDTH = 600
HEIGHT = 800
FPS = 60

# Цвета (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# Создаем игру и окно
pygame.init()
pygame.font.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))      
pygame.display.set_caption('Кпитан Старшип')
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (60, 50))
        self.image.fill((5, 5, 5), special_flags=pygame.BLEND_SUB)
        self.rect = self.image.get_rect()
        self.radius = 23
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.shield = 100

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -6
        if keystate[pygame.K_RIGHT]:
            self.speedx = 6
        self.rect.x += self.speedx
        if keystate[pygame.K_UP]:
            self.speedy = -8
        if keystate[pygame.K_DOWN]:
            self.speedy = 4
        self.rect.y += self.speedy

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (10, 30))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # Убить, если он заходит за верхнюю часть экрана
        if self.rect.bottom < 0:
            self.kill()
        

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_img)
        # self.image_orig.set_colorkey(YELLOW)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(3, 10)
        self.speedx = random.randrange(-1, 1)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            # self.rect.x = random.randrange(WIDTH - self.rect.width)
            # self.rect.y = random.randrange(-100, -40)
            # self.speedy = random.randrange(3, 8)
            # self.speedx = random.randrange(-1, 1)
            self.image_orig = random.choice(meteor_img)
            self.image = self.image_orig.copy()
            self.rect = self.image.get_rect()
            self.radius = int(self.rect.width * .85 / 2)
            # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(3, 10)
            self.speedx = random.randrange(-1, 1)
            self.rot = 0
            self.rot_speed = random.randrange(-8, 8)
            self.last_update = pygame.time.get_ticks()


    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center


class Stars(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.star_size = random.randrange(1, 3)
        self.image = pygame.Surface((self.star_size, self.star_size))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH)
        self.rect.y = random.randrange(0, HEIGHT)
        self.speedy = random.randrange(1, 5)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 5:
            self.rect.x = random.randrange(0, WIDTH)
            self.rect.y = random.randrange(-5, 0)
            self.speedy = random.randrange(1, 5)


# Загрузка всей игровой графики
player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png"))
meteor_img = pygame.image.load(path.join(img_dir, "meteorBrown_med1.png"))
bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png"))
meteor_img = []
meteor_list = ['meteorBrown_big1.png', 'meteorBrown_big3.png', 'meteorBrown_med3.png',
               'meteorBrown_med3.png', 'meteorBrown_small1.png'] #, 'meteorBrown_tiny1.png']
for img in meteor_list:
    meteor_img.append(pygame.image.load(path.join(img_dir, img)))

# Загрузка всех игровых звуков
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'Laser_Shoot.wav'))
expl_sound = []
for snd in ['expl3.wav', 'expl6.wav']:
    expl_sound.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
pygame.mixer.music.load(path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.mp3'))
pygame.mixer.music.set_volume(0.4)

# Создаем группы для спрайтов
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
# Определяем количество астероидов
for i in range(10):
    mob = Mob()
    all_sprites.add(mob)
    mobs.add(mob)
# Определяем количество звезд на фоне
for i in range(500):
    star = Stars()
    all_sprites.add(star)

score = 0
pygame.mixer.music.play(loops=-1)

# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)

    # Ввод процесса (события)
    for event in pygame.event.get():
        # Проверить закрытие окна
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Обновление (Update)
    all_sprites.update()
    # Проверка, попала ли пуля в моба
    hits_bullets = pygame.sprite.groupcollide(mobs, bullets, True, True, pygame.sprite.collide_circle)
    for hit in hits_bullets:
        score += 50 - hit.radius
        random.choice(expl_sound).play()
        mob = Mob()
        all_sprites.add(mob)
        mobs.add(mob)
    # Проверка, не ударил ли моб игрока
    hits_player = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits_player:
        mob = Mob()
        all_sprites.add(mob)
        mobs.add(mob)
    if hits_player:
        pass
        # running = False

    # Визуализация (Рендеринг)
    screen.fill((0, 0, 33))
    all_sprites.draw(screen)
    draw_text(screen, str(score), 24, WIDTH / 2, 10)
    # после отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()