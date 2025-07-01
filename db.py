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
    
    # def hash_password(self, password):
    #     """Hash password menggunakan SHA-256"""
    #     return hashlib.sha256(password.encode()).hexdigest()
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
    
    # CRUD Operations untuk Customer
# CRUD Operations untuk Customer
    def create_customer(self, id, nama, alamat, telepon):
        query = "INSERT INTO customer (id, nama, alamat, telepon) VALUES (%s, %s, %s, %s)"
        return self.execute_query(query, (id, nama, alamat, telepon))

    def get_all_customers(self):
        query = "SELECT * FROM customer ORDER BY id"
        return self.fetch_all(query)

    def update_customer(self, customer_id, id,  nama, alamat, telepon):
        query = "UPDATE customer SET id = %s, nama = %s, alamat = %s, telepon = %s WHERE id = %s"
        return self.execute_query(query, (id, nama, alamat, telepon, customer_id))

    def delete_customer(self, customer_id):
        query = "DELETE FROM customer WHERE id = %s"
        return self.execute_query(query, (customer_id,))

    
    # CRUD Operations untuk Barang
    def create_barang(self, id, nama_barang, harga, stok):
        query = "INSERT INTO barang (nama_barang, harga, stok) VALUES (%s, %s, %s, %s)"
        return self.execute_query(query, (id, nama_barang, harga, stok))
    
    def get_all_barang(self):
        query = "SELECT * FROM barang ORDER BY id"
        return self.fetch_all(query)
    
    def update_barang(self, barang_id, id,  nama_barang, harga, stok):
        query = "UPDATE barang SET  id = %s, nama_barang = %s, kategori = %s, harga = %s, stok = %s WHERE id = %s"
        return self.execute_query(query, (id, nama_barang, harga, stok, barang_id))
    
    def delete_barang(self, barang_id):
        query = "DELETE FROM barang WHERE id = %s"
        return self.execute_query(query, (barang_id,))
    
    # CRUD Operations untuk Transaksi
    def create_transaksi(self, customer_id, barang_id, jumlah, total, tanggal):
        query = "INSERT INTO transaksi (customer_id, barang_id, jumlah, total, tanggal) VALUES (%s, %s, %s, %s, %s)"
        values = (customer_id, barang_id, jumlah, total, tanggal)
        return self.execute_query(query, values)


    def get_all_transaksi(self):
        query = """
        SELECT t.id, c.nama AS customer_nama, b.nama AS nama_barang,
            t.jumlah, t.total, t.tanggal
        FROM transaksi t
        JOIN customer c ON t.customer_id = c.id
        JOIN barang b ON t.barang_id = b.id
        ORDER BY t.tanggal DESC
        """
        return self.fetch_all(query)

    
    def delete_transaksi(self, transaksi_id):
        query = "DELETE FROM transaksi WHERE id = %s"
        return self.execute_query(query, (transaksi_id,))