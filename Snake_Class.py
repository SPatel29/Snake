import random
import pygame
import time
from Food import Food
from Game import Game
from pygame import mixer

# initialize the pygame
pygame.init()

# create the SCREEN
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # width, height

# game over image
GAME_OVER = pygame.image.load('death_background.png')

MY_DICT = {
    "left": ['left', 'down', 'up'],
    "down": ['down', 'right', 'left'],
    'right': ["right", 'up', 'down'],
    'up': ["up", "left", 'right']
}

# GRID SQUARE
GRID_SIZE = 20
GRID_HEIGHT = SCREEN_WIDTH / GRID_SIZE
GRID_WIDTH = SCREEN_HEIGHT / GRID_SIZE

# Title and Icon
pygame.display.set_caption("Snake")
ICON = pygame.image.load('snake_image.png')
pygame.display.set_icon(ICON)


class Snake:
    def __init__(self, x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 2):
        self.x = int(x)
        self.y = int(y)
        self.body = [[int(x), int(y)]]
        self.snake_color = random.choice([[100, 0, 0], [0, 100, 0], [0, 0, 100]])
        self.length = 1
        self.head_direction = None

    def get_color(self):
        return self.snake_color

    def get_length(self):
        return self.length

    def check_move(self, direction):
        if direction in MY_DICT[self.head_direction]:
            return True
        return False

    def get_head_direction(self):
        return self.head_direction

    def set_head_direction(self, direction):
        if self.get_head_direction() != direction:
            self.head_direction = direction

    def draw(self, surface):
        for i in self.body:
            if i == self.get_head():
                pygame.draw.rect(surface, self.snake_color, [i[0], i[1], GRID_SIZE, GRID_SIZE])
            else:
                if self.get_color() == [100, 0, 0]:
                    pygame.draw.rect(surface, (255, 204, 203), [i[0], i[1], GRID_SIZE, GRID_SIZE])
                elif self.get_color() == [0, 100, 0]:
                    pygame.draw.rect(surface, (144, 238, 144), [i[0], i[1], GRID_SIZE, GRID_SIZE])
                else:
                    pygame.draw.rect(surface, (135, 206, 250), [i[0], i[1], GRID_SIZE, GRID_SIZE])

    def get_body(self):
        return self.body

    def get_head(self):
        return self.body[0]

    def set_body(self, direction):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i][0], self.body[i][1] = self.body[i - 1][0], self.body[i - 1][1]
            if i == 1 and direction == "right":
                self.body[0][0] += GRID_SIZE
            elif i == 1 and direction == "left":
                self.body[0][0] -= GRID_SIZE
            elif i == 1 and direction == "up":
                self.body[0][1] -= GRID_SIZE
            elif i == 1 and direction == "down":
                self.body[0][1] += GRID_SIZE

    def set_body_y_constant(self, y):
        for i in range(len(self.body)):
            self.body[i][1] += y

    def set_body_x_constant(self, x):
        for i in range(len(self.body)):
            self.body[i][0] += x

    def add(self, surface):
        self.body.append([self.body[-1][0] + 0.0005, self.body[-1][1] + 0.0005])
        self.length += 1
        pygame.draw.rect(surface, self.snake_color, [self.body[-1][0], self.body[-1][1], GRID_SIZE, GRID_SIZE])


def grid(surface):
    count = 0
    for i in range(int(GRID_HEIGHT)):
        for j in range(int(GRID_WIDTH)):
            if count % 2 == 0:
                pygame.draw.rect(surface, (93, 216, 228), [i * GRID_SIZE, j * GRID_SIZE, GRID_SIZE, GRID_SIZE])
            else:
                pygame.draw.rect(surface, (84, 194, 205), [i * GRID_SIZE, j * GRID_SIZE, GRID_SIZE, GRID_SIZE])
            count += 1
        count -= 1

    for i in range(surface.get_width()):  # draws the bottom red square
        pygame.draw.rect(surface, (255, 0, 0),
                         (i * -GRID_SIZE + SCREEN_HEIGHT - GRID_SIZE, SCREEN_WIDTH - GRID_SIZE, GRID_SIZE, GRID_SIZE))
    for i in range(surface.get_height()):  # draws the left-hand-side red square
        pygame.draw.rect(surface, (255, 0, 0), (0, i * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    for i in range(surface.get_height(), 0, -1):  # draws the right-hand-side square
        pygame.draw.rect(surface, (255, 0, 0), (SCREEN_HEIGHT - GRID_SIZE, i * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    for i in range(surface.get_width()):  # draws the top red square
        pygame.draw.rect(surface, (255, 0, 0), (i * GRID_SIZE, 0, GRID_SIZE, GRID_SIZE))


def handle_keys(event, snake, food, surface, game):
    if event == "left" or event == pygame.K_LEFT or event == pygame.K_a:
        if snake.length == 1:
            snake.set_head_direction("left")
            snake.set_body_x_constant(-GRID_SIZE)
        elif snake.check_move("left"):
            snake.set_head_direction("left")
            snake.set_body("left")
        else:
            snake.set_body("right")
    elif event == "right" or event == pygame.K_RIGHT or event == pygame.K_d:
        if snake.length == 1:
            snake.set_head_direction("right")
            snake.set_body_x_constant(GRID_SIZE)
        elif snake.check_move("right"):
            snake.set_head_direction("right")
            snake.set_body("right")
        else:
            snake.set_body("left")

    elif event == "up" or event == pygame.K_UP or event == pygame.K_w:
        if snake.length == 1:
            snake.set_head_direction("up")
            snake.set_body_y_constant(-GRID_SIZE)
        elif snake.check_move("up"):
            snake.set_head_direction("up")
            snake.set_body("up")
        else:
            snake.set_body("down")

    elif event == "down" or event == pygame.K_DOWN or event == pygame.K_s:
        if snake.length == 1:
            snake.set_head_direction("down")
            snake.set_body_y_constant(GRID_SIZE)
        elif snake.check_move("down"):
            snake.set_head_direction("down")
            snake.set_body("down")
        else:
            snake.set_body("up")
    if food.food_collision(snake, surface):
        food.get_sound().play()
        game.set_score()


def start_screen(game, screen):
    screen.fill((0, 0, 0))
    game.set_message("Snake Game", (255, 0, 0), screen, SCREEN_WIDTH / 2 - 60, 70)
    game.set_message("INSTRUCTIONS:", (255, 0, 0), screen, 50, 130)
    game.set_message("1) Arrow keys or WASD Keys to move", (255, 0, 0), screen, 50, 170)
    game.set_message("2) Avoid colliding with the red tiles or yourself", (255, 0, 0), screen, 50, 200)
    game.set_message("3) Collide with the purple squares to increase", (255, 0, 0), screen, 50, 230)
    game.set_message("your score and your body.", (255, 0, 0), screen, 73, 255)
    game.set_message("Highscore: " + str(game.get_high_score()), (255, 255, 255), screen, 170, 350)
    game.set_message("Press Spacebar to play the game", (255, 0, 0), screen, 100, 310)

    start = False
    pygame.display.update()
    while not start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start = True
                    return start


def lose(screen, score, game):
    mixer.Sound("death_sound.wav").play()
    pygame.display.update()
    screen.fill((0, 0, 0))
    game.set_message("You died. Press Space to restart or ESC to quit", (255, 0, 0), screen, 45, 100)
    game.set_message(f"Score: {str(score)}", (255, 0, 0), screen, 200, 270)
    pygame.display.update()
    lose_game = True
    while lose_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    lose_game = False
                    main()
                elif event.key == pygame.K_ESCAPE:
                    screen.fill((0, 0, 0))
                    screen.blit(GAME_OVER, (13, 100))
                    pygame.display.update()
                    time.sleep(1.5)
                    return False


def main():
    pygame.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    grid(surface)
    snake = Snake()
    food = Food()
    game = Game()
    lst = []
    game.get_background_sound()
    running = True
    start = start_screen(game, screen)
    while running and start:
        clock.tick(8)
        grid(surface)
        snake.draw(surface)
        screen.blit(surface, (0, 0))
        if not food.location:
            food.generate(snake.get_body())
            pygame.draw.rect(screen, (0, 0, 0), [food.get_location()[0], food.get_location()[1], GRID_SIZE, GRID_SIZE])
            game.set_message("Score " + str(game.get_score()), (255, 255, 255), screen, 400, 460)
            game.set_message("Highscore: " + str(game.get_high_score()), (255, 255, 255), screen, 20, 460)

            pygame.display.update()
        else:
            pygame.draw.rect(screen, (0, 0, 0), [food.get_location()[0], food.get_location()[1], GRID_SIZE, GRID_SIZE])
            game.set_message("Score " + str(game.get_score()), (255, 255, 255), screen, 400, 460)
            game.set_message("Highscore: " + str(game.get_high_score()), (255, 255, 255), screen, 20, 460)

            pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                lst = [event.key]
                handle_keys(lst[0], snake, food, surface, game)
        if food.food_collision(snake, surface):
            game.set_score()
            food.get_sound().play()
            game.set_score()
        if lst:
            handle_keys(lst[0], snake, food, surface, game)

        if snake.get_body()[0][1] >= SCREEN_HEIGHT - GRID_SIZE or snake.get_body()[0][0] >= SCREEN_WIDTH - GRID_SIZE or \
                snake.get_body()[0][1] <= 0 or snake.get_body()[0][0] <= 0:
            game.append_to_file()
            running = lose(screen, game.get_score(), game)

        if snake.length > 1 and snake.get_body()[0] in snake.get_body()[1:]:
            game.append_to_file()
            running = lose(screen, game.get_score(), game)
        game.set_high_score(game.get_score(), game.get_high_score())
        game.set_message("Highscore: " + str(game.get_high_score()), (255, 255, 255), screen, 20, 460)
        pygame.display.update()


main()
