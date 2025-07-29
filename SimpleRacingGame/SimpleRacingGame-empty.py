import pygame
import os

WIDTH = 720
HEIGHT = 480
METER = 16
FPS = 60

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Lucida Console', 30)

clock = pygame.time.Clock()
background1 = pygame.image.load(os.path.join('Assets', 'background1.png'))
background2 = pygame.image.load(os.path.join('Assets', 'background2.png'))
background3 = pygame.image.load(os.path.join('Assets', 'sky.png'))
vehicle = pygame.image.load(os.path.join('Assets', 'vehicle2.png'))
bgrect1 = background1.get_rect()
bgrect2 = background2.get_rect()
bgrect3 = background3.get_rect()
vehiclerect = vehicle.get_rect()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("1/4 mile race")

def display():
    WIN.blit(background3, bgrect3)
    WIN.blit(background2, bgrect2)
    WIN.blit(background2, bgrect2.move(bgrect2.width, 0))
    WIN.blit(background1, bgrect1)
    WIN.blit(background1, bgrect1.move(bgrect1.width, 0))
    WIN.blit(vehicle, (40, HEIGHT - 140))

    if bgrect1.right <= 0 and bgrect1.left <= WIDTH:
        bgrect1.x = 0
    if bgrect2.right <= 0 and bgrect2.left <= WIDTH:
        bgrect2.x = 0
def main():
    throttle = 0
    running = True
    while running:
        keys = pygame.key.get_pressed()
        movement = METER * throttle * 5 / FPS * (-1)
        display()
        bgrect1.move_ip(movement, 0)
        bgrect2.move_ip(movement / 4, 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False

        if keys[pygame.K_UP]:
            throttle = 1
        else:
            throttle = 0

        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()


main()
