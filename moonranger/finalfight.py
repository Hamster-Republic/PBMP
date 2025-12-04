import pygame
import math

pygame.init()
pygame.mixer.init()

screen_width, screen_height = 600, 400
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Moon ranger")

background_day = pygame.image.load("day.jpg")
background_night = pygame.image.load("night.jpg")
background = background_day

def scale_background():
    global background_day, background_night, background
    background_day = pygame.transform.scale(background_day, (screen_width, screen_height))
    background_night = pygame.transform.scale(background_night, (screen_width, screen_height))
    background = background_day

scale_background()

frog_image = pygame.image.load("player.png").convert()
frog_image.set_colorkey((255, 255, 255))
frog_image = pygame.transform.scale(frog_image, (40, 40))

x = 0
y = screen_height // 2
y_speed = 0
x_speed = 0
gravity = 1.2

ball_img = pygame.image.load("ball.jpg")
ball_img = pygame.transform.scale(ball_img, (20, 20))
shots = []

power = 12
angle = 0

obstacles = [pygame.Rect(800, 250, 40, 40),
             pygame.Rect(1300, 200, 40, 100)]

font = pygame.font.Font(None, 32)
health = 3
score = 0

shoot_sound = pygame.mixer.Sound("score.wav")
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)

running = True
clock = pygame.time.Clock()

while running:
    dt = clock.tick(60) / 16

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.VIDEORESIZE:
            screen_width, screen_height = event.w, event.h
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            scale_background()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                y_speed = -18
            elif event.key == pygame.K_a:
                x_speed = -6
            elif event.key == pygame.K_d:
                x_speed = 6
            elif event.key == pygame.K_SPACE:
                background = background_night if background == background_day else background_day
            elif event.key == pygame.K_f:
                rad = math.radians(angle)
                vx = power * math.cos(rad) + 10
                vy = power * math.sin(rad)
                shots.append([screen_width//2, y, vx, vy])
                shoot_sound.play()

        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_a, pygame.K_d):
                x_speed = 0

    y_speed += gravity
    y += y_speed
    x += x_speed

    if y < 20:
        y = 20
        y_speed = 0
    if y > screen_height - 20:
        y = screen_height - 20
        y_speed = 0

    bg_x = -x % screen_width

    screen.blit(background, (bg_x, 0))
    screen.blit(background, (bg_x - screen_width, 0))

    for s in shots:
        s[0] += s[2]
        s[1] += s[3]
        screen.blit(ball_img, (int(s[0]), int(s[1])))

    obstacle_speed = 4 + x_speed * 0.7

    for obs in obstacles:
        obs.x -= obstacle_speed
        pygame.draw.rect(screen, (255, 0, 0), obs)

        frog_rect = pygame.Rect(screen_width//2 - 20, y - 20, 40, 40)
        if frog_rect.colliderect(obs):
            health -= 1
            obs.x += 900

        for s in shots:
            if pygame.Rect(s[0], s[1], 20, 20).colliderect(obs):
                score += 10
                obs.x += 800
                shots.remove(s)
                break

        if obs.x < -100:
            obs.x += 1200

    screen.blit(frog_image, (screen_width//2 - 20, y - 20))

    text = font.render(f"HP: {health}   Score: {score}", True, (255, 255, 0))
    screen.blit(text, (10, 10))

    if health <= 0:
        lose_text = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(lose_text, (screen_width//2 - 80, screen_height//2 - 20))
        pygame.display.flip()
        pygame.time.wait(2000)
        break

    pygame.display.flip()

pygame.quit()
