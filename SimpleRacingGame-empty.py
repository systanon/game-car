import math

import pygame
import os

WIDTH = 720
HEIGHT = 480
METER = 16
WHEEL_RAD = 0.32535
FINAL_DRIVE = 4.47
WEIGHT = 1650
GEAR_RATIO = [0, 3.538, 1.92, 1.322, 0.975, 0.76, 0.654]
FPS = 60
TORQUE = [150, 160, 185, 260, 330, 370, 360, 355, 350, 340, 325, 300, 275, 260, 255, 0]


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
    speed = 0
    running = True
    distance = 0
    time = 0
    gear = 0

    while running:
        keys = pygame.key.get_pressed()
        movement = METER * speed / FPS * (-1)
        time += FPS/3600


        wheel_RPM = speed / (WHEEL_RAD * 2 * math.pi / 60)
        eng_RPM = wheel_RPM * GEAR_RATIO[gear] * FINAL_DRIVE

        if eng_RPM < 750:
            print("Silnik gaśnie")
            eng_RPM = 750
        if eng_RPM > 4250:
            print("Odcina!")
            eng_RPM = 4250

        force = TORQUE[round(eng_RPM/250) -2] * GEAR_RATIO[gear] * FINAL_DRIVE / WHEEL_RAD
        rolling_res = WEIGHT * 9.81 * 0.01 / math.sqrt(WHEEL_RAD * WHEEL_RAD + 0.01 * 0.01)
        aero_drag = 0.5 * 1.2 * speed * speed * 0.3 * 2.61
        acceleration = (force - rolling_res - aero_drag) / WEIGHT


        if acceleration < 0:
            acceleration = 0
        decceleration = (rolling_res - aero_drag) / WEIGHT
        display()
        sppedSurface = myfont.render("Speed: " + str(round(speed*3.6)) + " kh/m" , True, (0, 0, 0))
        distanceSurface = myfont.render("Distance: " + f"{distance/1000: .3f} km", True, (0, 0, 0))
        timeSurface = myfont.render("Time: " + str(round(time)) + "s", True, (0, 0, 0))
        gearSurface = myfont.render("Gear: " + str(gear), True, (0, 0, 0))
        revSurface = myfont.render("Revs: " + str(round(eng_RPM)) + " RPM", True, (0, 0, 0))

        WIN.blit(gearSurface, (0, 120))
        WIN.blit(sppedSurface, (0, 0))
        WIN.blit(distanceSurface, (0, 40))
        WIN.blit(timeSurface, (0, 80))
        WIN.blit(revSurface, (0, 160))
        bgrect1.move_ip(movement, 0)
        bgrect2.move_ip(movement / 4, 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                if event.key == pygame.K_w and gear < len(GEAR_RATIO) - 1:
                    gear += 1
                if event.key == pygame.K_s and gear > 0:
                    gear -= 1

        if keys[pygame.K_UP] and speed < 53.3:
            speed += acceleration / FPS
            distance += speed / FPS
        elif speed > 0:
            speed -= decceleration / FPS
            distance += speed / FPS
        if keys[pygame.K_DOWN] and speed > 0:
            speed -= 18 / FPS
            distance += speed / FPS
        if eng_RPM < 750:
            eng_RPM = 750
        if eng_RPM > 4250:
            eng_RPM = 4250

        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()


main()
