class Time(object):
    def __init__(self, hour, minute):
        self.hour = hour
        self.minute = minute

    def __str__(self):
        return f'{self.hour:02d}:{self.minute:02d}'
    
    def __eq__(self,other):
        if type(other) is not Time:
            raise TypeError('Can only compare Time objects')
        return self.hour == other.hour and self.minute == other.minute
    def __lt__(self,other):
        if type(other) is not Time:
            raise TypeError('Can only compare Time objects')
        return self.hour < other.hour or self.hour == other.hour and self.minute <= other.minute
    def __le__(self,other):
        if type(other) is not Time:
            raise TypeError('Can only compare Time objects')
        return self == other or self < other

class Task(object):
    def __init__(self, day, time, name, details = ''):
        self.day = day
        self.time = time
        self.name = name
        self.details = details

    def __eq__(self, other):
        if type(other) is not Task:
            raise TypeError('Can only compare Task objects')
        return self.time == other.time and self.name == other.name
    def __lt__(self, other):
        if type(other) is not Task:
            raise TypeError('Can only compare Task objects')
        return self.time < other.time or self.time == other.time and self.name < other.name
    def __le__(self, other):
        if type(other) is not Task:
            raise TypeError('Can only compare Task objects')
        return self < other or self == other

class Day(object):
    def __init__(self, number):
        self.number = number
        self.name = Day.get_name(number)
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)
        self.tasks.sort()

    @classmethod
    def get_name(cls, number):
        return ['Domingo','Segunda','Terça','Quarta','Quinta','Sexta','Sábado'][number]