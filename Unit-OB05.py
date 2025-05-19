import pygame
import random
import sys
import os

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
FPS = 60
CAR_SPEED = 5
OBSTACLE_SPEED = 4
SCORE_INCREMENT = 0.1

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ROAD_COLOR = (50, 50, 50)
YELLOW = (255, 255, 0)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Гонки с препятствиями")
clock = pygame.time.Clock()



# Загрузка изображений
def load_image(name, size=None, transparent_color=None):
    try:
        # Загружаем как обычный Surface без конвертации
        image = pygame.image.load(name)

        # Если нужно — меняем размер
        if size:
            image = pygame.transform.scale(image, size)

        # Если задан цвет для прозрачности — делаем его прозрачным
        if transparent_color is not None:
            image = image.convert()  # Нужно для set_colorkey
            image.set_colorkey(transparent_color)
            image = image.convert_alpha()  # Теперь сохраняем прозрачность
        else:
            image = image.convert_alpha()  # Для других изображений просто нормальная загрузка

        return image

    except Exception as e:
        print(f"Ошибка загрузки изображения: {name} | {e}")
        image = pygame.Surface((50, 50) if not size else size)
        image.fill(YELLOW)
        pygame.draw.rect(image, RED, (0, 0, *image.get_size()), 2)
        return image


# Класс игрока
class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = load_image("carw.png", (50, 100), transparent_color=(248, 248, 248))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 100)
        self.speed = CAR_SPEED
        self.last_move = None

    def update(self):
        keys = pygame.key.get_pressed()
        self.last_move = None

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.last_move = "left"
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
            self.last_move = "right"

        # Ограничение движения
        if self.rect.left < 200:
            self.rect.left = 200
        if self.rect.right > 600:
            self.rect.right = 600


# Класс препятствий
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("obstacle.png", (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(200, 550)
        self.rect.y = -100
        self.speed = OBSTACLE_SPEED

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


# Класс дороги
class Road:
    def __init__(self):
        self.y = 0
        self.speed = OBSTACLE_SPEED

    def update(self):
        self.y += self.speed
        if self.y >= 100:
            self.y = 0

    def draw(self):
        screen.fill(ROAD_COLOR)
        for i in range(-1, HEIGHT // 100 + 1):
            pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 5, self.y + i * 100, 10, 50))


# Класс анимации взрыва
class Explosion:
    def __init__(self, pos):
        # Пытаемся загрузить кадры взрыва
        self.frames = []
        for i in range(1, 6):
            try:
                frame = pygame.image.load(f"explosion_{i}.png").convert_alpha()
                frame = pygame.transform.scale(frame, (100, 100))
                self.frames.append(frame)
            except:
                # Если файл не найден, создаем простой кадр
                frame = pygame.Surface((100, 100), pygame.SRCALPHA)
                color = (255, min(69 + i * 30, 255), 0, 200)
                pygame.draw.circle(frame, color, (50, 50), 50 - i * 5)
                self.frames.append(frame)

        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center=pos)
        self.counter = 0
        self.animation_speed = 5

    def update(self):
        self.counter += 1
        if self.counter >= self.animation_speed:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.frames):
                return False
            self.image = self.frames[self.index]
        return True

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Основная функция игры
def main():
    # Загрузка ресурсов
    car = Car()
    obstacles = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(car)
    road = Road()

    # Взрыв
    explosion = None
    explosion_active = False

    # Игровые переменные
    score = 0
    game_over = False
    obstacle_timer = 0
    last_score_increase = 0

    # Звуки
    try:
        crash_sound = pygame.mixer.Sound("crash.wav")
    except:
        crash_sound = None

    running = True
    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if game_over and event.key == pygame.K_r:
                    return main()  # Рестарт
                if not game_over and event.key == pygame.K_SPACE:
                    # Ускорение при нажатии пробела
                    car.speed = CAR_SPEED * 1.5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    car.speed = CAR_SPEED

        if not game_over:
            # Генерация препятствий
            obstacle_timer += 1
            if obstacle_timer >= 60 - min(int(score / 10), 30):  # Увеличиваем сложность
                obstacle = Obstacle()
                obstacles.add(obstacle)
                all_sprites.add(obstacle)
                obstacle_timer = 0

            # Обновление объектов
            road.update()
            all_sprites.update()

            # Увеличение счета
            current_time = pygame.time.get_ticks()
            if current_time - last_score_increase > 100:
                score += SCORE_INCREMENT
                last_score_increase = current_time

            # Проверка столкновений
            if pygame.sprite.spritecollide(car, obstacles, False):
                game_over = True
                explosion = Explosion(car.rect.center)
                explosion_active = True
                if crash_sound:
                    crash_sound.play()

        # Отрисовка
        road.draw()
        all_sprites.draw(screen)

        # Анимация взрыва
        if explosion_active:
            if explosion.update():
                explosion.draw(screen)
            else:
                explosion_active = False

        # Вывод информации
        font = pygame.font.SysFont("Arial", 36)
        score_text = font.render(f"Очки: {int(score)}", True, WHITE)
        screen.blit(score_text, (20, 20))

        if game_over:
            game_over_text = font.render("АВАРИЯ! Нажмите R для рестарта", True, RED)
            screen.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2 - 50))

            best_score = max(score, int(open("score.txt").read()) if os.path.exists("score.txt") else 0)
            with open("score.txt", "w") as f:
                f.write(str(int(best_score)))

            best_score_text = font.render(f"Рекорд: {int(best_score)}", True, WHITE)
            screen.blit(best_score_text, (WIDTH // 2 - 80, HEIGHT // 2 + 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    # Создаем файл для рекордов, если его нет
    if not os.path.exists("score.txt"):
        with open("score.txt", "w") as f:
            f.write("0")
    main()