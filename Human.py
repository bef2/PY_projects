class Human:
    def __init__(self, age=0, sex='?'):
        self.age = age
        self.sex = sex
    def speak(self):
        print('Hello i am:', self.age, 'and', self.sex)

Boris = Human()
Boris.age = 32
Boris.sex = 'male'
Boris.speak()