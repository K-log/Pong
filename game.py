import pygame
import sys
import random
import os
from pygame.locals import *

# Initialise pygame
pygame.init()
pygame.font.init()

SCREEN_WIDTH = 540
SCREEN_HEIGHT = 420
SCREEN_CAPTION = "Pong"

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(SCREEN_CAPTION)

clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
OFF_WHITE = (230, 230, 230)
BLACK = (0, 0, 0)
GREY = (50, 50, 50)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

paddles = []
balls = []

# Text for start screen
start_button_font = pygame.font.SysFont('verdana', 30)
start_title_font = pygame.font.SysFont('comicsansms', 90)
score_board_font = pygame.font.SysFont('verdana', 30)
paused_font = pygame.font.SysFont('impact', 70)
start_text = start_button_font.render('START', True, BLACK)
game_title = start_title_font.render('Pong', True, WHITE)
game_instruction_text = start_button_font.render('Instructions', True, BLACK)
instruction_back_text = start_button_font.render('Back', True, BLUE)
paused_text = paused_font.render('Game Paused', True, BLUE)
unpause_text = start_button_font.render('Unpause', True, BLUE)
info_text = start_button_font.render('First to 5 points wins', True, WHITE)
game_over_text = paused_font.render('GAME OVER', True, WHITE)


# Classes
class Paddle(object):
    id = "Default"
    pos = (0, 0)
    height = 60
    width = 10
    score = 0
    dy = 3

    def __init__(self, id, x, y):
        self.id = id
        self.pos = (x, y)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
        paddles.append(self)

    def move(self, user_input):
        if self.id == "right":
            if user_input[pygame.K_DOWN] and self.rect.y < SCREEN_HEIGHT - self.height:
                self.rect.y += self.dy
            if user_input[pygame.K_UP] and self.rect.y > 0:
                self.rect.y -= self.dy
        elif self.id == "left":
            if user_input[pygame.K_s] and self.rect.y < SCREEN_HEIGHT - self.height:
                self.rect.y += self.dy
            if user_input[pygame.K_w] and self.rect.y > 0:
                self.rect.y -= self.dy

    def draw_score(self, location):
        score_text = score_board_font.render(str(self.score), True, WHITE)
        screen.blit(score_text, location)

    def scored(self):
            pass


class Ball(object):
    pos = (0, 0)
    height = 10
    width = 10
    dx = 2.5
    dy = 2.5
    r = 0

    def __init__(self, x, y):
        self.pos = (x, y)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
        balls.append(self)

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def collide(self):
        if self.rect.y <= 0 or self.rect.y >= SCREEN_HEIGHT:
            self.dy *= -1  # check if collision with top or bottom of screen
        for p in paddles:
            if self.rect.colliderect(p):
                self.dx *= -1  # check if collision with paddles
        if self.rect.x <= 0:
            paddles[0].score += 1
            self.reset()
            return True
        elif self.rect.x >= SCREEN_WIDTH:
            paddles[1].score += 1
            self.reset()
            return True

    def reset(self):
        self.r = random.randint(-1, 1)

        self.rect.x = SCREEN_WIDTH / 2
        self.rect.y = SCREEN_HEIGHT / 2

        self.dx = 0
        self.dy = 0

        self.start()

    def start(self):
        self.dx = 3
        self.dy = 3
        if self.r == -1:
            self.dx *= -1
        elif self.r == 1:
            self.dx *= 1
        elif self.r == 0:
            self.dy *= -1


# Functions
def pause_game(key):
    paused = False

    if key[K_ESCAPE]:
        paused = True
    while paused:
        mouse_pressed = pygame.mouse.get_pressed()
        screen.blit(paused_text, (SCREEN_WIDTH * 0.15, SCREEN_HEIGHT * 0.3))
        get_quit_event()

        unpause_button_rect = pygame.Rect(SCREEN_WIDTH * 0.32, SCREEN_HEIGHT * 0.7, SCREEN_WIDTH * 0.4, 40)

        if mouse_pointer().colliderect(unpause_button_rect):
            unpause_button_color = WHITE
            if mouse_pressed[0]:
                paused = False
        else:
            unpause_button_color = OFF_WHITE

        pygame.draw.rect(screen, unpause_button_color, unpause_button_rect)
        screen.blit(unpause_text, ((SCREEN_WIDTH * 0.40), SCREEN_HEIGHT * 0.7))
        pygame.display.flip()
        clock.tick(60)


def mouse_pointer():
    curser = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 10, 10)
    # pygame.draw.rect(window, WHITE, curser)
    return curser


def get_quit_event():
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


def instruction_screen():
    back_button_rect = pygame.Rect(SCREEN_WIDTH * 0.65, SCREEN_HEIGHT * 0.8, SCREEN_WIDTH * 0.2, 40)
    back = False
    while not back:
        get_quit_event()
        mouse_pressed = pygame.mouse.get_pressed()
        screen.fill(BLACK)
        instruct_img = pygame.image.load(os.path.join('instruction.png'))
        screen.blit(instruct_img, (40, 20))
        if mouse_pointer().colliderect(back_button_rect):
            back_button_color = WHITE
            if mouse_pressed[0]:
                back = True
        else:
            back_button_color = OFF_WHITE

        pygame.draw.rect(screen, back_button_color, back_button_rect)
        screen.blit(instruction_back_text, ((SCREEN_WIDTH * 0.68), SCREEN_HEIGHT * 0.8))

        pygame.display.flip()


def start_screen():
    get_quit_event()
    mouse_pressed = pygame.mouse.get_pressed()
    screen.fill(BLACK)
    start_button_rect = pygame.Rect(SCREEN_WIDTH * 0.32, SCREEN_HEIGHT * 0.5, SCREEN_WIDTH * 0.4, 40)
    instruction_button_rect = pygame.Rect(SCREEN_WIDTH * 0.32, SCREEN_HEIGHT * 0.7, SCREEN_WIDTH * 0.4, 40)

    if mouse_pointer().colliderect(start_button_rect):
        start_button_color = WHITE
        if mouse_pressed[0]:
            return True
    else:
        start_button_color = OFF_WHITE

    if mouse_pointer().colliderect(instruction_button_rect):
        instruction_button_color = WHITE
        if mouse_pressed[0]:
            instruction_screen()
    else:
        instruction_button_color = OFF_WHITE

    pygame.draw.rect(screen, start_button_color, start_button_rect) # Start button Rect
    pygame.draw.rect(screen, instruction_button_color, instruction_button_rect) # Instruction button Rect
    screen.blit(game_title, ((SCREEN_WIDTH * 0.35), SCREEN_HEIGHT * 0.07))
    screen.blit(start_text, ((SCREEN_WIDTH * 0.42), SCREEN_HEIGHT * 0.5))
    screen.blit(game_instruction_text, ((SCREEN_WIDTH * 0.35), SCREEN_HEIGHT * 0.7))
    screen.blit(info_text, (SCREEN_WIDTH * 0.22, SCREEN_HEIGHT * 0.9))

    pygame.display.flip()


def game_over(player):
    player_wins = str(player.id) + ' won the game!'
    player_win_text = start_button_font.render(player_wins, True, BLUE)
    while True:
        screen.blit(game_over_text, ((SCREEN_WIDTH * 0.24), SCREEN_HEIGHT * 0.2))
        screen.blit(player_win_text, (SCREEN_WIDTH * 0.24, SCREEN_HEIGHT * 0.7))
        get_quit_event()
        pygame.display.flip()


def reset_game():
    for p in paddles:
        p.score = 0
        started = False
        done = False


def main():
    rpaddle = Paddle("right", SCREEN_WIDTH - 12, SCREEN_HEIGHT / 2)
    lpaddle = Paddle("left", 3, SCREEN_HEIGHT / 2)
    ball = Ball(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    global started
    global done
    started = False
    done = False
    # Game loop
    while not done:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                done = True

        pressed = pygame.key.get_pressed()

        screen.fill(BLACK)

        if started:

            for p in paddles:
                if p.score >= 5:
                    game_over(p)
                    done = True

            pause_game(pressed)

            # Draw score
            rpaddle.draw_score((SCREEN_WIDTH*0.7, 5))
            lpaddle.draw_score((SCREEN_WIDTH*0.27, 5))

            # Draw paddle rects
            pygame.draw.rect(screen, WHITE, rpaddle.rect)
            pygame.draw.rect(screen, WHITE, lpaddle.rect)

            # Draw ball rects
            for ball in balls:
                pygame.draw.rect(screen, WHITE, ball.rect)

            # Test ball collision
            ball.collide()

            # Move paddles
            rpaddle.move(pressed)
            lpaddle.move(pressed)

            # Move balls
            for ball in balls:
                ball.move()

        elif start_screen():
            ball.reset()
            started = True
        else:
            started = False

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
