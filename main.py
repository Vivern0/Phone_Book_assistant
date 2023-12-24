from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value):
        if self.validate(value):
            self.__value = value

    def validate(slef, new_value):
        return True

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if self.validate(new_value):
            self.__value = new_value

    def __str__(self):
        return str(self.__value)


class Name(Field):
    pass


class Birthday(Field):
    def validate(slef, new_birth):
        if new_birth is None:
            return True
        elif not all([len(new_birth) == 10,
                      isinstance(new_birth, str)]):
            raise ValueError('Wrong date format, should be dd.mm.yyyy')
        return True


class Phone(Field):
    def validate(slef, new_phone):
        if not all([len(new_phone) == 10,
                    new_phone.isdecimal()]):
            raise ValueError('Wrong phone number format, should be 10 digits')
        return True


class Record:
    def __init__(self, name, *phones, birthday=None):
        self.name = Name(name)
        self.phones = [Phone(i) for i in phones] if phones else []
        self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        if phone not in map(lambda x: x.value, self.phones):
            self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for el in self.phones:
            if el.value == phone:
                self.phones.remove(el)

    def edit_phone(self, old, new):
        temp = {p.value: p for p in self.phones}
        if old in temp.keys():
            old_ind = self.phones.index(temp[old])
            self.phones[old_ind].value = new
        else:
            raise ValueError('No such phone number')

    def find_phone(self, phone):
        temp = {p.value: p for p in self.phones}
        if phone in temp.keys():
            return temp[phone]
        return None

    def add_birthday(self, birthday):
        self.birthday.value = birthday

    def days_to_birthday(self):
        if self.birthday.value is not None:
            cur_date = datetime.now().date()
            try:
                cur_birthday = datetime.strptime(self.birthday.value,
                                                 '%d.%m.%Y').date()
            except ValueError('Wrong date format, should be dd.mm.yyyy'):
                return None
            next_birth = cur_birthday.replace(year=cur_date.year)
            if next_birth < cur_date:
                next_birth = next_birth.replace(year=cur_date.year + 1)
            return (next_birth - cur_date).days
        return None

    def __str__(self):
        if self.birthday.value is None:
            return f"Contact name: {self.name.value}; " \
                    f"phones: {', '.join(p.value for p in self.phones)}."

        return f"Contact name: {self.name.value}; " \
               f"phones: {', '.join(p.value for p in self.phones)}; " \
               f"birthday: {self.birthday.value}."


class AddressBook(UserDict):
    def add_record(self, user):
        self.data[user.name.value] = user

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if self.data.get(name) is not None:
            del self.data[name]

    def iterator(self, n):
        if n == 0:
            raise ValueError('n should be greater than 0')

        start = 0
        step = n
        end = len(self.data)
        while start < end:
            temp = list(self.data.values())[start:step]
            yield [str(i) for i in temp]
            start += n
            step += n


if __name__ == '__main__':
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane", '1111111111', '2222222222',
                         birthday="01.01.2000")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for record in book.data.values():
        print(record)
    print('-'*50)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 555555555
    print('-'*50)

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: John: 5555555555
    print('-'*50)

    # Видалення запису Jane
    book.delete("Jane")

    for record in book.data.values():
        print(record)
    print('-'*50)

    # Виведення днів до наступного дня народження John
    print(john_record.days_to_birthday())

    # Редагування дня народження John
    john_record.add_birthday("01.01.2000")
    print(john_record)

    # Виведення днів до наступного дня народження John
    print(john_record.days_to_birthday())
    print('-'*50)

    # Додавання 10 нових записів для тесту ітератора AddressBook
    rec_1 = Record("Name1", "1234567890", birthday="01.01.2000")
    book.add_record(rec_1)
    rec_2 = Record("Name2", "1234567890", birthday="01.01.2000")
    book.add_record(rec_2)
    rec_3 = Record("Name3", "1234567890", birthday="01.01.2000")
    book.add_record(rec_3)
    rec_4 = Record("Name4", "1234567890", birthday="01.01.2000")
    book.add_record(rec_4)

    # Виведення записів по 3
    records_per_page = book.iterator(3)
    for page in records_per_page:
        print(page, end='\n\n')
