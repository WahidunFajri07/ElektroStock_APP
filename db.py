import mysql.connector
from mysql.connector import Error
import hashlib
from datetime import datetime

class Database:
    def __init__(self):
        self.host = 'localhost'
        self.database = 'wahid_app'
        self.user = 'root'  # Sesuaikan dengan username MySQL Anda
        self.password = ''  # Sesuaikan dengan password MySQL Anda
        self.connection = None
    
    def connect(self):
        """Membuat koneksi ke database"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                return True
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return False
    
    def disconnect(self):
        """Menutup koneksi database"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def create_pengguna(self, username, password, role):
        query = "INSERT INTO pengguna (username, password, role) VALUES (%s, %s, %s)"
        return self.execute_query(query, (username, password, role))

    def authenticate_user(self, username, password):
        """Login tanpa hash"""
        if not self.connect():
            return None

        try:
            cursor = self.connection.cursor()
            
            query = "SELECT id, username, role FROM pengguna WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))  # password langsung cocokkan
            result = cursor.fetchone()
            
            if result:
                return {'id': result[0], 'username': result[1], 'role': result[2]}
            return None

        except Error as e:
            print(f"Error during authentication: {e}")
            return None
        finally:
            cursor.close()
            self.disconnect()

    def mask_phone(self, phone):
        """Menyamarkan nomor telepon: 081234567890 -> 0812****7890"""
        if not phone or len(phone) < 6:
            return phone
        return phone[:4] + "*" * (len(phone) - 6) + phone[-2:]
    
    def mask_address(self, address):
        """Menyamarkan alamat: hanya menampilkan 3 kata pertama"""
        if not address:
            return address
        words = address.split()
        if len(words) <= 3:
            return address
        return " ".join(words[:3]) + " ..."
    
    def mask_sensitive_data(self, data, role):
        """Menyamarkan data sensitif berdasarkan role"""
        if role == 'user':
            return data  # Admin bisa melihat semua data
        
        if isinstance(data, list):
            masked_data = []
            for row in data:
                if isinstance(row, tuple) and len(row) >= 4:
                    # Asumsi format: (id, nama, alamat, telepon)
                    masked_row = (
                        row[0],  # id
                        row[1],  # nama
                        self.mask_address(row[2]),  # alamat
                        self.mask_phone(row[3])     # telepon
                    )
                    masked_data.append(masked_row)
                else:
                    masked_data.append(row)
            return masked_data
        return data
    
    def execute_query(self, query, params=None):
        """Eksekusi query dengan parameter"""
        if not self.connect():
            return False
        
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error executing query: {e}")
            return False
        finally:
            cursor.close()
            self.disconnect()
    
    def fetch_all(self, query, params=None):
        """Mengambil semua data dari query"""
        if not self.connect():
            return []
        
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"Error fetching data: {e}")
            return []
        finally:
            cursor.close()
            self.disconnect()
    
    def fetch_one(self, query, params=None):
        """Mengambil satu data dari query"""
        if not self.connect():
            return None
        
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchone()
            return result
        except Error as e:
            print(f"Error fetching data: {e}")
            return None
        finally:
            cursor.close()
            self.disconnect()
    
    # CRUD Operations untuk Customer dengan keamanan role
    def create_customer(self, id, nama, alamat, telepon):
        query = "INSERT INTO customer (id, nama, alamat, telepon) VALUES (%s, %s, %s, %s)"
        return self.execute_query(query, (id, nama, alamat, telepon))

    def get_all_customers(self, user_role='user'):
        """Mengambil semua customer dengan penyamaran data untuk role user"""
        query = "SELECT * FROM customer ORDER BY id"
        data = self.fetch_all(query)
        return self.mask_sensitive_data(data, user_role)

    def get_customer_by_id(self, customer_id, user_role='user'):
        """Mengambil customer berdasarkan ID dengan penyamaran data untuk role user"""
        query = "SELECT * FROM customer WHERE id = %s"
        data = self.fetch_one(query, (customer_id,))
        if data and user_role == 'user':
            # Menyamarkan data untuk single record
            return (
                data[0],  # id
                data[1],  # nama
                self.mask_address(data[2]),  # alamat
                self.mask_phone(data[3])     # telepon
            )
        return data

    def update_customer(self, customer_id, id, nama, alamat, telepon):
        query = "UPDATE customer SET id = %s, nama = %s, alamat = %s, telepon = %s WHERE id = %s"
        return self.execute_query(query, (id, nama, alamat, telepon, customer_id))

    def delete_customer(self, customer_id):
        query = "DELETE FROM customer WHERE id = %s"
        return self.execute_query(query, (customer_id,))

    # CRUD Operations untuk Barang
    def create_barang(self, id, nama_barang, harga, stok):
        query = "INSERT INTO barang (id, nama, harga, stok) VALUES (%s, %s, %s, %s)"
        return self.execute_query(query, (id, nama_barang, harga, stok))
    
    def get_all_barang(self):
        query = "SELECT * FROM barang ORDER BY id"
        return self.fetch_all(query)
    
    def update_barang(self, barang_id, id, nama_barang, harga, stok):
        query = "UPDATE barang SET id = %s, nama = %s, harga = %s, stok = %s WHERE id = %s"
        return self.execute_query(query, (id, nama_barang, harga, stok, barang_id))
    
    def delete_barang(self, barang_id):
        query = "DELETE FROM barang WHERE id = %s"
        return self.execute_query(query, (barang_id,))
    
    # CRUD Operations untuk Transaksi dengan keamanan role
    def create_transaksi(self, customer_id, barang_id, jumlah, total, tanggal):
        query = "INSERT INTO transaksi (customer_id, barang_id, jumlah, total, tanggal) VALUES (%s, %s, %s, %s, %s)"
        values = (customer_id, barang_id, jumlah, total, tanggal)
        return self.execute_query(query, values)

    def get_all_transaksi(self, user_role='user'):
        """Mengambil semua transaksi dengan penyamaran data customer untuk role user"""
        if user_role == 'admin':
            query = """
            SELECT t.id, c.nama AS customer_nama, b.nama AS nama_barang,
                t.jumlah, t.total, t.tanggal, c.alamat, c.telepon
            FROM transaksi t
            JOIN customer c ON t.customer_id = c.id
            JOIN barang b ON t.barang_id = b.id
            ORDER BY t.tanggal DESC
            """
        else:
            # Untuk user biasa, tidak menampilkan alamat dan telepon customer
            query = """
            SELECT t.id, c.nama AS customer_nama, b.nama AS nama_barang,
                t.jumlah, t.total, t.tanggal
            FROM transaksi t
            JOIN customer c ON t.customer_id = c.id
            JOIN barang b ON t.barang_id = b.id
            ORDER BY t.tanggal DESC
            """
        return self.fetch_all(query)

    def get_transaksi_summary(self, user_role='user'):
        """Mendapatkan ringkasan transaksi (aman untuk semua role)"""
        query = """
        SELECT 
            COUNT(*) as total_transaksi,
            SUM(total) as total_penjualan,
            AVG(total) as rata_rata_transaksi
        FROM transaksi
        """
        return self.fetch_one(query)

    def get_top_customers(self, user_role='user', limit=5):
        """Mendapatkan top customer berdasarkan total pembelian"""
        if user_role == 'admin':
            query = """
            SELECT c.id, c.nama, c.alamat, c.telepon, 
                   COUNT(t.id) as total_transaksi,
                   SUM(t.total) as total_pembelian
            FROM customer c
            LEFT JOIN transaksi t ON c.id = t.customer_id
            GROUP BY c.id, c.nama, c.alamat, c.telepon
            ORDER BY total_pembelian DESC
            LIMIT %s
            """
        else:
            query = """
            SELECT c.id, c.nama,
                   COUNT(t.id) as total_transaksi,
                   SUM(t.total) as total_pembelian
            FROM customer c
            LEFT JOIN transaksi t ON c.id = t.customer_id
            GROUP BY c.id, c.nama
            ORDER BY total_pembelian DESC
            LIMIT %s
            """
        return self.fetch_all(query, (limit,))

    def delete_transaksi(self, transaksi_id):
        query = "DELETE FROM transaksi WHERE id = %s"
        return self.execute_query(query, (transaksi_id,))

    # Method untuk validasi akses berdasarkan role
    def check_admin_access(self, user_role):
        """Mengecek apakah user memiliki akses admin"""
        return user_role == 'admin'
    
    def check_write_access(self, user_role, operation):
        """Mengecek apakah user memiliki akses write untuk operasi tertentu"""
        if user_role == 'admin':
            return True
        
        # User biasa hanya bisa membuat transaksi
        if operation == 'create_transaksi':
            return True
        
        return False