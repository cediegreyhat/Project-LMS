import sqlite3
from contextlib import closing
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()

    def connect(self):
        """Establish or reconnect to the database."""
        try:
            if not self.conn or self.conn.closed:
                self.conn = sqlite3.connect(self.db_path)
                self.cursor = self.conn.cursor()
                logger.info(f"Connected to database: {self.db_path}")
        except sqlite3.Error as e:
            logger.error(f"Failed to connect to database: {e}")
            raise

    def create_tables(self):
        """Create necessary tables if they don't exist."""
        table_queries = [
            """CREATE TABLE IF NOT EXISTS tools (
                tool_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                condition TEXT DEFAULT 'Good',
                quantity INTEGER NOT NULL,
                location TEXT,
                status TEXT DEFAULT 'available',
                borrower TEXT,
                borrow_date TEXT,
                user_id INTEGER,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );""",
            """CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                name TEXT,
                age INTEGER,
                email TEXT
            );""",
            """CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                progress INTEGER,
                working_hours INTEGER
            );""",
            """CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                tool_id INTEGER,
                user_id INTEGER,
                transaction_type TEXT NOT NULL,
                transaction_date TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(tool_id) REFERENCES tools(tool_id),
                FOREIGN KEY(user_id) REFERENCES users(id)
            );"""
        ]
        try:
            with closing(self.conn.cursor()) as cursor:
                for query in table_queries:
                    cursor.execute(query)
                self.conn.commit()
                logger.info("Tables created or already exist.")
        except sqlite3.Error as e:
            logger.error(f"Failed to create tables: {e}")
            raise

    def _execute_query(self, query, params=None, fetch=False):
        """Helper function to execute queries with error handling."""
        try:
            with closing(self.conn.cursor()) as cursor:
                cursor.execute(query, params or [])
                if fetch:
                    return cursor.fetchall()
                self.conn.commit()
        except sqlite3.IntegrityError as e:
            logger.error(f"Integrity error in query: {query}\n{e}")
            raise
        except Exception as e:
            logger.error(f"Error in executing query: {query}\n{e}")
            raise

    def ensure_connection_open(self):
        """Ensure the connection is open."""
        if self.conn is None:
            self.connect()
        try:
            # Check if the connection is still alive
            self.conn.cursor().execute('SELECT 1')
        except sqlite3.ProgrammingError:
            # If cursor cannot be executed, the connection is closed, so we reconnect
            self.connect()

    def delete_tool(self, tool_id):
        """Delete a tool from the database."""
        self.ensure_connection_open()
        try:
            with closing(self.conn.cursor()) as cursor:
                cursor.execute("DELETE FROM tools WHERE tool_id = ?", (tool_id,))
                if cursor.rowcount == 0:
                    raise ValueError(f"Tool with ID {tool_id} does not exist.")
                self.conn.commit()
                logger.info(f"Tool with ID {tool_id} deleted.")
        except Exception as e:
            logger.error(f"Error deleting tool with ID {tool_id}: {e}")
            self.conn.rollback()
            raise

    def fetch_all_tools(self):
        """Fetch all tools."""
        return self._execute_query("SELECT * FROM tools", fetch=True)

    def fetch_tool_by_name(self, name):
        """Fetch a tool by its name."""
        return self._execute_query("SELECT * FROM tools WHERE name=?", (name,), fetch=True)

    def fetch_tools_by_status(self, status, user_id=None):
        """Fetch tools by status (e.g., 'available', 'borrowed')."""
        query = "SELECT tool_id, name, status FROM tools WHERE status = ?"
        params = [status]

        if user_id:
            query += " AND user_id = ?"
            params.append(user_id)

        return self._execute_query(query, tuple(params), fetch=True)

    def update_tool_quantity(self, tool_id, new_quantity):
        """Update the quantity of a tool."""
        query = "UPDATE tools SET quantity=? WHERE tool_id=?"
        self._execute_query(query, (new_quantity, tool_id))

    def borrow_tool(self, tool_id, user_id, borrower_name, borrow_date):
        """Borrow a tool."""
        self.ensure_connection_open()
        try:
            with closing(self.conn.cursor()) as cursor:
                tool_update_query = """
                    UPDATE tools SET 
                        quantity = quantity - 1,
                        status = CASE WHEN quantity - 1 = 0 THEN 'unavailable' ELSE 'available' END,
                        user_id = ?, borrower = ?, borrow_date = ? 
                    WHERE tool_id = ? AND quantity > 0
                """
                cursor.execute(tool_update_query, (user_id, borrower_name, borrow_date, tool_id))
                if cursor.rowcount == 0:
                    raise ValueError("Tool is unavailable or quantity is insufficient.")

                transaction_query = """
                    INSERT INTO transactions (tool_id, user_id, transaction_type, transaction_date)
                    VALUES (?, ?, 'borrow', ?)
                """
                cursor.execute(transaction_query, (tool_id, user_id, borrow_date))
                self.conn.commit()
        except Exception as e:
            logger.error(f"Error in borrow_tool: {e}")
            self.conn.rollback()
            raise

    def return_tool(self, tool_id, user_id, return_date):
        """Return a borrowed tool."""
        self.ensure_connection_open()
        try:
            with closing(self.conn.cursor()) as cursor:
                cursor.execute("""UPDATE tools SET status = 'available', borrower = NULL, borrow_date = NULL, user_id = NULL
                                  WHERE tool_id = ? AND borrower IS NOT NULL""", (tool_id,))
                cursor.execute("""
                    INSERT INTO transactions (tool_id, user_id, transaction_type, transaction_date)
                    VALUES (?, ?, 'return', ?)
                """, (tool_id, user_id, return_date))
                self.conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Error in return_tool: {e}")
            self.conn.rollback()
            return False

    def insert_tool(self, name, category, condition, quantity, location):
        """Insert a new tool into the database."""
        query = '''INSERT INTO tools (name, category, condition, quantity, location, status) 
                   VALUES (?, ?, ?, ?, ?, ?)'''
        try:
            self._execute_query(query, (name, category, condition, quantity, location, 'available'))
            logger.info(f"Inserted tool: {name}")
            return True
        except Exception as e:
            logger.error(f"Error inserting tool: {e}")
            return False

    def insert_user(self, username, password, name, age, email):
        """Insert a new user into the database."""
        try:
            self._execute_query('INSERT INTO users (username, password, name, age, email) VALUES (?, ?, ?, ?, ?)',
                                (username, password, name, age, email))
            logger.info(f"Inserted user: {username}")
            return True
        except sqlite3.IntegrityError as e:
            logger.error(f"Error inserting user: {e}")
            return False
        except Exception as e:
            logger.error(f"Error inserting user: {e}")
            return None

    def get_user(self, username, password):
        """Get user by username and password."""
        return self._execute_query('SELECT * FROM users WHERE username = ? AND password = ?',
                                   (username, password), fetch=True)

    def close(self):
        """Close the database connection.""" 
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed.")

# Example usage
if __name__ == "__main__":
    user_db = DatabaseManager('db/users.db')
    inventory_db = DatabaseManager('db/inventory.db')

    user_db.check_and_add_default_data()
    inventory_db.check_and_add_default_data()

    tools = inventory_db.fetch_all_tools()
    logger.info(f"Tools fetched: {tools}")

    user_db.close()
    inventory_db.close()
