from database import DatabaseManager
from colorama import Fore, Style, init
import traceback

# Initialize colorama
init(autoreset=True)

# ASCII Art Banner
def print_banner():
    banner = '''
     ____  ____   __     __  ____  ___  ____      __    _  _  ____ 
    (  _ \(  _ \ /  \  _(  )(  __)/ __)(_  _)___ (  )  ( \/ )/ ___)
     ) __/ )   /(  O )/ \) \ ) _)( (__   )( (___)/ (_/\/ \/ \\___ \
    (__)  (__\_) \__/ \____/(____)\___) (__)     \____/\_)(_/(____/
    '''
    print(Fore.YELLOW + banner)

def main_menu():
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
    print("\n=== Tool Management System ===")
    for option in menu_options:
        print(Fore.CYAN + option)

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
                print(Fore.CYAN + f"Tool ID: {tool[0]}, Name: {tool[1]}, Category: {tool[2]}, Condition: {tool[3]}, Quantity: {tool[4]}, Location: {tool[5]}")
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
        user_id = get_valid_int("Enter User ID: ")
        tool_id = get_valid_int("Enter Tool ID to borrow: ")
        db.borrow_tool(tool_id, user_id, str(datetime.now()))
        print(Fore.GREEN + f"Tool {tool_id} borrowed successfully!" + Style.RESET_ALL)
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
        sql_command = input(Fore.YELLOW + "Enter SQL command to execute: ")
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
    
    print_banner()  # Display the welcoming banner
    
    while not account_login(db):
        pass  # Keep prompting until successful login
    
    while True:
        main_menu()
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
