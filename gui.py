import tkinter as tk
from tkinter import ttk, messagebox
from database import DatabaseManager


class ToolManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tool Management System")
        self.center_window(800, 600)

        # Initialize database manager and user role
        self.db_manager = DatabaseManager()
        self.user_role = None

        # Start with the login screen
        self.create_login_frame()

    def center_window(self, width, height):
        """Center the window on the screen."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def clear_frame(self):
        """Clear all widgets from the current frame."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_login_frame(self):
        """Create the login frame for role selection."""
        self.clear_frame()
        tk.Label(self.root, text="Tool Management System", font=("Arial", 18)).pack(pady=20)
        tk.Label(self.root, text="Select Role:", font=("Arial", 14)).pack(pady=10)

        tk.Button(self.root, text="Admin", font=("Arial", 12), command=lambda: self.switch_role("Admin")).pack(pady=5)
        tk.Button(self.root, text="Regular User", font=("Arial", 12), command=lambda: self.switch_role("User")).pack(pady=5)

    def switch_role(self, role):
        """Switch to the appropriate dashboard based on the selected role."""
        self.user_role = role
        if role == "Admin":
            self.create_admin_frame()
        elif role == "User":
            self.create_user_frame()

    def create_admin_frame(self):
        """Create the admin dashboard."""
        self.clear_frame()
        tk.Label(self.root, text="Admin Dashboard", font=("Arial", 18)).pack(pady=20)

        tk.Button(self.root, text="Add Tool", command=self.add_tool_window).pack(pady=5)
        tk.Button(self.root, text="Edit/Delete Tools", command=self.edit_tool_window).pack(pady=5)
        tk.Button(self.root, text="View Inventory", command=self.view_inventory_window).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.create_login_frame).pack(pady=20)

    def create_user_frame(self):
        """Create the user dashboard."""
        self.clear_frame()
        tk.Label(self.root, text="User Dashboard", font=("Arial", 18)).pack(pady=20)

        tk.Button(self.root, text="Borrow Tools", command=self.borrow_tool_window).pack(pady=5)
        tk.Button(self.root, text="Return Tools", command=self.return_tool_window).pack(pady=5)
        tk.Button(self.root, text="View Inventory", command=self.view_inventory_window).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.create_login_frame).pack(pady=20)

    def add_tool_window(self):
        """Create a window to add tools."""
        top = tk.Toplevel(self.root)
        top.title("Add Tool")

        labels = ["Tool Name:", "Category:", "Condition:", "Quantity:", "Location:"]
        entries = {}

        for i, label_text in enumerate(labels):
            tk.Label(top, text=label_text).grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entry = tk.Entry(top)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[label_text[:-1].lower()] = entry

        def save_tool():
            try:
                # Extract and validate inputs
                name = entries["tool name"].get().strip()
                category = entries["category"].get().strip()
                condition = entries["condition"].get().strip() or "Good"
                quantity = entries["quantity"].get().strip()
                location = entries["location"].get().strip()

                if not name or not category or not quantity:
                    raise ValueError("Tool Name, Category, and Quantity are required.")
                if not quantity.isdigit() or int(quantity) <= 0:
                    raise ValueError("Quantity must be a positive integer.")

                self.db_manager.add_tool(name, category, condition, int(quantity), location)
                messagebox.showinfo("Success", f"Tool '{name}' added successfully!")
                top.destroy()
            except ValueError as ve:
                messagebox.showerror("Input Error", str(ve))
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred: {e}")

        tk.Button(top, text="Add Tool", command=save_tool).grid(row=len(labels), column=0, columnspan=2, pady=10)

    def edit_tool_window(self):
        """Placeholder for the edit/delete tools functionality."""
        messagebox.showinfo("Coming Soon", "Edit/Delete functionality will be implemented soon.")

    def view_inventory_window(self):
        """Create a window to view all tools in the inventory."""
        top = tk.Toplevel(self.root)
        top.title("Inventory")

        tk.Label(top, text="Inventory List", font=("Arial", 14)).pack(pady=10)
        tree = ttk.Treeview(top, columns=("ID", "Name", "Category", "Condition", "Quantity", "Location"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Category", text="Category")
        tree.heading("Condition", text="Condition")
        tree.heading("Quantity", text="Quantity")
        tree.heading("Location", text="Location")
        tree.pack(fill=tk.BOTH, expand=True)

        def refresh_inventory():
            # Clear existing rows
            for row in tree.get_children():
                tree.delete(row)

            # Fetch and insert updated tools
            tools = self.db_manager.get_all_tools()
            for tool in tools:
                tree.insert("", tk.END, values=tool)

        refresh_inventory()

        tk.Button(top, text="Refresh", command=refresh_inventory).pack(pady=5)

    def borrow_tool_window(self):
        """Placeholder for the borrow tool functionality."""
        messagebox.showinfo("Coming Soon", "Borrow functionality will be implemented soon.")

    def return_tool_window(self):
        """Placeholder for the return tool functionality."""
        messagebox.showinfo("Coming Soon", "Return functionality will be implemented soon.")


if __name__ == "__main__":
    root = tk.Tk()
    app = ToolManagementApp(root)
    root.mainloop()
