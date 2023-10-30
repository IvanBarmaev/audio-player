import pygame

pygame.font.init()
class Button:
    def __init__(self, surf, x, y, text, size, command=None, description=None, width=None, height=None):
        self.font = pygame.font.SysFont("Lucida Console", size)
        self.description = description
        self.command = command
        self.surf = surf
        self.x = x
        self.y = y
        self.text = text
        self.txt = self.font.render(text, True, (10, 20, 30))
        self.rect = self.txt.get_rect(topleft=(x, y))
        self.rect.width += 10
        if width:
            self.rect.width = width
            self.width = width
        if height:
            self.rect.height = height
        else:
            self.rect.height += self.rect.height // 2

    def render(self, shift_y=0):
        pygame.draw.rect(self.surf, (200, 200, 200), (self.rect.x, self.rect.y + shift_y, self.rect.right-self.rect.left, self.rect.height))
        self.surf.blit(self.txt, (self.rect.x + self.rect.width // 2 - self.txt.get_rect().width // 2, self.rect.y + shift_y + self.rect.height // 12))

    def change_text(self, text):
        self.text = text
        self.txt = self.font.render(text, True, (10, 20, 30))
        self.rect = self.txt.get_rect(topleft=(self.x, self.y))
        self.rect.width = self.width
        self.rect.height += self.rect.height // 2

    def in_rect(self, x, y, shift_y=0):
         if x in range(self.rect.left, self.rect.right) and y in range(self.rect.y + shift_y, self.rect.y + self.rect.height + shift_y):
             return True
         return False

    def draw_rect(self, shift_y=0):
        pygame.draw.rect(self.surf, (255, 0, 0), (self.rect.x, self.rect.y + shift_y, self.rect.width, self.rect.height), 2)

    @classmethod  #Метод класса для получения высоты кнопки
    def get_height(cls, size):
        new_font = pygame.font.SysFont("Lucida Console", size)
        return int(new_font.render("hi", True, (0, 0, 0)).get_rect().height * 1.5)
        

class ProgressBar:
    def __init__(self, surf, x, y, width, height, value, max_value, command=None, description=None):
        self.text = "ProgressBar"
        if command:
            self.command = command
        self.description = description
        self.surf = surf
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.value = value
        self.max_value = max_value
        self.rect = pygame.Rect(x, y, width, height)

    def render(self, shift_y=0):
        pygame.draw.rect(self.surf, (255, 255, 255), (self.x, self.y + shift_y, self.width, self.height))
        pygame.draw.rect(self.surf, (155, 155, 155), (self.x, self.y + shift_y, int(self.width * self.value / self.max_value), self.height))

    def in_rect(self, x, y, shift_y=0):
        if x in range(self.x, self.x + self.width) and y in range(self.y + shift_y, self.y + self.height + shift_y):
            return True
        return False

    def change_value(self, x):
        if x in range(self.x, self.x + self.width):
            self.value = (x - self.x) / self.width * self.max_value

    def draw_rect(self, shift_y=0):
        pygame.draw.rect(self.surf, (255, 0, 0), (self.rect.x, self.rect.y + shift_y, self.rect.width, self.rect.height), 2)

class ListBox(Button):
    """
    Класс для 
    """
    all_box = []
    active_box = None
    def __init__(self, surf, x, y, text:list, size, description=None, height=None):
        self.font = pygame.font.SysFont("Lucida Console", size)
        self.surf = surf
        self.x = x
        self.y = y
        self.text = text
        self.all_txt, self.all_y = [], []
        self.txt = self.font.render(text[0], True, (10, 50, 20))
        self.rect = self.txt.get_rect(topleft=(x, y))
        if height:
            self.rect.height = height
        else:
            self.rect.height += self.rect.height // 2
        self.iter_y = 0
        for i in text:
            self.all_txt.append((self.font.render(i, True, (10, 50, 20))))
            self.all_y.append(self.rect.y + self.rect.height * self.iter_y)
            if self.all_txt[len(self.all_txt) - 1].get_rect().width > self.rect.width:
                self.rect.width = self.all_txt[len(self.all_txt) - 1].get_rect().width
            self.iter_y += 1
        self.txt = self.all_txt[0]
        self.rect.width += 10
        self.activated = False
        self.description = description
        ListBox.all_box.append(self)

    def render(self):
        if self.activated:
            self.iter_y = 0
            for i in self.all_txt:
                pygame.draw.rect(self.surf, (200, 200, 200), (self.x, self.all_y[self.all_txt.index(i)], self.rect.width, self.rect.height))
                self.surf.blit(self.all_txt[self.all_txt.index(i)], (self.rect.x + 5, self.all_y[self.all_txt.index(i)] + self.rect.height // 12))
                self.iter_y += 1
        else:
            pygame.draw.rect(self.surf, (200, 200, 200), (self.x, self.y, self.rect.width, self.rect.height))
            self.surf.blit(self.txt, (self.rect.x + 5, self.rect.y + self.rect.height // 12))

    def in_rect(self, x, y):
        if self.activated:
            self.iter_y = 0
            for i in self.text:
                if x in range(self.x, self.x + self.rect.width) and y in range(self.y + self.rect.height * self.iter_y, self.y + self.rect.height * (self.iter_y + 1)):
                    return self.text[self.iter_y]
                self.iter_y += 1
        else:
            if x in range(self.x, self.x + self.rect.width) and y in range(self.y, self.y + self.rect.height):
                return True
            return False

    def draw_rect(self, shift_y=0):
        pygame.draw.rect(self.surf, (255, 0, 0), (self.rect.x, self.rect.y + shift_y, self.rect.width, self.rect.height), 2)


class YesNoSurface:
    active_surf = None
    def change_text(self, text):
        self.text = text
        self.words = text.split(" ")
        self.lines, self.line = [], ""
        for i in self.words:
            if self.font.render(self.line + i, True, (10, 20, 30)).get_rect().width < self.width - 20:
                self.line += i + " "
                continue
            self.lines.append(self.font.render(self.line, True, (200, 200, 200)))
            self.line = i + " "
        if len(self.lines) >= 1:
            self.lines.append(self.font.render(i, True, (200, 200, 200)))
        else:
            self.lines.append(self.font.render(self.line, True, (200, 200, 200)))
        self.iter_y = 0
        self.surf.fill((10, 10, 10))
        for i in self.lines:
            self.surf.blit(i, (10, i.get_rect().height * self.iter_y + 5))
            self.iter_y += 1
            
    def __init__(self, sc, x, y, width, height, text, size):
        self.sc = sc
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.font = pygame.font.SysFont("Lucida Console", size)
        self.surf = pygame.Surface((width, height))
        self.change_text(text)
        self.yes_button = Button(self.surf, self.width // 20, self.height - Button.get_height(size) - 10, "Да", size)
        self.no_button = Button(self.surf, self.width - self.yes_button.rect.width * 1.7, self.height - Button.get_height(size) - 10, "Нет", size)

    def render(self):
        self.sc.blit(self.surf, (self.x, self.y, shift_y))
        self.yes_button.render()
        self.no_button.render()

    def in_rect(self, x, y, shift_y=0):
        if x in range(self.x, self.x + self.width) and y in range(self.y, self.y + self.height + shift_y):
            if self.yes_button.in_rect(x - self.x, y - self.y, shift_y):
                return 2
            elif self.no_button.in_rect(x - self.x, y - self.y, shift_y):
                return 1

    def draw_rect(self, shift_y=0):
        pygame.draw.rect(self.surf, (255, 0, 0), (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 2)
        

class ScrollBar:
    def set_slider_height(self):
        self.slider_height = 1.0 if self.value <= self.rect.height else self.rect.height / self.value
        if self.slider_height < 0.01:
            self.slider_height = 0.01
        self.slider_value_max = 1.0 - self.slider_height
        self.slider = pygame.Surface((self.rect.width, self.rect.height * self.slider_height))
        self.slider.fill((215, 215, 215))

    def add_slider_y(self, value):
        self.slider_value += value

    def set_value(self, value):
        self.value = value
        self.set_slider_height()

    def check_slider_value(self):
        if self.slider_value > self.slider_value_max:
            self.slider_value = self.slider_value_max
        elif self.slider_value < 0.0:
            self.slider_value = 0.0

    def set_slider_y(self, value):
        self.slider_value = value
        self.check_slider_value()

    def __init__(self, surf, x, y, width, height, value, slider_value, command=None):
        self.surf = surf
        self.sc = pygame.Surface((width, height))
        self.rect = self.sc.get_rect(topleft=(x, y))
        self.value = value
        self.slider_value = slider_value  #Значение на котором назодится slider от 0.0 до self.slider_value_max
        self.slider_value_max = 0  #Максимальное значение slider от 0.0 до 1.0
        self.slider_height = 0.0
        self.slider = None
        self.set_slider_height()
        self.command = self.set_value
        if command:
            self.command = command

    def render(self, shift_y=0):
        self.sc.fill((145, 180, 70))
        self.sc.blit(self.slider, (0, int(self.slider_value * self.rect.height)))
        self.surf.blit(self.sc, self.rect.topleft)

    def in_rect(self, x, y, shift_y=0):
        if x in range(self.rect.x, self.rect.x + self.rect.width) and y in range(self.rect.y, self.rect.y + self.rect.height):
            return True
        return False

    def draw_rect(self, shift_y=0):
        pygame.draw.rect(self.surf, (255, 0, 0), (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 2)
