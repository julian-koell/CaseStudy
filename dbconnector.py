import os
from serializer import serializer
from tinydb import TinyDB

class DatabaseConnector:

    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json')
        return cls.__instance
    
    #def __init__(self):
    #    self.table = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage=serializer)

    def print(self):
        """
        Prints the id(...) of the objects instance
        """
        print(f"This DatabaseConnector's id is {self.__instance}")

    def get_table(self, table_name: str):
        return TinyDB(self.__instance.__path).table(table_name)

if __name__ is "__main__":
    db1 = DatabaseConnector()
    db2 = DatabaseConnector()
    db3 = DatabaseConnector()

    db1.print()
    db2.print()
    db3.print()

    print("\n")

    print(db1.get_table('devices'))
    print(db2.get_table('devices'))
    print(db3.get_table('devices'))