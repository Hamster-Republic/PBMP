import pygame
import math
pygame.init()

screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Ball")

background = pygame.image.load("ruins.jpg")
background = pygame.transform.scale(background, (600, 400))
ball_image = pygame.image.load("fridge.jpg")
ball_image = pygame.transform.scale(ball_image, (30, 30))
hoop_img = pygame.image.load("fly.jpg")
hoop_img = pygame.transform.scale(hoop_img, (60, 60))


pygame.mixer.init()
pygame.mixer.music.load("play.mp3")
pygame.mixer.music.play(-1)

score_sound = pygame.mixer.Sound("click.wav")

start_x, start_y = 100, 300
x, y = start_x, start_y
radius = 15

vx, vy = 0, 0
gravity = 0.5
power = 12
angle = 45
bounce_loss = 0.7
on_ground = True

hoop_x, hoop_y = 500, 200
hoop_width, hoop_height = 60, 10
hoop_speed = 1.2 

font = pygame.font.Font(None, 24)

scored_flag = False
score = 0

key_up = False
key_down = False
key_w = False
key_s = False

running = True
clock = pygame.time.Clock()

while running:
    dt = clock.tick(60) / 16  
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                key_up = True
            elif event.key == pygame.K_DOWN:
                key_down = True
            elif event.key == pygame.K_w:
                key_w = True
            elif event.key == pygame.K_s:
                key_s = True

            elif event.key == pygame.K_SPACE and on_ground:
                rad = math.radians(angle)
                vx = power * math.cos(rad)
                vy = -power * math.sin(rad)
                on_ground = False
        
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                key_up = False
            elif event.key == pygame.K_DOWN:
                key_down = False
            elif event.key == pygame.K_w:
                key_w = False
            elif event.key == pygame.K_s:
                key_s = False

    
    if key_up:
        angle = min(angle + 0.5, 80)
    if key_down:
        angle = max(angle - 0.5, 10)
    if key_w:
        power = min(power + 0.1, 25)
    if key_s:
        power = max(power - 0.1, 5)

    
    hoop_x += hoop_speed

    if hoop_x <= 350:
        hoop_speed = abs(hoop_speed)
    if hoop_x + hoop_width >= 580:
        hoop_speed = -abs(hoop_speed)

    
    if not on_ground:
        vy += gravity
        x += vx
        y += vy

    if y + radius >= 400:
        y = 400 - radius
        vy = -vy * bounce_loss
        vx *= bounce_loss
        if abs(vy) < 1 and abs(vx) < 1:
            x, y = start_x, start_y
            vx, vy = 0, 0
            on_ground = True
            scored_flag = False

   
    hoop_rect = pygame.Rect(hoop_x, hoop_y, hoop_width, hoop_height)
    ball_rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)

    if ball_rect.colliderect(hoop_rect) and not scored_flag:
        scored_flag = True
        score += 1
        score_sound.play()

    
    screen.blit(background, (0, 0))

    
    if on_ground:
        points = []
        rad = math.radians(angle)
        temp_vx = power * math.cos(rad)
        temp_vy = -power * math.sin(rad)
        temp_x, temp_y = start_x, start_y

        for i in range(120):
            temp_vy += gravity
            temp_x += temp_vx
            temp_y += temp_vy
            if temp_y + radius >= 400:
                break
            points.append((int(temp_x), int(temp_y)))

        if len(points) > 1:
            pygame.draw.lines(screen, (0, 0, 0), False, points, 2)

    screen.blit(hoop_img, (hoop_x, hoop_y - 25))  
    screen.blit(ball_image, (int(x - radius), int(y - radius)))

    text_angle = font.render(f"Угол: {int(angle)}°", True, (255, 0, 0))
    text_power = font.render(f"Сила: {int(power)}", True, (255, 0, 0))
    text_score = font.render(f"Счёт: {score}", True, (255, 0, 0))
    screen.blit(text_angle, (10, 10))
    screen.blit(text_power, (10, 30))
    screen.blit(text_score, (10, 50))

    if scored_flag:
        hit_text = font.render("ПОПАДАНИЕ!", True, (0, 255, 0))
        screen.blit(hit_text, (250, 50))

    pygame.display.flip()

pygame.quit()
