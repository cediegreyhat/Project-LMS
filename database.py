import sqlite3
from contextlib import closing
from datetime import datetime
import bcrypt

class DatabaseManager:
    def __init__(self, db_name="inventory.db"):
        self.db_name = db_name
        self.logged_in_user = None
        self._initialize_database()

    def _execute_query(self, query, params=None, fetch=False):
        params = params or []
        with sqlite3.connect(self.db_name) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute(query, params)
                conn.commit()
                if fetch:
                    return cursor.fetchall()

    def _initialize_database(self):
        self._execute_query("""
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );""")
        self._execute_query("""
        CREATE TABLE IF NOT EXISTS Tools (
            tool_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            condition TEXT DEFAULT 'Good',
            quantity INTEGER NOT NULL,
            location TEXT
        );""")
        self._execute_query("""
        CREATE TABLE IF NOT EXISTS Transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            tool_id INTEGER,
            borrow_date TEXT DEFAULT CURRENT_TIMESTAMP,
            return_date TEXT,
            FOREIGN KEY(tool_id) REFERENCES Tools(tool_id),
            FOREIGN KEY(user_id) REFERENCES Users(user_id)
        );""")

    def create_user(self, username, password):
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        try:
            self._execute_query("INSERT INTO Users (username, password) VALUES (?, ?);", [username, hashed_password])
        except sqlite3.IntegrityError:
            print(f"Username '{username}' already exists.")

    def login(self, username, password):
        user = self._execute_query("SELECT * FROM Users WHERE username = ?;", [username], fetch=True)
        if user and bcrypt.checkpw(password.encode(), user[0][2].encode()):
            self.logged_in_user = {"user_id": user[0][0], "username": user[0][1]}
            return self.logged_in_user
        print("Invalid username or password.")
        return None

    def logout(self):
        if self.logged_in_user:
            self.logged_in_user = None
        else:
            print("No user is currently logged in.")

    def get_logged_in_user(self):
        return self.logged_in_user

    def add_tool(self, name, category, condition, quantity, location):
        self._execute_query("""
        INSERT INTO Tools (name, category, condition, quantity, location)
        VALUES (?, ?, ?, ?, ?);""", [name, category, condition, quantity, location])

    def get_all_tools(self):
        return self._execute_query("SELECT * FROM Tools;", fetch=True)

    def update_tool(self, tool_id, name=None, category=None, condition=None, quantity=None, location=None):
        query = "UPDATE Tools SET "
        params = []
        if name: query += "name = ?, "; params.append(name)
        if category: query += "category = ?, "; params.append(category)
        if condition: query += "condition = ?, "; params.append(condition)
        if quantity is not None: query += "quantity = ?, "; params.append(quantity)
        if location: query += "location = ?, "; params.append(location)
        query = query.rstrip(", ") + " WHERE tool_id = ?;"
        params.append(tool_id)
        self._execute_query(query, params)

    def delete_tool(self, tool_id):
        self._execute_query("DELETE FROM Tools WHERE tool_id = ?;", [tool_id])

    def borrow_tool(self, tool_id):
        if not self.logged_in_user:
            print("Please log in to borrow tools.")
            return
        tool = self._execute_query("SELECT quantity FROM Tools WHERE tool_id = ?", [tool_id], fetch=True)
        if not tool or tool[0][0] <= 0:
            print("Tool not available.")
            return
        self._execute_query("INSERT INTO Transactions (user_id, tool_id) VALUES (?, ?);",
                            [self.logged_in_user["user_id"], tool_id])
        self.update_tool(tool_id, quantity=tool[0][0] - 1)

    def return_tool(self, tool_id):
        if not self.logged_in_user:
            print("Please log in to return tools.")
            return
        transaction = self._execute_query("""
        SELECT transaction_id FROM Transactions 
        WHERE user_id = ? AND tool_id = ? AND return_date IS NULL;""",
                                          [self.logged_in_user["user_id"], tool_id], fetch=True)
        if not transaction:
            print("No active borrow transaction found.")
            return
        self._execute_query("""
        UPDATE Transactions SET return_date = ? 
        WHERE transaction_id = ?;""", [datetime.now().strftime('%Y-%m-%d %H:%M:%S'), transaction[0][0]])
        tool = self._execute_query("SELECT quantity FROM Tools WHERE tool_id = ?", [tool_id], fetch=True)
        self.update_tool(tool_id, quantity=tool[0][0] + 1)

    def search_tools(self, keyword):
        return self._execute_query("""
        SELECT * FROM Tools WHERE name LIKE ? OR category LIKE ?;""",
                                   [f"%{keyword}%", f"%{keyword}%"], fetch=True)

    def clear_tables(self):
        self._execute_query("DELETE FROM Tools;")
        self._execute_query("DELETE FROM Transactions;")

if __name__ == "__main__":
    db = DatabaseManager()
    db.create_user("admin", "admin123")
    db.login("admin", "admin123")
    db.add_tool("Hammer", "Hand Tool", "Good", 5, "Storage A")
    db.add_tool("Drill", "Power Tool", "Good", 3, "Storage B")
    print("Tools in inventory:", db.get_all_tools())
    db.borrow_tool(1)
    db.return_tool(1)
    print("Search results for 'Drill':", db.search_tools("Drill"))
    db.logout()
