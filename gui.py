import os
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from tkinter import messagebox
from tkinter import simpledialog
from PIL import Image
from matplotlib.figure import Figure
from database import DatabaseManager
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Set global configurations
ctk.set_appearance_mode("dark")  # Dark mode
ctk.set_default_color_theme("dark-blue")


class LoginApp:
    def __init__(self, db_path):
        print("Initializing LoginApp...")
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.db = DatabaseManager(self.db_path)  
        print("Creating login window...")
        self.create_login_window()

    def create_login_window(self):
        print("Creating login window...")
        self.login_window = ctk.CTk()
        self.login_window.geometry('500x400')
        self.login_window.title('Login to Project-LMS')
        self.login_window.resizable(False, False) 

        # Background image
        bg_image_path = "assets/background_image.jpg"
        bg_image = Image.open(bg_image_path)
        self.bg_image = ctk.CTkImage(light_image=None, dark_image=bg_image, size=(1280, 720))
        bg_label = ctk.CTkLabel(self.login_window, image=self.bg_image)
        bg_label.place(relwidth=1, relheight=1)

        # Main frame for login
        login_frame = ctk.CTkFrame(self.login_window, corner_radius=10, fg_color="#2b2b2b")  # A simple styled frame
        login_frame.pack(pady=50, padx=50, fill='both', expand=True)

        # Title label
        title_label = ctk.CTkLabel(login_frame, text="Login", font=('Roboto', 24, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

        # Username Entry
        self.username_label = ctk.CTkLabel(login_frame, text='Username', font=('Roboto', 14))
        self.username_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.username_entry = ctk.CTkEntry(login_frame, font=('Roboto', 14), width=250, placeholder_text="Enter username")
        self.username_entry.grid(row=1, column=1, pady=10)
        self.username_entry.bind("<Return>", lambda event: self.password_entry.focus())

        # Password Entry
        self.password_label = ctk.CTkLabel(login_frame, text='Password', font=('Roboto', 14))
        self.password_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.password_entry = ctk.CTkEntry(login_frame, show='*', font=('Roboto', 14), width=250, placeholder_text="Enter password")
        self.password_entry.grid(row=2, column=1, pady=10)
        self.password_entry.bind("<Return>", lambda event: self.login())

        # Error label
        self.error_label = ctk.CTkLabel(login_frame, text="", font=('Roboto', 12), text_color="red")
        self.error_label.grid(row=3, column=0, columnspan=2, pady=10)

        # Login Button
        self.login_button = ctk.CTkButton(login_frame, text='Login', font=('Roboto', 16), command=self.login, width=200)
        self.login_button.grid(row=4, column=0, columnspan=2, pady=20)
        print("Entering Tkinter event loop...")
        self.login_window.mainloop()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            self.error_label.configure(text="Please fill in both fields")
            return

        user = self.db.get_user(username, password)

        if user:
            self.login_window.destroy()
            ToolManagementApp(user, self.db)  # Pass the db instance to ToolManagementApp
        else:
            self.error_label.configure(text="Incorrect username or password.")

    def signup(self):
        username = self.signup_username_entry.get()
        password = self.signup_password_entry.get()
        name = self.signup_name_entry.get()
        age = self.signup_age_entry.get()
        email = self.signup_email_entry.get()

        if self.db.insert_user(username, password, name, age, email):
            messagebox.showinfo('Sign Up Successful', 'You can now login.')
            self.signup_window.destroy()
            self.create_login_window()  # Go back to login window
        else:
            messagebox.showerror('Sign Up Failed', 'Username already exists or invalid data.')


class ToolManagementApp:
    def __init__(self, user, db):
        self.user = user
        self.db = db
        self.create_dashboard_window()

    def create_dashboard_window(self):
        # Main Window
        self.window = ctk.CTk()
        self.window.geometry('1280x720')
        self.window.title('Learner Management System')

        # Sidebar
        sidebar = ctk.CTkFrame(self.window, width=250, fg_color="#2b2b2b", corner_radius=0)
        sidebar.pack(side="left", fill="y")

        # Profile Section
        profile_image_path = "assets/user.png"
        profile_image = Image.open(profile_image_path).resize((180, 180))
        self.profile_image_ctk = ctk.CTkImage(light_image=None, dark_image=profile_image)

        profile_label = ctk.CTkLabel(sidebar, image=self.profile_image_ctk, text="")
        profile_label.pack(pady=(30, 20))
        
        # Sidebar Buttons
        self.borrow_button = ctk.CTkButton(sidebar, text="Borrow Tool", command=self.borrow_tool)
        self.borrow_button.pack(pady=10, padx=20, fill="x")

        self.add_tool_button = ctk.CTkButton(sidebar, text="Add Tool", command=self.add_tool)
        self.add_tool_button.pack(pady=10, padx=20, fill="x")

        self.view_tools_button = ctk.CTkButton(sidebar, text="View Tools", command=self.view_tools)
        self.view_tools_button.pack(pady=10, padx=20, fill="x")

        self.delete_tool_button = ctk.CTkButton(sidebar, text="Delete Tool", command=self.delete_tool)
        self.delete_tool_button.pack(pady=10, padx=20, fill="x")

        self.return_tool_button = ctk.CTkButton(sidebar, text="Return Tool", command=self.return_tool)
        self.return_tool_button.pack(pady=10, padx=20, fill="x")

        self.logout_button = ctk.CTkButton(sidebar, text="Logout", fg_color="#d9534f", command=self.logout)
        self.logout_button.pack(side="bottom", pady=20, padx=20, fill="x")

        # Main Dashboard Area
        dashboard_frame = ctk.CTkFrame(self.window, fg_color="#f9f9f9")
        dashboard_frame.pack(side="right", fill="both", expand=True)

        # Inventory Table Section
        inventory_label = ctk.CTkLabel(dashboard_frame, text="Inventory Overview", font=("Roboto", 20))
        inventory_label.pack(pady=(20, 10))

        self.inventory_table = ttk.Treeview(dashboard_frame, columns=("ID", "Name", "Category", "Condition", "Quantity"), show="headings")
        self.inventory_table.pack(pady=10, padx=20, fill="both", expand=True)

        for col in self.inventory_table["columns"]:
            self.inventory_table.heading(col, text=col)
            self.inventory_table.column(col, width=150)  # Adjust width for better visibility

        self.update_inventory_table()

        # Pie Chart Section
        pie_chart_label = ctk.CTkLabel(dashboard_frame, text="Tool Categories Distribution", font=("Roboto", 20))
        pie_chart_label.pack(pady=(20, 10))

        # Initialize pie chart canvas only once here
        self.pie_chart_canvas = ctk.CTkFrame(dashboard_frame)
        self.pie_chart_canvas.pack(pady=10, padx=20, fill="both", expand=True)

        self.update_pie_chart()
        self.window.mainloop()

    def update_inventory_table(self):
        # Clear existing data
        for row in self.inventory_table.get_children():
            self.inventory_table.delete(row)

        # Fetch and insert new data
        tools = self.db.fetch_all_tools()
        for tool in tools:
            self.inventory_table.insert("", "end", values=(tool[0], tool[1], tool[2], tool[3], tool[4]))

        # Update the pie chart after the inventory table is updated
        self.update_pie_chart()

    def update_pie_chart(self):
        if hasattr(self, 'pie_chart_canvas') and self.pie_chart_canvas:
            for widget in self.pie_chart_canvas.winfo_children():
                widget.destroy()

            tools = self.db.fetch_all_tools()  # Fetch tools from the database
            categories = {}

            # Collect categories and their counts
            for tool in tools:
                category = tool[2]
                categories[category] = categories.get(category, 0) + 1

            # Create Pie chart
            fig = Figure(figsize=(4, 3), dpi=100)
            ax = fig.add_subplot(111)
            ax.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%', startangle=90)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            # Embed the pie chart in Tkinter window
            chart_canvas = FigureCanvasTkAgg(fig, self.pie_chart_canvas)
            chart_canvas.draw()
            chart_canvas.get_tk_widget().pack(fill="both", expand=True)

    def borrow_tool(self):
        tool_name = simpledialog.askstring("Borrow Tool", "Enter tool name:")
        if tool_name:
            tool = self.db.fetch_tool_by_name(tool_name)
            if tool:
                if tool[4] > 0:  # Check if tool is available
                    self.db.update_tool_quantity(tool_name, tool[4] - 1)  # Decrease the quantity
                    messagebox.showinfo("Success", f"Successfully borrowed {tool_name}.")
                    self.update_inventory_table()
                else:
                    messagebox.showerror("Error", f"{tool_name} is out of stock.")
            else:
                messagebox.showerror("Error", "Tool not found.")
            
    def delete_tool(self):
        selected_item = self.inventory_table.selection()
        
        if not selected_item:
            messagebox.showwarning("No Tool Selected", "Please select a tool to delete.")
            return
        
        # Get the tool name from the selected row
        selected_tool = self.inventory_table.item(selected_item, 'values')
        tool_id = selected_tool[0]  # Assuming 'ID' is the first column in the treeview

        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the tool '{selected_tool[1]}'?")
        
        if confirm:
            self.db.delete_tool(tool_id)  # Delete the tool from the database
            messagebox.showinfo("Tool Deleted", f"'{selected_tool[1]}' has been deleted from the inventory.")
            self.update_inventory_table()  # Update the table after deletion
            self.update_pie_chart()  # Update the pie chart
            
    def view_tools(self):
        """Display the tools in the inventory."""
        self.update_inventory_table()
        messagebox.showinfo("View Tools", "Tools have been displayed in the table.")

    def return_tool(self):
        try:
            # Get all tools from the database
            tools = self.db.get_tools()
            borrowed_tools = [tool for tool in tools if tool[2] == 'borrowed']

            # Check if there are any borrowed tools to return
            if not borrowed_tools:
                messagebox.showwarning("No Borrowed Tools", "You have no tools to return.")
                return

            # Extract the names of the borrowed tools
            tool_names = [tool[1] for tool in borrowed_tools]
            
            # Ask the user for the tool they want to return
            tool_name = simpledialog.askstring(
                "Return Tool", 
                f"Borrowed tools: \n{', '.join(tool_names)}\n\nEnter the tool name you want to return:"
            )

            # Validate the tool name entered by the user
            if tool_name and tool_name in tool_names:
                # Get the tool ID based on the name entered
                tool_id = borrowed_tools[tool_names.index(tool_name)][0]
                
                # Debugging: Print the tool_id to ensure it's correct
                print(f"Selected tool_id: {tool_id}")  # Add this line for debugging
                
                # Return the tool by updating the database
                self.db.return_tool(tool_id)
                
                # Notify the user that the tool has been returned successfully
                messagebox.showinfo("Tool Returned", f"'{tool_name}' has been returned.")
                
                # Update the inventory table and pie chart
                self.update_inventory_table()
                self.update_pie_chart()
            else:
                messagebox.showerror("Invalid Tool", "The selected tool is not valid for return.")
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while returning the tool: {e}")
            



    def search_tool(self):
        tool_name = simpledialog.askstring("Search Tool", "Enter the name of the tool you want to search:")

        if tool_name:
            tools = self.db.search_tool(tool_name)
            if tools:
                tool_list = '\n'.join([f"{tool[1]}: {tool[2]}" for tool in tools])
                messagebox.showinfo("Search Results", f"Found tools: \n{tool_list}")
            else:
                messagebox.showinfo("Search Results", "No tools found.")
                
    def add_tool(self):
        # Create a Toplevel window for the add tool popup
        add_tool_window = ctk.CTkToplevel(self.window)
        add_tool_window.geometry("400x400")  # Adjusted height to accommodate location field
        add_tool_window.title("Add New Tool")
        add_tool_window.attributes('-topmost', True)  # Keep the window always on top
        
        # Create a frame for the add tool form
        add_tool_frame = ctk.CTkFrame(add_tool_window)
        add_tool_frame.pack(pady=20, padx=20, fill='both', expand=True)

        # Tool Name
        name_label = ctk.CTkLabel(add_tool_frame, text="Tool Name", font=('Roboto', 14))
        name_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        name_entry = ctk.CTkEntry(add_tool_frame, font=('Roboto', 14), width=250, placeholder_text="Enter tool name")
        name_entry.grid(row=0, column=1, pady=10)

        # Tool Category
        category_label = ctk.CTkLabel(add_tool_frame, text="Category", font=('Roboto', 14))
        category_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        category_entry = ctk.CTkEntry(add_tool_frame, font=('Roboto', 14), width=250, placeholder_text="Enter tool category")
        category_entry.grid(row=1, column=1, pady=10)

        # Tool Condition
        condition_label = ctk.CTkLabel(add_tool_frame, text="Condition", font=('Roboto', 14))
        condition_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        condition_entry = ctk.CTkEntry(add_tool_frame, font=('Roboto', 14), width=250, placeholder_text="Enter tool condition")
        condition_entry.grid(row=2, column=1, pady=10)

        # Tool Quantity
        quantity_label = ctk.CTkLabel(add_tool_frame, text="Quantity", font=('Roboto', 14))
        quantity_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        quantity_entry = ctk.CTkEntry(add_tool_frame, font=('Roboto', 14), width=250, placeholder_text="Enter tool quantity")
        quantity_entry.grid(row=3, column=1, pady=10)

        # Tool Location
        location_label = ctk.CTkLabel(add_tool_frame, text="Location", font=('Roboto', 14))
        location_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")
        location_entry = ctk.CTkEntry(add_tool_frame, font=('Roboto', 14), width=250, placeholder_text="Enter tool location")
        location_entry.grid(row=4, column=1, pady=10)

        # Add Tool Button
        def save_tool():
            tool_name = name_entry.get()
            tool_category = category_entry.get()
            tool_condition = condition_entry.get()
            tool_quantity = quantity_entry.get()
            tool_location = location_entry.get()

            # Perform validation
            if not tool_name or not tool_category or not tool_condition or not tool_quantity or not tool_location:
                messagebox.showerror("Error", "Please fill in all fields.")
                return

            if not tool_quantity.isdigit():
                messagebox.showerror("Error", "Quantity must be a number.")
                return

            # Insert tool into the database
            if self.db.insert_tool(tool_name, tool_category, tool_condition, int(tool_quantity), tool_location):
                messagebox.showinfo("Success", f"{tool_name} added successfully.")
                add_tool_window.destroy()  # Close the popup
                self.update_inventory_table()  # Update the inventory table
            else:
                messagebox.showerror("Error", "Failed to add tool. Please try again.")

        # Save Button
        save_button = ctk.CTkButton(add_tool_frame, text="Save", command=save_tool)
        save_button.grid(row=5, column=0, columnspan=2, pady=20)

        # Close Button
        close_button = ctk.CTkButton(add_tool_window, text="Close", command=add_tool_window.destroy)
        close_button.pack(side="bottom", pady=10)

        # Keyboard controls to move between fields and trigger the save function on 'Enter' key press
        name_entry.bind("<Return>", lambda event: category_entry.focus_set())
        category_entry.bind("<Return>", lambda event: condition_entry.focus_set())
        condition_entry.bind("<Return>", lambda event: quantity_entry.focus_set())
        quantity_entry.bind("<Return>", lambda event: location_entry.focus_set())
        location_entry.bind("<Return>", lambda event: save_button.invoke())  # Trigger save when Enter is pressed in location field


    def logout(self):
        self.window.destroy()
        LoginApp(self.db_path)


if __name__ == '__main__':
    db_path = './db/inventory.db'
    LoginApp(db_path)
