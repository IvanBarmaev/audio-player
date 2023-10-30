import pygame
from button import Button

pygame.font.init()
text_font = pygame.font.SysFont("Lucida Console", 24)

class Enter(pygame.sprite.Sprite):
    buttons = {pygame.K_q:"q", pygame.K_w:"w", pygame.K_e:"e", pygame.K_r:"r", pygame.K_t:"t", pygame.K_y:"y", pygame.K_u:"u", pygame.K_i:"i", pygame.K_o:"o", pygame.K_p:"p",\
               pygame.K_a:"a", pygame.K_s:"s", pygame.K_d:"d", pygame.K_f:"f", pygame.K_g:"g", pygame.K_h:"h", pygame.K_j:"j", pygame.K_k:"k", pygame.K_l:"l", pygame.K_z:"z",\
               pygame.K_x:"x", pygame.K_c:"c", pygame.K_v:"v", pygame.K_b:"b", pygame.K_n:"n", pygame.K_m:"m", pygame.K_1:"1", pygame.K_2:"2", pygame.K_3:"3", pygame.K_4:"4",\
               pygame.K_5:"5", pygame.K_6:"6", pygame.K_7:"7", pygame.K_8:"8", pygame.K_9:"9", pygame.K_0:"0", pygame.K_SPACE:" "}
    def __init__(self, surf, width, height, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.surf = surf
        self.delay = 0

    def render(self, shift_y=0):
        pygame.draw.rect(self.surf, (10, 20, 30), (self.rect.x, self.rect.y, self.rect.width, 50))
        self.txt = text_font.render(self.text, True, (210, 200, 220))
        self.text_rect = self.txt.get_rect()
        self.surf.blit(self.txt, (self.rect.x + 7, self.rect.height * 2))

    def add_letter(self, fps):
        key = pygame.key.get_pressed()
        if any(key):
            if self.delay == 0 or self.delay >= fps // 2:
                for i in Enter.buttons:
                    if key[i]:
                        if not self.delay % 10:
                            self.text += Enter.buttons[i]
                if key[pygame.K_BACKSPACE]:
                    self.text = list(self.text)
                    if len(self.text) > 0 and not self.delay % 10:
                        self.text.pop(len(self.text) - 1)
                    self.text = "".join(self.text)
                self.delay += 1
            elif self.delay in range(1, int(fps) // 2):
                self.delay += 1
        else:
            self.delay = 0

class EnterSurf(pygame.sprite.Sprite):
    def change_text(self, text):
        self.text = text
        self.words = text.split(" ")
        self.lines, self.line = [], ""
        for i in self.words:
            if self.font.render(self.line + i, True, (10, 20, 30)).get_rect().width < self.surf.get_rect().width - 20:
                self.line += i + " "
                continue
            self.lines.append(self.font.render(self.line, True, (200, 200, 200)))
            self.line = i + " "
        if len(self.lines) >= 1:
            self.lines.append(self.font.render(i, True, (200, 200, 200)))
        else:
            self.lines.append(self.font.render(self.line, True, (200, 200, 200)))
        self.iter_y = 4
        self.surf.fill((10, 10, 10))
        for i in self.lines:
            self.surf.blit(i, (10, i.get_rect().height * self.iter_y))
            self.iter_y += 1
            
    def __init__(self, sc, x, y, width, height, size, description, desc_size, command=None):
        pygame.sprite.Sprite.__init__(self)
        self.sc = sc
        self.surf = pygame.Surface((width, height))
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.description = description
        self.font = pygame.font.SysFont("Lucida Console", desc_size)
        self.delay = 0
        self.rect = self.surf.get_rect(topleft=(x, y))
        self.enter = Enter(self.surf, int(width - width * 0.04), int(width * 0.02), int(width * 0.02), int(height * 0.01))
        self.yes_button = Button(self.surf, int(width * 0.02), height - Button.get_height(35) - int(height * 0.03), "Подтвердить", 35)
        self.no_button = Button(self.surf, 0, height - Button.get_height(35) - int(height * 0.03), "Отмена", 35)
        self.no_button.rect.x = width - self.no_button.rect.width - int(width * 0.01)
        self.change_text(description)
        self.command = command

    def render(self, shift_y=0):
        self.sc.blit(self.surf, (self.x, self.y))
        self.enter.render()
        self.yes_button.render()
        self.no_button.render()

    def in_rect(self, x, y, shift_y=0):
        if x in range(self.x, self.x + self.width) and y in range(self.y, self.y + self.height):
            if self.yes_button.in_rect(x - self.x, y - self.y):
                return 2
            elif self.no_button.in_rect(x - self.x, y - self.y):
                return 1
            return 0

    def draw_rect(self, shift_y=0):
        pygame.draw.rect(self.sc, (255, 0, 0), (self.rect.x, self.rect.y, self.rect.width, self.rect.height - 1), 2)
        
