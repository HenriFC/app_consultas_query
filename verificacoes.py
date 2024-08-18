
import os

class validar_entry():

    def validar_entry_nome(self, text):
        if len(text) <= 27:
            return True
        return False


    def validar_entry_horario(self, text):
        if text == '': 
            return True
        
        try:
            if len(text) > 5:
                return False
            
            if len(text) == 1 and int(text[0]) >= 3:
                return False
            
            if len(text) == 2 and int(text[0:2]) >= 24:
                return False
            
            if len(text) == 3 and text[2] != ':':
                return False
        
            if len(text) == 4 and int(text[3]) >= 6:
                return False
            
            if len(text) == 5 and int(text[4]) >= 10:
                return False
                 
        except ValueError:
            return False
        return True

            





