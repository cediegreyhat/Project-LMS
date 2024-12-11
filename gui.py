import tkinter as tk
from tkinter import messagebox
from database import DatabaseManager


class LoginApp:
    def __init__(self):
        self.db = DatabaseManager()
        self.db.init_user_database()  # Initialize the user database
        self.create_login_window()

    def create_login_window(self):
        self.login_window = tk.Tk()
        self.login_window.geometry('1920x1080')
        self.login_window.title('Login to Alpax Application')

        font_large = ('Arial', 24)
        font_medium = ('Arial', 20)

        tk.Label(self.login_window, text='Username', font=font_large).pack(pady=20)
        self.username_entry = tk.Entry(self.login_window, font=font_medium, width=30)
        self.username_entry.pack(pady=10)

        tk.Label(self.login_window, text='Password', font=font_large).pack(pady=20)
        self.password_entry = tk.Entry(self.login_window, show='*', font=font_medium, width=30)
        self.password_entry.pack(pady=10)

        self.login_button = tk.Button(self.login_window, text='Login', font=font_large, command=self.login, width=15)
        self.login_button.pack(pady=20)

        self.signup_button = tk.Button(self.login_window, text='Sign Up', font=font_large, command=self.open_signup_window, width=15)
        self.signup_button.pack(pady=10)

        self.login_window.mainloop()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = self.db.get_user(username, password)

        if user:
            self.login_window.destroy()
            ToolManagementApp(user, self.db)  # Pass the db instance to ToolManagementApp
        else:
            messagebox.showerror('Login Failed', 'Incorrect username or password.')

    def open_signup_window(self):
        self.login_window.destroy()
        self.signup_window = tk.Tk()
        self.signup_window.geometry('1920x1080')
        self.signup_window.title('Sign Up to Alpax Application')

        font_large = ('Arial', 24)
        font_medium = ('Arial', 20)

        tk.Label(self.signup_window, text='Username', font=font_large).pack(pady=20)
        self.signup_username_entry = tk.Entry(self.signup_window, font=font_medium, width=30)
        self.signup_username_entry.pack(pady=10)

        tk.Label(self.signup_window, text='Password', font=font_large).pack(pady=20)
        self.signup_password_entry = tk.Entry(self.signup_window, show='*', font=font_medium, width=30)
        self.signup_password_entry.pack(pady=10)

        tk.Label(self.signup_window, text='Name', font=font_large).pack(pady=20)
        self.signup_name_entry = tk.Entry(self.signup_window, font=font_medium, width=30)
        self.signup_name_entry.pack(pady=10)

        tk.Label(self.signup_window, text='Age', font=font_large).pack(pady=20)
        self.signup_age_entry = tk.Entry(self.signup_window, font=font_medium, width=30)
        self.signup_age_entry.pack(pady=10)

        tk.Label(self.signup_window, text='Email', font=font_large).pack(pady=20)
        self.signup_email_entry = tk.Entry(self.signup_window, font=font_medium, width=30)
        self.signup_email_entry.pack(pady=10)

        self.signup_button = tk.Button(self.signup_window, text='Sign Up', font=font_large, command=self.signup, width=15)
        self.signup_button.pack(pady=20)

        self.signup_window.mainloop()

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
        self.create_tool_management_window()

    def create_tool_management_window(self):
        self.window = tk.Tk()
        self.window.geometry('1920x1080')
        self.window.title('Tool Management Application')

        self.user_label = tk.Label(self.window, text=f"Logged in as {self.user[2]}", font=('Arial', 24))
        self.user_label.pack(pady=10)

        # Updated buttons to show "Coming Soon" feature
        self.view_tools_button = tk.Button(self.window, text='View All Tools', font=('Arial', 20), command=self.coming_soon)
        self.view_tools_button.pack(pady=20)

        self.borrow_button = tk.Button(self.window, text='Borrow Tool', font=('Arial', 20), command=self.coming_soon)
        self.borrow_button.pack(pady=20)

        self.return_button = tk.Button(self.window, text='Return Tool', font=('Arial', 20), command=self.coming_soon)
        self.return_button.pack(pady=20)

        self.search_button = tk.Button(self.window, text='Search Tool', font=('Arial', 20), command=self.coming_soon)
        self.search_button.pack(pady=20)

        self.logout_button = tk.Button(self.window, text='Logout', font=('Arial', 20), command=self.logout)
        self.logout_button.pack(pady=20)

        self.window.mainloop()

    def coming_soon(self):
        """Function to show 'Coming Soon' message."""
        messagebox.showinfo("Coming Soon", "This feature is coming soon!")

    def logout(self):
        self.window.destroy()
        LoginApp()


# Start the application
if __name__ == "__main__":
    LoginApp()  # Start with the login screen
