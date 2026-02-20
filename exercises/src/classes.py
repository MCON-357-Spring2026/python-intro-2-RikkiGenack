"""
Exercise 2: Classes
===================
Practice: constructors, instance/class attributes, methods, inheritance

Instructions:
- Complete each class where you see TODO
- Run this file to test your solutions
- All tests should print "PASSED"

Run with: python exercise_2_classes.py
"""


# =============================================================================
# EXERCISE 2.1: Basic Class with Constructor
# =============================================================================
"""
Create a Product class representing an item in a store.

Attributes (instance):
    name (str): Product name
    price (float): Product price
    quantity (int): Quantity in stock (default: 0)

Methods:
    get_total_value(): Returns price * quantity
    is_in_stock(): Returns True if quantity > 0

Example:
    p = Product("Laptop", 999.99, 5)
    p.name -> "Laptop"
    p.get_total_value() -> 4999.95
    p.is_in_stock() -> True
"""

class Product:
    def __init__(self, name: str, price: float, quantity: int = 0):
        # TODO: Initialize instance attributes
        self.name=name
        self.price=price
        self.quantity=quantity

    def get_total_value(self) -> float:
        # TODO: Return price * quantity
        return self.price * self.quantity

    def is_in_stock(self) -> bool:
        # TODO: Return True if quantity > 0
        if self.quantity > 0:
            return True
        else:
            return False


# =============================================================================
# EXERCISE 2.2: Class with Class Attributes
# =============================================================================
"""
Create a BankAccount class with account tracking.

Class Attributes:
    bank_name (str): "Python Bank" (shared by all accounts)
    total_accounts (int): Counter of all accounts created (starts at 0)

Instance Attributes:
    account_number (str): Unique account number
    owner (str): Account owner name
    balance (float): Current balance (default: 0.0)

Methods:
    deposit(amount): Add amount to balance, return new balance
    withdraw(amount): Subtract amount from balance, return new balance
                     Raise ValueError if insufficient funds
    get_info(): Return formatted string with account details

The constructor should increment total_accounts each time an account is created.

Example:
    acc1 = BankAccount("A001", "Alice")
    acc1.deposit(100) -> 100.0
    acc1.withdraw(30) -> 70.0
    BankAccount.total_accounts -> 1
"""

class BankAccount:
    # TODO: Add class attributes here
    bank_name="Python Bank"
    total_accounts=0

    def __init__(self, account_number: str, owner: str, balance: float = 0.0):
        # TODO: Initialize instance attributes
        self.account_number=account_number
        self.owner=owner
        self.balance=balance
        # TODO: Increment total_accounts
        BankAccount.total_accounts+=1


    def deposit(self, amount: float) -> float:
        # TODO: Add amount to balance and return new balance
        self.balance+=amount
        return self.balance

    def withdraw(self, amount: float) -> float:
        # TODO: Subtract amount from balance
        # TODO: Raise ValueError if amount > balance
        if amount> self.balance:
            raise ValueError
        else:
            self.balance-=amount
        return self.balance



    def get_info(self) -> str:
        # TODO: Return string like "Account A001 (Alice): $100.00"
        return f'Account {self.account_number} ({self.owner}): ${self.balance:,.2f}'


# =============================================================================
# EXERCISE 2.3: Class Methods
# =============================================================================
"""
Create a Temperature class with conversion methods.

Instance Attributes:
    celsius (float): Temperature in Celsius

Class Methods (alternative constructors):
    from_fahrenheit(f): Create Temperature from Fahrenheit value
    from_kelvin(k): Create Temperature from Kelvin value

Instance Methods:
    to_fahrenheit(): Return temperature in Fahrenheit
    to_kelvin(): Return temperature in Kelvin

Conversion formulas:
    F = C * 9/5 + 32
    K = C + 273.15
    C = (F - 32) * 5/9
    C = K - 273.15

Example:
    t1 = Temperature(100)
    t1.to_fahrenheit() -> 212.0
    
    t2 = Temperature.from_fahrenheit(32)
    t2.celsius -> 0.0
"""

class Temperature:
    def __init__(self, celsius: float):
        # TODO: Initialize celsius attribute
        self.celsius=celsius

    @classmethod
    def from_fahrenheit(cls, fahrenheit: float) -> "Temperature":
        # TODO: Convert F to C and create Temperature instance
        temp = (fahrenheit-32)*5/9
        return cls(temp)

    @classmethod
    def from_kelvin(cls, kelvin: float) -> "Temperature":
        # TODO: Convert K to C and create Temperature instance
        temp2= kelvin-273.15
        return cls(temp2)

    def to_fahrenheit(self) -> float:
        # TODO: Return temperature in Fahrenheit
        return self.celsius * 9/5 + 32

    def to_kelvin(self) -> float:
        # TODO: Return temperature in Kelvin
        return self.celsius + 273.15


# =============================================================================
# EXERCISE 2.4: Inheritance
# =============================================================================
"""
Create an Employee class hierarchy.

Base Class - Employee:
    Attributes:
        name (str): Employee name
        employee_id (str): Employee ID
        base_salary (float): Base annual salary
    
    Methods:
        get_annual_salary(): Return base_salary
        get_info(): Return "ID: {employee_id} - {name}"

Child Class - Manager(Employee):
    Additional Attributes:
        department (str): Department they manage
        bonus (float): Annual bonus amount (default: 0)
    
    Override Methods:
        get_annual_salary(): Return base_salary + bonus
        get_info(): Return "ID: {employee_id} - {name} (Manager, {department})"

Child Class - Developer(Employee):
    Additional Attributes:
        programming_languages (list): List of known languages
    
    Additional Methods:
        add_language(lang): Add a language to the list
    
    Override Methods:
        get_info(): Return "ID: {employee_id} - {name} (Developer)"

Example:
    emp = Employee("Alice", "E001", 50000)
    emp.get_annual_salary() -> 50000
    
    mgr = Manager("Bob", "M001", 70000, "Engineering", 10000)
    mgr.get_annual_salary() -> 80000
    
    dev = Developer("Charlie", "D001", 60000, ["Python", "Java"])
    dev.add_language("Go")
    dev.programming_languages -> ["Python", "Java", "Go"]
"""

class Employee:
    def __init__(self, name: str, employee_id: str, base_salary: float):
        # TODO: Initialize attributes
        self.name=name
        self.employee_id=employee_id
        self.base_salary=base_salary

    def get_annual_salary(self) -> float:
        # TODO: Return base_salary
        return self.base_salary

    def get_info(self) -> str:
        # TODO: Return formatted string
        return f'Info:{self.name} Employee: {self.employee_id}'


class Manager(Employee):
    def __init__(self, name: str, employee_id: str, base_salary: float,
                 department: str, bonus: float = 0):
        # TODO: Call parent constructor with super()
        super(self.__class__, self).__init__(name, employee_id, base_salary)
        # TODO: Initialize department and bonus
        self.department=department
        self.bonus=bonus

    def get_annual_salary(self) -> float:
        # TODO: Return base_salary + bonus
        return self.base_salary + self.bonus

    def get_info(self) -> str:
        # TODO: Return formatted string with Manager info
        return f'Manager: {self.name} Department: {self.department}'


class Developer(Employee):
    def __init__(self, name: str, employee_id: str, base_salary: float,
                 programming_languages: list = None):
        # TODO: Call parent constructor with super()
        super(self.__class__, self).__init__(name, employee_id, base_salary)
        # TODO: Initialize programming_languages (use empty list if None)
        self.programming_languages=programming_languages

    def add_language(self, language: str) -> None:
        # TODO: Add language to the list
        self.programming_languages.append(language)

    def get_info(self) -> str:
        # TODO: Return formatted string with Developer info
        return f'Developer: {self.name} Languages: {self.programming_languages}'


