from PIL import Image, ImageDraw

'''
Поддерживает типы: BMP, EPS, GIF, IM, JPEG, MSP, PCX PNG, PPM,
                   TIFF, WebP, ICO, PSD, PDF
'''

class Convert():

    def __init__(self, name_picture: str):
        self.image = Image.open(name_picture).convert('RGB') # Открываем изображение
        self.draw = ImageDraw.Draw(self.image) # Создаем инструмент для рисования


    def show(self):
        self.image.show()


    def grey_convert(self):
        print('Преобразование в серый')
        width = self.image.size[0]  # Определяем ширину
        height = self.image.size[1]  # Определяем высоту
        pix = self.image.load()  # Выгружаем значения пикселей
        for x in range(width):
            for y in range(height):
                r = pix[x, y][0] #узнаём значение красного цвета пикселя
                g = pix[x, y][1] #зелёного
                b = pix[x, y][2] #синего
                sr = (r + g + b) // 3 #среднее значение
                self.draw.point((x, y), (sr, sr, sr)) #рисуем пиксель
        print('Завершено')


    def inversion(self):
        print('Преобразование в инверсию')
        width = self.image.size[0]  # Определяем ширину
        height = self.image.size[1]  # Определяем высоту
        pix = self.image.load()  # Выгружаем значения пикселей
        for x in range(width):
            for y in range(height):
                r = pix[x, y][0]
                g = pix[x, y][1]
                b = pix[x, y][2]
                self.draw.point((x, y), (255 - r, 255 - g, 255 - b))
        print('Завершено')


    def brightness(self, value):
        print('Изменение яркости на', value)
        width = self.image.size[0]  # Определяем ширину
        height = self.image.size[1]  # Определяем высоту
        pix = self.image.load()  # Выгружаем значения пикселей
        for x in range(width):
            for y in range(height):
                r = pix[x, y][0]
                g = pix[x, y][1]
                b = pix[x, y][2]
                self.draw.point((x, y), (r + value, g + value, b + value))
        print('Завершено')
                

    def rotate(self, value):
        self.image = self.image.rotate(value, expand=True)


    def reflect_x(self):
            self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)


    def reflect_y(self):
            self.image = self.image.transpose(Image.FLIP_TOP_BOTTOM)


    def save(self, new_name_picture: str):
        self.image.save(new_name_picture) # сохранить изображение
        print('Новое изображение сохранено')


if __name__ == "__main__":
    im = Convert('/home/barkas/Изображения/mclaren.jpg')
    # im.grey_convert()
    # im.inversion()
    # im.brightness(-30)
    # im.rotate(90)
    # im.reflect_x()
    # im.save('/h.ome/barkas/Изображения/mclaren_0.pdf')
    im.show()