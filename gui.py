import datetime
import os
import tkinter as tk
from tkinter import StringVar, ttk
import customtkinter as ctk
from tkinter import messagebox
from tkinter import simpledialog
from PIL import Image, ImageTk
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
        self.create_login_window()
        
    def create_login_window(self):
        print("Creating login window...")
        self.login_window = ctk.CTk()
        self.login_window.geometry('600x450')
        self.login_window.title('Login to Project-LMS')
        self.login_window.resizable(False, False)  # Disable resizing

        # Background image with a modern, sleek design
        bg_image_path = "assets/background_image.jpg"  # You can customize this
        bg_image = Image.open(bg_image_path)
        self.bg_image = ctk.CTkImage(light_image=None, dark_image=bg_image, size=(1280, 720))
        bg_label = ctk.CTkLabel(self.login_window, image=self.bg_image)
        bg_label.place(relwidth=1, relheight=1)

        # Main frame for login
        login_frame = ctk.CTkFrame(self.login_window, corner_radius=15, fg_color="#2b2b2b", width=400, height=350) 
        login_frame.place(relx=0.5, rely=0.5, anchor="center")  # Centered

        # Title label (LMS Login)
        title_label = ctk.CTkLabel(login_frame, text="Login", font=('Roboto', 28, 'bold'), text_color="white")
        title_label.grid(row=0, column=0, columnspan=2, pady=(20, 40), sticky="n")

        # Username Entry
        self.username_label = ctk.CTkLabel(login_frame, text='Username', font=('Roboto', 14), text_color="white")
        self.username_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.username_entry = ctk.CTkEntry(login_frame, font=('Roboto', 14), width=250, placeholder_text="Enter username")
        self.username_entry.grid(row=1, column=1, pady=10, sticky="w")
        self.username_entry.bind("<Return>", lambda event: self.password_entry.focus())

        # Password Entry
        self.password_label = ctk.CTkLabel(login_frame, text='Password', font=('Roboto', 14), text_color="white")
        self.password_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.password_entry = ctk.CTkEntry(login_frame, show='*', font=('Roboto', 14), width=250, placeholder_text="Enter password")
        self.password_entry.grid(row=2, column=1, pady=10, sticky="w")
        self.password_entry.bind("<Return>", lambda event: self.login())

        # Error label
        self.error_label = ctk.CTkLabel(login_frame, text="", font=('Roboto', 12), text_color="red")
        self.error_label.grid(row=3, column=0, columnspan=2, pady=10)

        # Login Button (Stylized)
        self.login_button = ctk.CTkButton(login_frame, text='Login', font=('Roboto', 16, 'bold'), command=self.login, width=250, height=40, corner_radius=10)
        self.login_button.grid(row=4, column=0, columnspan=2, pady=20)

        # Signup label (Stylized like a link)
        signup_label = ctk.CTkLabel(login_frame, text="New User? Sign Up Here", font=('Arial', 12, 'underline'), text_color="lightblue", cursor="hand2")
        signup_label.grid(row=5, column=0, columnspan=2, pady=10)
        signup_label.bind("<Button-1>", self.SignupTransition)

        # Adding subtle shadow effect
        self.login_button.configure(fg_color="lightblue", hover_color="skyblue")

        # Centering the window on the screen
        self.login_window.eval('tk::PlaceWindow %s center' % self.login_window.winfo_toplevel())

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

    def create_signup_window(self):
        print("Creating signup window...")
        self.signup_window = ctk.CTk()
        self.signup_window.geometry('500x600+200+200')  # Initial off-screen position
        self.signup_window.title('Sign Up for Project-LMS')
        
        # Main frame for signup with a custom background
        signup_frame = ctk.CTkFrame(self.signup_window, corner_radius=15, fg_color="transparent", border_width=2, border_color="#444444")
        signup_frame.grid(row=0, column=0, padx=50, pady=50, sticky="nsew")
        
        # Load Image
        bg_image_path_light = "assets/background_image_light.jpg"
        bg_image_path_dark = "assets/background_image.jpg"
        bg_image_light = Image.open(bg_image_path_light)
        bg_image_dark = Image.open(bg_image_path_dark)
        
        # Create CTkImage with size
        self.bg_image = ctk.CTkImage(light_image=bg_image_light, dark_image=bg_image_dark, size=(500, 600))
        
        # Create background label and place it at the back of the signup frame
        bg_label = ctk.CTkLabel(signup_frame, image=self.bg_image)
        bg_label.place(relwidth=1, relheight=1) 

        # Set frame grid to expand correctly
        signup_frame.grid_rowconfigure(0, weight=1)
        signup_frame.grid_columnconfigure(0, weight=1)

        # Create a label for the background image and place it at the back of the frame
        bg_label = ctk.CTkLabel(signup_frame, image=self.bg_image, width=500, height=600)
        bg_label.place(relwidth=1, relheight=1)  # Use place to fill the entire frame

        # Title label
        title_label = ctk.CTkLabel(signup_frame, text="Create an Account", font=('Roboto', 20, 'bold'), text_color="white", bg_color="transparent")
        title_label.grid(row=1, column=0, columnspan=2, pady=(10, 20), sticky="n")

        # Username Entry
        self.signup_username_label = ctk.CTkLabel(signup_frame, text='Username', font=('Roboto', 14), text_color="white", bg_color="transparent")
        self.signup_username_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.signup_username_entry = ctk.CTkEntry(signup_frame, font=('Roboto', 14), width=280, placeholder_text="Enter username")
        self.signup_username_entry.grid(row=2, column=1, pady=10, sticky="w")

        # Password Entry
        self.signup_password_label = ctk.CTkLabel(signup_frame, text='Password', font=('Roboto', 14), text_color="white", bg_color="transparent")
        self.signup_password_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.signup_password_entry = ctk.CTkEntry(signup_frame, show='*', font=('Roboto', 14), width=280, placeholder_text="Enter password")
        self.signup_password_entry.grid(row=3, column=1, pady=10, sticky="w")

        # Confirm Password Entry
        self.confirm_password_label = ctk.CTkLabel(signup_frame, text='Confirm Password', font=('Roboto', 14), text_color="white", bg_color="transparent")
        self.confirm_password_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.confirm_password_entry = ctk.CTkEntry(signup_frame, show='*', font=('Roboto', 14), width=280, placeholder_text="Confirm password")
        self.confirm_password_entry.grid(row=4, column=1, pady=10, sticky="w")

        # Name Entry
        self.signup_name_label = ctk.CTkLabel(signup_frame, text='Name', font=('Roboto', 14), text_color="white", bg_color="transparent")
        self.signup_name_label.grid(row=5, column=0, padx=10, pady=10, sticky="e")
        self.signup_name_entry = ctk.CTkEntry(signup_frame, font=('Roboto', 14), width=280, placeholder_text="Enter your name")
        self.signup_name_entry.grid(row=5, column=1, pady=10, sticky="w")
        
        # Age Entry
        self.signup_age_label = ctk.CTkLabel(signup_frame, text='Age', font=('Roboto', 14), text_color="white", bg_color="transparent")
        self.signup_age_label.grid(row=6, column=0, padx=10, pady=10, sticky="e")
        self.signup_age_entry = ctk.CTkEntry(signup_frame, font=('Roboto', 14), width=280, placeholder_text="Enter your age")
        self.signup_age_entry.grid(row=6, column=1, pady=10, sticky="w")

        # Email Entry
        self.signup_email_label = ctk.CTkLabel(signup_frame, text='Email', font=('Roboto', 14), text_color="white", bg_color="transparent")
        self.signup_email_label.grid(row=7, column=0, padx=10, pady=10, sticky="e")
        self.signup_email_entry = ctk.CTkEntry(signup_frame, font=('Roboto', 14), width=280, placeholder_text="Enter your email")
        self.signup_email_entry.grid(row=7, column=1, pady=10, sticky="w")
        
        # Error label
        self.signup_error_label = ctk.CTkLabel(signup_frame, text="", font=('Roboto', 12), text_color="red", bg_color="transparent")
        self.signup_error_label.grid(row=8, column=0, columnspan=2, pady=10)
        
        # Sign Up Button with modern styling
        self.signup_button = ctk.CTkButton(signup_frame, text='Sign Up', font=('Roboto', 16), command=self.register_user, width=240, fg_color="#4CAF50", hover_color="#45a049")
        self.signup_button.grid(row=9, column=0, columnspan=2, pady=20)
        
        # Back to Login Button with flat design and hover effect
        back_to_login_button = ctk.CTkButton(signup_frame, text="Back to Login", font=('Roboto', 14), command=self.back_to_login, width=240, fg_color="#f44336", hover_color="#e53935")
        back_to_login_button.grid(row=10, column=0, columnspan=2, pady=10)
        
        # Bind keyboard events for navigation
        self.signup_window.bind('<Tab>', self.navigate_signup_fields)
        self.signup_window.bind('<Return>', lambda event: self.register_user())

        # Slide-in signup window with smooth animation
        def slide_in():
            for i in range(self.signup_window.winfo_x(), 200, -10):
                self.signup_window.geometry(f'500x650+{i}+200')
                self.signup_window.after(10)
                self.signup_window.update()

        # Start the sliding effect after a short delay
        self.signup_window.after(500, slide_in)
        self.signup_window.update()
        self.signup_window.mainloop()



        
    def navigate_signup_fields(self, event):
        """Navigate between fields with the Tab key."""
        current_widget = self.signup_window.focus_get()
        if current_widget == self.signup_username_entry:
            self.signup_password_entry.focus()
        elif current_widget == self.signup_password_entry:
            self.confirm_password_entry.focus()
        elif current_widget == self.confirm_password_entry:
            self.signup_name_entry.focus()
        elif current_widget == self.signup_name_entry:
            self.signup_age_entry.focus()
        elif current_widget == self.signup_age_entry:
            self.signup_email_entry.focus()
        elif current_widget == self.signup_email_entry:
            self.signup_button.focus()
        else:
            self.signup_username_entry.focus()
        
        
    def register_user(self):
        username = self.signup_username_entry.get()
        password = self.signup_password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        name = self.signup_name_entry.get()
        age = self.signup_age_entry.get()
        email = self.signup_email_entry.get()

        # Validate input fields
        if not username or not password or not confirm_password or not name or not age or not email:
            self.signup_error_label.configure(text="Please fill in all fields")
            return

        if password != confirm_password:
            self.signup_error_label.configure(text="Passwords do not match")
            return

        # Try to convert age to integer
        try:
            age = int(age)
        except ValueError:
            self.signup_error_label.configure(text="Age must be a valid number")
            return

        # Register the user in the database
        if self.db.insert_user(username, password, name, age, email):
            self.signup_error_label.configure(text="Signup successful!")
            self.signup_window.destroy()  # Close the signup window
            self.create_login_window()  # Create and show the login window
        else:
            self.signup_error_label.configure(text="Signup failed. Try again.")

    def back_to_login(self):
        self.signup_window.destroy()
        self.create_login_window()
            
    def SignupTransition(self, event=None):
        self.login_window.destroy()
        self.create_signup_window()


class ToolManagementApp:
    def __init__(self, user, db):
        self.user = user
        self.db_path = db_path
        self.db = DatabaseManager(db_path)
        self.create_dashboard_window()

    def create_dashboard_window(self):
        # Main Window
        self.window = ctk.CTk()
        self.window.geometry('1280x720')
        self.window.title('Learner Management System')

        # Sidebar
        sidebar = ctk.CTkFrame(self.window, width=250, fg_color="#2b2b2b", corner_radius=0)
        sidebar.pack(side="left", fill="y", padx=10, pady=10)

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

        self.inventory_table = ttk.Treeview(dashboard_frame, columns=("ID", "Name", "Category", "Condition", "Quantity", "Status"), show="headings")
        self.inventory_table.pack(pady=10, padx=20, fill="both", expand=True)

        for col in self.inventory_table["columns"]:
            self.inventory_table.heading(col, text=col, command=lambda col=col: self.sort_inventory(col))  # Added sorting feature
            self.inventory_table.column(col, width=150)

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
            borrowed_status = "Borrowed" if tool[2] == 'borrowed' else "Available"
            self.inventory_table.insert("", "end", values=(tool[0], tool[1], tool[2], tool[3], tool[4], borrowed_status))

        self.update_pie_chart()

    def sort_inventory(self, col):
        """ Sort the inventory table by a column """
        items = [(self.inventory_table.item(item)["values"], item) for item in self.inventory_table.get_children()]
        items.sort(key=lambda x: x[0][self.inventory_table["columns"].index(col)])

        for index, (values, item) in enumerate(items):
            self.inventory_table.item(item, values=values)

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
        try:
            # Fetch all tools
            tools = self.db.get_tools()
            print(f"Tools fetched from database: {tools}")  # Debugging

            # Filter available tools
            available_tools = [tool for tool in tools if tool[2] == 'available']
            print(f"Available tools: {available_tools}")  # Debugging

            if not available_tools:
                messagebox.showwarning("No Tools Available", "There are no tools available to borrow.")
                return

            # Populate dropdown
            tool_names = [tool[1] for tool in available_tools]
            print(f"Tool names in dropdown: {tool_names}")  # Debugging

            # Create borrowing window
            borrow_tool_window = ctk.CTkToplevel(self.window)
            borrow_tool_window.geometry("400x400")
            borrow_tool_window.title("Borrow Tool")
            borrow_tool_window.attributes('-topmost', True)

            borrow_tool_frame = ctk.CTkFrame(borrow_tool_window)
            borrow_tool_frame.pack(pady=20, padx=20, fill='both', expand=True)

            # Tool Dropdown
            tool_label = ctk.CTkLabel(borrow_tool_frame, text="Select Tool", font=('Roboto', 14))
            tool_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
            tool_var = StringVar(borrow_tool_frame)
            tool_var.set(tool_names[0])  # Default to first available tool
            tool_dropdown = ctk.CTkOptionMenu(borrow_tool_frame, variable=tool_var, values=tool_names)
            tool_dropdown.grid(row=0, column=1, pady=10)

            # Borrower Details
            borrower_label = ctk.CTkLabel(borrow_tool_frame, text="Borrower's Name", font=('Roboto', 14))
            borrower_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
            borrower_entry = ctk.CTkEntry(borrow_tool_frame, font=('Roboto', 14), width=250, placeholder_text="Enter borrower's name")
            borrower_entry.grid(row=1, column=1, pady=10)

            # Borrow Date
            date_label = ctk.CTkLabel(borrow_tool_frame, text="Borrow Date", font=('Roboto', 14))
            date_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
            date_entry = ctk.CTkEntry(borrow_tool_frame, font=('Roboto', 14), width=250, placeholder_text="Enter borrow date (YYYY-MM-DD)")
            date_entry.grid(row=2, column=1, pady=10)

            # Borrow Button Logic
            def borrow_selected_tool():
                selected_tool_name = tool_var.get()
                borrower_name = borrower_entry.get().strip()
                borrow_date = date_entry.get().strip()

                # Validate fields
                if not borrower_name or not borrow_date:
                    messagebox.showerror("Error", "Please fill in all fields.")
                    return

                # Validate borrow date format
                try:
                    datetime.datetime.strptime(borrow_date, "%Y-%m-%d").date()
                except ValueError:
                    messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
                    return

                # Borrow Tool
                tool_id = next((tool[0] for tool in available_tools if tool[1] == selected_tool_name), None)
                print(f"Borrowing tool with ID: {tool_id}")  # Debugging

                if tool_id:
                    # Attempt to borrow the tool in the database
                    success = self.db.borrow_tool(tool_id, borrower_name, borrow_date)
                    if success:
                        messagebox.showinfo("Success", f"'{selected_tool_name}' borrowed by '{borrower_name}'.")
                        borrow_tool_window.destroy()
                        self.update_inventory_table()
                        self.update_pie_chart()
                    else:
                        messagebox.showerror("Error", "Failed to borrow tool. Please try again.")
                else:
                    messagebox.showerror("Error", "Selected tool not found.")

            # Buttons
            borrow_button = ctk.CTkButton(borrow_tool_frame, text="Borrow", command=borrow_selected_tool)
            borrow_button.grid(row=3, column=0, columnspan=2, pady=20)

            close_button = ctk.CTkButton(borrow_tool_window, text="Close", command=borrow_tool_window.destroy)
            close_button.pack(side="bottom", pady=10)

        except Exception as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")


    
    def delete_tool(self):
        selected_item = self.inventory_table.selection()
        if not selected_item:
            messagebox.showwarning("No Tool Selected", "Please select a tool to delete.")
            return

        selected_tool = self.inventory_table.item(selected_item, 'values')
        tool_id = selected_tool[0]

        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the tool '{selected_tool[1]}'?")
        if confirm:
            self.db.delete_tool(tool_id)
            messagebox.showinfo("Tool Deleted", f"'{selected_tool[1]}' has been deleted from the inventory.")
            self.update_inventory_table()
            self.update_pie_chart()
            
    def view_tools(self):
        try:
            # Create a new window for viewing tools
            view_window = ctk.CTkToplevel(self.window)
            view_window.geometry("600x500")
            view_window.title("View Tools")

            # Make the window always stay on top
            view_window.attributes("-topmost", True)

            # Title Label
            title_label = ctk.CTkLabel(view_window, text="View Tools", font=("Roboto", 20))
            title_label.pack(pady=10)

            # Filter Options
            filter_frame = ctk.CTkFrame(view_window)
            filter_frame.pack(pady=20)

            filter_label = ctk.CTkLabel(filter_frame, text="Filter by Condition:", font=("Roboto", 14))
            filter_label.grid(row=0, column=0, padx=10)

            filter_entry = ctk.CTkEntry(filter_frame, font=("Roboto", 14), width=200, placeholder_text="Enter condition (e.g. 'good')")
            filter_entry.grid(row=0, column=1, pady=10)

            # Filter Button
            filter_button = ctk.CTkButton(view_window, text="Filter", font=("Roboto", 14), command=lambda: self.filter_tools(filter_entry, view_window))
            filter_button.pack(pady=10)

            # View All Tools Button
            view_all_button = ctk.CTkButton(view_window, text="View All Tools", font=("Roboto", 14), command=lambda: self.view_all_tools(view_window))
            view_all_button.pack(pady=10)

            # Tools Display Area (Listbox or Treeview)
            self.tools_listbox = ttk.Treeview(view_window, columns=("ID", "Name", "Category", "Condition", "Quantity", "Status"), show="headings")
            self.tools_listbox.pack(pady=10, padx=20, fill="both", expand=True)

            for col in self.tools_listbox["columns"]:
                self.tools_listbox.heading(col, text=col)

            # Load all tools initially
            self.update_tools_list()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while viewing tools: {e}")

    def filter_tools(self, filter_entry, view_window):
        filter_condition = filter_entry.get()
        if not filter_condition:
            messagebox.showwarning("Invalid Input", "Please enter a condition to filter by.")
            return

        # Fetch filtered tools based on the entered condition
        tools = self.db.fetch_tools_by_condition(filter_condition)
        if not tools:
            messagebox.showinfo("No Tools Found", f"No tools found with condition '{filter_condition}'.")
        else:
            self.update_tools_list(tools)
            messagebox.showinfo("Filtered Tools", f"Tools with condition '{filter_condition}' displayed.")

    def view_all_tools(self, view_window):
        # Fetch all tools and update the list
        self.update_tools_list()
        messagebox.showinfo("View Tools", "All tools have been displayed.")

    def update_tools_list(self, tools=None):
        # Clear existing tools in the listbox
        for item in self.tools_listbox.get_children():
            self.tools_listbox.delete(item)

        if tools is None:
            tools = self.db.fetch_all_tools()

        # Insert the tools into the listbox
        for tool in tools:
            borrowed_status = "Borrowed" if tool[2] == 'borrowed' else "Available"
            self.tools_listbox.insert("", "end", values=(tool[0], tool[1], tool[2], tool[3], tool[4], borrowed_status))

        
    
    def return_tool(self):
        try:
            # Fetch all tools
            tools = self.db.get_tools()
            borrowed_tools = [tool for tool in tools if tool[2] == 'borrowed']

            if not borrowed_tools:
                messagebox.showwarning("No Borrowed Tools", "There are no borrowed tools to return.")
                return

            # Get tool names for the borrowed tools
            tool_names = [tool[1] for tool in borrowed_tools]
            tool_name = simpledialog.askstring(
                "Return Tool",
                f"Borrowed tools: \n{', '.join(tool_names)}\n\nEnter the tool name you want to return:"
            )

            if tool_name and tool_name in tool_names:
                tool_id = borrowed_tools[tool_names.index(tool_name)][0]
                self.db.return_tool(tool_id)
                messagebox.showinfo("Tool Returned", f"'{tool_name}' has been returned.")
                self.update_inventory_table()  # Update inventory display
                self.update_pie_chart()  # Update pie chart
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

        # Add Tool Save Function
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

            # Check if the tool already exists in the database
            if self.db.fetch_tool_by_name(tool_name):
                messagebox.showwarning("Duplicate Tool", "A tool with this name already exists.")
                return

            # Insert tool into the database
            try:
                # Insert the tool using the insert_tool method of the database
                if self.db.insert_tool(tool_name, tool_category, tool_condition, int(tool_quantity), tool_location):
                    messagebox.showinfo("Success", f"{tool_name} added successfully.")
                    add_tool_window.destroy()  # Close the popup
                    self.update_inventory_table()  # Update the inventory table
                else:
                    messagebox.showerror("Error", "Failed to add tool. Please try again.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add tool: {e}")


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
