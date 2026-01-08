import os

from tinydb import TinyDB, Query
from serializer import serializer
from datetime import datetime


class Device():
    # Class variable that is shared between all instances of the class
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage=serializer).table('devices')

    # Constructor
    def __init__(self, device_name : str, device_id : int, managed_by_user_id : str, end_of_life : datetime):       
        if device_id is None or device_name is None or managed_by_user_id is None or end_of_life is None:
            raise ValueError("Alle Pflichtattribute müssen ausgefüllt sein!")    

        self.device_name = device_name
        self.device_id = device_id
        self.end_of_life = end_of_life
        # The user id of the user that manages the device
        # We don't store the user object itself, but only the id (as a key)
        self.managed_by_user_id = managed_by_user_id
        self.is_active = True

        self.__creation_date = datetime.now()
        self.__last_update = datetime.now()
        
    # String representation of the class
    def __str__(self):
        return f'Device (Object) {self.device_name} ({self.managed_by_user_id})'

    # String representation of the class
    def __repr__(self):
        return self.__str__()
    
    def store_data(self):
        print("Storing data...")
        # Check if the device already exists in the database
        DeviceQuery = Query()
        result = self.db_connector.search(DeviceQuery.device_name == self.device_name)
        if result:
            # Update the existing record with the current instance's data
            result = self.db_connector.update(self.__dict__, doc_ids=[result[0].doc_id])
            print("Data updated.")
        else:
            # If the device doesn't exist, insert a new record
            self.db_connector.insert(self.__dict__)
            print("Data inserted.")
    
    def delete(self):
        print("Deleting data...")
        # Check if the device exists in the database
        DeviceQuery = Query()
        result = self.db_connector.search(DeviceQuery.device_name == self.device_name)
        if result:
            # Delete the record from the database
            self.db_connector.remove(doc_ids=[result[0].doc_id])
            print("Data deleted.")
        else:
            print("Data not found.")

    def set_managed_by_user_id(self, managed_by_user_id: str):
        """Expects `managed_by_user_id` to be a valid user id that exists in the database."""
        self.managed_by_user_id = managed_by_user_id

    # Class method that can be called without an instance of the class to construct an instance of the class
    @classmethod
    def find_by_attribute(cls, by_attribute: str, attribute_value: str, num_to_return=1):
        # Load data from the database and create an instance of the Device class
        DeviceQuery = Query()
        result = cls.db_connector.search(DeviceQuery[by_attribute] == attribute_value)

        if result:
            data = result[:num_to_return]
            device_results = [cls(d['device_name'], d['device_id'], d['managed_by_user_id'], d['end_of_life']) for d in data]
            return device_results if num_to_return > 1 else device_results[0]
        else:
            return None

    @classmethod
    def find_all(cls) -> list:
        # Load all data from the database and create instances of the Device class
        devices = []
        for device_data in Device.db_connector.all():
            devices.append(Device(device_data['device_name'], device_data['device_id'], device_data['managed_by_user_id'], device_data['end_of_life']))
        return devices



    

if __name__ == "__main__":
    # Create a device
    device1 = Device("Device1",1, "one@mci.edu",datetime(2026,2,20))
    device2 = Device("Device2",2, "two@mci.edu",datetime(2026,6,20)) 
    device3 = Device("Device3",3, "two@mci.edu",datetime(2027,2,20)) 
    device4 = Device("Device4",4, "two@mci.edu",datetime(2027,6,20)) 
    device1.store_data()
    device2.store_data()
    device3.store_data()
    device4.store_data()
    device5 = Device("Device3",5, "four@mci.edu", datetime(2026,6,20)) 
    device5.store_data()

    #loaded_device = Device.find_by_attribute("device_name", "Device2")
    loaded_device = Device.find_by_attribute("managed_by_user_id", "two@mci.edu")
    if loaded_device:
        print(f"Loaded Device: {loaded_device}")
    else:
        print("Device not found.")

    devices = Device.find_all()
    print("All devices:")
    for device in devices:
        print(device)

    