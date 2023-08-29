from PyQt5.QtWidgets import QWidget, QPushButton, QFrame, QApplication, \
                            QHBoxLayout, QVBoxLayout, QGridLayout, \
                            QRadioButton, QTextEdit, QLabel, QSplashScreen
                            
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize
import sys
import Calendar


# Цвета интерфейса
DARK_GREY = (80, 80, 80)
GREY = (180, 180, 180)
ROSY_BROWN = (188, 143, 143)
DODGER_BLUE = (30, 100, 200)    # селектор

LAWN_GREEN = (124, 232, 0)      # Поставки
ORANGE = (255, 115, 50)         # Этапы
AQUA = (60, 155, 255)           # Авансы
BURLY_WOOD = (222, 184, 135)    # Прочее
RED = (255, 30, 30)             # Последний день



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # self.splash_screen()
        self.years = {}

        # Загрузка календаря из файла (требуется предварительное создание и сохранение календаря в памяти)
        # cl = Calendar.Calendar(2023, 2031)
        # cl.write()
        with open('D:\Code\Py\Calendar\data.pickle', 'rb') as f:
            self.cl = Calendar.pickle.load(f)

        self.day_names = self.cl.day_names
        self.month_names = self.cl.month_names
        self.work_year = None
        self.work_month = None
        self.work_day = None
        self.btn_light = ["", "", 0, ""]
        self.setup_ui()
    

    def splash_screen(self):
        self.splash = QSplashScreen()
        self.image = QPixmap('D:\Code\Py\Calendar\image2.png')
        self.splash.setPixmap(self.image)
        self.splash.show()


    def create_month(self, year_name: str, month_name: str, qty_days):
        size_btn = 27
        month = {}
        month["frame"] = QFrame()
        month["lay"] = QGridLayout(month["frame"])
        month["lay"].setSpacing(4)
        month["buttons"] = []
        month["labels"] = []

        # Определяем номер дня недели
        first_day_name = self.cl.years[year_name][self.month_names.index(month_name)][0].day_week
        number_day_week = self.day_names.index(first_day_name)

        # Создаем лэйбл месяца
        mon_list = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
                    "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
        label = QLabel(mon_list[self.month_names.index(month_name)])
        label.setFont(QFont("Arial", 11))
        label.setStyleSheet(f"color: rgb{ROSY_BROWN};")
        label.setAlignment(Qt.AlignCenter|Qt.AlignBottom)
        month["lay"].addWidget(label, 0, 0, 1, 0)

        # Создаем названия дней недели
        positions = [(1, j) for j in range(7)]
        for pos, day in zip(positions, self.day_names):
            label = QLabel(day)
            label.setStyleSheet(f"color: rgb{DARK_GREY};")
            label.setAlignment(Qt.AlignCenter|Qt.AlignBottom)
            label.setFont(QFont("Arial", 8))
            if pos[1] > 4:
                label.setStyleSheet(f"color: rgb{ROSY_BROWN};")
            label.setAlignment(Qt.AlignCenter|Qt.AlignBottom)
            month["lay"].addWidget(label, *pos)
            month["labels"].append(label)

        # Создаем числа месяца в виде кнопок
        positions = [(i, j) for i in range(2, 8) for j in range(7)]
        for pos, num in zip(positions, list(range(42))):
            if pos[0] == 2 and pos[1] <= number_day_week - 1:
                continue
            if num > qty_days + number_day_week - 1:
                frame = QFrame()
                frame.setMinimumSize(size_btn, size_btn)
                frame.setMaximumSize(size_btn, size_btn)
                month["lay"].addWidget(frame, *pos)
            else:
                button = QPushButton()
                button.setStyleSheet('color: rgb(50, 60, 185);')
                button.setText(str(num - number_day_week + 1))
                button.setMinimumSize(size_btn, size_btn)
                button.setMaximumSize(size_btn, size_btn)
                button.clicked.connect(lambda state, d=(num - number_day_week + 1), m=month_name, y=int(year_name): self.push_calendar_day(d, m, y))
                month["buttons"].append(button)
                month["lay"].addWidget(button, *pos)

        return month


    def create_year(self, year_name: str): 
        qty_days = [len(m) for m in self.cl.years[year_name]]
        self.years[year_name] = {}
        self.years[year_name + "_frame"] = QFrame()
        self.years[year_name + "_lay"] = QGridLayout(self.years[year_name + "_frame"])

        for month, qty in zip(self.month_names, qty_days):
            self.years[year_name][month] = self.create_month(year_name, month, qty)

        # Создаем год
        positions = [(i,j) for i in range(4) for j in range(4)]
        for mon, pos in zip(self.month_names, positions):
            self.years[year_name + "_lay"].addWidget(self.years[year_name][mon]["frame"], *pos)


    def setup_ui(self):
        # Настройки окна
        self.setWindowTitle(f"Календарь")
        self.move(150,50)
        self.setWindowIcon(QIcon('D:\Code\Py\Calendar\hearth.png'))

        # Левая сторона -----------------------------------------------------

        # Создаем лэйбл года
        self.number = str(Calendar.datetime.now().year)
        self.head_label = QLabel(self.number)
        self.head_label.setMaximumWidth(100)
        self.head_label.setFont(QFont("Arial", 18))
        self.head_label.setStyleSheet(f"color: rgb{ROSY_BROWN};")
        self.head_label.setAlignment(Qt.AlignCenter)

        # Создаем кнопки перехода к следующим годам
        button_next = QPushButton()
        button_next.setIcon(QIcon('D:\Code\Py\Calendar\\row_right2.png'))
        button_next.setIconSize(QSize(25, 25))
        button_next.setStyleSheet('color: rgb(50, 60, 185);')
        button_next.setMaximumSize(30, 30)
        button_next.clicked.connect(lambda: self.next_year(int(self.number)))

        button_prev = QPushButton()
        button_prev.setIcon(QIcon('D:\Code\Py\Calendar\\row_left2.png'))
        button_prev.setIconSize(QSize(25, 25))
        button_prev.setStyleSheet('color: rgb(50, 60, 185);')
        button_prev.setMaximumSize(30, 30)
        button_prev.clicked.connect(lambda: self.prev_year(int(self.number)))

        # Рамка шапки календаря
        calendar_head_frame = QFrame()
        calendar_head_lay = QHBoxLayout(calendar_head_frame)
        calendar_head_lay.setContentsMargins(420, 0, 420, 0)
        calendar_head_lay.addWidget(button_prev)
        calendar_head_lay.addWidget(self.head_label)
        calendar_head_lay.addWidget(button_next)

        # Создаем годы с рамками и макетами
        for y in range(self.cl.begin_year, self.cl.end_year):
            self.create_year(str(y))

        # Рамка календаря
        calendar_frame = QFrame()
        calendar_lay = QVBoxLayout(calendar_frame)
        calendar_lay.setContentsMargins(0, 0, 0, 0)
        calendar_lay.addWidget(calendar_head_frame)
        for num in range(self.cl.begin_year, self.cl.end_year):
            calendar_lay.addWidget(self.years[str(num) + "_frame"])
            self.years[str(num) + "_frame"].hide()



        # Правая сторона ----------------------------------------------------

        # Выбор сложности задачи
        self.radio_buttons = [ QRadioButton("Поставки", styleSheet=f'background-color: rgb{LAWN_GREEN};'),
                               QRadioButton("Этапы", styleSheet=f'background-color: rgb{ORANGE};'),
                               QRadioButton("Авансы", styleSheet=f'background-color: rgb{AQUA};'),
                               QRadioButton("Прочее", styleSheet=f'background-color: rgb{BURLY_WOOD};') ]

        # self.radio_buttons[3].setChecked(True)

        save_but = QPushButton("Сохранить")
        save_but.clicked.connect(self.push_save)

        # Рамка шапки заметок
        note_head_frame = QFrame()
        note_head_lay = QHBoxLayout(note_head_frame)
        note_head_lay.setContentsMargins(0, 0, 0, 0)
        for rb in self.radio_buttons:
            note_head_lay.addWidget(rb)
        note_head_lay.addWidget(save_but)

        # Текстовое поле
        self.text_edit = QTextEdit()
        self.text_edit.setFont(QFont("Arial", 10))

        # Рамка заметок
        self.note_frame = QFrame()
        self.note_frame.hide()
        note_lay = QVBoxLayout(self.note_frame)
        note_lay.setContentsMargins(0, 0, 0, 0)
        note_lay.addWidget(note_head_frame)
        note_lay.addWidget(self.text_edit)


        # Корень ---------------------------------------------------------

        # Макет корневого окна
        main_lay = QHBoxLayout(self)
        main_lay.setContentsMargins(0, 10, 0, 0)
        main_lay.addWidget(calendar_frame)
        main_lay.addWidget(self.note_frame)

        # Подсветка текущего дня и дней с заметками
        dt = Calendar.datetime.now()
        y = str(dt.year)
        m = self.month_names[dt.month - 1]
        d = dt.day

        for n in self.cl.notes:
            if self.cl.dist(n[0], n[1], n[2]) < 0:
                # self.years[str(n[2])][n[1]]["buttons"][n[0] - 1].setStyleSheet(f'background-color: rgb{GREY};')
                if self.cl.date(n[0], n[1], n[2]).level == 0:
                    self.years[str(n[2])][n[1]]["buttons"][n[0] - 1].setStyleSheet(f'background-color: rgb{GREY}; border: 1px solid rgb{LAWN_GREEN};')
                elif self.cl.date(n[0], n[1], n[2]).level == 1:
                    self.years[str(n[2])][n[1]]["buttons"][n[0] - 1].setStyleSheet(f'background-color: rgb{GREY}; border: 1px solid rgb{ORANGE};')
                elif self.cl.date(n[0], n[1], n[2]).level == 2:
                    self.years[str(n[2])][n[1]]["buttons"][n[0] - 1].setStyleSheet(f'background-color: rgb{GREY}; border: 1px solid rgb{AQUA};')
                elif self.cl.date(n[0], n[1], n[2]).level == 3:
                    self.years[str(n[2])][n[1]]["buttons"][n[0] - 1].setStyleSheet(f'background-color: rgb{GREY}; border: 1px solid rgb{BURLY_WOOD};')
            else:
                if self.cl.date(n[0], n[1], n[2]).level == 0:
                    self.years[str(n[2])][n[1]]["buttons"][n[0] - 1].setStyleSheet(f'background-color: rgb{LAWN_GREEN};')
                elif self.cl.date(n[0], n[1], n[2]).level == 1:
                    self.years[str(n[2])][n[1]]["buttons"][n[0] - 1].setStyleSheet(f'background-color: rgb{ORANGE};')
                elif self.cl.date(n[0], n[1], n[2]).level == 2:
                    self.years[str(n[2])][n[1]]["buttons"][n[0] - 1].setStyleSheet(f'background-color: rgb{AQUA};')
                elif self.cl.date(n[0], n[1], n[2]).level == 3:
                    self.years[str(n[2])][n[1]]["buttons"][n[0] - 1].setStyleSheet(f'background-color: rgb{BURLY_WOOD};')

        if [d, m, int(y)] in self.cl.notes:
            style = self.years[y][m]["buttons"][d - 1].styleSheet()
            self.years[y][m]["buttons"][d - 1].setStyleSheet(style + f'border: 5px solid rgb{ROSY_BROWN};')
        else:
            self.years[y][m]["buttons"][d - 1].setStyleSheet(f'border: 5px solid rgb{ROSY_BROWN};')

        # Показ текущего года
        self.years[str(y) + "_frame"].show()


    def next_year(self, number):
        if number < self.cl.end_year - 1:
            self.years[str(number) + "_frame"].hide()
            self.years[str(number + 1) + "_frame"].show()
            self.number = str(int(self.number) + 1)
            self.head_label.setText(self.number)


    def prev_year(self, number):
        if number > self.cl.begin_year:
            self.years[str(number) + "_frame"].hide()
            self.years[str(number - 1) + "_frame"].show()
            self.number = str(int(self.number) - 1)
            self.head_label.setText(self.number)


    def push_calendar_day(self, d, m, y):
        # Снимает выделение с предыдущей кнопки
        if self.btn_light != ["", "", 0, ""]:
            self.years[self.btn_light[0]][self.btn_light[1]]["buttons"][self.btn_light[2]].setStyleSheet(self.btn_light[3])

        # Сосраняем аргументы функции
        self.work_year = y
        self.work_month = m
        self.work_day = d
        
        # Подсветка нажатой кнопки
        button = self.years[str(y)][m]["buttons"][d - 1]
        self.btn_light = [str(y), m, d - 1, button.styleSheet()]
        button.setStyleSheet(button.styleSheet() + f'border: 3px solid rgb{DODGER_BLUE};')
        self.note_frame.show()

        # Загрузка текста и категории из календаря
        text = self.cl.date(d, m, y).text
        self.text_edit.setPlainText(text)
        self.radio_buttons[self.cl.date(d, m, y).level].setChecked(True)


    def push_save(self):
        # Записываем текст и категорию в календарь
        day = self.cl.date(self.work_day, self.work_month, self.work_year)
        day.text = self.text_edit.toPlainText()
        day.level = self.radio_checked()

        # Определение текущей даты
        dt = Calendar.datetime.now()
        # Переменные получают значения после нажатия кнопки даты
        d = [self.work_day, self.work_month, self.work_year]

        # Есть текст и прошедший день
        if day.text != '' and self.cl.dist(self.work_day, self.work_month, self.work_year) < 0:
            self.years[str(self.work_year)][self.work_month]["buttons"][self.work_day - 1].setStyleSheet(f'background-color: rgb{GREY}; border: 3px solid rgb{DODGER_BLUE};')
            if self.radio_checked() == 0:
                self.btn_light[3] = f'background-color: rgb{GREY}; border: 1px solid rgb{LAWN_GREEN};'
            elif self.radio_checked() == 1:
                self.btn_light[3] = f'background-color: rgb{GREY}; border: 1px solid rgb{ORANGE};'
            elif self.radio_checked() == 2:
                self.btn_light[3] = f'background-color: rgb{GREY}; border: 1px solid rgb{AQUA};'
            elif self.radio_checked() == 3:
                self.btn_light[3] = f'background-color: rgb{GREY}; border: 1px solid rgb{BURLY_WOOD};'
            # Новая дата
            if not d in self.cl.notes:
                self.cl.notes.append(d)
        # Есть текст
        elif day.text != '':
            if self.radio_checked() == 0:
                self.years[str(self.work_year)][self.work_month]["buttons"][self.work_day - 1].setStyleSheet(f'background-color: rgb{LAWN_GREEN}; border: 3px solid rgb{DODGER_BLUE};')
                self.btn_light[3] = f'background-color: rgb{LAWN_GREEN};'
            elif self.radio_checked() == 1:
                self.years[str(self.work_year)][self.work_month]["buttons"][self.work_day - 1].setStyleSheet(f'background-color: rgb{ORANGE}; border: 3px solid rgb{DODGER_BLUE};')
                self.btn_light[3] = f'background-color: rgb{ORANGE};'
            elif self.radio_checked() == 2:
                self.years[str(self.work_year)][self.work_month]["buttons"][self.work_day - 1].setStyleSheet(f'background-color: rgb{AQUA}; border: 3px solid rgb{DODGER_BLUE};')
                self.btn_light[3] = f'background-color: rgb{AQUA};'
            elif self.radio_checked() == 3:
                self.years[str(self.work_year)][self.work_month]["buttons"][self.work_day - 1].setStyleSheet(f'background-color: rgb{BURLY_WOOD}; border: 3px solid rgb{DODGER_BLUE};')
                self.btn_light[3] = f'background-color: rgb{BURLY_WOOD};'

            # Текущий день
            if (self.work_day, self.work_month, self.work_year) == (dt.day, self.month_names[dt.month - 1], dt.year):
                self.btn_light[3] += f"border: 5px solid rgb{ROSY_BROWN};"
            
            # Новая дата
            if not d in self.cl.notes:
                self.cl.notes.append(d)

        # Нет текста
        elif day.text == '':
            # Дата есть в списке заметок
            if d in self.cl.notes:
                self.cl.notes.remove(d)
            # Возвращение исходного цвета
            # Сегодняшний день
            if (self.work_day, self.work_month, self.work_year) == (dt.day, self.month_names[dt.month - 1], dt.year):
                self.btn_light[3] = f'border: 5px solid rgb{ROSY_BROWN};'
                self.years[str(self.work_year)][self.work_month]["buttons"][self.work_day - 1].setStyleSheet(f'border: 3px solid rgb{DODGER_BLUE};')  
            # Любой день кроме сегодняшнего
            else:
                self.btn_light[3] = ''
                self.years[str(self.work_year)][self.work_month]["buttons"][self.work_day - 1].setStyleSheet(f'border: 3px solid rgb{DODGER_BLUE};')

        # Запись на жесткий диск
        self.cl.write()


    def radio_checked(self):
        for i in range(len(self.radio_buttons)):
            if self.radio_buttons[i].isChecked():
                return i



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    # win.splash.finish(win)
    win.show()
    sys.exit(app.exec())