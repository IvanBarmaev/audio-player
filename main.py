import pygame
from button import *
from window import Window, Frame
from os import sep, getcwd, listdir
from sys import exit
from enter import *
from psutil import disk_partitions  #Чтобы найти диски


sc = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
FPS = 60
WIDTH, HEIGHT = 1280, 720
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()


class Player:
    def update(self):
        self.playlist_frame.reset()
        y = 0
        for i in listdir(getcwd() + sep + "playlists"):
            self.playlist_frame.add_element(Button(None, int(WIDTH * 0.01), int(HEIGHT // 20 + HEIGHT * 0.07 * y),
                i.split(".")[0], WIDTH // 50, command=self.open_playlist, width=int(WIDTH * 0.92),))
            y += 1
        self.playlist_frame.find_render_elements()

    def open_playlist(self, act_by_b=False):  #Да, это костыль)
        if self.element:
            self.music_frame.scrollbar = None
            with open(self.path + self.element.text + ".txt") as f:
                self.music_frame.reset()
                self.viewed_playlist = f.read().split("\n")
                self.playlist_name = self.element.text
                y = 0
                if self.viewed_playlist[0] == "":
                    self.viewed_playlist.pop(0)
                for i in self.viewed_playlist:
                    self.music_frame.add_element(Button(None, int(WIDTH * 0.01), int(HEIGHT // 20 + HEIGHT * 0.07 * y),
                        i.split("\\")[-1], WIDTH // 50, command=self.play, width=int(WIDTH * 0.92)))
                    y += 1
                self.surf.elements[1] = self.music_frame
            self.main_frame.elements[-1] = self.add_music
            self.main_frame.render_elements[-1] = self.add_music
            self.music_frame.add_scrollbar(self.scroll_click)
            self.music_frame.find_render_elements()

    def play(self, path=None, act_by_b=False):  #act_by_b - аргумент для перезаписи self.playlist
        if self.music:
            self.music.stop()
        if act_by_b:
            self.playlist = self.viewed_playlist
            self.index = self.music_frame.elements.index(self.element)
        self.music = pygame.mixer.Sound(path) if path else pygame.mixer.Sound(self.playlist[self.music_frame.elements.index(self.element)])
        self.music.set_volume(self.volume_bar.value)
        self.music.play()
        self.pause = False
        self.main_frame.elements[0].change_text("  ||  ")
        self.time_bar.max_value = self.music.get_length()
        self.time_bar.value = 0

    def play_button(self, act_by_b=False):  #Да, это костыль)
        if self.music:
            if self.pause:
                pygame.mixer.unpause()
                self.main_frame.elements[0].change_text("  ||  ")
            else:
                pygame.mixer.pause()
                self.main_frame.elements[0].change_text("  >  ")
            self.pause = not self.pause

    def next_track(self, act_by_b=False):  #Да, это костыль)
        if self.playlist:
            self.index = self.index + 1 if len(self.playlist) - 1 > self.index else 0
            self.play(self.playlist[self.index])

    def prev_track(self, act_by_b=False):  #Да, это костыль)
        if self.playlist:
            self.index -= 1
            if self.index < 0:
                self.index = len(self.playlist) - 1
            self.play(self.playlist[self.index])

    def change_volume(self, act_by_b=False):  #Да, это костыль)
        self.volume_bar.change_value(self.coord[0])
        if self.music:
            self.music.set_volume(self.volume_bar.value)

    def change_repeat(self, act_by_b=False):  #Да, это костыль)
        self.repeat = not self.repeat
        if self.repeat:
            self.main_frame.elements[3].change_text("R")
        else:
            self.main_frame.elements[3].change_text("A")

    def change_time(self, act_by_b=False):  #Да, это костыль)
        None

    def new_playlist(self, act_by_b=False):
        self.surf.elements[1].render_elements.append(self.add_playlist_surf)
        self.add_playlist_surf.sc = self.surf.elements[1].surf
        self.task.append(self.add_playlist_surf.enter.add_letter)
        self.playlist_frame.special_element = self.add_playlist_surf
        self.playlist_frame.active_mode = self.playlist_frame.special_active_element

    def new_playlist_file(self, act_by_b=False):
        if self.add_playlist_surf.in_rect(*self.coord) == 2:
            with open(self.path + self.add_playlist_surf.enter.text + ".txt", "w") as f:
                self.task.remove(self.add_playlist_surf.enter.add_letter)
                self.surf.elements[1].render_elements.remove(self.add_playlist_surf)
                self.update()
        else:
            self.surf.elements[1].render_elements.remove(self.add_playlist_surf)
            self.task.remove(self.add_playlist_surf.enter.add_letter)
        self.add_playlist_surf.enter.text = ""
        self.playlist_frame.active_mode = self.playlist_frame.active_element

    def open_folder(self, act_by_b=False):
        self.path_frame.reset()
        if self.element.text == "Добавить музыку":
            y = 0
            for i in disk_partitions():
                self.path_frame.add_element(Button(None, int(WIDTH * 0.01), int(HEIGHT // 20 + HEIGHT * 0.07 * y),
                    i[0][0]+":", WIDTH // 50, command=self.open_folder, width=int(WIDTH * 0.92)))
                y += 1
        else:
            self.folder_path += self.element.text + sep
            y = 0
            for i in listdir(self.folder_path):
                self.file_type = i.split(".")
                if len(self.file_type) == 1:
                    self.path_frame.add_element(Button(None, int(WIDTH * 0.01), int(HEIGHT // 20 + HEIGHT * 0.07 * y),
                        i, WIDTH // 50, command=self.open_folder, width=int(WIDTH * 0.92)))
                    y += 1
                elif self.file_type[1] == "wav" or self.file_type[1] == "mp3":
                    self.path_frame.add_element(Button(None, int(WIDTH * 0.01), int(HEIGHT // 20 + HEIGHT * 0.07 * y),
                        i, WIDTH // 50, command=self.add_music_to_playlist, width=int(WIDTH * 0.92)))
                    y += 1
        self.path_frame.add_scrollbar(self.scroll_click)
        self.path_frame.find_render_elements()

    def add_music_to_playlist(self, act_by_b=False):
        with open(self.path + self.playlist_name + ".txt", "a") as f:
            if f.read == "":
                f.write(self.folder_path + self.element.text)
            else:
                f.write("\n" + self.folder_path + self.element.text)
            self.folder_path = ""
            self.path_frame.reset()
            self.surf.elements[1] = self.playlist_frame
    def new_music(self, act_by_b=False):
        self.surf.elements[1] = self.path_frame
        self.folder_path = ""
        self.open_folder(act_by_b=True)

    def scroll(self, act_by_b=False, y=0):
        if self.frame.scrollbar and self.add_playlist_surf.enter.add_letter not in self.task:
            self.frame.scrollbar.add_slider_y(y / self.frame.scrollbar.value * 20)
            self.frame.scrollbar.check_slider_value()
            self.frame.shift_y = -int(self.frame.scrollbar.slider_value * self.frame.scrollbar.value)
            self.frame.update_render_elements(y)

    def scroll_click(self, act_by_b=False):
        self.frame.scrollbar.set_slider_y((self.coord[1] - self.frame.scrollbar.rect.y - (self.frame.scrollbar.slider_height * self.frame.scrollbar.rect.height) / 2) /
                                          self.frame.scrollbar.rect.height)
        self.frame.shift_y = -int(self.frame.scrollbar.slider_value * self.frame.elements_height)
        self.frame.find_render_elements()

    def music_state(self, *args):
        if self.music and not pygame.mixer.get_busy():
            if self.repeat:
                self.music.play()
            else:
                self.next_track()

    def time_bar_update(self, *args):
        if self.music and not self.pause:
            self.time_bar.value += 1 / FPS

    def __init__(self):
        self.surf = Window(sc, WIDTH, HEIGHT, (0, 0), [])
        self.main_frame = Frame(self.surf, WIDTH, HEIGHT // 6, (0, HEIGHT - HEIGHT // 6), [], color=(10, 10, 10))
        self.playlist_frame = Frame(self.surf, WIDTH, HEIGHT - HEIGHT // 6, (0, 0), [])
        self.music_frame = Frame(self.surf, WIDTH, HEIGHT - HEIGHT // 6, (0, 0), [])
        self.path_frame = Frame(self.surf, WIDTH, HEIGHT - HEIGHT // 6, (0, 0), [])
        self.add_playlist_surf = EnterSurf(None, WIDTH // 2 - WIDTH // 6, HEIGHT // 2 - HEIGHT // 6, WIDTH // 3,
                                           HEIGHT // 3, WIDTH // 50, "Введите название", WIDTH // 60, command=self.new_playlist_file)
        self.main_frame.add_element(Button(None, int(WIDTH * 0.465), int(HEIGHT // 6 * 0.15), "||", WIDTH // 40,
                                           command=self.play_button, width=int(WIDTH * 0.07)))  #пауза и воспроизведение
        self.main_frame.add_element(Button(None, int(WIDTH * 0.55), int(HEIGHT // 6 * 0.15), ">>", WIDTH // 40,
                                           command=self.next_track, width=int(WIDTH * 0.07)))  # следующий трек
        self.main_frame.add_element(Button(None, int(WIDTH * 0.38), int(HEIGHT // 6 * 0.15), "<<", WIDTH // 40,
                                           command=self.prev_track, width=int(WIDTH * 0.07)))  #предыдущий трек
        self.main_frame.add_element(Button(None, int(WIDTH * 0.638), int(HEIGHT // 6 * 0.15), "A", WIDTH // 40,
                                           command=self.change_repeat, width=int(WIDTH * 0.07)))  #все треки или один
        self.volume_bar = ProgressBar(None, int(WIDTH * 0.725), int(HEIGHT // 6 * 0.3), int(WIDTH * 0.25), HEIGHT // 30, 0.1, 1,
                                      command=self.change_volume)
        self.main_frame.add_element(self.volume_bar)
        self.time_bar = ProgressBar(None, int(WIDTH * 0.38), int(HEIGHT // 8 * 0.9), int(WIDTH * 0.24),
                                                HEIGHT // 30, 0, 1, command=self.change_volume)  #Время
        self.main_frame.add_element(self.time_bar)
        self.add_playlist = Button(None, int(WIDTH * 0.03), int(HEIGHT * 0.03), "Создать плейлист", WIDTH // 40,
                                   command=self.new_playlist)
        self.add_music = Button(None, int(WIDTH * 0.03), int(HEIGHT * 0.03), "Добавить музыку", WIDTH // 40,
                                   command=self.new_music)
        self.add_music.surf = self.main_frame.surf
        self.main_frame.add_element(self.add_playlist)  #В main_frame последний элемент - add_music или add_playlist
        self.surf.add_element(self.main_frame)
        self.music_frame.surf.fill((10, 10, 10))
        self.playlist_frame.surf.fill((10, 10, 10))
        self.update()
        self.surf.add_element(self.playlist_frame)
        self.coord = (0, 0)  #Координаты курсора
        self.frame = None  #frame на который наведен курсор
        self.element = None  #Элемент на который наведен курсор
        self.playlist = []
        self.viewed_playlist = []
        self.playlist_name = ""
        self.index = 0
        self.music = None
        self.play_time = 0
        self.pause = False
        self.repeat = False
        self.path = getcwd() + sep + "playlists" + sep
        self.folder_path = ""  #Путь для path_frame
        self.task = [self.music_state, self.time_bar_update]
        self.playlist_frame.add_scrollbar(self.scroll_click)
        self.main_frame.find_render_elements()
        self.playlist_frame.find_render_elements()

    def main(self):
        while True:
            self.coord = pygame.mouse.get_pos()
            self.frame = self.surf.active_frame(self.coord)
            if self.frame:
                self.element = self.frame.active_mode(self.coord)
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    exit()
                elif i.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_key = pygame.mouse.get_pressed()
                    if self.mouse_key[0] and self.element:
                        self.element.command(act_by_b=True)
                    elif self.mouse_key[2]:
                        self.surf.elements[1] = self.playlist_frame
                        self.main_frame.elements[-1] = self.add_playlist
                        self.main_frame.render_elements[-1] = self.add_playlist
                        self.folder_path = ""
                        #self.main_frame.elements[self.main_frame.elements.index(self.add_music)] = self.add_playlist
                elif i.type == pygame.MOUSEWHEEL:
                    self.scroll(y=-i.y)
            for i in self.task:
                i(FPS)
            self.main_frame.render()
            self.surf.elements[1].render()
            if self.element:
                self.element.draw_rect(self.frame.shift_y)
            self.surf.render()
            pygame.display.flip()
            clock.tick(FPS)


player = Player()
player.main()

