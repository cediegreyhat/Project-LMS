import tkinter as tk
from tkinter import ttk, messagebox
from database import DatabaseManager  # Import the DatabaseManager class


# Main App
class ToolManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tool Management System")
        self.root.geometry("800x600")

        # Center the window
        self.center_window(800, 600)

        # Initialize the DatabaseManager
        self.db_manager = DatabaseManager()

        # Initialize user role
        self.user_role = None

        # Create Frames
        self.create_login_frame()

    # Center Window
    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    # Login Screen
    def create_login_frame(self):
        self.clear_frame()

        tk.Label(self.root, text="Tool Management System", font=("Arial", 18)).pack(pady=20)
        tk.Label(self.root, text="Select Role:", font=("Arial", 14)).pack(pady=10)

        tk.Button(self.root, text="Admin", font=("Arial", 12), command=lambda: self.switch_role("Admin")).pack(pady=5)
        tk.Button(self.root, text="Regular User", font=("Arial", 12), command=lambda: self.switch_role("User")).pack(
            pady=5)

    def switch_role(self, role):
        self.user_role = role
        if role == "Admin":
            self.create_admin_frame()
        elif role == "User":
            self.create_user_frame()

    # Admin Dashboard
    def create_admin_frame(self):
        self.clear_frame()
        tk.Label(self.root, text="Admin Dashboard", font=("Arial", 18)).pack(pady=20)

        tk.Button(self.root, text="Add Tool", command=self.add_tool_window).pack(pady=5)
        tk.Button(self.root, text="Edit/Delete Tools", command=self.edit_tool_window).pack(pady=5)
        tk.Button(self.root, text="View Inventory", command=self.view_inventory_window).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.create_login_frame).pack(pady=20)

    # Regular User Dashboard
    def create_user_frame(self):
        self.clear_frame()
        tk.Label(self.root, text="User Dashboard", font=("Arial", 18)).pack(pady=20)

        tk.Button(self.root, text="Borrow Tools", command=self.borrow_tool_window).pack(pady=5)
        tk.Button(self.root, text="Return Tools", command=self.return_tool_window).pack(pady=5)
        tk.Button(self.root, text="View Inventory", command=self.view_inventory_window).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.create_login_frame).pack(pady=20)

    # Add Tool Window
    def add_tool_window(self):
        top = tk.Toplevel(self.root)
        top.title("Add Tool")

        tk.Label(top, text="Tool Name:").grid(row=0, column=0, padx=10, pady=5)
        tool_name = tk.Entry(top)
        tool_name.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(top, text="Category:").grid(row=1, column=0, padx=10, pady=5)
        category = tk.Entry(top)
        category.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(top, text="Condition:").grid(row=2, column=0, padx=10, pady=5)
        condition = tk.Entry(top)
        condition.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(top, text="Quantity:").grid(row=3, column=0, padx=10, pady=5)
        quantity = tk.Entry(top)
        quantity.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(top, text="Location:").grid(row=4, column=0, padx=10, pady=5)
        location = tk.Entry(top)
        location.grid(row=4, column=1, padx=10, pady=5)

        def save_tool():
            name = tool_name.get()
            cat = category.get()
            cond = condition.get()
            qty = int(quantity.get())
            loc = location.get()

            self.db_manager.add_tool(name, cat, cond, qty, loc)  # Add tool to the database
            messagebox.showinfo("Success", f"Tool '{name}' added successfully!")
            top.destroy()

        tk.Button(top, text="Add Tool", command=save_tool).grid(row=5, column=0, columnspan=2, pady=10)

    # Edit/Delete Tool Window
    def edit_tool_window(self):
        top = tk.Toplevel(self.root)
        top.title("Edit/Delete Tools")
        tk.Label(top, text="Feature Coming Soon!").pack(pady=20)

    # View Inventory Window
    def view_inventory_window(self):
        top = tk.Toplevel(self.root)
        top.title("Inventory")
        tk.Label(top, text="Inventory List").pack(pady=10)

        tree = ttk.Treeview(top, columns=("ID", "Name", "Category", "Condition", "Quantity", "Location"),
                            show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Category", text="Category")
        tree.heading("Condition", text="Condition")
        tree.heading("Quantity", text="Quantity")
        tree.heading("Location", text="Location")
        tree.pack(fill=tk.BOTH, expand=True)

        # Fetch tools from the database
        tools = self.db_manager.get_all_tools()
        for tool in tools:
            tree.insert("", tk.END, values=tool)

    # Borrow Tool Window
    def borrow_tool_window(self):
        top = tk.Toplevel(self.root)
        top.title("Borrow Tools")
        tk.Label(top, text="Feature Coming Soon!").pack(pady=20)

    # Return Tool Window
    def return_tool_window(self):
        top = tk.Toplevel(self.root)
        top.title("Return Tools")
        tk.Label(top, text="Feature Coming Soon!").pack(pady=20)

    # Clear Frame
    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# Run the App
if __name__ == "__main__":
    root = tk.Tk()
    app = ToolManagementApp(root)
    root.mainloop()
