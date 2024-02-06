import os
import sys
import pygame
import requests

SCREEN_SIZE = [600, 450]
WHITE = (255, 255, 255)

class MapApp:
    def __init__(self):
        pygame.init()
        print('Введите координаты через пробел:')
        self.cor = input()
        if ',' in self.cor:
            print('Координаты введены неверно')
        print('Введите масштаб в %:')
        print('Чем меньше число, тем больше охват карты')
        self.mash = input()
        self.check()
        self.getImage()
        self.initUI()

    def check(self):
        self.cor = ','.join(self.cor.split())
        if 100 < float(self.mash):
            self.prov = 1
            print('Маштаб должен быть введен в диапазоне от 0 до 100!')
        self.mash = round(0.17 * int(self.mash))
        if self.mash < 0:
            self.mash = 0
        if self.mash > 17:
            self.mash = 17

    def getImage(self):
        map_request = "http://static-maps.yandex.ru/1.x/?ll=" + self.cor + "&z=" + str(self.mash) + "&size=600,450&l=map"
        response = requests.get(map_request)

        if not response:
            print('Координаты введены неверно!')
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('Отображение карты')

        self.map_image = pygame.image.load(self.map_file)
        self.screen.blit(self.map_image, (0, 0))
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()
        os.remove(self.map_file)
        sys.exit()

if __name__ == '__main__':
    app = MapApp()
    app.run()
