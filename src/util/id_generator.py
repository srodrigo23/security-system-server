
class IDGenerator():
    
    def __init__(self):
        """
        Method to initialize a consecituve num code generator
        """    
        self.__i__ = 0
        
    def get_generate_id(self):
        """
        Method to generate an conseucive number.
        """
        self.__i__ = self.__i__ + 1
        return self.__i__