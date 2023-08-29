import pickle
from datetime import datetime


class Day:
    def __init__(self):
        self.level = 0
        self.text = ""
        self.day_week = ""


class Calendar:
    def __init__(self, begin: int, end: int):
        self.begin_year = begin
        self.end_year = end
        self.day_names = [ "Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        self.month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        self.years = {}
        self.notes = []
        self.__years_filling(begin, end)

    
    def date(self, day, month, year):
        if day < 1 or day > len(self.years[str(year)][self.month_names.index(month)]):
            raise ValueError("Uncorrect day number")
        d = self.years[str(year)][self.month_names.index(month)][day - 1]
        return d


    def dist(self, day, month, year):
        if day < 1 or day > len(self.years[str(year)][self.month_names.index(month)]):
            raise ValueError("Uncorrect day number")

        itr_A = 0
        flag = True
        for y in range(self.begin_year, self.end_year):
            for m in range(len(self.years[str(y)])):
                if flag:
                    for d in range(len(self.years[str(y)][m])):
                        if y == year and m == self.month_names.index(month) and d == day - 1:
                            flag = False
                            break
                        itr_A += 1

        dt = datetime.now()

        itr_B = 0
        flag = True
        for y in range(self.begin_year, self.end_year):
            for m in range(len(self.years[str(y)])):
                if flag:
                    for d in range(len(self.years[str(y)][m])):
                        if y == dt.year and m == dt.month - 1 and d == dt.day - 1:
                            flag = False
                            break
                        itr_B += 1
                          
        return itr_A - itr_B


    def write(self):
        with open('D:\Code\Py\Calendar\data.pickle', 'wb') as f:
            pickle.dump(self, f)


    def read(self):
        with open('D:\Code\Py\Calendar\data.pickle', 'rb') as f:
            cl = pickle.load(f)
            self =  cl


    def __years_filling(self, begin: int, end: int):
        for i in range (begin, end):
            self.years[str(i)] = [ [Day() for i in range(31)], [Day() for i in range(28)], [Day() for i in range(31)],
                                     [Day() for i in range(30)], [Day() for i in range(31)], [Day() for i in range(30)],
                                     [Day() for i in range(31)], [Day() for i in range(31)], [Day() for i in range(30)],
                                     [Day() for i in range(31)], [Day() for i in range(30)], [Day() for i in range(31)] ]
            if i % 4 == 0:
                self.years[str(i)][1].append(Day())
        self.__days_week()


    def __days_week(self):
        i = 6   # 1 янв 2023
        for year in self.years.values():
            for month in year:
                for day in month:
                    day.day_week = self.day_names[i]
                    i += 1
                    if i > 6:
                        i = 0



if __name__ == "__main__":
    cl = Calendar(2023, 2031)
    x = cl.dist(1, "Jan", 2023)
    print(x)