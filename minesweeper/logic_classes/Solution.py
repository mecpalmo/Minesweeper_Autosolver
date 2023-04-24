from Field_Guess import Field_Guess

class Solution:

    def __init__(self):
        self.field_guesses = []

    def __init__(self, id_table, content_table):
        self.field_guesses = []
        try:
            for (id, content)  in (id_table, content_table):
                self.field_guesses.append(Field_Guess(id, content))
        except:
            if(len(id_table)!=len(content_table)):
                print("Creating Solution ERROR: array sizes don't match")