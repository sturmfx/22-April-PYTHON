import pygame
import random

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ОХОТА НА КРУЖКИ")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

PLAYER_RADIUS = 20
TARGET_RADIUS = 10
TARGET_COUNT = 5
SPEED = 3
PLAYER_SPEED = 2
FPS = 60

player_x = WIDTH/2
player_y = HEIGHT/2

pygame.font.init()
font = pygame.font.Font(None, 20)
text_color = (0, 0, 0)
start_ticks = pygame.time.get_ticks()
score = 0
elapsed_time = 0


class Target:
    def __init__(self):
        self.lives = True
        self.x = random.randint(TARGET_RADIUS, WIDTH - TARGET_RADIUS)
        self.y = random.randint(TARGET_RADIUS, WIDTH - TARGET_RADIUS)
        self.dx = random.choice([-SPEED, SPEED])
        self.dy = random.choice([-SPEED, SPEED])

    def move(self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy

        if self.x < TARGET_RADIUS or self.x > WIDTH - TARGET_RADIUS:
            self.dx = -self.dx * random.uniform(0.9, 1.1)
        if self.y < TARGET_RADIUS or self.y > HEIGHT - TARGET_RADIUS:
            self.dy = -self.dy * random.uniform(0.9, 1.1)

    def draw(self, surface):
        pygame.draw.circle(surface, RED, (self.x, self.y), TARGET_RADIUS)


targets = [Target() for _ in range(TARGET_COUNT)]

running = True
clock = pygame.time.Clock()
while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x = max(player_x - PLAYER_SPEED, PLAYER_RADIUS)
    if keys[pygame.K_RIGHT]:
        player_x = min(player_x + PLAYER_SPEED, WIDTH - PLAYER_RADIUS)
    if keys[pygame.K_UP]:
        player_y = max(player_y - PLAYER_SPEED, PLAYER_RADIUS)
    if keys[pygame.K_DOWN]:
        player_y = min(player_y + PLAYER_SPEED, HEIGHT - PLAYER_RADIUS)
    pygame.draw.circle(screen, BLUE, (player_x, player_y), PLAYER_RADIUS)
    live_targets = 0
    for target in targets:
        if target.lives:
            live_targets = live_targets + 1
            target.move()
            target.draw(screen)
            distance = ((player_x - target.x) ** 2 + (player_y - target.y) ** 2) ** 0.5
            if distance < PLAYER_RADIUS + TARGET_RADIUS and elapsed_time > 10:
                target.lives = False
                score = score + 1
    while live_targets < 3:
        targets.append(Target())
        live_targets = live_targets + 1
    elapsed_time = int((pygame.time.get_ticks() - start_ticks) / 1000)
    average_time = int(elapsed_time / score if score > 0 else 0)

    score_text = font.render(f"Score: {score}", True, text_color)
    elapsed_time_text = font.render(f"Elapsed time: {elapsed_time} seconds", True, text_color)
    average_time_text = font.render(f"Average time per target: {average_time} seconds per target", True, text_color)

    screen.blit(score_text, (10,10))
    screen.blit(elapsed_time_text, (10, 30))
    screen.blit(average_time_text, (10, 50))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
