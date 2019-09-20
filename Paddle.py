import pygame

WHITE = (255, 255, 255)


class PaddleClass(pygame.sprite.Sprite):
    def __init__(self, paddle_height, paddle_width, color):
        super().__init__()
        self.image = pygame.Surface([paddle_width, paddle_height])
        self.image.set_colorkey(WHITE)
        pygame.draw.rect(self.image, color, [0, 0, paddle_width, paddle_height])
        self.rect = self.image.get_rect()

    # Function to move paddles via a numbered code sent from Pong.py (Need to take into account the top-left location
    # of each paddle when creating the dimensions in which each paddle can move)
    def move_paddles(self, code, move):
        # Move up
        if code == 1:
            self.rect.y -= move
            if self.rect.y <= 0:
                self.rect.y = 0
        # Move down
        elif code == 2:
            self.rect.y += move
            if self.rect.y >= 705:
                self.rect.y = 705
        # Move Left
        elif code == 3:
            self.rect.x += move
            if self.rect.x >= 905:
                self.rect.x = 905
        # Move Right
        elif code == 4:
            self.rect.x -= move
            if self.rect.x <= 500:
                self.rect.x = 500
