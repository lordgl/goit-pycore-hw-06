from collections import UserDict


class Field:
    def __init__(self):
        self._value = None

    @property
    def value(self):
        return self._value
        
    def __str__(self):
        return str(self._value) if self._value is not None else ""

class Name(Field):
    def __init__(self, name: str):
        """
        Initialize Name instance and set name value.
        Return:
            str: Message indicating that the name was set.
        """
        super().__init__()
        self.set_name(name)

    def set_name(self, name: str) -> str:
        """
        Set name value.
        Single source of truth for name setting.
        Returns:
                str: Message indicating that the name was set.
        """
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name cannot be empty")
        self._value = name
        return "Name is set"

class Phone(Field):
    def __init__(self, phone: str):
        """
        Initialize Phone instance and set phone number after validation.
        Return:
            str: Message indicating whether the phone number was set or invalid.
        """
        super().__init__()
        self.add_phone(phone)

    def add_phone(self, phone: str) -> str:
        """
        Set phone number after validation.
        Single source of truth for phone number validation.
        Returns:
            str: Message indicating whether the phone number was set or invalid.
        """
        if self._value is not None:
            return "Phone number is already set"
        else:
            self._value = phone
            return "Phone number is set"
        
    def delete_phone(self) -> str:
        """
        Delete phone number.
        Return:
            str: Message indicating that the phone number was deleted.
        """
        if self._value is None:
            return "No phone number to delete"
        else:
            self._value = None
            return "Phone number is deleted"
    

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone_number: str) -> str:
        """
        Create and store a phone if it passes validation.
        Return:
            str: Message indicating whether the phone number was set or invalid.
        """
        phone = Phone(phone_number)
        if phone.value is None:
            return "Wrong phone number"
        self.phones.append(phone)
        return "Phone number is set"

    def find_phone(self, phone_number: str):
        """
        Return the Phone instance matching the number, if any.
        Return:
            Phone or None: The found Phone instance or None if not found.
        """
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def edit_phone(self, old_number: str, new_number: str) -> str:
        """
        Replace an existing phone with a new validated value.
        Return:
            str: Message indicating whether the phone number was updated, not found, or invalid.
        """
        phone = self.find_phone(old_number)
        if phone is None or new_number == "":
            return "Phone number not found"
        phone._value = new_number
        return "Phone number is set"

    def remove_phone(self, phone_number: str) -> str:
        """
        Remove a phone number from the record.
        Return:
            str: Message indicating whether the phone number was deleted or not found.
        """
        phone = self.find_phone(phone_number)
        if phone is None:
            return "Phone number not found"
        self.phones.remove(phone)
        return "Phone number is deleted"

    def __str__(self):
        return f"Contact name: {self.name}, phones: {'; '.join(str(single_phone) for single_phone in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record: Record) -> str:
        """
        Add a new record to the address book.
        Return:    
            str: Message indicating that the record was added.
        """
        self.data[record.name.value] = record
        return "Record added"

    def find(self, name: str):
        """
        Find a record by name.
        Return:    
            Record or None: The found record or None if not found.
        """
        return self.data.get(name)

    def delete(self, name: str) -> str:
        """
        Delete a record by name.
        Return:    
            str: Message indicating whether the record was deleted or not found.
        """
        if name in self.data:
            del self.data[name]
            return "Record deleted"
        return "Record not found"
