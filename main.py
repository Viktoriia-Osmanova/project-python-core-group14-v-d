from string import digits, punctuation
from prettytable import PrettyTable
import re
from datetime import datetime

class Validator:
    days_count = {
        "January": 31,
        "February": 28,
        "March": 31,
        "April": 30,
        "May": 31,
        "June": 30,
        "July": 31,
        "August": 31,
        "September": 30,
        "October": 31,
        "November": 30,
        "December": 31,
    }

    @staticmethod
    def is_leap_year(year):
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    @staticmethod
    def can_be_empty(func):
        def wrapper(self, value):
            if value != "":
                return func(self, value)
            else:
                return True
        return wrapper

    def valid_as_name(self, text):
        if len(text) < 2:
            return False
        for digit in digits + punctuation:
            if digit in text:
                return False
        return True

    @can_be_empty
    def valid_as_address(self, text):
        return True

    @can_be_empty
    def valid_as_phone_number(self, text):
        phone_number_patterns = [
            r'\+\d{1,4} \d{3} \d{2} \d{2} \d{2}',
            r'\+\d{1,4}-\d{3}-\d{2}-\d{2}-\d{2}',
            r"\+\d{10,12}",
        ]
        return any([bool(re.fullmatch(ptrn, text)) for ptrn in phone_number_patterns])

    @can_be_empty
    def valid_as_email(self, text):
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        return bool(re.fullmatch(email_pattern, text))

    @can_be_empty
    def valid_as_birthday(self, text):
        if len(text.split()) != 3:
            return False
        year = int(text.split()[0])
        days = int(text.split()[1])
        month = text.split()[2].capitalize()

        if (year < 1920 or year > datetime.now().year) or (month not in self.days_count) or (days < 1 or days > (self.days_count[month] + Validator.is_leap_year(year))):
            return False
        return True

    def valid_input(self, validator, text, error_text):
        value = input(text)
        while not validator(value):
            print(error_text)
            value = input(text)
        return value

class Person:
    def __init__(self,
                 name: str,
                 address: str = None,
                 phone_number: str = None,
                 email: str = None,
                 birthday: str = None,
                 notes: str = None
                 ):
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.address = address
        self.birthday = birthday
        self.notes = notes

    @property
    def row(self):
        return [self.name, self.phone_number, self.email, self.address, self.birthday, self.notes._value]

    def __repr__(self):
        return f"Person {self.name}, {self.address}, {self.phone_number}, {self.email}, {self.birthday}"

class Notes:
    def __init__(self, value) -> None:
        self._value = value
        self._tags = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if new_value:
            self._value = new_value

    @property
    def tags(self):
        if self._tags:
            return self._tags
        return f'There are no tags.'

    @tags.setter
    def tags(self, new_tag_values):
        if new_tag_values:
            self._tags = new_tag_values

    def delete(self):
        if self._value:
            self._value = None
            return "Notes have been deleted."
        return "There are no notes."

class UserInterface:
    def __init__(self):
        self.people = []
        self.validator = Validator()
        self._attributes = ['name', 'phone number', 'email address', 'address', 'birthday date', 'notes']

    def _message(self, attribute, valid_input=True):
        if valid_input:
            if attribute == 'birthday date':
                return f'Enter {self._attributes[self._attributes.index(attribute)]} (e.g., 2004 23 May): '
            elif attribute == "address":
                return f'Enter {self._attributes[self._attributes.index(attribute)]} (e.g., USA, New-York, Wall-Street, 23a): '
            else:
                return f'Enter {self._attributes[self._attributes.index(attribute)]}: '
        return f"You have entered invalid {self._attributes[self._attributes.index(attribute)]}. Please recheck and try again. "

    def create(self):
        name = self.validator.valid_input(
            self.validator.valid_as_name, self._message('name'),  self._message('name', 0))
        phone_number = self.validator.valid_input(self.validator.valid_as_phone_number, self._message(
            'phone number'), self._message('phone number', 0))
        email = self.validator.valid_input(self.validator.valid_as_email, self._message(
            'email address'), self._message('email address', 0))
        address = self.validator.valid_input(self.validator.valid_as_address, self._message(
            'address'), self._message('address', 0))
        birthday = self.validator.valid_input(self.validator.valid_as_birthday, self._message(
            'birthday date'), self._message('birthday date', 0)).title()
        notes = Notes(input(self._message('notes')))

        new_person = Person(name, address, phone_number,
                            email, birthday, notes)

        self.people.append(new_person)

    def edit_attribute_menu(self, contact):
        text = """Choose attribute to edit:
        1. Name
        2. Phone
        3. Email
        4. Address
        5. Birthday
        6. Notes
        0. Cancel
        Your choice: """
        attribute = input(text)
        if attribute == "1":
            contact.name = self.validator.valid_input(
                self.validator.valid_as_name, self._message('name'),  self._message('name', 0))
        elif attribute == "2":
            contact.phone_number = self.validator.valid_input(
                self.validator.valid_as_phone_number, self._message('phone number'), self._message('phone number', 0))
        elif attribute == "3":
            contact.email = self.validator.valid_input(self.validator.valid_as_email, self._message(
                'email address'), self._message('email address', 0))
        elif attribute == "4":
            contact.address = self.validator.valid_input(
                self.validator.valid_as_address, self._message('address'), self._message('address', 0))
        elif attribute == "5":
            contact.birthday = self.validator.valid_input(self.validator.valid_as_birthday, self._message(
                'birthday date'), self._message('birthday date', 0))
        elif attribute == "6":
            edit_delete_note_input = input(
                '\n1. Edit note.\n2. Delete note.\nYour choice: ').strip()
            if edit_delete_note_input == '1':
                contact.notes.value = input('Please enter your new note: ')
            elif edit_delete_note_input == '2':
                contact.notes.delete()

    def edit(self):
        text = "Enter contact name to edit: "
        contact_name = input(text)
        found = list(filter(lambda con: contact_name.lower()
                     in con.name.lower(), self.people))

        if found:
            if len(found) == 1:
                self.edit_attribute_menu(found[0])
                return 1
            else:
                table = PrettyTable()
                table.field_names = ["№", "Name"]
                for index, con in enumerate(found):
                    table.add_row((index, con.name))
                print(table)
                number = input("Choose number contact to change: ")
                if number.isdigit() and int(number) < len(found):
                    self.edit_attribute_menu(found[int(number)])
                    return 1

        return

    def delete_contact(self):
        name_to_delete = input(
            "Enter the name of the contact you want to delete: ")
        matching_contacts = [
            person for person in self.people if person.name.lower() == name_to_delete.lower()]

        if not matching_contacts:
            print(f"No contact with the name '{name_to_delete}' found.")
        else:
            if len(matching_contacts) == 1:
                contact_to_delete = matching_contacts[0]
                self.people.remove(contact_to_delete)
                print(f"{contact_to_delete.name} has been deleted.")
            else:
                print(
                    "Contacts with the same name found. Please select the contact to delete:")
                table = PrettyTable()
                table.field_names = ["ID", "Name", "Phone"]
                for index, contact in enumerate(matching_contacts):
                    table.add_row([index, contact.name, contact.phone_number])
                print(table)
                contact_id = int(
                    input("Enter the ID of the contact to delete: "))
                if 0 <= contact_id < len(matching_contacts):
                    contact_to_delete = matching_contacts[contact_id]
                    self.people.remove(contact_to_delete)
                    print(f"{contact_to_delete.name} has been deleted.")
                else:
                    print("Invalid ID. No contact has been deleted.")

    def find_by_coming_birthday(self):
        def convert_str_to_date(str_date) -> datetime:
            splited = str_date.split()
            if len(splited) != 3:
                return None
            year = int(splited[0])
            day = int(splited[1])
            month = splited[2]
            month_order = list(Validator.days_count.keys())
            if month not in month_order:
                return None
            return datetime(year, month_order.index(month)+1, day)

        messages = []
        for con in self.people:
            if con.birthday is not None:
                date = convert_str_to_date(con.birthday)
                if date is not None:
                    avarage = date.day - datetime.now().day
                    if avarage == 0:
                        messages.append(
                            f"It's your contact '{con.name}' birthday today.")
                    elif avarage > 0 and avarage <= 3:
                        days_count_str = ["one day",
                                          "two days", "three days"][avarage-1]
                        messages.append(
                            f"Your contact {con.name} has a birthday in {days_count_str}.")

        for message in messages:
            print(message)

        if len(messages) == 0:
            print("None of your contacts have birthdays within three days.")

    def display_contacts(self):
        table = PrettyTable()
        table.field_names = [attr.upper() for attr in self._attributes]
        for con in self.people:
            table.add_row(con.row)
        print(table)

    def search_contact_by_name_or_phone(self):
        value_to_search = input("Enter the name or phone number to search for: ")
        self.search_contact(value_to_search, by_notes=False)


    def search_contact_by_notes(self):
        value_to_search = input("Enter the notes to search for: ")
        self.search_contact(value_to_search, by_notes=True)

    
    def search_contact(self, value_to_search, by_notes=False):
        search_term = value_to_search.strip().lower()
        results = []

        for contact in self.people:
            if by_notes and contact.notes.value and search_term in contact.notes.value.lower():
                results.append(contact)
            elif not by_notes and (search_term in contact.name.lower() or (contact.phone_number and search_term in contact.phone_number)):
                results.append(contact)

        if results:
            table = PrettyTable()
            table.field_names = [attr.upper() for attr in self._attributes]
            for contact in results:
                table.add_row(contact.row)
            if by_notes:
                print("\nSearch results by notes:")
            else:
                print("\nSearch results:")
            print(table)
        else:
            if by_notes:
                print(f"No contacts found with notes containing '{search_term}'.")
            else:
                print(f"No contacts found for '{value_to_search}'.")



    def menu(self):
        while True:
            menu_text = """Hello, it's your Personal Assistant! I can help you organize your contacts.\n
            Menu:
            1. Create a new contact
            2. Edit contact
            3. Find by coming birthday
            4. Display contacts
            5. Delete contact
            6. Search contacts by name or phone number
            7. Search contacts by notes
            0. Exit
            Choose a number: """
            ans = input(menu_text)
            if ans == "1":
                self.create()
                print('Contact has been created.')
            elif ans == "2":
                edit_success = self.edit()
                print("Changes have been saved") if edit_success else print(
                    'Contact not found. Please try again.')
            elif ans == "3":
                self.find_by_coming_birthday()
            elif ans == "4":
                self.display_contacts()
            elif ans == "5":
                self.delete_contact()
            elif ans == "6":
                self.search_contact_by_name_or_phone()
            elif ans == "7":
                self.search_contact_by_notes()
            else:
                return

if __name__ == "__main__":
    h = UserInterface()
    h.menu()
