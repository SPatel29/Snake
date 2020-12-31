import random
import pygame
from pygame import mixer
GRID_SIZE = 20
class Food:
    def __init__(self):
        self.location = []
        self.color = (128,0,128)
        self.sound = mixer.Sound("apple_cunrch_sound.wav")

    def generate(self, x):
        x1 = random.randrange(20, 441, 20)
        y1 = random.randrange(20,441, 20)
        while [x1,y1] in x:
            x1 = random.randrange(20, 441, 20)
            y1 = random.randrange(20, 441, 20)
        self.location = [x1,y1]
        return self.location

    def get_location(self):
        return self.location
    def get_sound(self):
        return self.sound
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, [self.location[0], self.location[1], 20, 20])

    def delete(self):
        del self.location

    def food_collision(self, snake, surface):
        if snake.get_head() == self.location:
            self.delete()
            self.generate(snake.get_body())
            snake.add(surface)
            pygame.display.update()
            return True
        return False
