from fields import AddressBook, datetime
from bithday import string_to_date
from collections import defaultdict
from datetime import datetime
import pickle
import re

class ContactError(Exception):
    pass

class Assistant:
    types=(int, float, str, datetime)
    def __init__(self):
        self.book = self.__load_data()
        self.handlers = defaultdict(list)

    @staticmethod
    def input_error(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (KeyError,IndexError,ContactError, ValueError) as e:
                return str(e)

        return inner
    
    def __save_data(self, filename="addressbook.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(self.book, f)

    @staticmethod
    def __load_data(filename="addressbook.pkl"):
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return AddressBook()
    
    def check_command(self, commands, args:tuple):
        regex = '^[a-z_][a-z0-9_]*'
        for i in commands:
            if(not re.search(regex, i)):
                raise SyntaxError(f"Invalid command: {i}")
            if(i in self.handlers):
                c = self.handlers.get(i)[0]["args"]
                if(args != c):
                    raise SyntaxError("Same command handlers can`t have different args.")

    def command_handler(self, commands:tuple|str, args:tuple|type = (), unnecessaryArgs:int = 0):
        if(type(commands) != tuple):
            commands = (commands,)
        if(type(args) != tuple):
            args = (args,)
        def dec(func):
            self.check_command(commands, args)
            if(len(args) < unnecessaryArgs):
                raise SyntaxError("More unnecessary args than args total!")
            for i in args:
                if(i not in self.types):
                    raise SyntaxError(f"Wrong arg type: {i}")
            handler = {"args": args, "func":self.input_error(func), "unnecessaryArgs": unnecessaryArgs}
            for i in commands:
                self.handlers[i].append(handler)
            return handler["func"]
        return dec
        
    def handle_input(self, input:str):
        args = 0
        cmd = ""
        try:
            cmd, *args = input.split()
            cmd = cmd.strip().lower()
        except ValueError:
            return "You haven`t entered command"
        
        handlers = self.handlers.get(cmd)
        if(handlers == None):
            return "Command not found"

        for handler in handlers:
            if(len(args) < len(handler["args"]) - handler["unnecessaryArgs"]):
                return "Too few args!"
            if(len(args) > len(handler["args"])):
                return "Too many args"
        
        _args = []
        for i, arg_ in enumerate(args):
            try:
                arg = handler["args"][i]
                if(arg == str):
                    _args.append(arg_)
                elif(arg == int):
                    _args.append(int(arg_))
                elif(arg == float):
                    _args.append(float(arg_))
                elif(arg == datetime):
                    try:
                        _args.append(string_to_date(arg_))
                    except ValueError:
                        return "Invalid date format. Use DD.MM.YYYY"
                
            except ValueError:
                return "Wrong args!"
            

        return [handler["func"](self, *args) for handler in handlers]
    
    def mainLoop(self):
        while True:
            try:
                res = self.handle_input(input(">>> "))
                if(type(res) == list):
                    print(*res, sep="\n")
                else:
                    print(res)
            except KeyboardInterrupt:
                print("\nGood bye!")
                self.__save_data()
                break
            except Exception as e:
                print(e)