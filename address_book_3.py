import datetime
import json
import re
from collections import UserDict


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()

    # приймаємо ім'я файлу та об'єкт адресної книги
    # та серіалізує його в JSON формат та записує у файл.

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    # відновлення даних з файлу

    def load_from_file(self, filename):
        with open(filename, 'r') as f:
            self.data = json.load(f)

    # метод iterator, який повертає генератор
    # за записами AddressBook і за одну ітерацію повертає уявлення для N записів

    def iterator(self, n=1):
        if n <= 0:
            raise ValueError("n should be greater than zero")
        total = len(self.data)
        for i in range(0, total, n):
            yield list(self.data.values())[i:i+n]


class Field:
    def __init__(self, value=None):
        self.__value = value

    def __str__(self):
        return str(self.__value)

    def __repr__(self):
        return str(self.__value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, val):
        self.__value = val


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value=None):
        if value:
            value = [value]
        else:
            value = []
        super().__init__(value)

    @Field.value.setter
    def value(self, val):
        if val is None:
            self.__value = None
        else:
            val = re.sub(r'[^\d]', '', val)
            if len(val) == 10:
                self.__value = f'({val[:3]}) {val[3:6]}-{val[6:]}'
            elif len(val) == 11:
                self.__value = f'{val[0]} ({val[1:4]}) {val[4:7]}-{val[7:]}'
            else:
                raise ValueError('Invalid phone number')

    @Field.value.getter
    def value(self):
        return self.__value

    def add_phone(self, phone):
        self.__value.append(phone)

    def remove_phone(self, phone):
        self.__value.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        index = self.__value.index(old_phone)
        self.__value[index] = new_phone


class Birthday(Field):
    def __init__(self, value=None):
        super().__init__()
        self.__value = None
        self.value = value

    @Field.value.setter
    def value(self, val):
        if val is None:
            self.__value = None
        else:
            try:
                date = datetime.datetime.strptime(val, '%d.%m.%Y')
                if date > datetime.datetime.now():
                    raise ValueError('Invalid date of birth')
                self.__value = date.date()
            except ValueError:
                raise ValueError('Invalid date format')

    @Field.value.getter
    def value(self):
        return self.__value


class Record:
    def __init__(self, name):
        self.name = name
        self.phones = Phone()
        self.birthday = Birthday()

    def __repr__(self):
        return f'{self.name}: {self.phones}, {self.birthday}'

    # метод days_to_birthday, який повертає кількість
    # днів до наступного дня народження контакту, якщо день народження заданий
    def days_to_birthday(self):
        if self.birthday is None:
            return None
        today = datetime.date.today()
        if today.month < self.birthday.month or (today.month == self.birthday.month and today.day < self.birthday.day):
            next_birthday = datetime.date(
                today.year, self.birthday.month, self.birthday.day)
        else:
            next_birthday = datetime.date(
                today.year+1, self.birthday.month, self.birthday.day)
        days_left = (next_birthday - today).days
        return days_left

    def input_error(handler):

        def wrapper(*args, **kwargs):
            try:
                return handler(*args, **kwargs)
            except KeyError:
                return "Contact not found"
            except ValueError:
                return "Please enter the name and phone number separated by a space"
            except IndexError:
                return "Please enter the name of the contact"
        return wrapper

    @Field.value.getter
    def value(self):
        return self.__value

    @input_error
    def add_phone(self, phone):
        self.__value.append(phone)

    @input_error
    def remove_phone(self, phone):
        self.__value.remove(phone)

    @input_error
    def edit_phone(self, old_phone, new_phone):
        index = self.__value.index(old_phone)
        self.__value[index] = new_phone

# метод, який буде шукати вказані рядки в іменах та номерах телефонів контактів
    @input_error
    def search(self, x):
        results = []
        for contact in self.data.values():
            if x.lower() in contact.name.value.lower() or x in contact.phones.value.lower():
                results.append(contact)
        return results


# Головна функція, яка взаємодіє з користувачем
def main():
    print("Hello! How can I help you?")
    while True:
        command = input(">>> ").lower()
        if command == "hello":
            print("How can I help you?")
        elif command == "add":
            data = input("Enter name and phone: ")
            print(Record.add_phone(data))
        elif command == "change":
            data = input("Enter name and phone: ")
            print(Record.change_phone(data))
        elif command == "phone":
            name = input("Enter name: ")
            print(Record.edit_phone(name))
        elif command == "remove":
            name = input("Enter name: ")
            print(Record.remove_phone(name))
        elif command == "search":
            print(Record.search(data, name))
        elif command in ["good bye", "close", "exit", "."]:
            print("Good bye!")
            break
        else:
            print("Sorry, I didn't understand the command. Please try again.")


# Запускаємо головну функцію
if __name__ == '__main__':
    main()
