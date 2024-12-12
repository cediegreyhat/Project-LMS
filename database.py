import sqlite3
from contextlib import closing
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.conn = None
        self.connect()
        self.create_tables()

    def connect(self):
        """Establish a connection to the database."""
        if not self.conn:
            self.conn = sqlite3.connect(self.db_path)

    def create_tables(self):
        """Create necessary tables."""
        with closing(self.conn.cursor()) as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tools (
                    tool_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    condition TEXT DEFAULT 'Good',
                    quantity INTEGER NOT NULL,
                    location TEXT,
                    status TEXT DEFAULT 'available',
                    borrower TEXT,
                    borrow_date TEXT 
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    name TEXT,
                    age INTEGER,
                    email TEXT
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    progress INTEGER,
                    working_hours INTEGER
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Transactions (
                    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    tool_id INTEGER,
                    borrow_date TEXT DEFAULT CURRENT_TIMESTAMP,
                    return_date TEXT,
                    FOREIGN KEY(tool_id) REFERENCES Tools(tool_id)
                );
            """)
            self.conn.commit()



    def check_and_add_default_data(self):
        """Add default data to the database."""
        with closing(self.conn.cursor()) as cursor:
            cursor.execute("SELECT COUNT(*) FROM users")
            if cursor.fetchone()[0] == 0:
                print("No users found. Adding default users.")
                cursor.executemany('INSERT INTO users (username, password, name, age, email) VALUES (?, ?, ?, ?, ?)', [
                    ('admin', 'adminpass', 'Admin', 30, 'admin@example.com'),
                ])
                self.conn.commit()

            cursor.execute("SELECT COUNT(*) FROM tools")
            if cursor.fetchone()[0] == 0:
                print("No tools found. Adding default tools.")
                cursor.executemany('INSERT INTO tools (name, category, condition, quantity, location) VALUES (?, ?, ?, ?, ?)', [
                    ('Hammer', 'Hand Tools', 'Good', 10, 'Storage A'),
                    ('Screwdriver', 'Hand Tools', 'Good', 15, 'Storage B'),
                    ('Wrench', 'Hand Tools', 'Good', 5, 'Storage C')
                ])
                self.conn.commit()

    def _execute_query(self, query, params=None, fetch=False):
        """Helper method to execute SQL queries."""
        with closing(self.conn.cursor()) as cursor:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            if fetch:
                return cursor.fetchall()
            self.conn.commit()

    def fetch_all_tools(self):
        """Fetch all tools."""
        return self._execute_query("SELECT * FROM tools", fetch=True)

    def fetch_tool_by_name(self, name):
        query = "SELECT * FROM tools WHERE name=?"
        with closing(self.conn.cursor()) as cursor:  # Using context manager for cursor
            cursor.execute(query, (name,))
            return cursor.fetchone()

    
    def update_tool_quantity(self, name, new_quantity):
        self.cursor.execute("UPDATE tools SET quantity=? WHERE name=?", (new_quantity, name))
        self.conn.commit()

    def borrow_tool(self, tool_id, borrower_name, borrow_date):
    # Decrement quantity and update status, borrower, and borrow date
        query = """
        UPDATE tools
        SET 
            quantity = quantity - 1,
            status = CASE WHEN quantity = 1 THEN 'borrowed' ELSE status END,
            borrower = ?,
            borrow_date = ? 
        WHERE tool_id = ? AND quantity > 0
    """
        with closing(self.conn.cursor()) as cursor:  # Using context manager for cursor
            cursor.execute(query, (borrower_name, borrow_date, tool_id)) 
        self.conn.commit()



        
    def get_tools(self):
        # Correct the query to use tool_id instead of id
        query = "SELECT tool_id, name, status FROM tools" 
        with closing(self.conn.cursor()) as cursor:  # Using context manager for cursor
            cursor.execute(query)
            return cursor.fetchall()




    def return_tool(self, tool_id):
        # Clear borrower and set status to 'available'
        query = "UPDATE tools SET status = 'available', borrower = NULL WHERE tool_id = ?"
        with closing(self.conn.cursor()) as cursor:  # Using context manager for cursor
            cursor.execute(query, (tool_id,))
            self.conn.commit()




    def search_tool(self, tool_name):
        """Search for a tool by name."""
        return self._execute_query('SELECT * FROM tools WHERE name LIKE ?', ('%' + tool_name + '%',), fetch=True)
    
    def insert_tool(self, tool_name, tool_category, tool_condition, tool_quantity, tool_location):
        try:
            query = '''INSERT INTO tools (name, category, condition, quantity, location, status) 
                    VALUES (?, ?, ?, ?, ?, ?)'''
            with closing(self.conn.cursor()) as cursor:  # Using context manager for cursor
                cursor.execute(query, (tool_name, tool_category, tool_condition, tool_quantity, tool_location, 'available'))
                self.conn.commit()
                return True
        except Exception as e:
            print(f"Error inserting tool: {e}")
        return False


    def add_tool(self, name, category, condition, quantity, location):
        """Add a new tool to the database."""
        self._execute_query("INSERT INTO tools (name, category, condition, quantity, location) VALUES (?, ?, ?, ?, ?)", 
                            [name, category, condition, quantity, location])

    def delete_tool(self, tool_id):
        """Delete a tool from the database."""
        self._execute_query("DELETE FROM tools WHERE tool_id = ?", [tool_id])

    def update_tool(self, tool_id, name=None, category=None, condition=None, quantity=None, location=None):
        """Update tool details in the database."""
        query = "UPDATE tools SET "
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
        query = query.rstrip(", ") + " WHERE tool_id = ?"
        params.append(tool_id)

        with closing(self.conn.cursor()) as cursor:  # Using context manager for cursor
            cursor.execute(query, params)
            self.conn.commit()


    def insert_user(self, username, password, name, age, email):
        """Insert a new user into the database."""
        try:
            self._execute_query('INSERT INTO users (username, password, name, age, email) VALUES (?, ?, ?, ?, ?)',
                                [username, password, name, age, email])
            return True
        except sqlite3.IntegrityError:
            return False
        except ValueError:
            return None

    def get_user(self, username, password):
        """Retrieve a user from the database."""
        return self._execute_query('SELECT * FROM users WHERE username = ? AND password = ?', [username, password], fetch=True)

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()

# Initialize the DatabaseManager for both databases
user_db = DatabaseManager('db/users.db')
inventory_db = DatabaseManager('db/inventory.db')

# Initialize databases and check for tables/data
user_db.check_and_add_default_data()
inventory_db.check_and_add_default_data()

# Example of interacting with the database (fetch all tools)
tools = inventory_db.fetch_all_tools()
print(tools)

# Close the connections
user_db.close()
inventory_db.close()
