import sqlite3
from contextlib import closing
from datetime import datetime


class DatabaseManager:
    def __init__(self, db_name="inventory.db"):
    def __init__(self, db_name="db/inventory.db"):
        
        self.db_name = db_name
        self._initialize_database()

    def _execute_query(self, query, params=None, fetch=False):
        """
        Utility method to execute SQL queries safely.
        """
        params = params or []
        with sqlite3.connect(self.db_name) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute(query, params)
                conn.commit()
                if fetch:
                    return cursor.fetchall()

    def _initialize_database(self):
        """
        Initializes the database and required tables.
        """
        tool_table = """
        CREATE TABLE IF NOT EXISTS Tools (
            tool_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            condition TEXT DEFAULT 'Good',
            quantity INTEGER NOT NULL,
            location TEXT
        );
        """
        transaction_table = """
        CREATE TABLE IF NOT EXISTS Transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            tool_id INTEGER,
            borrow_date TEXT DEFAULT CURRENT_TIMESTAMP,
            return_date TEXT,
            FOREIGN KEY(tool_id) REFERENCES Tools(tool_id)
        );
        """
        self._execute_query(tool_table)
        self._execute_query(transaction_table)

    def add_tool(self, name, category, condition, quantity, location):
        """
        Adds a new tool to the database.
        """
        query = """
        INSERT INTO Tools (name, category, condition, quantity, location)
        VALUES (?, ?, ?, ?, ?);
        """
        self._execute_query(query, [name, category, condition, quantity, location])

    def get_all_tools(self):
        """
        Retrieves all tools from the database.
        """
        query = "SELECT * FROM Tools;"
        return self._execute_query(query, fetch=True)

    def update_tool(self, tool_id, name=None, category=None, condition=None, quantity=None, location=None):
        """
        Updates tool details in the database.
        """
        query = "UPDATE Tools SET "
        params = []
        if name:
            query += "name = ?, "
            params.append(name)
        if category:
            query += "category = ?, "
            params.append(category)
        if condition:
            query += "condition = ?, "
            params.append(condition)
        if quantity is not None:
            query += "quantity = ?, "
            params.append(quantity)
        if location:
            query += "location = ?, "
            params.append(location)

        # Remove the trailing comma and space
        query = query.rstrip(", ") + " WHERE tool_id = ?;"
        params.append(tool_id)

        self._execute_query(query, params)

    def borrow_tool(self, user_id, tool_id):
        """
        Logs a borrow transaction and reduces tool quantity.
        """
        tool = self._execute_query("SELECT quantity FROM Tools WHERE tool_id = ?", [tool_id], fetch=True)
        if not tool or tool[0][0] <= 0:
            print("Error: Tool is not available for borrowing.")
            return

        # Borrow the tool
        query = """
        INSERT INTO Transactions (user_id, tool_id)
        VALUES (?, ?);
        """
        self._execute_query(query, [user_id, tool_id])
        self.update_tool(tool_id, quantity=tool[0][0] - 1)

    def return_tool(self, user_id, tool_id):
        """
        Logs a return transaction and increases tool quantity.
        """
        query = """
        SELECT transaction_id FROM Transactions 
        WHERE user_id = ? AND tool_id = ? AND return_date IS NULL;
        """
        transaction = self._execute_query(query, [user_id, tool_id], fetch=True)
        if not transaction:
            print("Error: No active borrow transaction found for this user and tool.")
            return

        # Return the tool
        update_query = """
        UPDATE Transactions SET return_date = ? 
        WHERE transaction_id = ?;
        """
        self._execute_query(update_query, [datetime.now().strftime('%Y-%m-%d %H:%M:%S'), transaction[0][0]])
        tool = self._execute_query("SELECT quantity FROM Tools WHERE tool_id = ?", [tool_id], fetch=True)
        self.update_tool(tool_id, quantity=tool[0][0] + 1)

    def search_tools(self, keyword):
        """
        Searches for tools by name or category.
        """
        query = """
        SELECT * FROM Tools 
        WHERE name LIKE ? OR category LIKE ?;
        """
        return self._execute_query(query, [f"%{keyword}%", f"%{keyword}%"], fetch=True)

    def insert_user(self, username, password, name, age, email):
        """Insert a new user into the database."""
        conn = sqlite3.connect('user_db.db')
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO users (username, password, name, age, email) VALUES (?, ?, ?, ?, ?)',
                (username, password, name, int(age), email)
            )
            conn.commit()
            return True  # Successful insertion
        except sqlite3.IntegrityError:
            return False  # Username already exists
        except ValueError:
            return None  # Invalid age value
        finally:
            conn.close()

    def get_user(self, username, password):
        """Retrieve a user from the database based on username and password."""
        conn = sqlite3.connect('user_db.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()
        return user

    def init_user_database(self):
        """Initialize the user database and create the users table if it doesn't exist."""
        conn = sqlite3.connect('user_db.db')
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                email TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()
