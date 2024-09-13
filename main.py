from fields import AddressBook, Record, Name, Phone, Birthday, datetime
from handlers import Assistant

assistant = Assistant()

@assistant.command_handler(("exit", "close", "bye"))
def close(caller:Assistant):
    caller.mainloopActive = False
    return "Good bye!"

@assistant.command_handler("hello")
def hello_handler(caller:Assistant):
    return "How can I help you?"

@assistant.command_handler("add", (str, str), 1)
def add_handler(caller:Assistant, name:str, phone:str = ""):
    book = caller.book
    res = ""
    if(not book.has_record(name)):
        book.add_record(Record(name))
        res = f"Record added: {name}"
    if(phone != ""):
        rec = book.get(name)
        if(rec != None):
            rec.add_phone(phone)
            if(res != ""):
                res += "\n"
            res += f"Phone added: {phone} for {name}"
        else:
            if(res != ""):
                res += "\n"
            res += f"Record {name} not found."
    return res

@assistant.command_handler("change", (str, str, str))
def change_handler(caller:Assistant, name:str, phone1:str, phone2:str):
    book = caller.book
    if(not book.has_record(name)):
        return f"Record {name} not found."
    rec = book.find(name)
    if(not rec.has_phone(phone1)):
        return f"Record {name} doesn`t have phone {phone1}."
    rec.edit_phone(phone1, phone2)
    return "Phone changed."

@assistant.command_handler("phone", str)
def get_phone(caller:Assistant, name:str):
    book = caller.book
    if(not book.has_record(name)):
        return f"Record {name} not found."
    rec = book.find(name)
    if(rec.phones_amount() <= 0):
        return f"Record {name} doesn`t have any phones."
    return rec.get_phones()

@assistant.command_handler("all")
def get_contacts(caller:Assistant):
    book = caller.book
    if(len(book) <= 0):
        return "There are no contacts registried."
    return book.get_all()

@assistant.command_handler("add-birthday", (str, datetime))
def add_birthday(caller:Assistant, name:str, birthday:datetime):
    print(type(birthday))
    book = caller.book
    if(not book.has_record(name)):
        return f"Record {name} not found."
    rec = book.find(name)
    if(rec.has_birthday()):
        return f"Record {name} already has birthday."
    rec.add_birthday(birthday)
    return f"Birthday added to record {name}"

@assistant.command_handler(("show-birthday", "birthday"), (str))
def get_birthday(caller:Assistant, name:str):
    book = caller.book
    if(not book.has_record(name)):
        return f"Record {name} not found."
    rec = book.find(name)
    return str(rec.birthday)

@assistant.command_handler("birthdays", int, 1)
def get_birthdays(caller:Assistant, days = 7):
    book = caller.book
    if(len(book) <= 0):
        return "There are no contacts registried."
    birthdays = book.get_birthdays(days)
    if(len(birthdays) <= 0):
        return "There are no upcoming birthdays."
    res = ""
    for i in birthdays:
        if(res != ""):
            res += "\n"
        res += i["name"] + ": " + i["congratulation_date"]
    return res

@assistant.command_handler("test", datetime)
def test(caller:Assistant, arg:datetime):
    return f"{str(arg)}: {str(type(arg))}"

assistant.mainLoop()