class Field:
    def __init__(self, _x, _y, _value):
        self.x
        self.y
        self.value = _value

    def count_Flags(self):
        ...

    def count_Closed_Unknown(self):
        ...
  

class Solution:
    def __init__(self):
        self.field_guesses = []

    def generate_Solution(self, _x, _y, _bomb):
        self.field_guesses.append(Field_guess(_x, _y, _bomb))

class Field_guess:
    def __init__(self, _x, _y, _bomb):
        self.x = _x
        self.y = _y
        self.bomb = _bomb #True or False