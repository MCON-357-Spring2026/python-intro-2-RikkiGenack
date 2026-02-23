"""
Exercise 4: Mini-Project - Library Management System
=====================================================
Combine everything: functions, classes, files, and JSON

This exercise brings together all the concepts from the course.
Build a simple library system that tracks books and borrowers.

Instructions:
- Complete all TODOs
- The system should persist data to JSON files
- Run this file to test your implementation

Run with: python exercise_4_project.py
"""

import json
import os
from datetime import datetime

from exercises.src.files import save_json


# =============================================================================
# PART 1: HELPER FUNCTIONS
# =============================================================================

def format_date(dt: datetime = None) -> str:
    """
    Format a datetime object as a string "YYYY-MM-DD".
    If no datetime provided, use current date.

    Example:
        format_date(datetime(2024, 1, 15)) -> "2024-01-15"
        format_date() -> "2024-02-04" (today's date)
    """
    # TODO: Implement this function
    if dt:
        return str(dt)
    return str(datetime.now())



def generate_id(prefix: str, existing_ids: list) -> str:
    """
    Generate a new unique ID with the given prefix.

    Parameters:
        prefix: String prefix (e.g., "BOOK", "USER")
        existing_ids: List of existing IDs to avoid duplicates

    Returns:
        New ID in format "{prefix}_{number:04d}"

    Example:
        generate_id("BOOK", ["BOOK_0001", "BOOK_0002"]) -> "BOOK_0003"
        generate_id("USER", []) -> "USER_0001"
    """
    # TODO: Implement this function
    # Hint: Find the highest existing number and add 1
    highest_num =0
    for id in existing_ids:
        if id > highest_num:
            highest_num = id
    return prefix + str(highest_num+1)




def search_items(items: list, **criteria) -> list:
    """
    Search a list of dictionaries by matching criteria.
    Uses **kwargs to accept any search fields.

    Parameters:
        items: List of dictionaries to search
        **criteria: Field-value pairs to match (case-insensitive for strings)

    Returns:
        List of matching items

    Example:
        books = [
            {"title": "Python 101", "author": "Smith"},
            {"title": "Java Guide", "author": "Smith"},
            {"title": "Python Advanced", "author": "Jones"}
        ]
        search_items(books, author="Smith") -> [first two books]
        search_items(books, title="Python 101") -> [first book]
    """
    # TODO: Implement this function
    # Hint: For each item, check if ALL criteria match
    lst = []

    for item in items:
        match =True
        for k, v in criteria.items():
            if k not in item:
                match = False
                break
            if isinstance(item[k], str) and isinstance(v, str):
                if not item[k].lower() == v.lower():
                    match = False
            elif item[k] != v:
                match = False
        if match:
            lst.append(item)
    return lst



# =============================================================================
# PART 2: BOOK CLASS
# =============================================================================

class Book:
    """
    Represents a book in the library.

    Class Attributes:
        GENRES: List of valid genres ["Fiction", "Non-Fiction", "Science", "History", "Technology"]

    Instance Attributes:
        book_id (str): Unique identifier
        title (str): Book title
        author (str): Author name
        genre (str): Must be one of GENRES
        available (bool): Whether book is available for borrowing

    Methods:
        to_dict(): Convert to dictionary for JSON serialization
        from_dict(data): Class method to create Book from dictionary
        __str__(): Return readable string representation
    """

    GENRES = ["Fiction", "Non-Fiction", "Science", "History", "Technology"]

    def __init__(self, book_id: str, title: str, author: str, genre: str, available: bool = True):
        # TODO: Initialize attributes
        self.book_id = book_id
        self.title=title
        self.author= author
        self.available= available
        # TODO: Validate that genre is in GENRES, raise ValueError if not
        if genre in Book.GENRES:
            self.genre= genre
        raise  ValueError


    def to_dict(self) -> dict:
        # TODO: Return dictionary with all attributes
        return {self.book_id: self.title, "author": self.author, "genre": self.genre}

    @classmethod
    def from_dict(cls, data: dict) -> "Book":
        # TODO: Create and return a Book instance from dictionary
        return cls.__init__(data["book_id"], data["title"], data["author"], data["genre"])

    def __str__(self) -> str:
        # TODO: Return string like "[BOOK_0001] Python 101 by Smith (Technology) - Available"
        return f'[{self.book_id} {self.title} by {self.author} ({self.genre}) - {self.available}]'


# =============================================================================
# PART 3: BORROWER CLASS
# =============================================================================

class Borrower:
    """
    Represents a library member who can borrow books.

    Instance Attributes:
        borrower_id (str): Unique identifier
        name (str): Borrower's name
        email (str): Borrower's email
        borrowed_books (list): List of book_ids currently borrowed

    Methods:
        borrow_book(book_id): Add book to borrowed list
        return_book(book_id): Remove book from borrowed list
        to_dict(): Convert to dictionary
        from_dict(data): Class method to create Borrower from dictionary
    """

    MAX_BOOKS = 3  # Maximum books a borrower can have at once

    def __init__(self, borrower_id: str, name: str, email: str, borrowed_books: list = None):
        # TODO: Initialize attributes (use empty list if borrowed_books is None)
        self.borrower_id=borrower_id
        self.name=name
        self.email=email
        self.borrowed_books=borrowed_books

    def can_borrow(self) -> bool:
        """Check if borrower can borrow more books."""
        # TODO: Return True if len(borrowed_books) < MAX_BOOKS
        if len(self.borrowed_books) < Borrower.MAX_BOOKS:
            return True
        return False

    def borrow_book(self, book_id: str) -> bool:
        """Add book to borrowed list. Return False if at max limit."""
        # TODO: Implement this method
        if Borrower.can_borrow(self):
            self.borrowed_books.append(book_id)
        else:
            return False

    def return_book(self, book_id: str) -> bool:
        """Remove book from borrowed list. Return False if not found."""
        # TODO: Implement this method
        if book_id not in self.borrowed_books:
            return False
        else:
            self.borrowed_books.remove(book_id)

    def to_dict(self) -> dict:
        # TODO: Return dictionary with all attributes
        return {self.borrower_id: self.name, "email" : self.email, "borrowed" : self.borrowed_books}

    @classmethod
    def from_dict(cls, data: dict) -> "Borrower":
        # TODO: Create and return a Borrower instance from dictionary
        return cls.__init__(data["borrower_id"], data["name"], data["email"])


# =============================================================================
# PART 4: LIBRARY CLASS (Main System)
# =============================================================================

class Library:
    """
    Main library system that manages books and borrowers.
    Persists data to JSON files.

    Attributes:
        name (str): Library name
        books (dict): book_id -> Book
        borrowers (dict): borrower_id -> Borrower
        books_file (str): Path to books JSON file
        borrowers_file (str): Path to borrowers JSON file

    Methods:
        add_book(title, author, genre) -> Book: Add a new book
        add_borrower(name, email) -> Borrower: Add a new borrower
        checkout_book(book_id, borrower_id) -> bool: Borrower checks out a book
        return_book(book_id, borrower_id) -> bool: Borrower returns a book
        search_books(**criteria) -> list: Search books by criteria
        get_available_books() -> list: Get all available books
        get_borrower_books(borrower_id) -> list: Get books borrowed by a borrower
        save(): Save all data to JSON files
        load(): Load data from JSON files
    """

    def __init__(self, name: str, data_dir: str = "."):
        self.name = name
        self.books = {}
        self.borrowers = {}
        self.books_file = os.path.join(data_dir, "library_books.json")
        self.borrowers_file = os.path.join(data_dir, "library_borrowers.json")
        # TODO: Call self.load() to load existing data
        self.load()

    def load(self) -> None:
        """Load books and borrowers from JSON files."""
        # TODO: Load books from self.books_file

        # TODO: Load borrowers from self.borrowers_file
        # Hint: Use try/except to handle files not existing
        try:
            json.load(open(self.books_file))
            json.load(open(self.borrowers_file))
        except FileNotFoundError:
            print("File not found")

    def save(self) -> None:
        """Save books and borrowers to JSON files."""
        # TODO: Save self.books to self.books_file
        # TODO: Save self.borrowers to self.borrowers_file
        # Hint: Convert Book/Borrower objects to dicts using to_dict()
        self.books_file.write(json.dumps(self.books))

        self.borrowers_file.write(json.dumps(self.borrowers))

    def add_book(self, title: str, author: str, genre: str) -> Book:
        """Add a new book to the library."""
        # TODO: Generate new book_id using generate_id
        # TODO: Create Book, add to self.books, save, and return
        my_id=generate_id("BOOK", existing_ids=None)
        newBook = Book(my_id, self.title, self.author, self.genre)
        self.books[my_id] = newBook
        self.books.save()
        return newBook

    def add_borrower(self, name: str, email: str) -> Borrower:
        """Register a new borrower."""
        # TODO: Generate new borrower_id, create Borrower, add to self.borrowers, save, return
        my_id = generate_id("BORROWER", existing_ids=None)
        newBorrower = Borrower(self.name, email)
        self.borrowers[my_id] = newBorrower
        self.borrowers.save()
        return newBorrower

    def checkout_book(self, book_id: str, borrower_id: str) -> bool:
        """
        Borrower checks out a book.
        Returns False if book unavailable, borrower not found, or at max limit.
        """
        # TODO: Validate book exists and is available
        # TODO: Validate borrower exists and can borrow
        # TODO: Update book.available, borrower.borrowed_books
        # TODO: Save and return True
        #if book_id in books:
        pass

    def return_book(self, book_id: str, borrower_id: str) -> bool:
        """
        Borrower returns a book.
        Returns False if book/borrower not found or book wasn't borrowed by this person.
        """
        # TODO: Validate book and borrower exist
        # TODO: Validate book is in borrower's borrowed_books
        # TODO: Update book.available, remove from borrowed_books
        # TODO: Save and return True
        pass

    def search_books(self, **criteria) -> list:
        """Search books by any criteria (title, author, genre, available)."""
        # TODO: Use search_items helper function
        # Hint: Convert self.books.values() to list of dicts first
        pass

    def get_available_books(self) -> list:
        """Get list of all available books."""
        # TODO: Return books where available=True
        pass

    def get_borrower_books(self, borrower_id: str) -> list:
        """Get list of books currently borrowed by a borrower."""
        # TODO: Get borrower, return list of Book objects for their borrowed_books
        pass

    def get_statistics(self) -> dict:
        """
        Return library statistics.
        Uses the concepts of dict comprehension and aggregation.
        """
        # TODO: Return dict with:
        # - total_books: total number of books
        # - available_books: number of available books
        # - checked_out: number of checked out books
        # - total_borrowers: number of borrowers
        # - books_by_genre: dict of genre -> count
        pass


