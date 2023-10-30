import pygame
from button import ScrollBar


class Frame:
    def __init__(self, window, width, height, coord, elements, color=(0, 0, 0)):
        self.window = window
        self.width, self.height = width, height
        self.surf = pygame.Surface((width, height))
        self.width, self.height = width, height
        self.coord = coord
        self.elements = []
        self.render_elements = []
        self.elements_height = 0
        for i in elements:
            self.elements.append(i)
        self.color = color
        self.scrollbar = None
        self.min_y, self.max_y = 0, 0
        self.shift_y = 0
        self.active_mode = self.active_element
        self.special_element = None

    def add_element(self, element):
        self.elements.append(element)
        self.elements[-1].surf = self.surf
        if element.rect.bottom > self.elements_height:
            self.elements_height = element.rect.bottom

    def render(self):
        self.surf.fill(self.color)
        for i in self.render_elements:
            i.render(self.shift_y)
        self.window.surf.blit(self.surf, self.coord)

    def active_element(self, mouse_pos):
        for i in self.render_elements:
            if i.in_rect(mouse_pos[0] - self.coord[0], mouse_pos[1] - self.coord[1], self.shift_y):
                return i
            if self.scrollbar and self.scrollbar.in_rect(*mouse_pos):
                return self.scrollbar
        else:
            return None

    def special_active_element(self, mouse_pos):  #Для элементов типа EnterSurf
        return self.special_element

    def reset(self):
        self.elements = []
        self.render_elements = []
        self.elements_height = 0
        self.shift_y = 0
        self.scrollbar = None

    def add_scrollbar(self, command=None):
        if self.elements_height > self.height:
            self.scrollbar = ScrollBar(self.surf, int(self.width * 0.95), int(self.height * 0.05), 40, int(self.height * 0.72),
                                       self.elements_height, 0, command=command)
            self.elements.append(self.scrollbar)

    def find_render_elements(self):
        self.render_elements = []
        for i in self.elements:
            if i.rect.bottom > -self.shift_y and i.rect.top < -self.shift_y + self.height and not i is self.scrollbar:
                self.render_elements.append(i)
                if i.rect.bottom > -self.shift_y + self.height:
                    break
        if self.scrollbar:
            self.render_elements.append(self.scrollbar)

    def update_render_elements(self, y):  #y - в какую сторону будет смещение
        if y < 0:
            self.start_index = self.elements.index(self.render_elements[0])
            for i in self.elements[self.start_index - 1: 0: -1]:
                if i.rect.bottom >= -self.shift_y:
                    if not i in self.render_elements:
                        self.render_elements.insert(0, i)
                        #print("inserted", len(self.render_elements), self.render_elements[-2].text)
                    if self.render_elements[-2].rect.top > -self.shift_y + self.height:
                        self.render_elements.remove(self.render_elements[-2])
            if -self.shift_y < 80:
                self.render_elements.insert(0, self.elements[0])
        else:
            self.start_index = self.elements.index(self.render_elements[-2])
            for i in self.elements[self.start_index: len(self.elements) - 1]:
                if i.rect.bottom > -self.shift_y and i.rect.top < -self.shift_y + self.height:
                    if i not in self.render_elements:
                        self.render_elements.insert(-1, i)
                    if self.render_elements[0].rect.bottom < -self.shift_y:
                        self.render_elements.remove(self.render_elements[0])




class Window:
    def __init__(self, sc, width, height, coord, elements, color=(77, 77, 77)):
        self.sc = sc
        self.width = width
        self.height = height
        self.coord = coord
        self.surf = pygame.Surface((width, height))
        self.elements = elements
        for i in self.elements:
            i.surf = self.surf
        self.color = color

    def add_element(self, element):
        self.elements.append(element)

    def render(self):
        self.surf.fill(self.color)
        for i in self.elements:
            self.surf.blit(i.surf, i.coord)
        self.sc.blit(self.surf, self.coord)

    def active_frame(self, mouse_pos):
        for i in self.elements:
            if mouse_pos[0] in range(i.coord[0], i.coord[0] + i.width) and mouse_pos[1] in range(i.coord[1], i.coord[1] + i.height):
                return i
        else:
            return None
