import sys
from PIL import Image, ImageDraw
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread


class myPIL():

    '''
        Поддерживает типы: BMP, EPS, GIF, IM, JPEG, MSP, PCX,
                           PNG, PPM, TIFF, WebP, ICO, PSD, PDF
    '''


    def __init__(self):
        self.image = None
        self.draw = None


    def open(self, path):
        self.image = Image.open(path).convert('RGB') # Открываем изображение
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


    def colorset(self, color: str, value):
        print('Изменение цвета', color, 'на', value)
        width = self.image.size[0]  # Определяем ширину
        height = self.image.size[1]  # Определяем высоту
        pix = self.image.load()  # Выгружаем значения пикселей
        for x in range(width):
            for y in range(height):
                r = pix[x, y][0]
                g = pix[x, y][1]
                b = pix[x, y][2]
                if color == 'red':
                    self.draw.point((x, y), (r + value, g, b))
                if color == 'green':
                    self.draw.point((x, y), (r, g + value, b))
                if color == 'blue':
                    self.draw.point((x, y), (r, g, b + value))
        print('Завершено')


    def save(self, new_name_picture: str):
        self.image.save(new_name_picture) # сохранить изображение
        print('Изображение сохранено')


class myMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.image_width = None
        self.image_height = None


    def initUI(self):
        self.setGeometry(250, 200, 800, 600)
        self.setWindowTitle('Archimage')

        # self.pixmap = QPixmap('/home/barkas/Изображения/mclaren.jpg')
        self.label_image = QLabel(self)
        # self.label_image.setPixmap(self.pixmap)
        self.image_width = self.label_image.size().width()
        self.image_height = self.label_image.size().height()
        self.label_image.setScaledContents(True)

        self.layout_main = QHBoxLayout(self)
        self.layout_main.addWidget(self.label_image)


        self.mythread = myThread(mainwindow=self)       # Создаю объект нового потока 
        self.mythread.start()                           # Запускю новый поток


class myThread(QThread):

    def __init__(self, mainwindow):
        super().__init__()
        self.mainwindow = mainwindow
        self.picture = None

    
    def run(self):
        self.picture = QPixmap('/home/barkas/Изображения/mclaren.jpg')
        self.mainwindow.label_image.setPixmap(self.picture)
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = myMainWindow()
    win.show()
    sys.exit(app.exec())