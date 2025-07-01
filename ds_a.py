import tkinter as tk
from tkinter import ttk, messagebox
from db import Database
from datetime import datetime


class AdminPanel:
    def __init__(self, user_data):
        self.user_data = user_data
        self.db = Database()
        
        self.window = tk.Tk()
        self.window.title("ElektroStock App - Admin Panel")
        self.window.geometry("1200x700")
        self.window.configure(bg='#2c3e50')
        self.window.state('zoomed')  # Maximize window
        
        self.setup_ui()
        self.window.mainloop()
    
    def setup_ui(self):
        # Header Frame
        header_frame = tk.Frame(self.window, bg='#34495e', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Header Content
        header_content = tk.Frame(header_frame, bg='#34495e')
        header_content.pack(expand=True, fill='both', padx=20, pady=15)
        
        # Title
        title_label = tk.Label(
            header_content,
            text="ADMIN DASHBOARD",
            font=('Arial', 20, 'bold'),
            fg='#ecf0f1',
            bg='#34495e'
        )
        title_label.pack(side='left')
        
        # User Info and Logout
        user_frame = tk.Frame(header_content, bg='#34495e')
        user_frame.pack(side='right')
        
        user_label = tk.Label(
            user_frame,
            text=f"Welcome, {self.user_data['username']}",
            font=('Arial', 12),
            fg='#bdc3c7',
            bg='#34495e'
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
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_customer_tab()
        self.create_barang_tab()
        self.create_transaksi_tab()
        
    
    def create_customer_tab(self):
        # Customer Tab
        customer_frame = ttk.Frame(self.notebook)
        self.notebook.add(customer_frame, text="Kelola Customer")
        
        # Customer Management
        self.setup_customer_management(customer_frame)
    
    def create_barang_tab(self):
        # Barang Tab
        barang_frame = ttk.Frame(self.notebook)
        self.notebook.add(barang_frame, text="Kelola Barang")
        
        # Barang Management
        self.setup_barang_management(barang_frame)
    
    def create_transaksi_tab(self):
        # Transaksi Tab
        transaksi_frame = ttk.Frame(self.notebook)
        self.notebook.add(transaksi_frame, text="Kelola Transaksi")
        
        # Transaksi Management
        self.setup_transaksi_management(transaksi_frame)
    
    def create_dashboard_tab(self):
        # Dashboard Tab
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="Dashboard", state='normal')
        self.notebook.select(dashboard_frame)  # Select dashboard as default
        
        # Dashboard Content
        self.setup_dashboard(dashboard_frame)
    
    def setup_dashboard(self, parent):
        # Dashboard content
        dashboard_title = tk.Label(
            parent,
            text="SYSTEM OVERVIEW",
            font=('Arial', 18, 'bold'),
            fg='#2c3e50'
        )
        dashboard_title.pack(pady=20)
        
        # Store parent reference for auto-refresh
        self.dashboard_parent = parent
        
        # Stats Frame
        self.stats_frame = tk.Frame(parent)
        self.stats_frame.pack(fill='x', padx=50, pady=20)
        
        # Recent transactions
        recent_frame = tk.LabelFrame(parent, text="Recent Transactions", font=('Arial', 12, 'bold'))
        recent_frame.pack(fill='both', expand=True, padx=50, pady=20)
        
        # Recent transactions treeview
        columns = ('ID', 'Customer', 'Barang', 'Jumlah', 'Total', 'Tanggal')
        self.recent_tree = ttk.Treeview(recent_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.recent_tree.heading(col, text=col)
            self.recent_tree.column(col, width=150)
        
        self.recent_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Load data and start auto-refresh
        self.update_dashboard()
        self.auto_refresh_dashboard()  # Sekarang aman
        

    def update_dashboard(self):
        """Update dashboard data"""
        try:
            # Get data
            customers = self.db.get_all_customers()
            barang = self.db.get_all_barang()
            transaksi = self.db.get_all_transaksi()
            
            # Update stats
            for widget in self.stats_frame.winfo_children():
                widget.destroy()
            
            self.create_stat_card(self.stats_frame, "Total Customers", len(customers), "#3498db", 0)
            self.create_stat_card(self.stats_frame, "Total Barang", len(barang), "#2ecc71", 1)
            self.create_stat_card(self.stats_frame, "Total Transaksi", len(transaksi), "#e74c3c", 2)
            
            # Update recent transactions
            for item in self.recent_tree.get_children():
                self.recent_tree.delete(item)
            
            # Urutkan transaksi berdasarkan ID (kolom pertama, indeks 0)
            sorted_transaksi = sorted(transaksi, key=lambda x: x[0])
            recent_transaksi = sorted_transaksi[:10] if len(sorted_transaksi) >= 10 else sorted_transaksi

            for trans in recent_transaksi:
                self.recent_tree.insert('', 'end', values=trans)
                
        except Exception as e:
            print(f"Error updating dashboard: {e}")

    def auto_refresh_dashboard(self):
        """Auto refresh setiap 5 detik dengan pengecekan keamanan"""
        def safe_refresh():
            try:
                # Cek apakah window masih ada dan valid
                if (hasattr(self, 'window') and 
                    hasattr(self, 'dashboard_parent') and 
                    self.window.winfo_exists() and 
                    self.dashboard_parent.winfo_exists()):
                    
                    self.update_dashboard()
                    # Schedule next refresh
                    self.refresh_job = self.dashboard_parent.after(5000, safe_refresh)
                
            except (tk.TclError, AttributeError):
                # Window sudah ditutup atau error lain, hentikan refresh
                return
        
        # Mulai refresh cycle
        safe_refresh()

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
    
    def setup_customer_management(self, parent):
        # Title
        title_label = tk.Label(
            parent,
            text="CUSTOMER MANAGEMENT",
            font=('Arial', 16, 'bold'),
            fg='#2c3e50'
        )
        title_label.pack(pady=10)
        
        # Form Frame
        form_frame = tk.LabelFrame(parent, text="Add/Edit Customer", font=('Arial', 10, 'bold'))
        form_frame.pack(fill='x', padx=20, pady=10)
        
        # Form fields
        fields = [
            ('ID:', 'id'),
            ('Nama:', 'nama'),
            ('Alamat:', 'alamat'),
            ('Telepon:', 'telepon')
        ]
        
        self.customer_entries = {}
        for i, (label, field) in enumerate(fields):
            row_frame = tk.Frame(form_frame)
            row_frame.pack(fill='x', padx=10, pady=5)
            
            tk.Label(row_frame, text=label, width=10, anchor='w').pack(side='left')
            entry = tk.Entry(row_frame, font=('Arial', 10))
            entry.pack(side='left', fill='x', expand=True, padx=(10, 0))
            self.customer_entries[field] = entry
        
        # Buttons
        btn_frame = tk.Frame(form_frame)
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(btn_frame, text="Add Customer", bg='#2ecc71', fg='white', 
                 command=self.add_customer).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Update Customer", bg='#f39c12', fg='white',
                 command=self.update_customer).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Delete Customer", bg='#e74c3c', fg='white',
                 command=self.delete_customer).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Clear Fields", bg='#95a5a6', fg='white',
                 command=self.clear_customer_fields).pack(side='left', padx=5)
        
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
        
        
        # Bind selection
        self.customer_tree.bind('<<TreeviewSelect>>', self.on_customer_select)
        
        # Load data
        self.load_customers()
    
    def setup_barang_management(self, parent):
        # Similar structure for barang management
        title_label = tk.Label(
            parent,
            text="BARANG MANAGEMENT",
            font=('Arial', 16, 'bold'),
            fg='#2c3e50'
        )
        title_label.pack(pady=10)
        
        # Form Frame
        form_frame = tk.LabelFrame(parent, text="Add/Edit Barang", font=('Arial', 10, 'bold'))
        form_frame.pack(fill='x', padx=20, pady=10)
        
        # Form fields
        fields = [
            ('ID :', 'id'),
            ('Nama Barang :', 'nama_barang'),
            ('Harga :', 'harga'),
            ('Stok :', 'stok')
        ]
        
        self.barang_entries = {}
        for i, (label, field) in enumerate(fields):
            row_frame = tk.Frame(form_frame)
            row_frame.pack(fill='x', padx=10, pady=5)
            
            tk.Label(row_frame, text=label, width=12, anchor='w').pack(side='left')
            entry = tk.Entry(row_frame, font=('Arial', 10))
            entry.pack(side='left', fill='x', expand=True, padx=(10, 0))
            self.barang_entries[field] = entry
        
        # Buttons
        btn_frame = tk.Frame(form_frame)
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(btn_frame, text="Add Barang", bg='#2ecc71', fg='white',
                 command=self.add_barang).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Update Barang", bg='#f39c12', fg='white',
                 command=self.update_barang).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Delete Barang", bg='#e74c3c', fg='white',
                 command=self.delete_barang).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Clear Fields", bg='#95a5a6', fg='white',
                 command=self.clear_barang_fields).pack(side='left', padx=5)
        
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
        
        
        # Bind selection
        self.barang_tree.bind('<<TreeviewSelect>>', self.on_barang_select)
        
        # Load data
        self.load_barang()
    
    def setup_transaksi_management(self, parent):
        # Transaksi management
        title_label = tk.Label(
            parent,
            text="TRANSAKSI MANAGEMENT",
            font=('Arial', 16, 'bold'),
            fg='#2c3e50'
        )
        title_label.pack(pady=10)
        
        # Form Frame
        form_frame = tk.LabelFrame(parent, text="Add New Transaksi", font=('Arial', 10, 'bold'))
        form_frame.pack(fill='x', padx=20, pady=10)
        
        # Customer selection
        customer_frame = tk.Frame(form_frame)
        customer_frame.pack(fill='x', padx=10, pady=5)
        tk.Label(customer_frame, text="Customer:", width=12, anchor='w', font=('Arial', 10)).pack(side='left')
        self.customer_var = tk.StringVar()
        self.customer_combo = ttk.Combobox(customer_frame, textvariable=self.customer_var, state='readonly', font=('Arial', 10))
        self.customer_combo.pack(side='left', fill='x', expand=True, padx=(10, 0))
        
        # Barang selection
        barang_frame = tk.Frame(form_frame)
        barang_frame.pack(fill='x', padx=10, pady=5)
        tk.Label(barang_frame, text="Barang:", width=12, anchor='w', font=('Arial', 10)).pack(side='left')
        self.barang_var = tk.StringVar()
        self.barang_combo = ttk.Combobox(barang_frame, textvariable=self.barang_var, state='readonly', font=('Arial', 10))
        self.barang_combo.pack(side='left', fill='x', expand=True, padx=(10, 0))
        
        # Jumlah
        jumlah_frame = tk.Frame(form_frame)
        jumlah_frame.pack(fill='x', padx=10, pady=5)
        tk.Label(jumlah_frame, text="Jumlah:", width=12, anchor='w', font=('Arial', 10)).pack(side='left')
        self.jumlah_entry = tk.Entry(jumlah_frame, font=('Arial', 10))
        self.jumlah_entry.pack(side='left', fill='x', expand=True, padx=(10, 0))
        
        # Total Harga Display (read-only)
        total_frame = tk.Frame(form_frame)
        total_frame.pack(fill='x', padx=10, pady=5)
        tk.Label(total_frame, text="Total Harga:", width=12, anchor='w', font=('Arial', 10)).pack(side='left')
        self.total_var = tk.StringVar()
        self.total_label = tk.Label(total_frame, textvariable=self.total_var, font=('Arial', 10, 'bold'), 
                                fg='#e74c3c', bg='#ecf0f1', relief='sunken', anchor='w')
        self.total_label.pack(side='left', fill='x', expand=True, padx=(10, 0), pady=2)
        
        # Bind events for auto calculation
        self.jumlah_entry.bind('<KeyRelease>', self.calculate_total)
        self.barang_combo.bind('<<ComboboxSelected>>', self.calculate_total)
        
        # Buttons
        btn_frame = tk.Frame(form_frame)
        btn_frame.pack(fill='x', padx=5, pady=5)
        
        tk.Button(btn_frame, text="Add Transaksi", bg='#2ecc71', fg='white', font=('Arial', 8, 'bold'),
                command=self.add_transaksi, cursor='hand2', pady=5).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Delete Transaksi", bg='#e74c3c', fg='white', font=('Arial', 8, 'bold'),
                command=self.delete_transaksi, cursor='hand2', pady=5).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Clear Fields", bg='#95a5a6', fg='white', font=('Arial', 8, 'bold'),
                command=self.clear_transaksi_fields, cursor='hand2', pady=5).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Refresh", bg='#3498db', fg='white', font=('Arial', 8, 'bold'),
                command=self.refresh_transaksi, cursor='hand2', pady=5).pack(side='left', padx=5)
        
        # Search Frame
        search_frame = tk.Frame(parent)
        search_frame.pack(fill='x', padx=20, pady=(0, 5))
        
        tk.Label(search_frame, text="Search:", font=('Arial', 10)).pack(side='left')
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=('Arial', 10))
        search_entry.pack(side='left', padx=(5, 10), fill='x', expand=True)
        tk.Button(search_frame, text="Search", bg='#3498db', fg='white', font=('Arial', 9),
                command=self.search_transaksi, cursor='hand2').pack(side='left', padx=2)
        tk.Button(search_frame, text="Show All", bg='#95a5a6', fg='white', font=('Arial', 9),
                command=self.load_transaksi, cursor='hand2').pack(side='left', padx=2)
        
        # Table Frame
        table_frame = tk.LabelFrame(parent, text="Transaksi List", font=('Arial', 10, 'bold'))
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Treeview with improved columns
        columns = ('ID', 'Customer', 'Barang', 'Harga Satuan', 'Jumlah', 'Total Harga', 'Tanggal')
        self.transaksi_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=12)
        
        # Configure columns
        column_widths = {'ID': 60, 'Customer': 150, 'Barang': 180, 'Harga Satuan': 120, 
                        'Jumlah': 80, 'Total Harga': 120, 'Tanggal': 140}
        
        for col in columns:
            self.transaksi_tree.heading(col, text=col, command=lambda c=col: self.sort_column(c))
            self.transaksi_tree.column(col, width=column_widths.get(col, 100), anchor='center')
        
        # Scrollbars
        scrollbar_transaksi_v = ttk.Scrollbar(table_frame, orient='vertical', command=self.transaksi_tree.yview)
        scrollbar_transaksi_h = ttk.Scrollbar(table_frame, orient='horizontal', command=self.transaksi_tree.xview)
        self.transaksi_tree.configure(yscrollcommand=scrollbar_transaksi_v.set, xscrollcommand=scrollbar_transaksi_h.set)
        
        # Pack treeview and scrollbars
        self.transaksi_tree.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        scrollbar_transaksi_v.grid(row=0, column=1, sticky='ns', pady=10)
        scrollbar_transaksi_h.grid(row=1, column=0, sticky='ew', padx=10)
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Bind selection event
        self.transaksi_tree.bind('<<TreeviewSelect>>', self.on_transaksi_select)
        
        # Status bar
        status_frame = tk.Frame(parent, bg='#ecf0f1', relief='sunken', bd=1)
        status_frame.pack(fill='x', padx=20, pady=(0, 10))
        
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_label = tk.Label(status_frame, textvariable=self.status_var, bg='#ecf0f1', 
                            font=('Arial', 9), anchor='w')
        status_label.pack(side='left', padx=10, pady=2)
        
        # Total revenue display
        self.revenue_var = tk.StringVar()
        revenue_label = tk.Label(status_frame, textvariable=self.revenue_var, bg='#ecf0f1',
                                font=('Arial', 9, 'bold'), fg='#27ae60', anchor='e')
        revenue_label.pack(side='right', padx=10, pady=2)
        
        # Load initial data
        self.load_transaksi()
        self.load_combo_data()
        
    
    # Customer CRUD Methods
    def load_customers(self):
        # Clear existing items
        for item in self.customer_tree.get_children():
            self.customer_tree.delete(item)
        
        # Load customers from database
        customers = self.db.get_all_customers()
        for customer in customers:
            self.customer_tree.insert('', 'end', values=customer)
    
    def on_customer_select(self, event):
        selection = self.customer_tree.selection()
        if selection:
            item = self.customer_tree.item(selection[0])
            values = item['values']
            
            # Fill form fields
            self.customer_entries['id'].delete(0, tk.END)
            self.customer_entries['id'].insert(0, values[0])
            self.customer_entries['nama'].delete(0, tk.END)
            self.customer_entries['nama'].insert(0, values[1])
            self.customer_entries['alamat'].delete(0, tk.END)
            self.customer_entries['alamat'].insert(0, values[2])
            self.customer_entries['telepon'].delete(0, tk.END)
            self.customer_entries['telepon'].insert(0, values[3])

    
    def add_customer(self):
        id = self.customer_entries['id'].get().strip()
        nama = self.customer_entries['nama'].get().strip()
        alamat = self.customer_entries['alamat'].get().strip()
        telepon = self.customer_entries['telepon'].get().strip()
        
        if not all([id, nama, alamat, telepon]):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        if self.db.create_customer(id, nama, alamat, telepon):
            messagebox.showinfo("Success", "Customer added successfully!")
            self.clear_customer_fields()
            self.load_customers()
            self.load_combo_data()
        else:
            messagebox.showerror("Error", "Failed to add customer!")
    
    def update_customer(self):
        selection = self.customer_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select a customer to update!")
            return
        
        item = self.customer_tree.item(selection[0])
        customer_id = item['values'][0]
        
        id = self.customer_entries['id'].get().strip()
        nama = self.customer_entries['nama'].get().strip()
        alamat = self.customer_entries['alamat'].get().strip()
        telepon = self.customer_entries['telepon'].get().strip()
        
        if not all([id, nama, alamat, telepon]):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        if self.db.update_customer(customer_id, id, nama, alamat, telepon):
            messagebox.showinfo("Success", "Customer updated successfully!")
            self.clear_customer_fields()
            self.load_customers()
            self.load_combo_data()
        else:
            messagebox.showerror("Error", "Failed to update customer!")
    
    def delete_customer(self):
        selection = self.customer_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select a customer to delete!")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this customer?"):
            item = self.customer_tree.item(selection[0])
            customer_id = item['values'][0]
            
            if self.db.delete_customer(customer_id):
                messagebox.showinfo("Success", "Customer deleted successfully!")
                self.clear_customer_fields()
                self.load_customers()
                self.load_combo_data()
            else:
                messagebox.showerror("Error", "Failed to delete customer!")
    
    def clear_customer_fields(self):
        for entry in self.customer_entries.values():
            entry.delete(0, tk.END)
    
    # Barang CRUD Methods
    def load_barang(self):
        # Clear existing items
        for item in self.barang_tree.get_children():
            self.barang_tree.delete(item)
        
        # Load barang from database
        barang_list = self.db.get_all_barang()
        for barang in barang_list:
            self.barang_tree.insert('', 'end', values=barang)
    
    def on_barang_select(self, event):
        selection = self.barang_tree.selection()
        if selection:
            item = self.barang_tree.item(selection[0])
            values = item['values']
            
            # Fill form fields
            self.barang_entries['id'].delete(0, tk.END)
            self.barang_entries['id'].insert(0, values[0])
            self.barang_entries['nama_barang'].delete(0, tk.END)
            self.barang_entries['nama_barang'].insert(0, values[1])
            self.barang_entries['harga'].delete(0, tk.END)
            self.barang_entries['harga'].insert(0, values[2])
            self.barang_entries['stok'].delete(0, tk.END)
            self.barang_entries['stok'].insert(0, values[3])
    
    def add_barang(self):
        id = self.barang_entries['id'].get().strip()
        nama_barang = self.barang_entries['nama_barang'].get().strip()
        harga = self.barang_entries['harga'].get().strip()
        stok = self.barang_entries['stok'].get().strip()
        
        if not all([id, nama_barang, harga, stok]):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        try:
            harga = float(harga)
            stok = int(stok)
        except ValueError:
            messagebox.showerror("Error", "Invalid price or stock value!")
            return
        
        if self.db.create_barang(id, nama_barang, harga, stok):
            messagebox.showinfo("Success", "Barang added successfully!")
            self.clear_barang_fields()
            self.load_barang()
            self.load_combo_data()
        else:
            messagebox.showerror("Error", "Failed to add barang!")
    
    def update_barang(self):
        selection = self.barang_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select a barang to update!")
            return
        
        item = self.barang_tree.item(selection[0])
        barang_id = item['values'][0]
        
        id = self.barang_entries['id'].get().strip()
        nama_barang = self.barang_entries['nama_barang'].get().strip()
        harga = self.barang_entries['harga'].get().strip()
        stok = self.barang_entries['stok'].get().strip()
        
        if not all([id, nama_barang, harga, stok]):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        try:
            harga = float(harga)
            stok = int(stok)
        except ValueError:
            messagebox.showerror("Error", "Invalid price or stock value!")
            return
        
        if self.db.update_barang(barang_id, id, nama_barang, harga, stok):
            messagebox.showinfo("Success", "Barang updated successfully!")
            self.clear_barang_fields()
            self.load_barang()
            self.load_combo_data()
        else:
            messagebox.showerror("Error", "Failed to update barang!")
    
    def delete_barang(self):
        selection = self.barang_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select a barang to delete!")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this barang?"):
            item = self.barang_tree.item(selection[0])
            barang_id = item['values'][0]
            
            if self.db.delete_barang(barang_id):
                messagebox.showinfo("Success", "Barang deleted successfully!")
                self.clear_barang_fields()
                self.load_barang()
                self.load_combo_data()
            else:
                messagebox.showerror("Error", "Failed to delete barang!")
    
    def clear_barang_fields(self):
        for entry in self.barang_entries.values():
            entry.delete(0, tk.END)
    
    # Transaksi Methods
    # Fixed Transaksi Methods
    def load_transaksi(self):
        try:
            # Clear existing items
            for item in self.transaksi_tree.get_children():
                self.transaksi_tree.delete(item)
            
            # Load transaksi dari database dan urutkan berdasarkan ID
            query = """
            SELECT t.id, c.nama, b.nama, b.harga, t.jumlah, t.total, t.tanggal
            FROM transaksi t
            JOIN customer c ON t.customer_id = c.id
            JOIN barang b ON t.barang_id = b.id
            ORDER BY t.id ASC
            """
            
            transaksi_list = self.db.fetch_all(query)
            total_revenue = 0
            
            for transaksi in transaksi_list:
                formatted_data = (
                    transaksi[0],  # ID
                    transaksi[1],  # Customer name
                    transaksi[2],  # Barang name
                    f"Rp {transaksi[3]:,.0f}",  # Harga satuan
                    transaksi[4],  # Jumlah
                    f"Rp {transaksi[5]:,.0f}",  # Total
                    transaksi[6].strftime("%d/%m/%Y %H:%M") if transaksi[6] else ""  # Tanggal
                )
                self.transaksi_tree.insert('', 'end', values=formatted_data)
                total_revenue += transaksi[5]

            
            # Update status and revenue
            count = len(transaksi_list)
            self.status_var.set(f"Total Transaksi: {count}")
            self.revenue_var.set(f"Total Revenue: Rp {total_revenue:,.0f}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load transaksi: {str(e)}")

    def load_combo_data(self):
        try:
            # Load customers for combobox
            customers = self.db.get_all_customers()
            customer_values = [f"{c[0]} - {c[1]}" for c in customers]
            self.customer_combo['values'] = customer_values
            
            # Load barang for combobox - Fixed the column index
            barang_list = self.db.get_all_barang()
            barang_values = [f"{b[0]} - {b[1]} (Stok: {b[3]}, Rp {b[2]:,.0f})" for b in barang_list]
            self.barang_combo['values'] = barang_values
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load combo data: {str(e)}")

    def calculate_total(self, event=None):
        try:
            barang_selection = self.barang_var.get()
            jumlah_str = self.jumlah_entry.get().strip()
            
            if barang_selection and jumlah_str:
                # Extract barang price from selection
                # Format: "ID - Nama (Stok: X, Rp Y)"
                price_part = barang_selection.split("Rp ")[-1].rstrip(")")
                price = float(price_part.replace(",", ""))
                jumlah = int(jumlah_str)
                
                total = price * jumlah
                self.total_var.set(f"Rp {total:,.0f}")
            else:
                self.total_var.set("Rp 0")
                
        except (ValueError, IndexError):
            self.total_var.set("Rp 0")

    def on_transaksi_select(self, event):
        selection = self.transaksi_tree.selection()
        if selection:
            item = self.transaksi_tree.item(selection[0])
            values = item['values']
            
            try:
                # Get the original data from database
                transaksi_id = values[0]
                query = """
                SELECT t.customer_id, t.barang_id, t.jumlah, c.nama, b.nama, b.harga
                FROM transaksi t
                JOIN customer c ON t.customer_id = c.id
                JOIN barang b ON t.barang_id = b.id
                WHERE t.id = %s
                """
                result = self.db.fetch_one(query, (transaksi_id,))
                
                if result:
                    customer_id, barang_id, jumlah, customer_name, barang_name, harga = result
                    
                    # Set combobox values
                    self.customer_var.set(f"{customer_id} - {customer_name}")
                    self.barang_var.set(f"{barang_id} - {barang_name} (Stok: -, Rp {harga:,.0f})")
                    self.jumlah_entry.delete(0, tk.END)
                    self.jumlah_entry.insert(0, str(jumlah))
                    
                    # Calculate and display total
                    self.calculate_total()
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load transaction data: {str(e)}")



    def add_transaksi(self):
        try:
            customer_selection = self.customer_var.get()
            barang_selection = self.barang_var.get()
            jumlah = self.jumlah_entry.get().strip()
            
            if not all([customer_selection, barang_selection, jumlah]):
                messagebox.showerror("Error", "All fields are required!")
                return
            
            jumlah = int(jumlah)
            if jumlah <= 0:
                messagebox.showerror("Error", "Quantity must be greater than 0!")
                return
                
            customer_id = int(customer_selection.split(' - ')[0])
            barang_id = int(barang_selection.split(' - ')[0])
            
            # Check stock availability
            barang_data = self.db.fetch_one("SELECT harga, stok FROM barang WHERE id = %s", (barang_id,))
            if not barang_data:
                messagebox.showerror("Error", "Barang not found!")
                return
            
            harga, stok = barang_data
            if jumlah > stok:
                messagebox.showerror("Error", f"Insufficient stock! Available: {stok}")
                return
            
            total = harga * jumlah
            tanggal = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Atau format lain sesuai DB
            
            # Create transaction dengan parameter lengkap
            if self.db.create_transaksi(customer_id, barang_id, jumlah, total, tanggal):
                # Update stock
                new_stok = stok - jumlah
                self.db.execute_query("UPDATE barang SET stok = %s WHERE id = %s", (new_stok, barang_id))
                
                messagebox.showinfo("Success", f"Transaksi added successfully!\nTotal: Rp {total:,.0f}")
                self.clear_transaksi_fields()
                self.load_transaksi()
                self.load_combo_data()  # Refresh to show updated stock
                self.update_dashboard()
            else:
                messagebox.showerror("Error", "Failed to add transaksi!")
                
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity value!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add transaksi: {str(e)}")


    def delete_transaksi(self):
        selection = self.transaksi_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select a transaksi to delete!")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this transaksi?"):
            try:
                item = self.transaksi_tree.item(selection[0])
                transaksi_id = item['values'][0]
                
                # Get transaction data to restore stock
                trans_data = self.db.fetch_one("SELECT barang_id, jumlah FROM transaksi WHERE id = %s", (transaksi_id,))
                if trans_data:
                    barang_id, jumlah = trans_data
                    
                    # Get current stock
                    barang_data = self.db.fetch_one("SELECT stok FROM barang WHERE id = %s", (barang_id,))
                    if barang_data:
                        current_stok = barang_data[0]
                        new_stok = current_stok + jumlah
                        
                        # Delete transaction and restore stock
                        if self.db.delete_transaksi(transaksi_id):
                            self.db.execute_query("UPDATE barang SET stok = %s WHERE id = %s", (new_stok, barang_id))
                            messagebox.showinfo("Success", "Transaksi deleted successfully!")
                            self.clear_transaksi_fields()
                            self.load_transaksi()
                            self.load_combo_data()
                            self.update_dashboard()
                        else:
                            messagebox.showerror("Error", "Failed to delete transaksi!")
                else:
                    messagebox.showerror("Error", "Transaction data not found!")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete transaksi: {str(e)}")

    def clear_transaksi_fields(self):
        self.customer_var.set('')
        self.barang_var.set('')
        self.jumlah_entry.delete(0, tk.END)
        self.total_var.set("Rp 0")

    def refresh_transaksi(self):
        self.load_transaksi()
        self.load_combo_data()
        self.clear_transaksi_fields()
        messagebox.showinfo("Info", "Data refreshed successfully!")

    def search_transaksi(self):
        search_term = self.search_var.get().strip()
        if not search_term:
            messagebox.showwarning("Warning", "Please enter a search term!")
            return
        
        try:
            # Clear existing items
            for item in self.transaksi_tree.get_children():
                self.transaksi_tree.delete(item)
            
            # Search in database
            query = """
            SELECT t.id, c.nama, b.nama, b.harga, t.jumlah, t.total, t.tanggal
            FROM transaksi t
            JOIN customer c ON t.customer_id = c.id
            JOIN barang b ON t.barang_id = b.id
            WHERE c.nama LIKE %s OR b.nama LIKE %s OR t.id LIKE %s
            ORDER BY t.tanggal DESC
            """
            
            search_pattern = f"%{search_term}%"
            results = self.db.fetch_all(query, (search_pattern, search_pattern, search_pattern))
            
            for transaksi in results:
                formatted_data = (
                    transaksi[0],  # ID
                    transaksi[1],  # Customer name
                    transaksi[2],  # Barang name
                    f"Rp {transaksi[3]:,.0f}",  # Harga satuan
                    transaksi[4],  # Jumlah
                    f"Rp {transaksi[5]:,.0f}",  # Total
                    transaksi[6].strftime("%d/%m/%Y %H:%M") if transaksi[6] else ""  # Tanggal
                )
                self.transaksi_tree.insert('', 'end', values=formatted_data)
            
            self.status_var.set(f"Search results: {len(results)} found")
            
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {str(e)}")

    def sort_column(self, col):
        try:
            # Get all items
            items = [(self.transaksi_tree.set(child, col), child) for child in self.transaksi_tree.get_children('')]
            
            # Sort items
            items.sort(reverse=getattr(self.sort_column, f'{col}_reverse', False))
            
            # Rearrange items
            for index, (val, child) in enumerate(items):
                self.transaksi_tree.move(child, '', index)
            
            # Toggle sort direction
            setattr(self.sort_column, f'{col}_reverse', not getattr(self.sort_column, f'{col}_reverse', False))
            
        except Exception as e:
            pass  # Ignore sorting errors
        
        def delete_transaksi(self):
            selection = self.transaksi_tree.selection()
            if not selection:
                messagebox.showerror("Error", "Please select a transaksi to delete!")
                return
            
            if messagebox.askyesno("Confirm", "Are you sure you want to delete this transaksi?"):
                item = self.transaksi_tree.item(selection[0])
                transaksi_id = item['values'][0]
                
                if self.db.delete_transaksi(transaksi_id):
                    messagebox.showinfo("Success", "Transaksi deleted successfully!")
                    self.load_transaksi()
                else:
                    messagebox.showerror("Error", "Failed to delete transaksi!")
    def logout(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to logout?"):
            # Hentikan auto refresh job
            if hasattr(self, 'refresh_job'):
                try:
                    self.dashboard_parent.after_cancel(self.refresh_job)
                except:
                    pass
            
            self.window.destroy()
            from login import LoginWindow
            LoginWindow().run()

# For testing purposes
if __name__ == "__main__":
    # Test user data
    test_Admin = {
        'id': 1,
        'username': 'test',
        'password': "user",
        'role': 'admin'
    }
    AdminPanel(test_Admin)