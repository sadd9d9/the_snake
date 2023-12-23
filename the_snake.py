import sys
from random import choice, randint

import pygame


SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)

SPEED = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption(
    'Змейка. Выход - Esc. Ускорение - 1. Замедление - 2.'
)

clock = pygame.time.Clock()


class GameObject:
    """Класс, от которого наследуются все объекты игры."""

    def __init__(self, body_color=None, fg_color=None):
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color
        self.fg_color = fg_color

    def draw(self, surface):
        """Абстрактный метод, который реализуется в дочерних классах."""
        pass

    def draw_cell(self, surface, position):
        """Метод отрисовки клетки объекта в игре."""
        rect = pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, self.fg_color, rect, 1)


class Snake(GameObject):
    """Класс объекта змейки."""

    def __init__(self, body_color=(0, 255, 0), fg_color=(93, 216, 228)):
        super().__init__(body_color, fg_color)
        self.reset()
        self.last = None

    def update_direction(self, new_direction=None):
        """Метод обновления направления после нажатия на кнопку."""
        if new_direction:
            self.direction = new_direction

    def move(self):
        """Метод обновления позиции змейки."""
        head = self.get_head_position()
        new_width = (head[0] + GRID_SIZE * self.direction[0]) % SCREEN_WIDTH
        new_height = (head[1] + GRID_SIZE * self.direction[1]) % SCREEN_HEIGHT
        if (new_width, new_height) in self.positions[2:]:
            print(f'Ты проиграл. Длина змейки - {self.length}')
            self.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        else:
            self.positions.insert(0, (new_width, new_height))
            if len(self.positions) > self.length:
                self.last = self.positions.pop()

    def draw(self, surface):
        """Метод отрисовки змейки на экране."""
        # Отрисовка головы змейки
        self.draw_cell(surface, self.positions[0])

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод возвращения позиции головы змейки."""
        return self.positions[0]

    def reset(self):
        """Метод сбрасывания змейки в начальное состояние при столкновении."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice((UP, DOWN, LEFT, RIGHT))


class Apple(GameObject):
    """Класс объекта яблока."""

    def __init__(self, positions=None, body_color=(255, 0, 0),
                 fg_color=(93, 216, 228)):
        super().__init__(body_color, fg_color)
        self.randomize_position(positions)

    def randomize_position(self, positions):
        """Метод выбира места появления яблока."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )
        while positions and self.position in positions:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )

    def draw(self, surface):
        """Метод отрисовки яблока на экране."""
        self.draw_cell(surface, self.position)


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    global SPEED

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit('Завершение игры.')
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit('Завершение игры.')
            elif event.key == pygame.K_1:
                if SPEED < 35:
                    SPEED += 5
                    print(f'Скорость: {SPEED // 5}')
            elif event.key == pygame.K_2:
                if SPEED > 5:
                    SPEED -= 5
                    print(f'Скорость: {SPEED // 5}')
            game_object.update_direction(CONTROL_DICT.get(
                (game_object.direction, event.key),
                game_object.direction
            ))


CONTROL_DICT = {
    (LEFT, pygame.K_UP): UP,
    (RIGHT, pygame.K_UP): UP,
    (LEFT, pygame.K_DOWN): DOWN,
    (RIGHT, pygame.K_DOWN): DOWN,
    (UP, pygame.K_LEFT): LEFT,
    (DOWN, pygame.K_LEFT): LEFT,
    (UP, pygame.K_RIGHT): RIGHT,
    (DOWN, pygame.K_RIGHT): RIGHT
}


def main():
    """Основная функция, которая содержит всю логику игры."""
    pygame.init()

    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        if apple.position == snake.get_head_position():
            snake.length += 1
            apple = Apple(snake.positions)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
