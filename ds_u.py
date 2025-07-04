import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import tkinter.font as tkfont
from db import Database

class UserPanel:
    def __init__(self, user_data):
        self.user_data = user_data
        self.db = Database()
        
        self.window = tk.Tk()
        self.window.title("ElektroStok APP - User Panel")
        self.window.geometry("1000x600")
        self.window.configure(bg='#2c3e50')
        self.window.state('zoomed')  # Maximize window
        
        # Create notification system
        self.notifications = []
        
        self.setup_ui()
        self.check_low_stock()  # Check for low stock on startup
        self.window.mainloop()
    
    def setup_ui(self):
        # Header Frame
        header_frame = tk.Frame(self.window, bg='#27ae60', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Header Content
        header_content = tk.Frame(header_frame, bg='#27ae60')
        header_content.pack(expand=True, fill='both', padx=20, pady=15)
        
        # Title
        title_label = tk.Label(
            header_content,
            text="USER DASHBOARD",
            font=('Arial', 20, 'bold'),
            fg='white',
            bg='#27ae60'
        )
        title_label.pack(side='left')
        
        # Notification Bell
        notification_frame = tk.Frame(header_content, bg='#27ae60')
        notification_frame.pack(side='right', padx=(0, 20))
        
        self.notification_btn = tk.Button(
            notification_frame,
            text="🔔",
            font=('Arial', 16),
            bg='#f39c12',
            fg='white',
            cursor='hand2',
            command=self.show_notifications,
            width=3
        )
        self.notification_btn.pack(side='left', padx=(0, 10))
        
        # Notification count
        self.notification_count = tk.Label(
            notification_frame,
            text="",
            font=('Arial', 8, 'bold'),
            fg='white',
            bg='#e74c3c'
        )
        
        # User Info and Logout
        user_frame = tk.Frame(header_content, bg='#27ae60')
        user_frame.pack(side='right')
        
        user_label = tk.Label(
            user_frame,
            text=f"Welcome, {self.user_data['username']}",
            font=('Arial', 12),
            fg='white',
            bg='#27ae60'
        )
        user_label.pack(side='left', padx=(0, 20))
        
        logout_btn = tk.Button(
            user_frame,
            text="Logout",
            font=('Arial', 10, 'bold'),
            bg='#e74c3c',
            fg='white',
            cursor='hand2',
            command=self.logout
        )
        logout_btn.pack(side='right')
        
        # Main Content Frame
        main_frame = tk.Frame(self.window, bg='#2c3e50')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Create Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(expand=True, fill='both')
        
        # Configure style
        style = ttk.Style()
        style.configure('TNotebook.Tab', padding=[20, 10])
        
        # Create tabs (Read-only for users)
        self.create_dashboard_tab()
        self.create_customer_view_tab()
        self.create_barang_view_tab()
        self.create_transaksi_view_tab()
    
    def create_dashboard_tab(self):
        # Dashboard Tab
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="Dashboard")
        self.notebook.select(dashboard_frame)  # Select dashboard as default
        
        # Dashboard Content
        self.setup_dashboard(dashboard_frame)
    
    def create_customer_view_tab(self):
        # Customer View Tab
        customer_frame = ttk.Frame(self.notebook)
        self.notebook.add(customer_frame, text="View Customers")
        
        # Customer View
        self.setup_customer_view(customer_frame)
    
    def create_barang_view_tab(self):
        # Barang View Tab
        barang_frame = ttk.Frame(self.notebook)
        self.notebook.add(barang_frame, text="View Barang")
        
        # Barang View
        self.setup_barang_view(barang_frame)
    
    def create_transaksi_view_tab(self):
        # Transaksi View Tab
        transaksi_frame = ttk.Frame(self.notebook)
        self.notebook.add(transaksi_frame, text="View Transaksi")
        
        # Transaksi View
        self.setup_transaksi_view(transaksi_frame)
    
    def setup_dashboard(self, parent):
        # Dashboard content
        dashboard_title = tk.Label(
            parent,
            text="SYSTEM OVERVIEW - READ ONLY",
            font=('Arial', 18, 'bold'),
            fg='#2c3e50'
        )
        dashboard_title.pack(pady=20)
        
        # Info message
        info_label = tk.Label(
            parent,
            text="Welcome to the User Dashboard! You have read-only access to view data.",
            font=('Arial', 12),
            fg='#7f8c8d'
        )
        info_label.pack(pady=10)
        
        # Stats Frame
        stats_frame = tk.Frame(parent)
        stats_frame.pack(fill='x', padx=50, pady=20)
        
        # Get statistics
        customers = self.db.get_all_customers()
        barang = self.db.get_all_barang()
        transaksi = self.db.get_all_transaksi()
        
        # Create stat cards
        self.create_stat_card(stats_frame, "Total Customers", len(customers), "#3498db", 0)
        self.create_stat_card(stats_frame, "Total Barang", len(barang), "#2ecc71", 1)
        self.create_stat_card(stats_frame, "Total Transaksi", len(transaksi), "#e74c3c", 2)
        
        # Recent transactions
        recent_frame = tk.LabelFrame(parent, text="Recent Transactions", font=('Arial', 12, 'bold'))
        recent_frame.pack(fill='both', expand=True, padx=50, pady=20)
        
        # Recent transactions treeview
        columns = ('ID', 'Customer', 'Barang', 'Jumlah', 'Total', 'Tanggal')
        self.recent_tree = ttk.Treeview(recent_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.recent_tree.heading(col, text=col)
            self.recent_tree.column(col, width=150)
        
        # Add recent transactions (last 10) - FIXED: Sort by ID ascending
        # Urutkan transaksi berdasarkan ID (asumsinya ID ada di indeks 0)
        sorted_transaksi = sorted(transaksi, key=lambda x: x[0])
        recent_transaksi = sorted_transaksi[:10] if len(sorted_transaksi) >= 10 else sorted_transaksi


        for trans in recent_transaksi:
            self.recent_tree.insert('', 'end', values=trans)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(recent_frame, orient='vertical', command=self.recent_tree.yview)
        self.recent_tree.configure(yscrollcommand=scrollbar.set)
        
        self.recent_tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar.pack(side='right', fill='y', pady=10)
        
        # Refresh button
        refresh_btn = tk.Button(
            parent,
            text="Refresh Data",
            font=('Arial', 12, 'bold'),
            bg='#3498db',
            fg='white',
            cursor='hand2',
            command=self.refresh_dashboard
        )
        refresh_btn.pack(pady=20)
    
    def create_stat_card(self, parent, title, value, color, column):
        card_frame = tk.Frame(parent, bg=color, relief='raised', bd=2)
        card_frame.grid(row=0, column=column, padx=20, pady=10, sticky='ew')
        parent.grid_columnconfigure(column, weight=1)
        
        title_label = tk.Label(
            card_frame,
            text=title,
            font=('Arial', 12, 'bold'),
            fg='white',
            bg=color
        )
        title_label.pack(pady=(20, 5))
        
        value_label = tk.Label(
            card_frame,
            text=str(value),
            font=('Arial', 24, 'bold'),
            fg='white',
            bg=color
        )
        value_label.pack(pady=(5, 20))
    
    def setup_customer_view(self, parent):
        # Title
        title_label = tk.Label(
            parent,
            text="CUSTOMER DATA - READ ONLY",
            font=('Arial', 16, 'bold'),
            fg='#2c3e50'
        )
        title_label.pack(pady=10)
        
        # Search Frame with Quick Search
        search_frame = tk.Frame(parent)
        search_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(search_frame, text="🔍 Quick Search Customer:", font=('Arial', 10, 'bold')).pack(side='left')
        self.customer_search_var = tk.StringVar()
        self.customer_search_var.trace('w', self.filter_customers)
        search_entry = tk.Entry(search_frame, textvariable=self.customer_search_var, font=('Arial', 10))
        search_entry.pack(side='left', fill='x', expand=True, padx=(10, 0))
        
        # Clear search button
        clear_btn = tk.Button(
            search_frame,
            text="Clear",
            font=('Arial', 8),
            bg='#95a5a6',
            fg='white',
            cursor='hand2',
            command=lambda: self.customer_search_var.set('')
        )
        clear_btn.pack(side='right', padx=(5, 0))
        
        # Table Frame
        table_frame = tk.LabelFrame(parent, text="Customer List", font=('Arial', 10, 'bold'))
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Treeview
        columns = ('ID', 'Nama', 'Alamat', 'Telepon')
        self.customer_tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        
        for col in columns:
            self.customer_tree.heading(col, text=col)
            self.customer_tree.column(col, width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.customer_tree.yview)
        self.customer_tree.configure(yscrollcommand=scrollbar.set)
        
        self.customer_tree.pack(side='left', fill='both', expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side='right', fill='y', pady=10)
        
        # Load data
        self.load_customers()
        
        # Action buttons frame
        action_frame = tk.Frame(parent)
        action_frame.pack(pady=10)
        
        # Refresh button
        refresh_btn = tk.Button(
            action_frame,
            text="🔄 Refresh Customer Data",
            font=('Arial', 10, 'bold'),
            bg='#27ae60',
            fg='white',
            cursor='hand2',
            command=self.load_customers
        )
        refresh_btn.pack(side='left', padx=5)
        
        # Print button
        print_btn = tk.Button(
            action_frame,
            text="🖨️ Print Customer List",
            font=('Arial', 10, 'bold'),
            bg='#3498db',
            fg='white',
            cursor='hand2',
            command=self.print_customer_list
        )
        print_btn.pack(side='left', padx=5)
    
    def setup_barang_view(self, parent):
        # Title
        title_label = tk.Label(
            parent,
            text="BARANG DATA - READ ONLY",
            font=('Arial', 16, 'bold'),
            fg='#2c3e50'
        )
        title_label.pack(pady=10)
        
        # Search Frame with Quick Search
        search_frame = tk.Frame(parent)
        search_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(search_frame, text="🔍 Quick Search Barang:", font=('Arial', 10, 'bold')).pack(side='left')
        self.barang_search_var = tk.StringVar()
        self.barang_search_var.trace('w', self.filter_barang)
        search_entry = tk.Entry(search_frame, textvariable=self.barang_search_var, font=('Arial', 10))
        search_entry.pack(side='left', fill='x', expand=True, padx=(10, 0))
        
        # Clear search button
        clear_btn = tk.Button(
            search_frame,
            text="Clear",
            font=('Arial', 8),
            bg='#95a5a6',
            fg='white',
            cursor='hand2',
            command=lambda: self.barang_search_var.set('')
        )
        clear_btn.pack(side='right', padx=(5, 0))
        
        # Low stock warning
        self.low_stock_frame = tk.Frame(parent, bg='#e74c3c')
        self.low_stock_label = tk.Label(
            self.low_stock_frame,
            text="⚠️ Items with low stock detected! Check notifications.",
            font=('Arial', 10, 'bold'),
            fg='white',
            bg='#e74c3c'
        )
        
        # Table Frame
        table_frame = tk.LabelFrame(parent, text="Barang List", font=('Arial', 10, 'bold'))
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Treeview
        columns = ('ID', 'Nama Barang', 'Harga', 'Stok')
        self.barang_tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        
        for col in columns:
            self.barang_tree.heading(col, text=col)
            self.barang_tree.column(col, width=150)
        
        # Scrollbar
        scrollbar_barang = ttk.Scrollbar(table_frame, orient='vertical', command=self.barang_tree.yview)
        self.barang_tree.configure(yscrollcommand=scrollbar_barang.set)
        
        self.barang_tree.pack(side='left', fill='both', expand=True, padx=(10, 0), pady=10)
        scrollbar_barang.pack(side='right', fill='y', pady=10)
        
        # Load data
        self.load_barang()
        
        # Action buttons frame
        action_frame = tk.Frame(parent)
        action_frame.pack(pady=10)
        
        # Refresh button
        refresh_btn = tk.Button(
            action_frame,
            text="🔄 Refresh Barang Data",
            font=('Arial', 10, 'bold'),
            bg='#27ae60',
            fg='white',
            cursor='hand2',
            command=self.load_barang
        )
        refresh_btn.pack(side='left', padx=5)
        
        # Print button
        print_btn = tk.Button(
            action_frame,
            text="🖨️ Print Stock Report",
            font=('Arial', 10, 'bold'),
            bg='#3498db',
            fg='white',
            cursor='hand2',
            command=self.print_stock_report
        )
        print_btn.pack(side='left', padx=5)
        
        # Check low stock button
        check_stock_btn = tk.Button(
            action_frame,
            text="⚠️ Check Low Stock",
            font=('Arial', 10, 'bold'),
            bg='#f39c12',
            fg='white',
            cursor='hand2',
            command=self.check_low_stock
        )
        check_stock_btn.pack(side='left', padx=5)
    
    def setup_transaksi_view(self, parent):
        # Title
        title_label = tk.Label(
            parent,
            text="TRANSAKSI DATA - READ ONLY",
            font=('Arial', 16, 'bold'),
            fg='#2c3e50'
        )
        title_label.pack(pady=10)
        
        # Filter Frame
        filter_frame = tk.LabelFrame(parent, text="Filters", font=('Arial', 10, 'bold'))
        filter_frame.pack(fill='x', padx=20, pady=10)
        
        # Search by text
        search_row = tk.Frame(filter_frame)
        search_row.pack(fill='x', padx=10, pady=5)
        
        tk.Label(search_row, text="🔍 Quick Search:", font=('Arial', 10, 'bold')).pack(side='left')
        self.transaksi_search_var = tk.StringVar()
        self.transaksi_search_var.trace('w', self.filter_transaksi)
        search_entry = tk.Entry(search_row, textvariable=self.transaksi_search_var, font=('Arial', 10))
        search_entry.pack(side='left', fill='x', expand=True, padx=(10, 0))
        
        # Date filter
        date_row = tk.Frame(filter_frame)
        date_row.pack(fill='x', padx=10, pady=5)
        
        tk.Label(date_row, text="📅 Filter by Period:", font=('Arial', 10, 'bold')).pack(side='left')
        
        # Period dropdown
        self.period_var = tk.StringVar(value="All Time")
        period_combo = ttk.Combobox(
            date_row,
            textvariable=self.period_var,
            values=["All Time", "Today", "Last 7 Days", "Last 30 Days", "Last 90 Days"],
            state="readonly",
            width=15
        )
        period_combo.pack(side='left', padx=(10, 0))
        period_combo.bind('<<ComboboxSelected>>', self.filter_by_period)
        
        # Clear filters button
        clear_btn = tk.Button(
            date_row,
            text="Clear Filters",
            font=('Arial', 8),
            bg='#95a5a6',
            fg='white',
            cursor='hand2',
            command=self.clear_filters
        )
        clear_btn.pack(side='right', padx=(5, 0))
        
        # Table Frame
        table_frame = tk.LabelFrame(parent, text="Transaksi List", font=('Arial', 10, 'bold'))
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Treeview
        columns = ('ID', 'Customer', 'Barang', 'Jumlah', 'Total Harga', 'Tanggal')
        self.transaksi_tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        
        for col in columns:
            self.transaksi_tree.heading(col, text=col)
            self.transaksi_tree.column(col, width=150)
        
        # Scrollbar
        scrollbar_transaksi = ttk.Scrollbar(table_frame, orient='vertical', command=self.transaksi_tree.yview)
        self.transaksi_tree.configure(yscrollcommand=scrollbar_transaksi.set)
        
        self.transaksi_tree.pack(side='left', fill='both', expand=True, padx=(10, 0), pady=10)
        scrollbar_transaksi.pack(side='right', fill='y', pady=10)
        
        # Load data
        self.load_transaksi()
        
        # Action buttons frame
        action_frame = tk.Frame(parent)
        action_frame.pack(pady=10)
        
        # Refresh button
        refresh_btn = tk.Button(
            action_frame,
            text="🔄 Refresh Transaksi Data",
            font=('Arial', 10, 'bold'),
            bg='#27ae60',
            fg='white',
            cursor='hand2',
            command=self.load_transaksi
        )
        refresh_btn.pack(side='left', padx=5)
        
        # Print invoice button
        print_invoice_btn = tk.Button(
            action_frame,
            text="🖨️ Print Selected Invoice",
            font=('Arial', 10, 'bold'),
            bg='#3498db',
            fg='white',
            cursor='hand2',
            command=self.print_selected_invoice
        )
        print_invoice_btn.pack(side='left', padx=5)
        
        # Print report button
        print_report_btn = tk.Button(
            action_frame,
            text="📊 Print Transaction Report",
            font=('Arial', 10, 'bold'),
            bg='#9b59b6',
            fg='white',
            cursor='hand2',
            command=self.print_transaction_report
        )
        print_report_btn.pack(side='left', padx=5)
    
    def check_low_stock(self):
        """Check for items with low stock and create notifications"""
        try:
            barang = self.db.get_all_barang()
            low_stock_items = []
            
            # Define low stock threshold
            LOW_STOCK_THRESHOLD = 10
            
            for item in barang:
                stock = int(item[3])  # Assuming stock is at index 3
                if stock <= LOW_STOCK_THRESHOLD:
                    low_stock_items.append({
                        'name': item[1],
                        'stock': stock,
                        'id': item[0]
                    })
            
            # Clear previous notifications
            self.notifications = []
            
            # Add low stock notifications
            for item in low_stock_items:
                notification = {
                    'type': 'low_stock',
                    'message': f"Low Stock Alert: {item['name']} (Stock: {item['stock']})",
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'item': item
                }
                self.notifications.append(notification)
            
            # Update notification display
            self.update_notification_display()
            
            # Show low stock warning in barang tab if any
            if hasattr(self, 'low_stock_frame') and low_stock_items:
                self.low_stock_frame.pack(fill='x', padx=20, pady=5)
                self.low_stock_label.pack(pady=5)
            elif hasattr(self, 'low_stock_frame'):
                self.low_stock_frame.pack_forget()
                
        except Exception as e:
            print(f"Error checking low stock: {str(e)}")
    
    def update_notification_display(self):
        """Update notification button and count"""
        count = len(self.notifications)
        if count > 0:
            self.notification_btn.configure(bg='#e74c3c')
            self.notification_count.configure(text=str(count))
            self.notification_count.pack(side='left')
        else:
            self.notification_btn.configure(bg='#f39c12')
            self.notification_count.pack_forget()
    
    def show_notifications(self):
        """Show notification window"""
        notification_window = tk.Toplevel(self.window)
        notification_window.title("Notifications")
        notification_window.geometry("500x400")
        notification_window.configure(bg='white')
        
        # Title
        title_label = tk.Label(
            notification_window,
            text="📢 Notifications",
            font=('Arial', 16, 'bold'),
            fg='#2c3e50',
            bg='white'
        )
        title_label.pack(pady=10)
        
        # Notifications frame
        notifications_frame = tk.Frame(notification_window, bg='white')
        notifications_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        if self.notifications:
            for i, notification in enumerate(self.notifications):
                notif_frame = tk.Frame(notifications_frame, bg='#ecf0f1', relief='raised', bd=1)
                notif_frame.pack(fill='x', pady=5)
                
                # Notification content
                message_label = tk.Label(
                    notif_frame,
                    text=notification['message'],
                    font=('Arial', 10, 'bold'),
                    fg='#e74c3c',
                    bg='#ecf0f1',
                    wraplength=400,
                    justify='left'
                )
                message_label.pack(anchor='w', padx=10, pady=5)
                
                time_label = tk.Label(
                    notif_frame,
                    text=f"Time: {notification['timestamp']}",
                    font=('Arial', 8),
                    fg='#7f8c8d',
                    bg='#ecf0f1'
                )
                time_label.pack(anchor='w', padx=10, pady=(0, 5))
        else:
            no_notif_label = tk.Label(
                notifications_frame,
                text="No notifications at this time.",
                font=('Arial', 12),
                fg='#7f8c8d',
                bg='white'
            )
            no_notif_label.pack(pady=50)
        
        # Close button
        close_btn = tk.Button(
            notification_window,
            text="Close",
            font=('Arial', 10, 'bold'),
            bg='#95a5a6',
            fg='white',
            cursor='hand2',
            command=notification_window.destroy
        )
        close_btn.pack(pady=10)
    
    def load_customers(self):
        """Load customers into treeview - FIXED: Sort by ID ascending"""
        # Clear existing items
        for item in self.customer_tree.get_children():
            self.customer_tree.delete(item)
        
        # Get and sort customers by ID (ascending)
        customers = self.db.get_all_customers()
        sorted_customers = sorted(customers, key=lambda x: int(x[0]))
        
        # Insert sorted data
        for customer in sorted_customers:
            self.customer_tree.insert('', 'end', values=customer)
    
    def load_barang(self):
        """Load barang into treeview - FIXED: Sort by ID ascending"""
        # Clear existing items
        for item in self.barang_tree.get_children():
            self.barang_tree.delete(item)
        
        # Get and sort barang by ID (ascending)
        barang = self.db.get_all_barang()
        sorted_barang = sorted(barang, key=lambda x: int(x[0]))
        
        # Insert sorted data
        for item in sorted_barang:
            # Add color coding for low stock
            stock = int(item[3])
            if stock <= 10:
                self.barang_tree.insert('', 'end', values=item, tags=('low_stock',))
            else:
                self.barang_tree.insert('', 'end', values=item)
        
        # Configure tag colors
        self.barang_tree.tag_configure('low_stock', background='#ffcccc')
    
    def load_transaksi(self):
        """Load transaksi into treeview - FIXED: Sort by ID ascending"""
        # Clear existing items
        for item in self.transaksi_tree.get_children():
            self.transaksi_tree.delete(item)
        
        # Get and sort transaksi by ID (ascending)
        transaksi = self.db.get_all_transaksi()
        sorted_transaksi = sorted(transaksi, key=lambda x: int(x[0]))
        
        # Insert sorted data
        for trans in sorted_transaksi:
            self.transaksi_tree.insert('', 'end', values=trans)
    
    def filter_customers(self, *args):
        """Filter customers based on search term"""
        search_term = self.customer_search_var.get().lower()
        
        # Clear current items
        for item in self.customer_tree.get_children():
            self.customer_tree.delete(item)
        
        # Get and filter customers
        customers = self.db.get_all_customers()
        sorted_customers = sorted(customers, key=lambda x: int(x[0]))
        
        for customer in sorted_customers:
            if (search_term in str(customer[1]).lower() or 
                search_term in str(customer[2]).lower() or 
                search_term in str(customer[3]).lower()):
                self.customer_tree.insert('', 'end', values=customer)
    
    def filter_barang(self, *args):
        """Filter barang based on search term"""
        search_term = self.barang_search_var.get().lower()
        
        # Clear current items
        for item in self.barang_tree.get_children():
            self.barang_tree.delete(item)
        
        # Get and filter barang
        barang = self.db.get_all_barang()
        sorted_barang = sorted(barang, key=lambda x: int(x[0]))
        
        for item in sorted_barang:
            if (search_term in str(item[1]).lower() or 
                search_term in str(item[0]).lower()):
# Add color coding for low stock
                stock = int(item[3])
                if stock <= 10:
                    self.barang_tree.insert('', 'end', values=item, tags=('low_stock',))
                else:
                    self.barang_tree.insert('', 'end', values=item)
        
        # Configure tag colors
        self.barang_tree.tag_configure('low_stock', background='#ffcccc')
    
    def filter_transaksi(self, *args):
        """Filter transaksi based on search term"""
        search_term = self.transaksi_search_var.get().lower()
        
        # Clear current items
        for item in self.transaksi_tree.get_children():
            self.transaksi_tree.delete(item)
        
        # Get and filter transaksi
        transaksi = self.db.get_all_transaksi()
        sorted_transaksi = sorted(transaksi, key=lambda x: int(x[0]))
        
        for trans in sorted_transaksi:
            if (search_term in str(trans[1]).lower() or  # Customer
                search_term in str(trans[2]).lower() or  # Barang
                search_term in str(trans[0]).lower()):   # ID
                self.transaksi_tree.insert('', 'end', values=trans)
    
    def filter_by_period(self, event=None):
        """Filter transaksi by time period"""
        period = self.period_var.get()
        current_date = datetime.now()
        
        # Clear current items
        for item in self.transaksi_tree.get_children():
            self.transaksi_tree.delete(item)
        
        # Get all transaksi
        transaksi = self.db.get_all_transaksi()
        sorted_transaksi = sorted(transaksi, key=lambda x: int(x[0]))
        
        if period == "All Time":
            filtered_transaksi = sorted_transaksi
        else:
            filtered_transaksi = []
            for trans in sorted_transaksi:
                try:
                    # Parse transaction date (assuming format YYYY-MM-DD)
                    trans_date = datetime.strptime(trans[5], "%Y-%m-%d")
                    
                    if period == "Today":
                        if trans_date.date() == current_date.date():
                            filtered_transaksi.append(trans)
                    elif period == "Last 7 Days":
                        if trans_date >= current_date - timedelta(days=7):
                            filtered_transaksi.append(trans)
                    elif period == "Last 30 Days":
                        if trans_date >= current_date - timedelta(days=30):
                            filtered_transaksi.append(trans)
                    elif period == "Last 90 Days":
                        if trans_date >= current_date - timedelta(days=90):
                            filtered_transaksi.append(trans)
                except ValueError:
                    # If date parsing fails, include the transaction
                    filtered_transaksi.append(trans)
        
        # Insert filtered data
        for trans in filtered_transaksi:
            # Apply search filter if exists
            search_term = self.transaksi_search_var.get().lower()
            if not search_term or (search_term in str(trans[1]).lower() or 
                                  search_term in str(trans[2]).lower() or 
                                  search_term in str(trans[0]).lower()):
                self.transaksi_tree.insert('', 'end', values=trans)
    
    def clear_filters(self):
        """Clear all filters in transaksi tab"""
        self.transaksi_search_var.set('')
        self.period_var.set('All Time')
        self.load_transaksi()
    
    def refresh_dashboard(self):
        """Refresh dashboard data"""
        try:
            # Get fresh statistics
            customers = self.db.get_all_customers()
            barang = self.db.get_all_barang()
            transaksi = self.db.get_all_transaksi()
            
            # Clear recent transactions
            for item in self.recent_tree.get_children():
                self.recent_tree.delete(item)
            
            # Add recent transactions (last 10)
            sorted_transaksi = sorted(transaksi, key=lambda x: int(x[0]), reverse=True)
            recent_transaksi = sorted_transaksi[:10] if len(sorted_transaksi) >= 10 else sorted_transaksi
            
            for trans in recent_transaksi:
                self.recent_tree.insert('', 'end', values=trans)
            
            # Refresh notifications
            self.check_low_stock()
            
            messagebox.showinfo("Success", "Dashboard data refreshed successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh dashboard: {str(e)}")
    
    def print_customer_list(self):
        """Print customer list"""
        try:
            customers = self.db.get_all_customers()
            
            # Create print content
            print_content = "CUSTOMER LIST REPORT\n"
            print_content += "=" * 50 + "\n\n"
            print_content += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            print_content += f"Total Customers: {len(customers)}\n\n"
            
            # Add customer data
            for customer in customers:
                print_content += f"ID: {customer[0]}\n"
                print_content += f"Name: {customer[1]}\n"
                print_content += f"Address: {customer[2]}\n"
                print_content += f"Phone: {customer[3]}\n"
                print_content += "-" * 30 + "\n"
            
            # Show print preview
            self.show_print_preview("Customer List Report", print_content)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate customer report: {str(e)}")
    
    def print_stock_report(self):
        """Print stock report"""
        try:
            barang = self.db.get_all_barang()
            
            # Create print content
            print_content = "STOCK REPORT\n"
            print_content += "=" * 50 + "\n\n"
            print_content += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            print_content += f"Total Items: {len(barang)}\n\n"
            
            # Categorize items
            low_stock_items = []
            normal_stock_items = []
            
            for item in barang:
                stock = int(item[3])
                if stock <= 10:
                    low_stock_items.append(item)
                else:
                    normal_stock_items.append(item)
            
            # Add low stock section
            if low_stock_items:
                print_content += "⚠️ LOW STOCK ITEMS (≤10):\n"
                print_content += "-" * 30 + "\n"
                for item in low_stock_items:
                    print_content += f"ID: {item[0]} | {item[1]} | Stock: {item[3]} | Price: Rp {item[2]:,}\n"
                print_content += "\n"
            
            # Add normal stock section
            print_content += "NORMAL STOCK ITEMS:\n"
            print_content += "-" * 30 + "\n"
            for item in normal_stock_items:
                print_content += f"ID: {item[0]} | {item[1]} | Stock: {item[3]} | Price: Rp {item[2]:,}\n"
            
            # Show print preview
            self.show_print_preview("Stock Report", print_content)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate stock report: {str(e)}")
    
    def print_selected_invoice(self):
        """Print selected transaction as invoice"""
        try:
            selected_item = self.transaksi_tree.selection()
            if not selected_item:
                messagebox.showwarning("Warning", "Please select a transaction to print invoice.")
                return
            
            # Get transaction data
            trans_data = self.transaksi_tree.item(selected_item[0])['values']
            
            # Format amount safely
            try:
                # Convert amount to string first, then clean it
                amount_str = str(trans_data[4])
                # Remove any existing formatting
                clean_amount = amount_str.replace('Rp', '').replace(',', '').replace('.', '').strip()
                if clean_amount.isdigit():
                    formatted_amount = f"Rp {int(clean_amount):,}"
                else:
                    formatted_amount = str(trans_data[4])
            except (ValueError, TypeError):
                formatted_amount = str(trans_data[4])
            
            # Create invoice content
            print_content = "INVOICE\n"
            print_content += "=" * 50 + "\n\n"
            print_content += "ElektroStock APP - TRANSACTION INVOICE\n"
            print_content += f"Invoice ID: INV-{trans_data[0]}\n"
            print_content += f"Date: {trans_data[5]}\n\n"
            
            print_content += "CUSTOMER INFORMATION:\n"
            print_content += f"Customer: {trans_data[1]}\n\n"
            
            print_content += "ITEM DETAILS:\n"
            print_content += f"Item: {trans_data[2]}\n"
            print_content += f"Quantity: {trans_data[3]}\n"
            print_content += f"Total Amount: {formatted_amount}\n\n"
            
            print_content += "Thank you for your purchase!\n"
            print_content += "=" * 50 + "\n"
            
            # Show print preview
            self.show_print_preview(f"Invoice INV-{trans_data[0]}", print_content)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate invoice: {str(e)}")
    
    def print_transaction_report(self):
        """Print transaction report"""
        try:
            transaksi = self.db.get_all_transaksi()
            
            # Create print content
            print_content = "TRANSACTION REPORT\n"
            print_content += "=" * 50 + "\n\n"
            print_content += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            print_content += f"Total Transactions: {len(transaksi)}\n\n"
            
            # Calculate total revenue
            total_revenue = 0
            for trans in transaksi:
                try:
                    # Remove 'Rp' and commas, then convert to int
                    amount_str = str(trans[4]).replace('Rp', '').replace(',', '').replace('.', '').strip()
                    total_revenue += int(amount_str)
                except (ValueError, TypeError):
                    continue
            
            print_content += f"Total Revenue: Rp {total_revenue:,}\n\n"
            
            # Add transaction details
            print_content += "TRANSACTION DETAILS:\n"
            print_content += "-" * 50 + "\n"
            
            for trans in transaksi:
                print_content += f"ID: {trans[0]} | Customer: {trans[1]} | Item: {trans[2]}\n"
                print_content += f"Qty: {trans[3]} | Amount: {trans[4]} | Date: {trans[5]}\n"
                print_content += "-" * 30 + "\n"
            
            # Show print preview
            self.show_print_preview("Transaction Report", print_content)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate transaction report: {str(e)}")
    
    def show_print_preview(self, title, content):
        """Show print preview window"""
        preview_window = tk.Toplevel(self.window)
        preview_window.title(f"Print Preview - {title}")
        preview_window.geometry("600x500")
        preview_window.configure(bg='white')
        
        # Title
        title_label = tk.Label(
            preview_window,
            text=f"🖨️ Print Preview - {title}",
            font=('Arial', 14, 'bold'),
            fg='#2c3e50',
            bg='white'
        )
        title_label.pack(pady=10)
        
        # Content frame with scrollbar
        content_frame = tk.Frame(preview_window, bg='white')
        content_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Text widget with scrollbar
        text_widget = tk.Text(
            content_frame,
            font=('Courier', 10),
            bg='#f8f9fa',
            fg='#2c3e50',
            wrap='word',
            padx=10,
            pady=2
        )
        
        scrollbar = ttk.Scrollbar(content_frame, orient='vertical', command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Insert content
        text_widget.insert('1.0', content)
        text_widget.configure(state='disabled')
        
        # Button frame
        button_frame = tk.Frame(preview_window, bg='white')
        button_frame.pack(pady=10)
        
        # Print button (simulated)
        print_btn = tk.Button(
            button_frame,
            text="🖨️ Print",
            font=('Arial', 10, 'bold'),
            bg='#27ae60',
            fg='white',
            cursor='hand2',
            command=lambda: self.simulate_print(title, preview_window)
        )
        print_btn.pack(side='left', padx=5)
        
        # Close button
        close_btn = tk.Button(
            button_frame,
            text="Close",
            font=('Arial', 10, 'bold'),
            bg='#95a5a6',
            fg='white',
            cursor='hand2',
            command=preview_window.destroy
        )
        close_btn.pack(side='left', padx=5)
    
    def simulate_print(self, title, window):
        """Simulate printing process"""
        try:
            messagebox.showinfo("Print", f"'{title}' has been sent to printer successfully!")
            window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to print: {str(e)}")
    
    def logout(self):
        """Logout and return to login screen"""
        result = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if result:
            self.window.destroy()
            # Import here to avoid circular import
            from login import LoginWindow
            LoginWindow()

if __name__ == "__main__":
    # Test data
    test_user = {
        'id': 1,
        'username': 'testuser',
        'role': 'user'
    }
    UserPanel(test_user)