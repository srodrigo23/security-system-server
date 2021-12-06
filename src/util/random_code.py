import random

class RandomCode():
    
    def __init__(self, lim_ini, lim_fin):
        """
        Method to initialize a ramdoom code generator
        """
        self.__set_codes__ = set()
        self.__lim_ini__ = lim_ini
        self.__lim_fin__ = lim_fin
        
    def get_random_num(self):
        """
        Method to generate 
        """
        return random.randint(self.__lim_ini__, self.__lim_fin__)
    
    def get_new_code(self):
        code = self.get_random_num()
        while code in self.__set_codes__:
            code = self.get_random_num()
        self.__set_codes__.add(code)
        return code
    
    def delete_code(self, code):        
        self.__set_codes__.discard(code)
    
    def print_set_codes(self):
        print(self.__set_codes__)
 