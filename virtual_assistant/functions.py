from base_cls import *
from items import *
from difflib import SequenceMatcher
import sys
import sort
#from main import messenger
contacts = Contacts()
notes = Notes()


def input_error(func):
    def handler(*args):
        argnames = func.__code__.co_varnames[:func.__code__.co_argcount]
        try:
            return func(*args)
        except KeyError:
            return "Error: key doesn't exist."
        except ValueError as e:
            return e
        except IndexError:
            return "Error: provide both name and phone number."
        except TypeError:
            return f"Error: required parameters are: {', '.join(argnames)}"
    return handler


def bye(messenger = None):
    save_book(filename)
    sys.exit(BYE)

def hello(messenger = None):
    return "Hello!"


def help(messenger=None):
    
    with open(file_help, "r") as fh:
        lines = fh.readlines()
        help_info = "\r".join(lines)
    return help_info



#@input_error
def add(items, name, messenger):
    non_item = []
    for item in items:
        
        if item == "contact":
            if name not in contacts:
                while True:
                    phone = messenger.input_message(
                        f"Enter the phone in following format {Colors.HEADER}{format_maps['phone']}{Colors.ENDC}: (or press <Enter> to create contact {Colors.HEADER}{name.capitalize()}{Colors.ENDC} without a phone) ")

                    if not phone:
                        record = Record(name)
                        break
                    try:
                        record = Record(name, phone)
                        break
                    except Exception as e:
                        messenger.send_message(
                            f"{Colors.FAIL}{Colors.UNDERLINE}{e}{Colors.ENDC}")
                    
                contacts.add_record(record)
            else:
                return "Contact already exists."
        elif item == "note":
            content = messenger.input_message(ENTER_CONTENT)

            try:
                tags = messenger.input_message(ADD_TAGS).split(", ")

                notes.add_note(Note(name, content, tags))
            except:
                return f"{Colors.FAIL}{Colors.UNDERLINE}Error: Provide tags{Colors.ENDC}"
        elif item == "tags":
            try:
                notes[name].add_tags(messenger.input_message(
                    ADD_TAGS).split(", "))

            except:
                return f"{Colors.FAIL}{Colors.UNDERLINE}Error: Provide tags{Colors.ENDC}"
        else:
            try:
                record:Record = contacts[name]
            except KeyError:
                return f"{Colors.FAIL}{Colors.UNDERLINE}Error: contact {name} doesn't exist.{Colors.ENDC}"
            item_maps = {
                "phone": record.add_phone,
                "email": record.add_email,
                "birthday": record.add_birthday,
                "address": record.add_address,
            }
            while True:
                item_input = messenger.input_message(f"Enter the {Colors.HEADER}{item}{Colors.ENDC} in following format {Colors.HEADER}{format_maps[item]}{Colors.ENDC}: (or press <Enter> to continue without add {item}) ")
                if not item_input:
                    non_item.append(item)
                    break
                try:
                    item_maps[item](item_input)
                    break
                except Exception as e:
                    messenger.send_message(f"{Colors.FAIL}{Colors.UNDERLINE}{e}{Colors.ENDC}")

        
    items = list(set(items) - set(non_item))
    if items:
        return f"{Colors.OKGREEN}{Colors.UNDERLINE}Success! {', '.join(items)} have been added.{Colors.ENDC}"
    else:
        return f"Nothing added"

#@input_error
def edit(items, name, messenger):
    non_item = []
    for item in items:
        if item == "note":
            try:
                notes[name]
                title = messenger.input_message("Enter new title (Press Enter to skip): ")
                content = messenger.input_message("Enter new content (Press Enter to skip): ")
                tags = messenger.input_message("Enter new tags (Press Enter to skip): ").split(", ")

                notes.edit_note(name,title = title, content=content, tags=tags)
            except:
                return f"{Colors.FAIL}{Colors.UNDERLINE}Error: note with such name doesn't exist.{Colors.ENDC}"
        else:
            try:
                record: Record = contacts[name]
            except:
                return f"{Colors.FAIL}{Colors.UNDERLINE}Error: contact {name} doesn't exist.{Colors.ENDC}"

            item_maps = {
                "phone": record.edit_phone,
                "email": record.edit_email,
                "birthday": record.edit_birthday,
                "address": record.edit_address,
            }
            if item == "phone":
                if len(record.phones) == 1:
                    while True:
                        new_phone = messenger.input_message(f"Enter new phone number in following format {Colors.HEADER}{format_maps['phone']}{Colors.ENDC}:  (or press <Enter> to continue without change {Colors.HEADER}{record.phones[0]}{Colors.ENDC}) ")
                        if not new_phone:
                            non_item.append(item)
                            break
                        try:
                            record.phones[0] = Phone(new_phone)
                            break
                        except Exception as e:
                            messenger.send_message(f"{Colors.FAIL}{Colors.UNDERLINE}{e}{Colors.ENDC}")

                elif len(record.phones) > 1:
                    messenger.send_message(AVAILABLE_PHONES)

                    for idx, phone in enumerate(record.phones):
                        messenger.send_message(f"{idx + 1}. {phone}")

                    try:
                        choice = messenger.input_message("Enter the number of the phone to edit: ")-1

                        if 0 <= choice < len(record.phones):
                            while True:
                                new_phone = messenger.input_message(f"Enter new phone number in following format {Colors.HEADER}{format_maps['phone']} {Colors.ENDC} (or press <Enter> to continue without change number :{Colors.HEADER}{record.phones[choice]}{Colors.ENDC}) ")

                                if not new_phone:
                                    non_item.append(item)
                                    break
                                try:
                                    record.phones[choice] = Phone(new_phone)
                                    break
                                except ValueError as e:
                                    messenger.send_message(e)

                        else:
                            messenger.send_message(ERROR_CHOICE)

                            non_item.append(item)
                    except ValueError:
                        messenger.send_message(ERROR_CHOICE)

                        non_item.append(item)
                else:
                    messenger.send_message(NO_PHONE)

                    non_item.append(item)
            elif item in item_maps:
                while True:
                    new_value = messenger.input_message(f"Enter the new {item} in the format: {Colors.HEADER}{format_maps[item]} {Colors.ENDC} (or press <Enter> to continue without change {Colors.HEADER}{item}{Colors.ENDC}) ")

                    if not new_value:
                        non_item.append(item)
                        break
                    try:
                        item_maps[item](new_value)
                        break
                    except Exception as e:
                        messenger.send_message(f"{Colors.FAIL}{Colors.UNDERLINE}{e}{Colors.ENDC}")

            else:
                return f"{Colors.FAIL}{Colors.UNDERLINE}Error: {item} cannot be edited.{Colors.ENDC}"
    items = list(set(items) - set(non_item))
    if items:
        return f"{Colors.OKGREEN}{Colors.UNDERLINE}Success! {', '.join(items)} have been edited.{Colors.ENDC}"
    else:
        return f"Nothing edited"
            
@input_error
def congratulate(messenger):
    while True:
        try:
            return contacts.congratulate_period(int(messenger.input_message(f"Enter the number of days for congratulations: ")))

        except:
            pass

@input_error   
def search(messenger):
    while True:
        choice = messenger.input_message(
            f"What would you like to search {Colors.HEADER}contact{Colors.ENDC} or {Colors.HEADER}note{Colors.ENDC}?: ")

        choice = nick_command(choice, ["contact", "note"])
        if choice == "contact":
            try:
                return '\n' + contacts.search_contacts(messenger.input_message(f"Enter the query for search: "))
            except:
                messenger.send_message(
                    f"{Colors.WARNING}{Colors.UNDERLINE}Provide query for the search!{Colors.ENDC}")
                continue
        elif choice == "note":
            return notes.search_note(messenger.input_message("Enter the query for search: "))
        else:
            return f"{Colors.FAIL}{Colors.UNDERLINE}Error: Choose between available options: contact, note{Colors.ENDC}"     
    
    
#@input_error       
def delete(items, name, messenger):
    for item in items:
        if item == "note":
            try:
                notes.pop(name)
            except:
                return f"{Colors.WARNING}{Colors.UNDERLINE}Note was not found.{Colors.ENDC}"
        elif item == "contact":
            try:
                contacts.pop(name)
            except:
                return f"{Colors.WARNING}{Colors.UNDERLINE}Contact was not found.{Colors.ENDC}"
        else:
            record:Record = contacts[name]
            for key, item in zip(vars(record), items):
                if item == key:
                    vars(record)[key] = None
                elif item == "phone":
                    if len(record.phones) <= 1:
                        record.phones = None
                    else:
                        messenger.send_message(AVAILABLE_PHONES)
                        for idx, phone in enumerate(record.phones):
                            messenger.send_message(f"{idx + 1}. {phone}")

                        try:
                            choice = int(
                                messenger.input_message("Choose the number of the phone to delete: ")) - 1
                            del record.phones[choice]
                        except ValueError:
                            return ERROR_CHOICE
    return f"{Colors.OKGREEN}{Colors.UNDERLINE}Success! {item} has been deleted!{Colors.ENDC}"

    
@input_error
def showall(messenger):
    item = messenger.input_message(
        f"{Colors.HEADER}Available options: contacts, notes{Colors.ENDC}\nWhat would you like to see?: ")
    item = nick_command(item, ["contacts", "notes"])
    if not item or item not in ["contacts", "notes"]:
        return f"{Colors.FAIL}{Colors.UNDERLINE}Option not available {item}.{Colors.ENDC}"
    elif item == "notes":
        if not notes:
            return f"{Colors.WARNING}{Colors.UNDERLINE}No notes were found.{Colors.ENDC}"
        choice = messenger.input_message(
            "Do you wish to sort notes by tags? y/n: ")
        if choice == "y":
            result = [str(x) for x in notes.sort_by_tag()]
            return '\n\n'.join(result)
        elif choice == "n":    
            result = [str(x) for x in notes.values()]
            return '\n\n'.join(result)
    else:
        number = 3
        try:
            number = int(messenger.input_message(
                f"How many records would you like to retrieve in one iteration?(by default = {Colors.HEADER}{number}{Colors.ENDC})\n>>> "))
        except ValueError:
            pass
        result = contacts.iterator(number)
        num_rec = len(contacts)
        for records_batch in result:
            num_rec -= number
            for i in records_batch:
                messenger.send_message(f"{i} {str(chr(10))}")
            if num_rec > 0:
                answer = messenger.input_message(
                    "Press Enter to continue. Press Q to exit.\n>>> ")
                if answer == "q":
                    break
        return f"{Colors.OKGREEN}{Colors.UNDERLINE}Total contacts: {len(contacts)}.{Colors.ENDC}"

def load_books(filename):
    try:
        with open(filename, "rb") as fh:
            contacts.load_book(fh)
            notes.load_book(fh)
    except FileNotFoundError:
        pass
    
def save_book(filename):
    with open(filename, "wb") as fh:
        contacts.save_book(fh)
        notes.save_book(fh)

def translate(name):
    CYRILLIC_SYMBOLS = "абвгдезийклмнопрстуфцчшщыьяєё"
    TRANSLATION = ("f", ",", "d", "u", "l", "t", "p", "b", "q", "r", "k", "v", "y", "j", "g", "h", "c", "n", "e", "a",
               "w", "x", "i", "o", "s", "m", "z", "\\")
    TRANS = {}
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()
        
    return re.sub(r'\W', '_', name.translate(TRANS))

def nick_command(command, command_list):
    indices =[]
    list_of_command = ','.join(list(map(lambda x: x if type(x) == str else ",".join(x), command_list))).split(",")

    while True:
        max_value = max(list(map(lambda x: SequenceMatcher(None, command, x).ratio() , list_of_command)))
        if max_value == 0:
            command = translate(command)
            max_value = max(list(map(lambda x: SequenceMatcher(None, command, x).ratio() , list_of_command)))
        break    
            
    if max_value > 0.50:
        indices = [val for index, val in enumerate(list_of_command) if SequenceMatcher(None, command, val).ratio()==max_value ]
        return list(filter(lambda x : indices[0] in x, command_list))[0]



def nick_str(command = None, command_item:str = None, command_items: list = None):
    if command_item:
        return nick_command(command_item, command_items)

    if command_items:
        command_list = []
        for item in command_items:
            try:
                command_list.append(nick_command(item, list(filter(lambda x: available_options[command][x] == True, available_options[command]))))
            except:
                pass
        return command_list


command_maps = {
    "hello": hello,
    ("bye", "close", "exit", "quit"): bye,
    "help": help,
    "add": add,
    "edit": edit,
    "delete": delete,
    ("search", "find"): search,
    "showall": showall,
    "congratulate": congratulate,
    "organize": sort.organize_files
}


def command_offer(command_maps):
    command_list = list(map(lambda x: x if type(x) == str else ", ".join(x), command_maps.keys()))
    command_list = ", ".join(command_list)
    return f"\n{Colors.HEADER}Available commands: {Colors.UNDERLINE}{command_list}.{Colors.ENDC}"
    
def command_items(command, messenger):
    messenger.send_message(f"{Colors.HEADER}Available options for command {Colors.ENDC}[{command}]: {Colors.HEADER}{Colors.UNDERLINE}{', '.join(list(filter(lambda x: available_options[command][x] == True, available_options[command])))}{Colors.ENDC}")
    items = re.findall(r'[а-яА-Яa-zA-Z]+', messenger.input_message(f"What would you like to {command}?: "))
    return items