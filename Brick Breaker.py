import pygame
import random

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BALL_RADIUS = 10
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
BRICK_WIDTH, BRICK_HEIGHT = 80, 20
BRICK_ROWS = 5
BRICK_COLUMNS = 10

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BRICK_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
THEME_COLORS = [
    [(255, 0, 0), (255, 128, 128), (255, 64, 64)],
    [(0, 255, 0), (128, 255, 128), (64, 255, 64)],
    [(0, 0, 255), (128, 128, 255), (64, 64, 255)]
]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brick Breaker")

clock = pygame.time.Clock()

def draw_paddle(paddle_x):
    pygame.draw.rect(screen, THEME_COLORS[current_theme][1], (paddle_x, SCREEN_HEIGHT - PADDLE_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT))

def draw_brick(brick_x, brick_y, color):
    pygame.draw.rect(screen, color, (brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT))

paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2

ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT // 2
ball_dx = 5
ball_dy = -5

bricks = []
for row in range(BRICK_ROWS):
    for col in range(BRICK_COLUMNS):
        brick_x = col * (BRICK_WIDTH + 5)
        brick_y = row * (BRICK_HEIGHT + 5) + 50
        bricks.append((brick_x, brick_y, random.choice(BRICK_COLORS)))

current_theme = 0

score = 0

font = pygame.font.Font(None, 36)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                paddle_x -= 5
            if event.key == pygame.K_RIGHT:
                paddle_x += 5
            if event.key == pygame.K_SPACE:
                current_theme = (current_theme + 1) % 3

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle_x -= 5
    if keys[pygame.K_RIGHT]:
        paddle_x += 5
    ball_x += ball_dx
    ball_y += ball_dy

    if ball_x <= 0 or ball_x >= SCREEN_WIDTH:
        ball_dx = -ball_dx
    if ball_y <= 0:
        ball_dy = -ball_dy

    if ball_y >= SCREEN_HEIGHT - PADDLE_HEIGHT and (paddle_x <= ball_x <= paddle_x + PADDLE_WIDTH):
        ball_dy = -ball_dy

    for brick in bricks:
        brick_x, brick_y, brick_color = brick
        if (brick_x <= ball_x <= brick_x + BRICK_WIDTH) and (brick_y <= ball_y <= brick_y + BRICK_HEIGHT):
            ball_dy = -ball_dy
            bricks.remove(brick)
            score += 10  

    screen.fill(BLACK)

    draw_paddle(paddle_x)

    for brick in bricks:
        brick_x, brick_y, brick_color = brick
        draw_brick(brick_x, brick_y, brick_color)

    pygame.draw.circle(screen, THEME_COLORS[current_theme][0], (ball_x, ball_y), BALL_RADIUS)

    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))
    pygame.display.update()

    clock.tick(60)

pygame.quit()
