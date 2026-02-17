"""
Простая солнечная система на Pygame
-----------------------------------
Программа показывает анимацию вращения планет вокруг солнца.
Можно использовать как демонстрацию навыков Python и Pygame.
"""

import pygame
import math
import random

# Настройки игры
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 900
FPS = 60  # Частота обновления экрана

# Цвета для разных объектов
SUN_COLOR = (237, 176, 12)           # Желтое солнце
MERCURY_COLOR = (79, 79, 79)         # Серый меркурий
VENUS_COLOR = (228, 150, 150)        # Розоватая венера
EARTH_COLOR = (150, 166, 228)        # Голубая земля
MARS_COLOR = (192, 12, 17)           # Красный марс
JUPITER_COLOR = (146, 61, 22)        # Коричневый юпитер
SATURN_COLOR = (123, 77, 55)         # Коричневатый сатурн
SATELLITE_COLOR = (176, 176, 176)    # Серые спутники
ASTEROID_COLORS = [(194, 107, 20), (250, 220, 0), (158, 87, 21)]  # Разные оттенки для астероидов

# Запускаем pygame
pygame.init()
pygame.display.set_caption("Моя Солнечная система")
clock = pygame.time.Clock()

class Planet:
    """Базовый класс для всех планет.

    Отвечает за движение по кругу и отрисовку планеты.
    У каждой планеты есть своя скорость и расстояние от солнца.
    """

    def __init__(self, screen, color, size, radius, speed, sun, distance, angle=45):
        self.screen = screen           # Экран для рисования
        self.color = color              # Цвет планеты
        self.center = (size[0]//2, size[1]//2)  # Центр экрана (там солнце)
        self.radius = radius            # Размер планеты
        self.speed = speed              # Скорость вращения
        self.sun = sun                  # Солнце (нужно для расстояния)
        self.distance = distance        # Расстояние от солнца
        if sun:  # Если солнце передано
            self.distance = distance + sun.radius  # Добавляем радиус солнца
        self.angle = angle               # Текущий угол поворота

    def get_coords(self):
        """Вычисляет текущие координаты планеты на экране."""
        x = int(self.center[0] + self.distance * math.cos(math.radians(self.angle)))
        y = int(self.center[1] + self.distance * math.sin(math.radians(self.angle)))
        return x, y

    def draw(self):
        """Рисует планету и её орбиту."""
        # Рисуем планету
        pygame.draw.circle(self.screen, self.color, (self.get_coords()), self.radius)
        # Рисуем орбиту
        if self.sun:  # Рисуем орбиту только если есть солнце
            pygame.draw.circle(self.screen, (100, 100, 100, 50), self.center, self.distance, 1)

    def update(self):
        """Обновляет положение планеты (поворачивает на один шаг)."""
        self.angle += self.speed
        if self.angle >= 360:
            self.angle -= 360

class Sun(Planet):
    """Солнце - особый вид планеты, которое стоит в центре."""

    def __init__(self, screen, color, size, radius):
        # Для солнца не нужно солнце (передаем None)
        super().__init__(screen, color, size, radius, 0, None, 0)
        self.center = (size[0] // 2, size[1] // 2)  # Центр экрана

    def draw(self):
        """Рисует солнце в центре экрана."""
        pygame.draw.circle(self.screen, self.color, self.center, self.radius)

class Star:
    """Звезда на заднем фоне."""

    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.color = (243, 236, 221)  # Бежевый цвет
        # Случайное положение на экране
        self.center = (random.randint(0, screen_width), random.randint(0, screen_height))
        self.radius = 2

    def draw(self):
        """Рисует звезду."""
        pygame.draw.circle(self.screen, self.color, self.center, self.radius)

class Satellite(Planet):
    """Спутник - вращается вокруг планеты, а не вокруг солнца."""

    def __init__(self, screen, color, size, radius, speed, host_planet, distance, angle=0):
        self.host_planet = host_planet  # Планета, вокруг которой летаем
        self.orbit_distance = distance   # Расстояние от планеты
        # Для спутника солнце не нужно (передаем None)
        super().__init__(screen, color, size, radius, speed, None, distance, angle)

    def get_coords(self):
        """Вычисляет координаты спутника (относительно своей планеты)."""
        host_x, host_y = self.host_planet.get_coords()
        x = host_x + self.orbit_distance * math.cos(math.radians(self.angle))
        y = host_y + self.orbit_distance * math.sin(math.radians(self.angle))
        return int(x), int(y)

    def draw(self):
        """Рисует спутник и его орбиту вокруг планеты."""
        pygame.draw.circle(self.screen, self.color, (self.get_coords()), self.radius)
        # Рисуем орбиту спутника вокруг планеты
        pygame.draw.circle(self.screen, (100, 100, 100, 50),
                          self.host_planet.get_coords(), self.orbit_distance, 1)

class Asteroid(Planet):
    """Астероид - маленькая случайная планетка в поясе астероидов."""

    def __init__(self, screen, color, size, sun):
        # Случайные параметры для каждого астероида
        radius = random.randint(1, 5)              # Размер
        speed = random.uniform(0.1, 0.3)           # Скорость
        distance = random.randint(270, 320)         # Расстояние от солнца
        angle = random.randint(0, 360)               # Начальный угол

        super().__init__(screen, color, size, radius, speed, sun, distance, angle)

    def draw(self):
        """Рисует астероид (без орбиты, чтобы не загромождать)."""
        pygame.draw.circle(self.screen, self.color, (self.get_coords()), self.radius)

class SolarSystem:
    """Главный класс, который собирает всё вместе и управляет анимацией."""

    def __init__(self):
        """Создаёт экран и все объекты солнечной системы."""
        self.size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen = pygame.display.set_mode(self.size)

        # Создаём солнце (оно нужно для планет)
        self.sun = Sun(self.screen, SUN_COLOR, self.size, 30)

        # Создаём звёзды на заднем фоне
        self.stars = [Star(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT)
                     for _ in range(random.randint(40, 70))]

        # Создаём планеты
        self.mercury = Planet(self.screen, MERCURY_COLOR, self.size, 10, 0.8, self.sun, 40)
        self.venus = Planet(self.screen, VENUS_COLOR, self.size, 20, 0.6, self.sun, 100)
        self.earth = Planet(self.screen, EARTH_COLOR, self.size, 17, 0.4, self.sun, 180)
        self.mars = Planet(self.screen, MARS_COLOR, self.size, 10, 0.3, self.sun, 240)
        self.jupiter = Planet(self.screen, JUPITER_COLOR, self.size, 45, 0.2, self.sun, 350)
        self.saturn = Planet(self.screen, SATURN_COLOR, self.size, 25, 0.15, self.sun, 480)

        # Список всех планет (для удобства)
        self.planets = [self.mercury, self.venus, self.earth,
                       self.mars, self.jupiter, self.saturn]

        # Создаём спутники для некоторых планет
        self.satellites = [
            Satellite(self.screen, SATELLITE_COLOR, self.size, 5, 2, self.earth, 30),
            Satellite(self.screen, SATELLITE_COLOR, self.size, 12, 1, self.jupiter, 70),
            Satellite(self.screen, SATELLITE_COLOR, self.size, 8, 1.5, self.jupiter, 95),
            Satellite(self.screen, SATELLITE_COLOR, self.size, 3, 2, self.saturn, 50),
            Satellite(self.screen, SATELLITE_COLOR, self.size, 2, 3, self.saturn, 40)
        ]

        # Создаём пояс астероидов (100-200 штук)
        self.asteroids = [
            Asteroid(self.screen, random.choice(ASTEROID_COLORS), self.size, self.sun)
            for _ in range(random.randint(100, 200))
        ]

        # Собираем все объекты в один список для удобной отрисовки
        self.all_objects = self.planets + self.asteroids + self.satellites

    def update(self):
        """Обновляет положение всех объектов."""
        for obj in self.all_objects:
            obj.update()

    def draw(self):
        """Рисует всё на экране."""
        # Очищаем экран (заливаем чёрным)
        self.screen.fill((0, 0, 0))

        # Рисуем звёзды
        for star in self.stars:
            star.draw()

        # Рисуем солнце
        self.sun.draw()

        # Рисуем все объекты
        for obj in self.all_objects:
            obj.draw()

    def run(self):
        """Запускает главный цикл игры."""
        while True:
            # Проверяем, не закрыл ли пользователь окно
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            # Обновляем и рисуем всё
            self.update()
            self.draw()

            # Показываем результат на экране
            pygame.display.update()
            clock.tick(FPS)

# Запускаем программу
if __name__ == "__main__":
    solar_system = SolarSystem()
    solar_system.run()
