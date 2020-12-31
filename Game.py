import pygame
from pygame import mixer


class Game:
    def __init__(self, file="Background_music.wav"):
        mixer.init()
        self.score = 0
        self.background_sound = pygame.mixer.music.load(file)
        self.high_score = 0

    def set_message(self, msg, color, surface, x_coord=150, y_coord=220):
        font = pygame.font.Font('freesansbold.ttf', 18)
        screen_txt = font.render(msg, True, color)
        surface.blit(screen_txt, [x_coord, y_coord])

    def get_score(self):
        return self.score

    def set_score(self):
        self.score += 1
        return self.score

    def get_background_sound(self):
        return mixer.music.play(-1)

    def append_to_file(self, file="Snake_Scores"):
        f = open(file, 'a')
        f.write(str(self.get_score()) + '\n')

    def get_high_score(self, file="Snake_High_Scores.txt"):
        try:
            with open(file) as f:
                self.high_score = f.read()
                if not self.high_score:
                    self.high_score = 0
        except FileNotFoundError:
            self.high_score = 0
        return self.high_score

    def set_high_score(self, current_score, old_high_score, file="Snake_High_Scores.txt"):
        if int(current_score) > int(old_high_score):
            self.high_score = current_score
            f = open(file, 'w')
            try:
                f.write(str(self.high_score))
            except FileNotFoundError:
                f = open(file, 'w')
                f.write(str(self.high_score))
