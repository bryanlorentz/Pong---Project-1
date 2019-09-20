import pygame
from pygame.math import Vector2

WHITE = (255, 255, 255)


def ball_velocity(tup, scale):
    v = Vector2()
    v[0], v[1] = tup[0], tup[1]
    return v * scale


class BallClass(pygame.sprite.Sprite):
    def __init__(self, circ, color, velocity, scale=1):
        super().__init__()
        self.circ = pygame.Rect(circ)
        self.color = color
        self.velocity = ball_velocity(velocity, scale)

    def get_velocity(self):
        return self.velocity

    def get_circ(self):
        return self.circ

    def get_color(self):
        return self.color

    def move_ball(self):
        self.circ.left += self.velocity[0]
        self.circ.top += self.velocity[1]
