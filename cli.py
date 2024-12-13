import os
import datetime
from database import DatabaseManager
from colorama import Fore, Style, init
import traceback

init(autoreset=True)

# New ASCII Art Banner for Project-LMS
def print_banner():
    banner = '''
 _____                                                                     _____ 
( ___ )                                                                   ( ___ )
 |   |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|   | 
 |   | 8""""8                                         8     8""8""8 8""""8 |   | 
 |   | 8    8 eeeee  eeeee    e  eeee eeee eeeee      8     8  8  8 8      |   | 
 |   | 8eeee8 8   8  8  88    8  8    8  8   8        8e    8e 8  8 8eeeee |   | 
 |   | 88     8eee8e 8   8    8e 8eee 8e     8e  eeee 88    88 8  8     88 |   | 
 |   | 88     88   8 8   8 e  88 88   88     88       88    88 8  8 e   88 |   | 
 |   | 88     88   8 8eee8 8ee88 88ee 88e8   88       88eee 88 8  8 8eee88 |   | 
 |___|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|___| 
(_____)                                                                   (_____)
'''
    print(Fore.CYAN + banner + Style.RESET_ALL)


def display_inventory(inventory):
    print("\nInventory List:")
    print(f"{'ID':<5}{'Name':<20}{'Category':<15}{'Condition':<10}{'Quantity':<10}{'Location':<20}{'Status':<15}{'Owner':<10}{'Date':<10}")
    print("-" * 90)
    for item in inventory:
        print(f"{item[0]:<5}{item[1]:<20}{item[2]:<15}{item[3]:<10}{item[4]:<10}{item[5]:<20}{item[6]:<15}{item[7]:<10}{item[8]:<10}")


def main_menu():
    print(Fore.GREEN + "\n=== Project-LMS[CLI] ===" + Style.RESET_ALL)
    menu_options = [
        "1. Add Tool",
        "2. View All Tools",
        "3. Update Tool",
        "4. Delete Tool",
        "5. Borrow Tool",
        "6. Return Tool",
        "7. Search Tools",
        "8. Clear All Data (Admin Only)",
        "9. Execute SQL Command (Admin Only)",
        "10. Exit"
    ]
    for option in menu_options:
        print(Fore.YELLOW + f"{option}" + Style.RESET_ALL)

def get_valid_int(prompt, allow_blank=False):
    while True:
        value = input(prompt).strip()
        if allow_blank and not value:
            return None
        if value.isdigit():
            return int(value)
        print(Fore.RED + "Invalid input. Please enter a valid integer.")

def get_valid_str(prompt, allow_blank=False):
    while True:
        value = input(prompt).strip()
        if allow_blank or value:
            return value
        print(Fore.RED + "Invalid input. Please enter a non-empty string.")



def handle_add_tool(db):
    try:
        name = get_valid_str("Enter tool name: ")
        category = get_valid_str("Enter tool category: ")
        condition = get_valid_str("Enter tool condition (Good/Fair/Poor): ").capitalize()
        while condition not in ["Good", "Fair", "Poor"]:
            print(Fore.RED + "Invalid condition. Please enter 'Good', 'Fair', or 'Poor'.")
            condition = get_valid_str("Enter tool condition (Good/Fair/Poor): ").capitalize()
        quantity = get_valid_int("Enter quantity: ")
        location = get_valid_str("Enter location: ")
        db.add_tool(name, category, condition, quantity, location)
        print(Fore.GREEN + f"Tool '{name}' added successfully!" + Style.RESET_ALL)
    except ValueError as e:
        print(Fore.RED + str(e) + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"An unexpected error occurred: {e}" + Style.RESET_ALL)

def handle_view_tools(db):
    try:
        tools = db.fetch_all_tools()
        if not tools:
            print(Fore.YELLOW + "No tools found in the inventory.")
        else:
            for tool in tools:
                tool_id = tool[0] if tool[0] is not None else 'N/A'
                name = tool[1] if tool[1] is not None else 'N/A'
                category = tool[2] if tool[2] is not None else 'N/A'
                condition = tool[3] if tool[3] is not None else 'N/A'
                quantity = tool[4] if tool[4] is not None else 'N/A'
                location = tool[5] if tool[5] is not None else 'N/A'

                print(Fore.CYAN + f"Tool ID: {tool_id}, Name: {name}, Category: {category}, Condition: {condition}, Quantity: {quantity}, Location: {location}")
    except Exception as e:
        print(Fore.RED + f"Error fetching tools: {e}" + Style.RESET_ALL)


def handle_update_tool(db):
    try:
        tool_id = get_valid_int("Enter the Tool ID to update: ")
        print("Leave fields blank to skip updating them.")
        updates = {
            "name": get_valid_str("New tool name: ", allow_blank=True),
            "category": get_valid_str("New tool category: ", allow_blank=True),
            "condition": get_valid_str("New tool condition (Good/Fair/Poor): ", allow_blank=True).capitalize(),
            "quantity": get_valid_int("New quantity: ", allow_blank=True),
            "location": get_valid_str("New location: ", allow_blank=True)
        }
        # Remove invalid updates
        updates = {k: v for k, v in updates.items() if v}
        db.update_tool(tool_id, **updates)
        print(Fore.GREEN + "Tool updated successfully!" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Error updating tool: {e}" + Style.RESET_ALL)

def handle_delete_tool(db):
    try:
        tool_id = get_valid_int("Enter the Tool ID to delete: ")
        db.delete_tool(tool_id)
        print(Fore.GREEN + f"Tool {tool_id} deleted successfully!" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Error deleting tool: {e}" + Style.RESET_ALL)

def handle_borrow_tool(db):
    try:
        # Step 1: Fetch and display available tools
        available_tools = db._execute_query(
            "SELECT tool_id, name, status FROM tools WHERE quantity > 0 AND status = 'available'",
            fetch=True
        )
        if not available_tools:
            print(Fore.YELLOW + "No tools are currently available for borrowing." + Style.RESET_ALL)
            return
        
        print("\nAvailable Tools for Borrowing:")
        print(f"{'ID':<5}{'Name':<20}{'Status':<10}")
        print("-" * 35)
        for tool in available_tools:
            print(f"{tool[0]:<5}{tool[1]:<20}{tool[2]:<10}")

        # Step 2: Prompt for user ID and tool ID
        user_id = get_valid_int("Enter your User ID: ")
        tool_id = get_valid_int("Enter the Tool ID to borrow: ")

        # Step 3: Validate selection
        selected_tool = db._execute_query(
            "SELECT tool_id, name, quantity, status FROM tools WHERE tool_id = ? AND quantity > 0 AND status = 'available'",
            [tool_id],
            fetch=True
        )
        if not selected_tool:
            print(Fore.RED + "Invalid selection. The tool is either unavailable or does not exist." + Style.RESET_ALL)
            return
        
        # Step 4: Update tool quantity and log the transaction
        db._execute_query(
            "UPDATE tools SET quantity = quantity - 1 WHERE tool_id = ?",
            [tool_id]
        )
        db._execute_query(
            "INSERT INTO transactions (tool_id, user_id, transaction_type, transaction_date) VALUES (?, ?, 'borrow', ?)",
            [tool_id, user_id, datetime.datetime.now()]
        )

        print(Fore.GREEN + f"Tool '{selected_tool[0][1]}' borrowed successfully!" + Style.RESET_ALL)

    except Exception as e:
        print(Fore.RED + f"Error borrowing tool: {e}" + Style.RESET_ALL)


def handle_return_tool(db):
    try:
        user_id = get_valid_int("Enter User ID: ")
        tool_id = get_valid_int("Enter Tool ID to return: ")
        db.return_tool(tool_id)
        print(Fore.GREEN + f"Tool {tool_id} returned successfully!" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Error returning tool: {e}" + Style.RESET_ALL)

def handle_search_tools(db):
    try:
        keyword = get_valid_str("Enter search keyword (tool name or category): ")
        results = db.search_tool(keyword)
        if not results:
            print(Fore.YELLOW + "No tools found matching the search criteria.")
        else:
            print(Fore.CYAN + "\nSearch Results:")
            for tool in results:
                print(Fore.CYAN + f"{tool[0]}\t{tool[1]}\t{tool[2]}\t{tool[3]}\t{tool[4]}\t{tool[5]}")
    except Exception as e:
        print(Fore.RED + f"Error searching for tools: {e}" + Style.RESET_ALL)

def handle_clear_data(db):
    confirmation = input(Fore.RED + "Are you sure you want to clear all data? Type 'YES' to confirm: ")
    if confirmation.upper() == "YES":
        db.clear_tables()
        print(Fore.GREEN + "All data cleared successfully." + Style.RESET_ALL)
    else:
        print(Fore.YELLOW + "Operation cancelled.")

def handle_execute_sql(db):
    try:
        sql_command = input(Fore.YELLOW + "Enter SQL command to execute: ").strip()
        if sql_command.lower().startswith("select"):
            # For SELECT queries, fetch and display results
            results = db._execute_query(sql_command, fetch=True)
            if not results:
                print(Fore.YELLOW + "No results found.")
            else:
                print(Fore.CYAN + "\nQuery Results:")
                for row in results:
                    print(Fore.CYAN + "\t".join(map(str, row)))
        else:
            # For non-SELECT queries, just execute
            db._execute_query(sql_command)
            print(Fore.GREEN + "SQL command executed successfully!" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Error executing SQL command: {e}" + Style.RESET_ALL)


def account_login(db):
    print(Fore.YELLOW + "=== Login ===")
    username = get_valid_str("Enter username: ")
    password = get_valid_str("Enter password: ")
    
    user = db.get_user(username, password)
    
    if user:
        print(Fore.GREEN + "Login successful!" + Style.RESET_ALL)
        return True
    else:
        print(Fore.RED + "Invalid username or password. Please try again." + Style.RESET_ALL)
        return False

if __name__ == "__main__":
    db = DatabaseManager('db/inventory.db')
    
    print_banner()  
    
    while not account_login(db):
        pass  # Retry login if login fails
    
    while True:
        main_menu()  # Display main menu
        choice = input(Fore.YELLOW + "Enter your choice: ").strip()
        if choice == "1":
            handle_add_tool(db)
        elif choice == "2":
            handle_view_tools(db)
        elif choice == "3":
            handle_update_tool(db)
        elif choice == "4":
            handle_delete_tool(db)
        elif choice == "5":
            handle_borrow_tool(db)
        elif choice == "6":
            handle_return_tool(db)
        elif choice == "7":
            handle_search_tools(db)
        elif choice == "8":
            handle_clear_data(db)
        elif choice == "9":
            handle_execute_sql(db)
        elif choice == "10":
            print(Fore.GREEN + "Thank you for using the Inventory Management System. Goodbye!" + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again.")
