

class Student:

    def __init__(self, first_name, last_name, group, number):
        self.first_name = first_name
        self.last_name = last_name
        self.group = group
        self.number = number

    @property
    def full_name (self):
        return '{} {}'.format(self.first, self.last)