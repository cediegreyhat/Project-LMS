#Function to initialize Communication to DB
import sqlite3
from contextlib import closing
from datetime import datetime

class DatabaseManager:
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

    # -------- Tool Management Methods --------

    def add_tool(self, name, category, condition, quantity, location):
        """
        Adds a new tool to the database.
        """
        query = """
        INSERT INTO Tools (name, category, condition, quantity, location)
        VALUES (?, ?, ?, ?, ?);
        """
        self._execute_query(query, [name, category, condition, quantity, location])
        print(f"Tool '{name}' added successfully.")

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
        if quantity is not None:  # Allow updating quantity to 0
            query += "quantity = ?, "
            params.append(quantity)
        if location:
            query += "location = ?, "
            params.append(location)
        
        # Remove the trailing comma and space
        query = query.rstrip(", ") + " WHERE tool_id = ?;"
        params.append(tool_id)
        
        self._execute_query(query, params)
        print(f"Tool with ID {tool_id} updated successfully.")

    def delete_tool(self, tool_id):
        """
        Deletes a tool from the database.
        """
        query = "DELETE FROM Tools WHERE tool_id = ?;"
        self._execute_query(query, [tool_id])
        print(f"Tool with ID {tool_id} deleted successfully.")

    # -------- Transaction Management Methods --------

    def borrow_tool(self, user_id, tool_id):
        """
        Logs a borrow transaction and reduces tool quantity.
        """
        # Check tool availability
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
        # Reduce tool quantity
        self.update_tool(tool_id, quantity=tool[0][0] - 1)
        print(f"Tool with ID {tool_id} borrowed successfully by User {user_id}.")

    def return_tool(self, user_id, tool_id):
        """
        Logs a return transaction and increases tool quantity.
        """
        # Check if the user has borrowed the tool
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
        # Increase tool quantity
        tool = self._execute_query("SELECT quantity FROM Tools WHERE tool_id = ?", [tool_id], fetch=True)
        self.update_tool(tool_id, quantity=tool[0][0] + 1)
        print(f"Tool with ID {tool_id} returned successfully by User {user_id}.")

    # -------- Search Methods --------

    def search_tools(self, keyword):
        """
        Searches for tools by name or category.
        """
        query = """
        SELECT * FROM Tools 
        WHERE name LIKE ? OR category LIKE ?;
        """
        return self._execute_query(query, [f"%{keyword}%", f"%{keyword}%"], fetch=True)

    # -------- Utility Methods --------

    def clear_tables(self):
        """
        Clears all data from the tables.
        """
        self._execute_query("DELETE FROM Tools;")
        self._execute_query("DELETE FROM Transactions;")
        print("All tables cleared.")

# Example Usage
if __name__ == "__main__":
    db = DatabaseManager()
    db.add_tool("Hammer", "Hand Tool", "Good", 5, "Storage A")
    db.add_tool("Drill", "Power Tool", "Good", 3, "Storage B")
    print("Tools in inventory:")
    for tool in db.get_all_tools():
        print(tool)
    db.borrow_tool(1, 1)  # User 1 borrows Tool 1
    db.return_tool(1, 1)  # User 1 returns Tool 1
    print("Search results for 'Drill':")
    for tool in db.search_tools("Drill"):
        print(tool)