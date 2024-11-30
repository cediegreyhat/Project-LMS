#Backend to mga Idol!
from database import DatabaseManager

def main_menu():
    print("\n=== Tool Management System ===")
    print("1. Add Tool")
    print("2. View All Tools")
    print("3. Update Tool")
    print("4. Delete Tool")
    print("5. Borrow Tool")
    print("6. Return Tool")
    print("7. Search Tools")
    print("8. Clear All Data (Admin Only)")
    print("9. Exit")

def get_valid_int(prompt, allow_blank=False):
    while True:
        value = input(prompt).strip()
        if allow_blank and not value:
            return None
        if value.isdigit():
            return int(value)
        print("Invalid input. Please enter a valid integer.")

def get_valid_str(prompt, allow_blank=False):
    while True:
        value = input(prompt).strip()
        if allow_blank or value:
            return value
        print("Invalid input. Please enter a non-empty string.")

def handle_add_tool(db):
    name = get_valid_str("Enter tool name: ")
    category = get_valid_str("Enter tool category: ")
    condition = get_valid_str("Enter tool condition (Good/Fair/Poor): ").capitalize()
    while condition not in ["Good", "Fair", "Poor"]:
        print("Invalid condition. Please enter 'Good', 'Fair', or 'Poor'.")
        condition = get_valid_str("Enter tool condition (Good/Fair/Poor): ").capitalize()
    quantity = get_valid_int("Enter quantity: ")
    location = get_valid_str("Enter location: ")
    db.add_tool(name, category, condition, quantity, location)

def handle_view_tools(db):
    tools = db.get_all_tools()
    if not tools:
        print("No tools found in the inventory.")
    else:
        for tool in tools:
            print(f"Tool ID: {tool[0]}, Name: {tool[1]}, Category: {tool[2]}, Condition: {tool[3]}, Quantity: {tool[4]}, Location: {tool[5]}")

def handle_update_tool(db):
    tool_id = get_valid_int("Enter the Tool ID to update: ")
    print("Leave fields blank to skip updating them.")
    name = get_valid_str("New tool name: ", allow_blank=True)
    category = get_valid_str("New tool category: ", allow_blank=True)
    condition = get_valid_str("New tool condition (Good/Fair/Poor): ", allow_blank=True).capitalize()
    if condition and condition not in ["Good", "Fair", "Poor"]:
        print("Invalid condition. Skipping update.")
        condition = None
    quantity = get_valid_int("New quantity: ", allow_blank=True)
    location = get_valid_str("New location: ", allow_blank=True)
    db.update_tool(tool_id, name, category, condition, quantity, location)

def handle_delete_tool(db):
    tool_id = get_valid_int("Enter the Tool ID to delete: ")
    db.delete_tool(tool_id)

def handle_borrow_tool(db):
    user_id = get_valid_int("Enter User ID: ")
    tool_id = get_valid_int("Enter Tool ID to borrow: ")
    db.borrow_tool(user_id, tool_id)

def handle_return_tool(db):
    user_id = get_valid_int("Enter User ID: ")
    tool_id = get_valid_int("Enter Tool ID to return: ")
    db.return_tool(user_id, tool_id)

def handle_search_tools(db):
    keyword = get_valid_str("Enter search keyword (tool name or category): ")
    results = db.search_tools(keyword)
    if not results:
        print("No tools found matching the search criteria.")
    else:
        for tool in results:
            print(f"Tool ID: {tool[0]}, Name: {tool[1]}, Category: {tool[2]}, Condition: {tool[3]}, Quantity: {tool[4]}, Location: {tool[5]}")

def handle_clear_data(db):
    confirmation = input("Are you sure you want to clear all data? Type 'YES' to confirm: ")
    if confirmation.upper() == "YES":
        db.clear_tables()
        print("All data cleared successfully.")
    else:
        print("Operation cancelled.")

if __name__ == "__main__":
    db = DatabaseManager()
    while True:
        main_menu()
        choice = input("Enter your choice: ").strip()
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
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
