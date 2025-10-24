import pygame
import random

pygame.init()

WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Падающие шары")

ball_radius = 20
player_radius = ball_radius
step = 20

x, y = WIDTH // 2, HEIGHT - player_radius - 10

background = pygame.image.load("background.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

player_image = pygame.image.load("player.png")
player_image = pygame.transform.smoothscale(player_image, (player_radius * 2, player_radius * 2))

miss_sound = pygame.mixer.Sound("click.wav")

spawn_interval = 1500
last_spawn_time = 0

score = 0
missed = 0
max_missed = 3

balls = []

font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)

clock = pygame.time.Clock()
running = True
game_over = False

while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN and not game_over:
          

            if event.key == pygame.K_a:
                x -= step
            elif event.key == pygame.K_d:
                x += step

            x = max(player_radius, min(WIDTH - player_radius, x))
            y = max(player_radius, min(HEIGHT - player_radius, y))

    if not game_over:
        if current_time - last_spawn_time > spawn_interval:
            x_ball = random.randint(ball_radius, WIDTH - ball_radius)
            y_ball = -ball_radius
            fall_speed_y = random.uniform(2, 5)
            fall_speed_x = random.uniform(-2, 2)
            balls.append([x_ball, y_ball, fall_speed_y, fall_speed_x, False])
            last_spawn_time = current_time

        for ball in balls:
            if ball[4]:
                ball[1] += ball[2]
            else:
                ball[0] += ball[3]
                ball[1] += ball[2]
                if ball[0] - ball_radius <= 0 or ball[0] + ball_radius >= WIDTH:
                    ball[3] = 0
                    ball[4] = True
                    ball[0] = max(ball_radius, min(WIDTH - ball_radius, ball[0]))

        for ball in balls[:]:
            dx = x - ball[0]
            dy = y - ball[1]
            distance = (dx**2 + dy**2)**0.5
            if distance < player_radius + ball_radius:
                score += 1
                balls.remove(ball)

        for ball in balls[:]:
            if ball[1] > HEIGHT:
                balls.remove(ball)
                missed += 1
                miss_sound.play()
                if missed >= max_missed:
                    game_over = True

    screen.blit(background, (0, 0))
    screen.blit(player_image, (x - player_radius, y - player_radius))

    for ball in balls:
        pygame.draw.circle(screen, (255, 0, 0), (int(ball[0]), int(ball[1])), ball_radius)

    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    missed_text = font.render(f"Missed: {missed}/{max_missed}", True, (255, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(missed_text, (10, 40))

    if game_over:
        over_text = big_font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2,
                                HEIGHT // 2 - over_text.get_height() // 2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
