"""
Exercise 3: Files and JSON
==========================
Practice: reading/writing files, JSON serialization

Instructions:
- Complete each function where you see TODO
- Run this file to test your solutions
- All tests should print "PASSED"

Run with: python exercise_3_files_json.py
"""

import json
import os


# =============================================================================
# EXERCISE 3.1: Writing to a File
# =============================================================================
"""
Create a function that writes a list of lines to a text file.

Parameters:
    filepath (str): Path to the file to create
    lines (list): List of strings to write (one per line)

The function should:
- Create/overwrite the file
- Write each line followed by a newline character
- Use UTF-8 encoding

Example:
    write_lines("output.txt", ["Hello", "World"])
    # Creates file with:
    # Hello
    # World
"""

def write_lines(filepath: str, lines: list) -> None:
    # TODO: Implement this function
    with open(filepath, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")


# =============================================================================
# EXERCISE 3.2: Reading from a File
# =============================================================================
"""
Create a function that reads a text file and returns its lines.

Parameters:
    filepath (str): Path to the file to read

Returns:
    list: List of lines (with whitespace/newlines stripped)

Example:
    # If file contains:
    # Hello
    # World
    read_lines("output.txt") -> ["Hello", "World"]
"""

def read_lines(filepath: str) -> list:
    # TODO: Implement this function
    # Hint: Use strip() on each line to remove newlines
    lines = []
    with open(filepath, "r", encoding = "utf-8") as f:
        for line in f:
            lines.append(line.strip())
        return lines




# =============================================================================
# EXERCISE 3.3: Appending to a File
# =============================================================================
"""
Create a function that appends a single line to an existing file.

Parameters:
    filepath (str): Path to the file
    line (str): Line to append

The function should add the line at the end of the file with a newline.
If the file doesn't exist, it should be created.

Example:
    append_line("log.txt", "Entry 1")
    append_line("log.txt", "Entry 2")
    # File now contains:
    # Entry 1
    # Entry 2
"""

def append_line(filepath: str, line: str) -> None:
    # TODO: Implement this function
    # Hint: Use "a" mode for append
    with open(filepath, "a", encoding = "utf-8") as f:
        f.write(line+"\n")


# =============================================================================
# EXERCISE 3.4: Count Words in a File
# =============================================================================
"""
Create a function that counts words in a text file.

Parameters:
    filepath (str): Path to the file

Returns:
    int: Total number of words in the file

A word is any sequence of characters separated by whitespace.

Example:
    # If file contains "Hello World\nThis is Python"
    count_words("file.txt") -> 5
"""

def count_words(filepath: str) -> int:
    # TODO: Implement this function
    # Hint: Read the file, split on whitespace, count the parts
    ctr = 0
    with open(filepath, "r", encoding = "utf-8") as f:
        for line in f:
            lst = line.split()
            ctr+=len(lst)
    return ctr



# =============================================================================
# EXERCISE 3.5: Write Dictionary to JSON File
# =============================================================================
"""
Create a function that saves a dictionary to a JSON file.

Parameters:
    filepath (str): Path to the JSON file
    data (dict): Dictionary to save

The function should write formatted JSON (indented with 2 spaces).

Example:
    save_json("data.json", {"name": "Alice", "age": 30})
    # Creates file with:
    # {
    #   "name": "Alice",
    #   "age": 30
    # }
"""

def save_json(filepath: str, data: dict) -> None:
    # TODO: Implement this function
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)



# =============================================================================
# EXERCISE 3.6: Load Dictionary from JSON File
# =============================================================================
"""
Create a function that loads a dictionary from a JSON file.

Parameters:
    filepath (str): Path to the JSON file

Returns:
    dict: The loaded dictionary

Example:
    data = load_json("data.json")
    data["name"] -> "Alice"
"""

def load_json(filepath: str) -> dict:
    # TODO: Implement this function
    with open(filepath, "r", encoding = "utf-8") as f:
        text = f.read()
        my_dict = json.loads(text)
    return my_dict

# =============================================================================
# EXERCISE 3.7: Update JSON File
# =============================================================================
"""
Create a function that updates specific keys in a JSON file.

Parameters:
    filepath (str): Path to the JSON file
    **updates: Key-value pairs to update

The function should:
1. Load the existing JSON data
2. Update it with the provided key-value pairs
3. Save it back to the file

Example:
    # If file contains {"name": "Alice", "age": 30}
    update_json("data.json", age=31, city="NYC")
    # File now contains {"name": "Alice", "age": 31, "city": "NYC"}
"""

def update_json(filepath: str, **updates) -> None:
    # TODO: Implement this function
    with open(filepath, "r", encoding = "utf-8") as f:
        text = f.read()
        my_dict = json.loads(text)


    for key, value in updates.items():
        my_dict[key] = value

    with open(filepath, "w", encoding = "utf-8") as f:
        json.dump(my_dict, f, indent=2)



# =============================================================================
# EXERCISE 3.8: Todo List Manager
# =============================================================================
"""
Create a TodoList class that persists to a JSON file.

The class should:
- Load existing todos from file on initialization (or start empty if file doesn't exist)
- Save to file after every modification

Attributes:
    filepath (str): Path to the JSON file
    todos (list): List of todo dictionaries

Each todo is a dict: {"id": int, "task": str, "done": bool}

Methods:
    add(task: str) -> int: Add a new todo, return its id
    complete(todo_id: int) -> bool: Mark todo as done, return True if found
    get_pending() -> list: Return list of todos where done=False
    get_all() -> list: Return all todos

Example:
    todo_list = TodoList("todos.json")
    id1 = todo_list.add("Buy groceries")  # Returns 1
    id2 = todo_list.add("Walk the dog")   # Returns 2
    todo_list.complete(1)                  # Returns True
    todo_list.get_pending()                # Returns [{"id": 2, "task": "Walk the dog", "done": False}]
"""

class TodoList:
    def __init__(self, filepath: str):
        self.filepath = filepath
        # TODO: Load existing todos from file, or initialize empty list
        # Hint: Use try/except to handle file not existing
        self.todos = []
        try:
            with open(filepath, "r", encoding = "utf-8") as f:
                self.todos = json.load(f)
        except FileNotFoundError:
            print("File doesn't exist")


    def _save(self) -> None:
        """Helper method to save todos to file."""
        # TODO: Save self.todos to self.filepath as JSON
        with open(self.filepath, "w", encoding = "utf-8") as f:
            json.dump(self.todos, f)

    def _next_id(self) -> int:
        """Helper method to get the next available ID."""
        # TODO: Return max id + 1, or 1 if no todos exist
        highest_id =-1
        for i in self.todos:
            if i["id"]>highest_id:
                highest_id = i["id"]
        if self.todos:
            return highest_id+1
        return 1


    def add(self, task: str) -> int:
        # TODO: Create new todo, add to list, save, return id
        #Each todo is a dict: {"id": int, "task": str, "done": bool}
        new_id = self._next_id()
        new_task = {
            "id": new_id,
            "task": task,
            "done": False
        }
        self.todos.append(new_task)
        self._save()
        return new_id

    def complete(self, todo_id: int) -> bool:
        # TODO: Find todo by id, set done=True, save, return True
        # Return False if not found
        for i in self.todos:
            if i["id"]==todo_id:
                i["done"] = True
                self._save()
                return True
            else:
                return False


    def get_pending(self) -> list:
        # TODO: Return todos where done=False
        #for key,value in self.todos:
        lst = []
        for i in self.todos:
            if not i["done"]:
                lst.append(i)
        return lst

    def get_all(self) -> list:
        # TODO: Return all todos
        return self.todos


