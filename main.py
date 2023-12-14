from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

        if not all([len(self.value) == 10,
                    self.value.isdecimal()]):
            raise ValueError


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

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
            self.phones[old_ind] = Phone(new)
        else:
            raise ValueError

    def find_phone(self, phone):
        temp = {p.value: p for p in self.phones}
        if phone in temp.keys():
            return temp[phone]
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, \
            phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, user):
        self.data[user.name.value] = user

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if self.data.get(name) is not None:
            del self.data[name]


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
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for _, record in book.data.items():
        print(record)
    print('-'*30)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 555555555
    print('-'*30)

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555
    print('-'*30)

    # Видалення запису Jane
    book.delete("Jane")

    for _, record in book.data.items():
        print(record)
