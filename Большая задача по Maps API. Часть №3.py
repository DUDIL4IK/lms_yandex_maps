import os
import sys
import pygame
import requests

# на моей клавиатуре нет стрелок, поэтому перемещение происходит по кнопкам wasd

SCREEN_SIZE = [600, 450]
WHITE = (255, 255, 255)
MAP_SIZE = [360, 360]


class MapApp:
    def __init__(self):
        pygame.init()
        print('Введите координаты через пробел:')
        self.cor = input()
        if ',' in self.cor:
            print('Используйте точку, а не запятую!')
        print('Введите масштаб (от 1 до 17):')
        self.mash = int(input())
        self.check()
        self.getImage()
        self.initUI()

    def check(self):
        self.cor = ','.join(self.cor.split())
        if 17 < float(self.mash):
            self.prov = 1
            print('Маштаб должен быть введен в диапазоне от 0 до 17!')
        if self.mash < 0:
            self.mash = 0
        if self.mash > 17:
            self.mash = 17

    def getImage(self):
        map_req = "http://static-maps.yandex.ru/1.x/?ll=" + self.cor + "&z=" + str(self.mash) + "&size=600,450&l=map"
        response = requests.get(map_req)

        if not response:
            print('Координаты введены неверно!')
            print("Ошибка выполнения запроса:")
            sys.exit(1)

        self.map_im = "map.png"
        with open(self.map_im, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('Большая задача по Maps API. Часть №1')
        self.map_image = pygame.image.load(self.map_im)
        self.screen.blit(self.map_image, (0, 0))
        pygame.display.flip()

    def update_map(self):
        map_req = "http://static-maps.yandex.ru/1.x/?ll=" + self.cor + "&z=" + str(self.mash) + "&size=600,450&l=map"
        response = requests.get(map_req)

        if not response:
            print('Ошибка выполнения запроса:', response.status_code)
            return

        with open(self.map_im, "wb") as file:
            file.write(response.content)

        self.map_image = pygame.image.load(self.map_im)
        self.screen.blit(self.map_image, (0, 0))
        pygame.display.flip()

    def move_map(self, dx, dy):
        lon, lat = map(float, self.cor.split(','))
        lon += dx * (360 / (2 ** self.mash))
        lat += dy * (360 / (2 ** self.mash))

        lon = max(-180, min(180, lon))
        lat = max(-90, min(90, lat))

        self.cor = '{},{}'.format(lon, lat)
        self.update_map()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_PAGEUP:
                        self.mash += 1
                        self.check()
                        self.update_map()
                    elif event.key == pygame.K_PAGEDOWN:
                        self.mash -= 1
                        self.check()
                        self.update_map()
                    elif event.key == pygame.K_w:
                        self.move_map(0, -1)
                    elif event.key == pygame.K_s:
                        self.move_map(0, 1)
                    elif event.key == pygame.K_a:
                        self.move_map(-1, 0)
                    elif event.key == pygame.K_d:
                        self.move_map(1, 0)

        pygame.quit()
        os.remove(self.map_im)
        sys.exit()


if __name__ == '__main__':
    app = MapApp()
    app.run()
