import tkinter as tk
from tkinter import ttk, messagebox
from db import Database
from ds_a import AdminPanel
from ds_u import UserPanel

class LoginWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("ElektroStock App - Login System")
        self.window.geometry("450x550")
        self.window.configure(bg='#2c3e50')
        self.window.resizable(False, False)
        
        # Center the window
        self.center_window()
        
        self.db = Database()
        self.setup_ui()

        self.window.mainloop()
    
    def center_window(self):
        """Center the window on screen"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.window.winfo_screenheight() // 2) - (550 // 2)
        self.window.geometry(f"450x550+{x}+{y}")
    
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.window, bg='#2c3e50')
        main_frame.pack(expand=True, fill='both', padx=30, pady=30)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#2c3e50')
        header_frame.pack(fill='x', pady=(0, 30))
        
        # Logo/Title
        title_label = tk.Label(
            header_frame, 
            text="ElektroStock APP", 
            font=('Arial', 24, 'bold'),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="Welcome to ElectroStok – Your Smart Selling Partner!",
            font=('Arial', 10),
            fg='#bdc3c7',
            bg='#2c3e50'
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Login Form Container
        form_frame = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=2)
        form_frame.pack(fill='both', expand=True, pady=0)
        
        # Form Title
        form_title = tk.Label(
            form_frame,
            text="LOGIN",
            font=('Arial', 16, 'bold'),
            fg='#ecf0f1',
            bg='#34495e'
        )
        form_title.pack(pady=(20, 15))
        
        # Username Field
        self.create_form_field(form_frame, "Username:", 'username')
        
        # Password Field
        self.create_form_field(form_frame, "Password:", 'password', show='*')
        
        # Login Button
        login_btn = tk.Button(
            form_frame,
            text="LOGIN",
            font=('Arial', 12, 'bold'),
            bg='#3498db',
            fg='white',
            cursor='hand2',
            relief='flat',
            pady=5,
            command=self.login
        )
        login_btn.pack(pady=(10, 10), padx=40, fill='x')
        
        
        
        # Footer
        footer_label = tk.Label(
            main_frame,
            text="© 2025 Wahidun Fajri - Universitas Muhammadiyah Cirebon",
            font=('Arial', 8),
            fg='#7f8c8d',
            bg='#2c3e50'
        )
        footer_label.pack(side='bottom', pady=(20, 0))
    
    def create_form_field(self, parent, label_text, field_name, show=None):
        """Create form field with label and entry"""
        field_frame = tk.Frame(parent, bg='#34495e')
        field_frame.pack(fill='x', padx=40, pady=10)
        
        label = tk.Label(
            field_frame,
            text=label_text,
            font=('Arial', 10, 'bold'),
            fg='#ecf0f1',
            bg='#34495e'
        )
        label.pack(anchor='w')
        
        entry = tk.Entry(
            field_frame,
            font=('Arial', 11),
            bg='#ecf0f1',
            fg='#2c3e50',
            relief='flat',
            bd=5,
            show=show
        )
        entry.pack(fill='x', pady=(5, 0), ipady=8)
        
        # Store entry widget reference
        setattr(self, f'{field_name}_entry', entry)
        
        # Bind Enter key to login - Fixed lambda function
        entry.bind('<Return>', self.on_enter_pressed)
    
    def on_enter_pressed(self, event):
        """Handle Enter key press"""
        self.login()
    
    def login(self):
        """Handle login process"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields!")
            return
        
        # Show loading cursor - with safety check
        try:
            if self.window.winfo_exists():
                self.window.configure(cursor='watch')
                self.window.update()
        except tk.TclError:
            return  # Window was destroyed, exit silently
        
        try:
            user_data = self.db.authenticate_user(username, password)
            
            if user_data:
                messagebox.showinfo("Success", f"Welcome, {user_data['username']}!")
                
                # Store window reference before destroying
                window_exists = True
                try:
                    window_exists = self.window.winfo_exists()
                except tk.TclError:
                    window_exists = False
                
                if window_exists:
                    self.window.destroy()
                
                # Open appropriate panel based on role
                if user_data['role'] == 'admin':
                    AdminPanel(user_data)
                else:
                    UserPanel(user_data)
            else:
                messagebox.showerror("Error", "Invalid username or password!")
                # Clear password field with safety check
                try:
                    if self.window.winfo_exists():
                        self.password_entry.delete(0, tk.END)
                except tk.TclError:
                    pass  # Window was destroyed, ignore
                
        except Exception as e:
            messagebox.showerror("Database Error", f"Connection failed: {str(e)}")
        finally:
            # Reset cursor with safety check
            try:
                if self.window.winfo_exists():
                    self.window.configure(cursor='')
            except tk.TclError:
                pass  # Window was destroyed, ignore
    
    def run(self):
        """Start the application"""
        self.window.mainloop()

if __name__ == "__main__":
    app = LoginWindow()
    app.run()