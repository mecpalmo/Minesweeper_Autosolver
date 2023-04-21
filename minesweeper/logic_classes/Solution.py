from Field_Guess import Field_Guess

class Solution:

    def __init__(self):
        self.field_guesses = []

    def generateSolution(self, _x, _y, _bomb):
        self.field_guesses.append(Field_Guess(_x, _y, _bomb))