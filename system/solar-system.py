
import pygame
import math
import random

pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption("Солнечная система")

WIDTH, HEIGHT = 800, 600
cx, cy = WIDTH // 2, HEIGHT // 2
FPS = 60
clock = pygame.time.Clock()


explosion_sound = pygame.mixer.Sound("explosion.wav")


REAL_RADII = {
    "mercury": 2440,
    "venus": 6052,
    "earth": 6371,
    "moon": 1737,
    "mars": 3390,
    "jupiter": 69911,
    "saturn": 58232,
    "uranus": 25362,
    "neptune": 24622
}

EARTH_R = REAL_RADII["earth"]

def scale_radius(real_r):
    return max(4, int(real_r / EARTH_R * 20 / 3))


PERIODS = {
    "mercury": 88,
    "venus": 225,
    "earth": 365,
    "moon": 27,
    "mars": 687,
    "jupiter": 4333,
    "saturn": 10759,
    "uranus": 30687,
    "neptune": 60182
}

SPEED_SCALE = 100
def orbital_speed(period_days):
    seconds = period_days * 24 * 3600
    return (2 * math.pi) / seconds * SPEED_SCALE


class Planet:
    def __init__(self, screen, name, orbit_radius, angle=0):
        self.screen = screen
        self.name = name

        self.radius = scale_radius(REAL_RADII[name])
        self.orbit_radius = orbit_radius
        self.angle = angle
        self.speed = orbital_speed(PERIODS[name])

        img = pygame.image.load(f"images/{name}.jpg").convert_alpha()
        self.image = pygame.transform.scale(img, (self.radius*2, self.radius*2))

        self.x = 0
        self.y = 0

    def update(self, dt):
        global cx, cy
        self.angle += self.speed * dt
        self.x = cx + self.orbit_radius * math.cos(self.angle)
        self.y = cy + self.orbit_radius * math.sin(self.angle)

    def draw(self):
        self.screen.blit(self.image, (int(self.x - self.radius), int(self.y - self.radius)))


class Moon(Planet):
    def __init__(self, screen, earth_obj, orbit_radius):
        super().__init__(screen, "moon", orbit_radius)
        self.earth = earth_obj

    def update(self, dt):
        self.angle += self.speed * dt
        self.x = self.earth.x + self.orbit_radius * math.cos(self.angle)
        self.y = self.earth.y + self.orbit_radius * math.sin(self.angle)




sun_radius = 35
sun_img = pygame.image.load("images/sun.jpg").convert_alpha()
sun_img = pygame.transform.scale(sun_img, (sun_radius*2, sun_radius*2))

sun_expanding = False
sun_expand_progress = 0
explosion_triggered = False

mercury = Planet(screen, "mercury", 50)
venus   = Planet(screen, "venus", 90)
earth   = Planet(screen, "earth", 140)
moon    = Moon(screen, earth, 25)
mars    = Planet(screen, "mars", 190)
jupiter = Planet(screen, "jupiter", 260)
saturn  = Planet(screen, "saturn", 330)
uranus  = Planet(screen, "uranus", 400)
neptune = Planet(screen, "neptune", 460)

planets = [mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]



asteroid_img = pygame.image.load("images/asteroid.jpg").convert_alpha()
asteroid_img = pygame.transform.scale(asteroid_img, (8, 8))

asteroids = []
for _ in range(280):
    angle = random.uniform(0, 2*math.pi)
    r = random.uniform(210, 250)  
    x = cx + r * math.cos(angle)
    y = cy + r * math.sin(angle)
    asteroids.append([x, y])



running = True
while running:
    dt = clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if (mx - cx)**2 + (my - cy)**2 <= sun_radius**2:
                sun_expanding = True

        elif event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            cx, cy = WIDTH // 2, HEIGHT // 2

    

    if not sun_expanding:
        for p in planets:
            p.update(dt)
        moon.update(dt)

    
    if sun_expanding and not explosion_triggered:
        sun_expand_progress += dt * 0.0005
        if sun_expand_progress >= 1:
            explosion_triggered = True
            explosion_sound.play()

    

    if explosion_triggered:
        screen.fill((150, 0, 0))  
        pygame.display.flip()
        continue

    screen.fill((0, 0, 20))

    
    for ax, ay in asteroids:
        screen.blit(asteroid_img, (ax - 4, ay - 4))

    
    if sun_expanding:
        R = int(sun_radius + (140 - sun_radius) * sun_expand_progress)
        sun_scaled = pygame.transform.scale(sun_img, (R*2, R*2))
        screen.blit(sun_scaled, (cx - R, cy - R))
    else:
        screen.blit(sun_img, (cx - sun_radius, cy - sun_radius))

    
    for p in planets:
        p.draw()

    
    moon.draw()

    pygame.display.flip()

pygame.quit()
