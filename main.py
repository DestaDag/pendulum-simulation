from distutils.log import debug
from turtle import pen, width
from numpy import angle
import pygame
from math import pi, sin, cos, floor


white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
yellow = (255,255,0)
grey = (220,220,220)
green = (0,255,0)
blue = (0,0,255)

height = 900
width = 900

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("pendulum simulation")

pygame.font.init()

debug_font = pygame.font.SysFont('Bauhuas 93', 30)
hint_font = pygame.font.SysFont('Bauhaus 93', 26)

gravity = 5
objects_group = []

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

class Origin():
    def __init__(self, x, y, color=grey):
        self.x = x
        self.y = y
        self.radius = 10
        self.color = color
    
    def draw(self):
        pygame.draw.circle(screen, self.color,(self.x, self.y), self.radius)

class Ball():
    global angle
    def __init__(self, x,y, length, color = red):
        self.x = x
        self.y = y
        self.radius = 15
        self.color = color
        self.origin = Origin(width //2, self.y)
        self.angle = pi/4
        self.angle_velocity = .1
        self.angle_acceleration = 0
        self.len = length
        self.timer = 0
        self.mass = 1

    def draw(self):
        global gravity
        force = (1 * self.mass)*gravity*sin(self.angle)
        self.angle_acceleration = (-1 * force) / self.len
        self.angle_velocity += self.angle_acceleration
        self.angle += self.angle_velocity

        self.x = self.len * sin(self.angle) + self.origin.x
        self.y = self.len * cos(self.angle) + self.origin.y

        self.origin.draw()
        pygame.draw.line(screen, grey, (self.origin.x, self.origin.y), (self.x, self.y))
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

        self.timer += 1

        draw_text(f"Current gravity: {gravity}", debug_font, white, width // 2, 30)
        draw_text(f"Current mass: {self.mass}", debug_font, white, width // 2, 60)
        draw_text(f"Current acceleration: {self.angle_acceleration}", debug_font, white, width // 2, 90)
        draw_text(f"Current momentum: {self.angle_velocity}", debug_font, white, width // 2, 120)
        draw_text(f"Press up or down key to change length! ", hint_font, white, 10, 30)
        draw_text(f"Press w or s key to change gravity! ", hint_font, white, 10, 60)
        draw_text(f"Press e or d key to change mass! ", hint_font, white, 10, 90)
        draw_text(f"Current length: {self.len} ", hint_font, white, 10, 120)
        
        """"
        if self.timer > 40:
            if gravity <= 160:
                if gravity >= 10:
                    gravity += 2
                    gravity = floor(gravity)
                
                else:
                    if gravity >= 1:
                        gravity += 1
                        gravity = floor(gravity)
                    else:
                        gravity += .10
            self.timer = 0
        """

class Pendulum(Ball):
    def __init__(self, x, y, length):
        Ball.__init__(self, x, y, length)

def update(window, obj_group):
    screen.fill(black)
    for obj in obj_group:
        obj.draw()
    pygame.display.update()


def main():
    global gravity
    run = True
    clock = pygame.time.Clock()

    pendulum = Pendulum(20, height //2 -200, 350)
    objects_group.append(pendulum)

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            key = pygame.key.get_pressed()
            if key[pygame.K_ESCAPE]:
                run = False
                pygame.quit()
            if key[pygame.K_UP]:
                pendulum.len -= 10
            if key[pygame.K_DOWN]:
                pendulum.len += 10
            if key[pygame.K_w]:
                if gravity <= 1:
                    gravity = 3
                gravity -= 2
            if key[pygame.K_s]:
                gravity += 2
            if key[pygame.K_e]:
                if pendulum.mass <= 1:
                    pendulum.mass = 2
                pendulum.mass -= 1
            if key[pygame.K_d]:
                pendulum.mass += 2
            if key[pygame.K_r]:
                pendulum.angle_velocity = .1
                pendulum.angle_acceleration = 0
                pendulum.angle = pi/4
                pendulum.timer = 0
                gravity = .01
        
        update(screen, objects_group)

if __name__ == "__main__":
    main()



