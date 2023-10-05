import pygame
import time
from random import randint

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
pygame.display.set_caption("Pong")
running = True

BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
WHITE = (255,255,255)

game_start_sfx = pygame.mixer.Sound('./audio/game-start-6104.mp3')
scored_sfx = pygame.mixer.Sound('./audio/8-bit-powerup-6768.mp3')
bounce_sfx = pygame.mixer.Sound('./audio/gameboy-pluck-41265.mp3')
game_over_sfx = pygame.mixer.Sound('./audio/game-over-38511.mp3')

pygame.mixer.music.load('./audio/8-bit-arcade-138828.mp3')
pygame.mixer.music.play(-1)

class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()

        self.image = pygame.Surface([width,height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image, color, [0,0,width,height])
        self.rect = self.image.get_rect()

    def moveUp(self, pixels):
        self.rect.y -= pixels
        #Check that you are not going too far (off the screen)
        if self.rect.y < 0:
          self.rect.y = 0
          
    def moveDown(self, pixels):
        self.rect.y += pixels
    #Check that you are not going too far (off the screen)
        if self.rect.y > 620:
          self.rect.y = 620

class Ball(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()

        self.image = pygame.Surface([width,height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image, color, [0,0,width,height])

        self.velocity = [randint(3,5), randint(3,5)]

        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = randint(-8,8)
        pygame.mixer.Sound.play(bounce_sfx)

    def reset(self):
        self.rect.x = 639
        self.rect.y = 355

def game_intro():
    intro = True
    while intro:
        pygame.mixer.Sound.play(game_start_sfx)
        intro = False

p1 = Paddle(GREEN, 10, 100)
p1.rect.x = 20
p1.rect.y = 310
p2 = Paddle(RED, 10, 100)
p2.rect.x = 1250
p2.rect.y = 310

ball = Ball(WHITE, 10, 10)
ball.reset()

scores = [0,0]

all_sprites_list = pygame.sprite.Group()
game_intro()

all_sprites_list.add(p1)
all_sprites_list.add(p2)
all_sprites_list.add(ball)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running == False

    input = pygame.key.get_pressed()
    if input[pygame.K_w]:
        p1.moveUp(7)
    if input[pygame.K_s]:
        p1.moveDown(7)
    if input[pygame.K_UP]:
        p2.moveUp(7)
    if input[pygame.K_DOWN]:
        p2.moveDown(7)

    screen.fill(BLACK)
    all_sprites_list.update()

    if ball.rect.x>=1270:
        ball.reset()
        scores[0] += 1
        pygame.mixer.Sound.play(scored_sfx)
        print(scores)
    if ball.rect.x<=0:
        ball.reset()
        scores[1] += 1
        pygame.mixer.Sound.play(scored_sfx)
        print(scores)
    if ball.rect.y>710:
        ball.velocity[1] = -ball.velocity[1]
        pygame.mixer.Sound.play(bounce_sfx)
    if ball.rect.y<0:
        ball.velocity[1] = -ball.velocity[1]
        pygame.mixer.Sound.play(bounce_sfx)

    if scores[0] >= 10:
        print("left win")
        pygame.mixer.Sound.play(game_over_sfx)
        time.sleep(4)
        running = False
    if scores[1] >= 10:
        print("right win")
        pygame.mixer.Sound.play(game_over_sfx)
        time.sleep(4)
        running = False

    if pygame.sprite.collide_mask(ball, p1) or pygame.sprite.collide_mask(ball, p2):
      ball.bounce()

    pygame.draw.line(screen, WHITE, [639,0], [639,720], 5)
    all_sprites_list.draw(screen)

    font = pygame.font.Font(None, 74)
    text = font.render(str(scores[0]), 1, WHITE)
    screen.blit(text, (250,10))
    text = font.render(str(scores[1]), 1, WHITE)
    screen.blit(text, (1030,10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
