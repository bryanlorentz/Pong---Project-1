import sys
import random
from pygame.locals import *
from Paddle import PaddleClass
from Ball import *

# Start pygame
pygame.init()

# Window Dimensions
WINDOWWIDTH = 1000
WINDOWHEIGHT = 800

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Speed of ball
BALLSPEED = random.randint(1, 3)

# Speed of paddles
PADDLESPEED = 4

# Tuple for Vector2
tup = ()

ws = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Pong')

paddle_list = pygame.sprite.Group()

# Sound files
collide_sound = pygame.mixer.Sound("ball_collide.wav")
end_music = pygame.mixer.Sound("end_music.wav")

# PLAYER PADDLES
# Player's side paddle, should be on right of screen
player_paddle_side = PaddleClass(95, 20, WHITE)
player_paddle_side.rect.x = 950
player_paddle_side.rect.y = 350
paddle_list.add(player_paddle_side)
player_side_img = pygame.image.load("paddle_3.png")
i = pygame.transform.rotate(player_side_img, 90)
transform_img_p1 = pygame.transform.scale(i, (20, 95))


# Player's top/bottom paddles
player_paddle_top = PaddleClass(20, 95, WHITE)
player_paddle_top.rect.x = 850
player_paddle_top.rect.y = 50
paddle_list.add(player_paddle_top)
player_top_img = pygame.image.load("paddle_3.png")
transform_img_p2 = pygame.transform.scale(player_top_img, (95, 20))

player_paddle_bottom = PaddleClass(20, 95, WHITE)
player_paddle_bottom.rect.x = 850
player_paddle_bottom.rect.y = 750
paddle_list.add(player_paddle_bottom)
player_bottom_img = pygame.image.load("paddle_3.png")
transform_img_p3 = pygame.transform.scale(player_bottom_img, (95, 20))


# NPC PADDLES
# NPC's side paddle, should be on right of screen
npc_paddle_side = PaddleClass(95, 20, WHITE)
npc_paddle_side.rect.x = 30
npc_paddle_side.rect.y = 350
paddle_list.add(npc_paddle_side)
npc_side_img = pygame.image.load("paddle_1.png")
j = pygame.transform.rotate(npc_side_img, 90)
transform_img_n1 = pygame.transform.scale(j, (20, 95))

# NPC's top/bottom paddles
npc_paddle_top = PaddleClass(20, 95, WHITE)
npc_paddle_top.rect.x = 50
npc_paddle_top.rect.y = 50
paddle_list.add(npc_paddle_top)
npc_top_img = pygame.image.load("paddle_1.png")
transform_img_n2 = pygame.transform.scale(npc_top_img, (95, 20))

npc_paddle_bottom = PaddleClass(20, 95, WHITE)
npc_paddle_bottom.rect.x = 50
npc_paddle_bottom.rect.y = 750
paddle_list.add(npc_paddle_bottom)
npc_bottom_img = pygame.image.load("paddle_1.png")
transform_img_n3 = pygame.transform.scale(npc_bottom_img, (95, 20))


def game_finished(win):
    end_music.play()
    if win is True:
        print("Play again? (Y/N)")
        ans = input()
        final_ans = ans.upper()
        if final_ans != "Y" or final_ans != "N":
            pygame.quit()
            sys.exit()
        else:
            play()


# Runs the game
def play():
    quit_game = False
    play_again = False

    fps = pygame.time.Clock()
    posx = 500
    posy = 400

    player_score = 0
    npc_score = 0

    # Draw the Ball
    ball = BallClass(circ=pygame.draw.circle(ws, WHITE, (posx, posy), 15, 0), color=WHITE,
                     velocity=(random.randint(-3, 3), random.randint(-3, 3)), scale=BALLSPEED)

    ball_img = pygame.image.load("pong_ball.png")
    transform_img_b = pygame.transform.scale(ball_img, (15, 15))

    ball_list = [ball]

    while not quit_game:
        for event in pygame.event.get():
            if event.type == QUIT:
                quit_game = True

        ws.fill(Color('#303030'))

        paddle_list.update()

        # Vertical Dashed Lines (Tried to loop/iterate to account for spacing between each line, but that didn't work)
        pygame.draw.line(ws, WHITE, [500, 0], [500, 50], 4)
        pygame.draw.line(ws, WHITE, [500, 75], [500, 125], 4)
        pygame.draw.line(ws, WHITE, [500, 150], [500, 200], 4)
        pygame.draw.line(ws, WHITE, [500, 225], [500, 275], 4)
        pygame.draw.line(ws, WHITE, [500, 300], [500, 350], 4)
        pygame.draw.line(ws, WHITE, [500, 375], [500, 425], 4)
        pygame.draw.line(ws, WHITE, [500, 450], [500, 500], 4)
        pygame.draw.line(ws, WHITE, [500, 525], [500, 575], 4)
        pygame.draw.line(ws, WHITE, [500, 600], [500, 650], 4)
        pygame.draw.line(ws, WHITE, [500, 675], [500, 725], 4)
        pygame.draw.line(ws, WHITE, [500, 750], [500, 800], 4)

        # Paddle Movement (From Paddle.py class)
        k = pygame.key.get_pressed()
        if k[pygame.K_DOWN]:
            player_paddle_side.move_paddles(2, PADDLESPEED)
        if k[pygame.K_UP]:
            player_paddle_side.move_paddles(1, PADDLESPEED)
        if k[pygame.K_LEFT]:
            player_paddle_top.move_paddles(4, PADDLESPEED)
            player_paddle_bottom.move_paddles(4, PADDLESPEED)
        if k[pygame.K_RIGHT]:
            player_paddle_top.move_paddles(3, PADDLESPEED)
            player_paddle_bottom.move_paddles(3, PADDLESPEED)

        # Ball logic
        for b in ball_list:
            cir = b.get_circ()
            vel = b.get_velocity()
            col = b.get_color()
            cir.left += vel[0]
            cir.top += vel[1]
            posx += int(vel[0])
            posy += int(vel[1])

            # Player collision
            if cir.colliderect(player_paddle_top):
                collide_sound.play()
                vel[1] *= -1
            if cir.colliderect(player_paddle_bottom):
                collide_sound.play()
                vel[1] *= -1
            if cir.colliderect(player_paddle_side):
                collide_sound.play()
                vel[0] *= -1

            # Enemy paddles track ball
            npc_paddle_bottom.rect.x = cir.bottom
            if npc_paddle_bottom.rect.x >= 405:
                npc_paddle_bottom.rect.x = 405
            npc_paddle_side.rect.y = cir.left
            if npc_paddle_side.rect.y >= WINDOWHEIGHT:
                npc_paddle_side.rect.y = WINDOWHEIGHT
            elif npc_paddle_side.rect.y <= 0:
                npc_paddle_side.rect.y = 0
            npc_paddle_top.rect.x = cir.top
            if npc_paddle_top.rect.x >= 405:
                npc_paddle_top.rect.x = 405

            # Enemy collision
            if cir.colliderect(npc_paddle_top):
                collide_sound.play()
                vel[1] *= -1
            if cir.colliderect(npc_paddle_bottom):
                collide_sound.play()
                vel[1] *= -1
            if cir.colliderect(npc_paddle_side):
                collide_sound.play()
                vel[0] *= -1

            # Conditionals to determine score if ball goes out of bounds, resets the ball to
            # middle of screen, and randomizes velocity
            if cir.top <= 0 or cir.bottom >= WINDOWHEIGHT:
                if (cir.top <= 0 and cir.left <= 499) or \
                        (cir.bottom >= WINDOWHEIGHT and cir.left <= 499) or (cir.left <= 0):
                    player_score += 1
                elif (cir.top <= 0 and cir.right >= 501) or (
                        cir.bottom >= WINDOWHEIGHT and cir.right >= 501) or (cir.right >= WINDOWWIDTH):
                    npc_score += 1

                cir.left = posx = 500
                cir.top = posy = 400
                vel[0] = random.randint(-5, 5)
                vel[1] = random.randint(-5, 5)

                if vel[0] == 0 and vel[1] == 0:
                    vel[0] = random.randint(-5, 5)
                    vel[1] = random.randint(-5, 5)

                if player_score == 11 and player_score == npc_score + 2:
                    print("player wins!")
                    play_again = True
                    game_finished(play_again)
                elif npc_score == 11 and npc_score == player_score + 2:
                    print("npc wins!")
                    play_again = True
                    game_finished(play_again)
                else:
                    continue
            elif cir.left <= 0 or cir.right >= WINDOWWIDTH:
                if (cir.top <= 0 and cir.left <= 499) or \
                        (cir.bottom >= WINDOWHEIGHT and cir.left <= 499) or (cir.left <= 0):
                    player_score += 1
                elif (cir.top <= 0 and cir.right >= 501) or (
                        cir.bottom >= WINDOWHEIGHT and cir.right >= 501) or (cir.right >= WINDOWWIDTH):
                    npc_score += 1

                cir.left = posx = 500
                cir.top = posy = 400
                vel[0] = random.randint(-5, 5)
                vel[1] = random.randint(-5, 5)

                if vel[0] == 0 and vel[1] == 0:
                    vel[0] = random.randint(-5, 5)
                    vel[1] = random.randint(-5, 5)

                if player_score == 11:
                    print("player wins!")
                    play_again = True
                    game_finished(play_again)
                elif npc_score == 11:
                    print("npc wins!")
                    play_again = True
                    game_finished(play_again)
                else:
                    continue

            pygame.draw.circle(ws, WHITE, (posx, posy), 15)

            # Scoreboard
            font = pygame.font.SysFont(None, 48)

            ptext = font.render(str(player_score), True, WHITE)
            text_player = ptext.get_rect()
            text_player.centerx = 525
            text_player.centery = 25
            ws.blit(ptext, text_player)

            ntext = font.render(str(npc_score), True, WHITE)
            text_npc = ntext.get_rect()
            text_npc.centerx = 475
            text_npc.centery = 25
            ws.blit(ntext, text_npc)

            ws.blit(transform_img_p1, player_paddle_side)
            ws.blit(transform_img_p2, player_paddle_top)
            ws.blit(transform_img_p3, player_paddle_bottom)
            ws.blit(transform_img_n1, npc_paddle_side)
            ws.blit(transform_img_n2, npc_paddle_top)
            ws.blit(transform_img_n3, npc_paddle_bottom)
            ws.blit(transform_img_b, b.get_circ())

        paddle_list.draw(ws)
        pygame.display.flip()

        fps.tick(60)

    pygame.quit()
    sys.exit()


play()
