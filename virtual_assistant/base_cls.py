from collections import UserDict
from abc import ABC, abstractmethod
import re
from datetime import datetime, timedelta
import pickle
from items import Colors


class OutInfo(ABC):
    @abstractmethod
    def __repr__(self) -> str:
        pass
         
class Field(ABC):
    def __init__(self, value) -> None:
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    @abstractmethod
    def __str__(self):
        pass

class Book(ABC):
    @abstractmethod
    def load_book(self, file):
        pass
    @abstractmethod
    def save_book(self, file):
        pass
        

class Name(Field):
    def __str__(self) -> str:
        return f"Name: {self.value.capitalize()}\n"
    

class Phone(Field):
    def __init__(self, value):
        self.value = value

    @Field.value.setter
    def value(self, phone):
        ukr_code = "+380"
        res_phone = re.sub(r"(\\|\ |\(|\)|\-)|\+","",phone) 
    
        if  (8<len(res_phone)< 14) and (res_phone[len(res_phone)-9] != '0') and (res_phone.startswith(ukr_code[13-len(res_phone):])) and ( res_phone == re.sub(r"(\D*)","", res_phone) ):
            self._value = ukr_code[:13-len(res_phone)] + res_phone

        else:
            raise ValueError(f"{Colors.FAIL}{Colors.UNDERLINE}Error: Please enter correct phone number in the format: +380(XX)XXX-XX-XX{Colors.ENDC}")
        
    def __str__(self) -> str:
        if self.value:
            return '{}({}){}-{}-{}'.format(self.value[0:4], self.value[4:6], self.value[6:9], self.value[9:11], self.value[11:13])

       
class Email(Field):
    def __init__(self, value):
        self.value = value

    @Field.value.setter
    def value(self, email):
        if re.match(r'^[a-z0-9]+[._\-+]*[a-z0-9]*@\w+\.[a-zA-Z]{2,}(?:\.[a-zA-Z]{2,})?$', email):
            self._value = email
        else:
            raise ValueError(f"{Colors.FAIL}{Colors.UNDERLINE}Error: Invalid email format.{Colors.ENDC}")

    def __str__(self) -> str :
        return f"Email: {self.value}\n"       

class Birthday(Field):
    def __init__(self, value):
        self.value = value

    @Field.value.setter
    def value(self, value):
        try:
            birth_value = re.sub(r'\D*','', value)
            if len(birth_value) == 8:
                birth_value = birth_value[:4] + birth_value[6:]
            res_data = datetime.strptime(birth_value, '%d%m%y')
        except:
            raise ValueError(f"{Colors.FAIL}Please enter correct data in the format: {Colors.UNDERLINE}dd-mm-yyyy.{Colors.ENDC}")
        else:
            if res_data <= datetime.now():
                self._value = res_data.date()
            else:
                raise ValueError(f"{Colors.FAIL}{Colors.UNDERLINE}Error: Date of birth cannot be in the future! Please try again.{Colors.ENDC}")
       
   
    def __str__(self) -> str:
        return f"Birthday: {self._value.strftime('%d-%m-%Y')}\n"

        

    def __calc_birthday__(self):
        today = datetime.now().date()
        birth_date = self.value
        if birth_date.month == 2 and birth_date.day == 29:
            future_birthday = datetime(year = today.year, month = 2, day = birth_date.day - int(bool(today.year%4))).date()
            
            if future_birthday < today: 
                future_birthday = datetime(year = today.year + 1, month = 2, day = birth_date.day - int(bool((today.year+1)%4))).date()
            
        else:
            future_birthday = datetime(year = today.year, month = birth_date.month, day = birth_date.day).date()
            if future_birthday < today:
                future_birthday = future_birthday.replace(year = today.year + 1)
        return (future_birthday - today).days


class Address(Field):
    def __str__(self) -> str :
        return f"Address: {self.value}\n"

    

class Record:
    def __init__(self, name, phone=None, birthday=None, email=None, address=None):
        self.name = Name(name)
        self.phones = []
        if phone:
            self.phones.append(Phone(phone))
        self.birthday = Birthday(birthday) if birthday else None
        self.email = Email(email) if email else None
        self.address = Address(address) if address else None


    def add_phone(self, phone):
        if not self.phones:
            self.phones = []
        self.phones.append(Phone(phone))

    def edit_phone(self, index, new_phone):
        self.phones[index] = Phone(new_phone)

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def edit_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_email(self, email):
        self.email = Email(email)

    def edit_email(self, email):
        if self.email:
            self.email.value = email
        else:
            self.email = Email(email)

    def add_address(self, address):
        self.address = Address(address)

    def edit_address(self, address):
        if self.address:
            self.address.value = address
        else:
            self.address = Address(address)

    def __iter__(self):
        self._iter_index = 0
        self._fields = [
            self.name,
            *self.phones,
            self.birthday,
            self.email,
            self.address
        ]
        return self

    def __next__(self):
        if self._iter_index < len(self._fields):
            value = self._fields[self._iter_index]
            self._iter_index += 1
            return value
        else:
            raise StopIteration

    def __repr__(self):             #Вывести все поля для класса Record в строку
        return (f"{self.name}"
                f"{(','+str(chr(10))).join('Phone '+str(i+1)+': '+str(phone) for i, phone in enumerate(self.phones))}\n"
                f"{self.email if self.email else ''}"
                f"{self.birthday if self.birthday else ''}"
                f"{self.address if self.address else ''}"
                f"{'_' * 30}")



class Contacts(UserDict, Book):
     
    def add_record(self, record: Record):       #Добавление записи
        self.data[record.name.value] = record

    def get_record(self, name):     #Вывод записи
        return self.data.get(name)

    def delete_record(self, name):      #Удаление записи
        try:
            self.data.pop(name)
            return(f"Contact {name} was successfully deleted from the book ")
        except KeyError:
            return f"There is no such contact: {name} in the book!"
   

    def iterator(self, num_records):        #Итератор(Принимает число, возвращает генератор)
        records = list(self.data.values())
        for i in range(0, len(records), num_records):
            yield records[i:i + num_records]

    def search_contacts(self, query):           #Функционал поиска в контактной книге
        result = []
        for record in self.data.values():
            united_str = ""
            for rec in record:
                try:
                    united_str = united_str + str(rec.value)
                except AttributeError:
                    pass
            united_str = re.sub(r"\+|\-|\)|\(", "", united_str)
            if query and query in united_str:
                result.append(str(record))

        return '\n\n'.join(result) if result else f"{Colors.WARNING}{Colors.UNDERLINE}Nothing was found{Colors.ENDC}"
    
    def congratulate_period(self, number_days):
        start_period = datetime.now().date()
        end_period = start_period + timedelta(number_days)
        congrat_message = f"{Colors.OKGREEN}For the period from {start_period} to {end_period}"
        list_congratulate = []
        for record in self.data.values():
            if record.birthday:
                if record.birthday.__calc_birthday__() <= number_days:
                    list_congratulate.append(record)
        if list_congratulate:
            return f"{congrat_message} the following contacts have birthdays: {str(chr(10))+str(chr(10)).join(str(p) for p in list_congratulate)}"
        return f"{congrat_message} there are no birthdays recorded in your book"
        
    def load_book(self, file):
        try:
            self.data = pickle.load(file)
        except EOFError:
            pass
    
    def save_book(self, file):
        pickle.dump(self.data, file)
        

class Note():
    def __init__(self, title: str = None, content: str = None, tags: list = None):
        self.title = title
        self.content = content
        self.tags = tags

    def add_content(self, content: str):
        self.content += '\n'+content

    def add_tags(self, tags: list):
        if tags:
            self.tags.extend(tags)
    
    def __str__(self) -> str:
        return f"\nTitle: {self.title.capitalize()},\nContent: {self.content.capitalize()},\nTags: {self.tags}"

class Notes(UserDict, Book):
    
    def add_note(self, note:Note):
        self.data[note.title] = note
    
    def get_note(self, title: str):
        return self.data.get(title)

    def edit_note(self, name, **kwargs):
        note = self.data[name]
        for key, value in kwargs.items():

            if value != '':
                setattr(note, key, value)

    def delete_note(self, name: str):
        try:
            self.data.pop(name)
            return f"Note {name} was successfully deleted from the notes "
        except KeyError:
            return f"There is no such note: {name} in the notes!"
          
    def search_note(self, query: str):
        notes_results = []        
        for note in self.data.values():
            if query in str(vars(note).values()):
                notes_results.append(str(note))
        return '\n\n'.join(notes_results) if notes_results else f"{Colors.WARNING}{Colors.UNDERLINE}No notes were found.{Colors.ENDC}"
    
    def sort_by_tag(self):
        sorted_notes = sorted(self.data.values(), key=lambda note: note.tags[0] if note.tags else "")
        self.data = {note.title: note for note in sorted_notes}
        return sorted_notes
      
    def load_book(self, file):
        try:
            self.data = pickle.load(file)
        except EOFError:
            pass
    
    def save_book(self, file):
        pickle.dump(self.data, file)   

class OutputBook(OutInfo):
    def __init__(self, obj):
        self.obj = obj
        
    def __repr__(self) -> str:
        out_list = []
        for items in self.obj.values():
            items_list = []
            item= (f"{items.name}"
                    f"{(','+str(chr(10))).join('Phone '+str(i+1)+': '+str(phone) for i, phone in enumerate(items.phones))}\n"
                    f"{items.email if items.email else ''}"
                    f"{items.birthday if items.birthday else ''}"
                    f"{items.address if items.address else ''}"
                    f"{'_' * 30}")

            items_list.append(item)
            if item:
                    try:
                        items_list.append(str(item))
                    except TypeError:
                        for it,index in enumerate(item):
                            items_list.append(f"Phone {index+1} {str(it)}")
                        
            out_list.append(items_list)
        return out_list
            

class Type_Messenger(ABC):
    @abstractmethod
    def input_message(self):
        pass

    @abstractmethod
    def send_message(self):
        pass
    
    @abstractmethod
    def input_folder(self):
        pass


class Console_Messenger(Type_Messenger):

    def input_message(self, value=None):
        item = input(f"{value:}").lower()
        return item

    def send_message(self, value) -> None:
        print(value)

    def input_folder(self, value):
        folder = input(f"{value:}")
        return folder


class Telegram_Messenger(Type_Messenger):
    
    def input_message(self, value=None):
        pass

    def send_message(self) -> None:
        pass
    
    def input_folder(self):
        pass

