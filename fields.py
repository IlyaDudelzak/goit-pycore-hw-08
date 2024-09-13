from collections import UserDict
from datetime import datetime
from bithday import get_upcoming_birthdays, string_to_date

class Field:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return str(self.value)
    
    def edit(self, value:str):
         self.__init__(value)

class Name(Field):
    def __init__(self, value:str):
          super().__init__(value.lower())

class Phone(Field):
    def __init__(self, value: str):
        if(len(value) != 10 or not value.isnumeric()):
            raise ValueError("Wrong phone format!")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, date):
         self.value = date
         
    def get_date(self):
         return string_to_date(self.value)

class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def find_phone(self, phone):
         for i in self.phones:
              if(str(i) == phone):
                   return Phone(phone)

         return None

    def has_phone(self, phone):
         for i in self.phones:
              if(i.value == phone):
                   return True
         return False
    
    def phones_amount(self):
         return len(self.phones)

    def add_phone(self, phone: Phone):
         if(self.has_phone(phone)):
              raise ValueError("Phone already registried")
         self.phones.append(Phone(phone))
     
    def add_birthday(self, birthday:datetime):
         self.birthday = Birthday(birthday)

    def has_birthday(self):
         return self.birthday != None

    def remove_phone(self, phone: str):
         self.phones.remove(Phone(phone))

    def edit_phone(self, phone1, phone2):
         Phone(phone1)
         Phone(phone2)
         for i, phone in enumerate(self.phones):
              if(phone.value == phone1):
                   self.phones[i].edit(phone2)
     
    def get_phones(self):
         return '; '.join(p.value for p in self.phones)

    def __str__(self):
         res = f"Contact name: {self.name.value}"
         if(len(self.phones) > 0):
              res += f", Phones: {self.get_phones()}"
         if(self.birthday != None):
              res += f", Birthday: {self.birthday}"
         return res

class AddressBook(UserDict):
    def has_record(self, name:str):
         return name.lower() in self.data
    
    def add_record(self, record: Record):
         if(not record.name.value in self.data):
            self.data[record.name.value] = record
         else:
            raise ValueError("Record already registried")
     
    def find(self, name:str) -> Record:
         return self.get(name)
    
    def get_all(self):
         res = ""
         for i in self.data:
              if(res != ""):
                    res += "\n"
              res += str(self.data[i])
         return res
    
    def get_birthdays(self, days = 7):
         users = []
         for i in self.data:
              rec = self.data[i]
              if(rec.birthday != None):
                   users.append({"name": i, "birthday": rec.birthday.value})
         return get_upcoming_birthdays(users, days)

    def delete(self, name:str):
         name = name.lower()
         if(name in self.data):
              del self.data[name]    
         else:
              raise ValueError(f"Record({name}) not registried")

    def __str__(self) -> str:
         return f"AdressBook:\n{self.get_all()}"