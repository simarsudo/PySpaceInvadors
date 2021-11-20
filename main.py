import pygame
import os
import time
import random

pygame.font.init()

WIDTH, HEIGHT = 800, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Enemy player images load
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# Player player image load
YELLOW_SHIP_PLAYER = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# Laser image load
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# Background image load
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))


class Ship:
    def __init__(self, x_pos, y_pos, health=100):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.health = health
        self.ship_image = None
        self.laser_img = None
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_image, (self.x_pos, self.y_pos))

    def get_width(self):
        return self.ship_image.get_width()

    def get_height(self):
        return self.ship_image.get_height()


class Player(Ship):
    def __init__(self, x_pos, y_pos, health=100):
        super().__init__(x_pos, y_pos)
        self.health = health
        self.ship_image = YELLOW_SHIP_PLAYER
        self.mask = pygame.mask.from_surface(self.ship_image)
        self.laser_img = YELLOW_LASER


class Enemy(Player):
    COLOR_MAP = {
        'red': (RED_SPACE_SHIP, RED_LASER),
        'green': (GREEN_SPACE_SHIP, GREEN_LASER),
        'blue': (BLUE_SPACE_SHIP, BLUE_LASER)
    }

    def __init__(self, x_pos, y_pos, color, health=100):
        super().__init__(x_pos, y_pos, health)
        self.ship_image, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_image)

    def move(self, vel):
        self.y_pos += vel


def main():
    run = True
    FPS = 60
    level = 1
    lives = 5

    enemy_vel = 1
    wave_length = 5
    enemies = []

    Clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    player = Player(300, 650)
    player_vel = 5

    main_font = pygame.font.SysFont("comicsans", 30)
    lost_font = pygame.font.SysFont("comicsans", 40)

    def redraw_window():
        WIN.blit(BG, (0, 0))

        lives_label = main_font.render(f"Lives: {lives}", True, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", True, (255, 255, 255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("You Lost!", True, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH/2, lost_label.get_width()/2, 350))

        pygame.display.update()

    while run:
        Clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randint(50, WIDTH - 100), random.randrange(-1500, 100), random.choice(['red', 'blue', 'green']))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and player.y_pos + player_vel > 0:  # up
            player.y_pos -= player_vel
        if keys[pygame.K_s] and player.y_pos + player_vel + player.get_height() < HEIGHT:  # down
            player.y_pos += player_vel
        if keys[pygame.K_a] and player.x_pos + player_vel > 0:  # left
            player.x_pos -= player_vel
        if keys[pygame.K_d] and player.x_pos + player_vel + player.get_width() < WIDTH:  # right
            player.x_pos += player_vel

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            if enemy.y_pos + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

    pygame.quit()


if __name__ == '__main__':
    main()
