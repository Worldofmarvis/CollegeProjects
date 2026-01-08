import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime


class ShoeShopManagementSystem:
    """
    Main application class for Shoe Shop Management System.
    
    This class handles the complete GUI application including:
    - Database initialization and management
    - User interface creation and navigation
    - Business logic for all shop operations
    - Real-time data visualization and reporting
    """
    
    def __init__(self, root):
        """
        Initialize the application with main window and setup components.
        """
        self.root = root
        self.root.title("BARAKO KICKS - Shoe Shop Management System")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f5f7fa')
        
        # UI color scheme
        self.colors = {
            'background': '#f5f7fa',
            'card_bg': '#ffffff',
            'primary': '#3498db',
            'secondary': '#7f8c8d',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'text_dark': '#2c3e50',
            'text_light': '#666666',
            'text_white': '#ffffff',
            'border': '#e1e8ed',
            'hover': '#ecf0f1',
            'card_header': '#34495e',
            'chart1': '#3498db',
            'chart2': '#2ecc71',
            'chart3': '#e74c3c',
            'chart4': '#f39c12',
        }
        
        # Professional button colors
        self.button_colors = {
            'add': '#28a745',
            'update': '#007bff',
            'delete': '#dc3545',
            'clear': '#6c757d',
            'add_hover': '#218838',
            'update_hover': '#0069d9',
            'delete_hover': '#c82333',
            'clear_hover': '#5a6268',
        }
        
        # Database setup
        self.db_name = "shoe_shop.db"
        self.create_tables()
        self.insert_sample_data()
        
        # Navigation state
        self.nav_buttons = []
        self.current_active_nav = 'Dashboard'
        
        # Main container
        self.main_container = tk.Frame(self.root, bg=self.colors['background'])
        self.main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Initialize UI components
        self.create_navigation_header()
        
        self.content_frame = tk.Frame(self.main_container, bg=self.colors['background'])
        self.content_frame.pack(fill='both', expand=True, pady=20)
        
        self.sections = {}
        self.create_dashboard_section()
        self.create_products_section()
        self.create_customers_section()
        self.create_orders_section()
        self.create_inventory_section()
        
        # Show default section
        self.show_section('Dashboard')
        
        self.apply_styles()
    
    def create_navigation_header(self):
        """Create the main navigation header with shop title and menu buttons."""
        header_frame = tk.Frame(self.main_container, bg=self.colors['background'])
        header_frame.pack(fill='x')
        
        # Shop title section
        title_frame = tk.Frame(header_frame, bg=self.colors['background'])
        title_frame.pack(fill='x', padx=20, pady=(20, 10))
        
        title_label = tk.Label(title_frame, text="BARAKO KICKS", 
                              font=('Arial', 32, 'bold'), 
                              bg=self.colors['background'], 
                              fg=self.colors['card_header'])
        title_label.pack(anchor='w')
        
        subtitle_label = tk.Label(title_frame, text="Shoe Shop Management System", 
                                 font=('Arial', 14), 
                                 bg=self.colors['background'], 
                                 fg=self.colors['text_light'])
        subtitle_label.pack(anchor='w')
        
        # Navigation menu
        nav_frame = tk.Frame(header_frame, bg=self.colors['background'])
        nav_frame.pack(fill='x', padx=20, pady=(10, 20))
        
        self.nav_buttons.clear()
        
        nav_items = ['Dashboard', 'Products', 'Customers', 'Orders', 'Inventory']
        for item in nav_items:
            nav_btn = tk.Button(nav_frame, text=item, font=('Arial', 11, 'bold'),
                              bg=self.colors['card_bg'], 
                              fg=self.colors['primary'] if item == 'Dashboard' else self.colors['secondary'],
                              padx=20, pady=8, cursor='hand2', 
                              relief='flat', bd=0, 
                              activebackground=self.colors['hover'],
                              highlightthickness=0,
                              command=lambda x=item: self.switch_to_section(x))
            
            nav_btn.config(borderwidth=2, highlightbackground=self.colors['border'])
            
            nav_btn.bind("<Enter>", lambda e, b=nav_btn: b.config(bg=self.colors['hover']))
            nav_btn.bind("<Leave>", lambda e, b=nav_btn, name=item: 
                        b.config(bg=self.colors['card_bg'], 
                                fg=self.colors['primary'] if name == self.current_active_nav else self.colors['secondary']))
            
            nav_btn.pack(side='left', padx=2)
            self.nav_buttons.append(nav_btn)
    
    def switch_to_section(self, section_name):
        """
        Switch to specified application section.
        """

        self.current_active_nav = section_name
        
        for btn in self.nav_buttons:
            if btn['text'] == section_name:
                btn.config(fg=self.colors['primary'], bg=self.colors['hover'], 
                          borderwidth=2, highlightbackground=self.colors['primary'])
            else:
                btn.config(fg=self.colors['secondary'], bg=self.colors['card_bg'],
                          borderwidth=2, highlightbackground=self.colors['border'])
        
        self.show_section(section_name)
    
    def show_section(self, section_name):
        """
        Display specified section while hiding others.
        """
        for section in self.sections.values():
            section.pack_forget()
        
        if section_name in self.sections:
            self.sections[section_name].pack(fill='both', expand=True)
        
        if section_name == "Dashboard":
            self.refresh_dashboard()
        elif section_name == "Products":
            self.load_products()
        elif section_name == "Customers":
            self.load_customers()
        elif section_name == "Orders":
            self.load_order_customers()
            self.load_order_products()
        elif section_name == "Inventory":
            self.load_inventory()
    
    def create_tables(self):
        """Create SQLite database tables if they don't exist."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Categories (
                category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_name VARCHAR(50) NOT NULL,
                description TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Suppliers (
                supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
                supplier_name VARCHAR(100) NOT NULL,
                contact_person VARCHAR(100),
                phone VARCHAR(20),
                email VARCHAR(100),
                address TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name VARCHAR(100) NOT NULL,
                category_id INTEGER,
                supplier_id INTEGER,
                brand VARCHAR(50),
                size DECIMAL(3,1),
                color VARCHAR(30),
                gender VARCHAR(10),
                price DECIMAL(10,2) NOT NULL,
                cost_price DECIMAL(10,2),
                description TEXT,
                FOREIGN KEY (category_id) REFERENCES Categories(category_id),
                FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Customers (
                customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                email VARCHAR(100),
                phone VARCHAR(20),
                address TEXT,
                registration_date DATE DEFAULT CURRENT_DATE
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Employees (
                employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                email VARCHAR(100),
                phone VARCHAR(20),
                position VARCHAR(50),
                salary DECIMAL(10,2),
                hire_date DATE DEFAULT CURRENT_DATE
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                employee_id INTEGER,
                order_date DATE DEFAULT CURRENT_DATE,
                total_amount DECIMAL(10,2),
                status VARCHAR(20) DEFAULT 'Pending',
                payment_method VARCHAR(30),
                FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
                FOREIGN KEY (employee_id) REFERENCES Employees(employee_id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS OrderDetails (
                order_detail_id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER,
                product_id INTEGER,
                quantity INTEGER NOT NULL,
                unit_price DECIMAL(10,2) NOT NULL,
                subtotal DECIMAL(10,2),
                FOREIGN KEY (order_id) REFERENCES Orders(order_id),
                FOREIGN KEY (product_id) REFERENCES Products(product_id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Inventory (
                inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER UNIQUE,
                quantity INTEGER DEFAULT 0,
                last_restocked DATE,
                min_stock_level INTEGER DEFAULT 10,
                FOREIGN KEY (product_id) REFERENCES Products(product_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def insert_sample_data(self):
        """Insert sample data for demonstration purposes."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM Categories")
        if cursor.fetchone()[0] == 0:
            # Categories
            categories = [
                ('Running Shoes', 'Athletic shoes for running'),
                ('Casual Shoes', 'Everyday casual footwear'),
                ('Formal Shoes', 'Dress shoes for formal occasions'),
                ('Sports Shoes', 'Shoes for various sports'),
                ('Sandals', 'Open footwear for warm weather'),
                ('Slippers', 'Comfortable indoor/outdoor footwear')
            ]
            cursor.executemany("INSERT INTO Categories (category_name, description) VALUES (?, ?)", categories)
            
            # Suppliers
            suppliers = [
                ('Nike Philippines', 'Juan Dela Cruz', '+63-2-8123-4567', 'juan.delacruz@nike.ph', '123 Bonifacio High Street, Taguig City, Metro Manila'),
                ('Adidas Philippines', 'Maria Santos', '+63-917-123-4567', 'maria.santos@adidas.ph', '456 SM Megamall, Ortigas Center, Mandaluyong City'),
                ('Puma Philippines', 'Roberto Reyes', '+63-2-8234-5678', 'roberto.reyes@puma.ph', '789 Ayala Center, Makati City, Metro Manila'),
                ('Skechers Philippines', 'Lisa Tan', '+63-918-234-5678', 'lisa.tan@skechers.ph', '101 Robinsons Place, Ermita, Manila'),
                ('World Balance', 'Carlos Lim', '+63-2-8765-4321', 'carlos.lim@worldbalance.ph', '555 Quezon Avenue, Quezon City'),
                ('San Marino', 'Andrea Gomez', '+63-919-345-6789', 'andrea.gomez@sanmarino.ph', '777 Pioneer Street, Mandaluyong City')
            ]
            cursor.executemany("INSERT INTO Suppliers (supplier_name, contact_person, phone, email, address) VALUES (?, ?, ?, ?, ?)", suppliers)
            
            # Products
            products = [
                ('Air Max 270', 1, 1, 'Nike', 10.5, 'Black/White', 'Men', 5499.99, 3299.99, 'Running shoes with Max Air cushioning'),
                ('Ultraboost 22', 1, 2, 'Adidas', 9.0, 'Blue', 'Women', 6799.99, 4099.99, 'Responsive running shoes'),
                ('Classic Leather', 2, 3, 'Puma', 11.0, 'White', 'Men', 2999.99, 1799.99, 'Iconic casual shoes'),
                ('Go Walk 5', 2, 4, 'Skechers', 8.5, 'Gray', 'Women', 2499.99, 1499.99, 'Comfortable walking shoes'),
                ('Court Royale', 3, 1, 'Nike', 10.0, 'Black', 'Men', 2299.99, 1379.99, 'Classic court-style shoes'),
                ('Predator Freak', 4, 2, 'Adidas', 9.5, 'Red/Black', 'Men', 8999.99, 5399.99, 'Soccer shoes with advanced grip'),
                ('Comfort Slippers', 6, 5, 'World Balance', 9.0, 'Blue/White', 'Unisex', 499.99, 299.99, 'Comfortable everyday slippers'),
                ('Leather Sandals', 5, 6, 'San Marino', 8.0, 'Brown', 'Men', 1299.99, 779.99, 'Premium leather sandals'),
                ('Running Pro', 1, 5, 'World Balance', 10.5, 'Green', 'Men', 1899.99, 1139.99, 'Affordable running shoes'),
                ('School Shoes', 3, 6, 'San Marino', 7.0, 'Black', 'Kids', 999.99, 599.99, 'Durable school shoes')
            ]
            cursor.executemany('''INSERT INTO Products (product_name, category_id, supplier_id, brand, size, color, gender, price, cost_price, description) 
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', products)
            
            # Customers
            customers = [
                ('Juan', 'Dela Cruz', 'juan.delacruz@email.com', '+63-917-111-2233', '123 Rizal Street, Barangay Poblacion, Makati City'),
                ('Maria', 'Santos', 'maria.santos@email.com', '+63-918-222-3344', '456 Mabini Road, Cebu City, Cebu'),
                ('Roberto', 'Reyes', 'roberto.reyes@email.com', '+63-919-333-4455', '789 Quezon Avenue, Quezon City'),
                ('Ana', 'Garcia', 'ana.garcia@email.com', '+63-920-444-5566', '101 Bonifacio Street, Davao City'),
                ('Michael', 'Tan', 'michael.tan@email.com', '+63-921-555-6677', '222 Ortigas Center, Pasig City'),
                ('Sofia', 'Lim', 'sofia.lim@email.com', '+63-922-666-7788', '333 Alabang, Muntinlupa City'),
                ('Jose', 'Gonzales', 'jose.gonzales@email.com', '+63-923-777-8899', '444 Taft Avenue, Manila'),
                ('Carmen', 'Torres', 'carmen.torres@email.com', '+63-924-888-9900', '555 Pioneer Street, Mandaluyong'),
                ('Pedro', 'Aquino', 'pedro.aquino@email.com', '+63-925-999-0011', '666 Commonwealth Avenue, Quezon City'),
                ('Lourdes', 'Fernandez', 'lourdes.fernandez@email.com', '+63-926-000-1122', '777 Katipunan Avenue, Quezon City')
            ]
            cursor.executemany("INSERT INTO Customers (first_name, last_name, email, phone, address) VALUES (?, ?, ?, ?, ?)", customers)
            
            # Employees
            employees = [
                ('Alice', 'Cruz', 'alice@barakokicks.ph', '+63-917-123-4567', 'Store Manager', 35000.00),
                ('Charlie', 'David', 'charlie@barakokicks.ph', '+63-918-234-5678', 'Sales Supervisor', 25000.00),
                ('Bianca', 'Ramos', 'bianca@barakokicks.ph', '+63-919-345-6789', 'Sales Associate', 18000.00),
                ('Daniel', 'Mendoza', 'daniel@barakokicks.ph', '+63-920-456-7890', 'Sales Associate', 18000.00),
                ('Elena', 'Sison', 'elena@barakokicks.ph', '+63-921-567-8901', 'Inventory Clerk', 20000.00)
            ]
            cursor.executemany("INSERT INTO Employees (first_name, last_name, email, phone, position, salary) VALUES (?, ?, ?, ?, ?, ?)", employees)
            
            # Inventory
            inventory_data = [
                (1, 45, '2024-01-15', 10),
                (2, 35, '2024-01-10', 8),
                (3, 50, '2024-01-20', 12),
                (4, 40, '2024-01-12', 10),
                (5, 25, '2024-01-18', 8),
                (6, 15, '2024-01-05', 5),
                (7, 100, '2024-01-25', 20),
                (8, 30, '2024-01-22', 10),
                (9, 60, '2024-01-28', 15),
                (10, 40, '2024-01-30', 12)
            ]
            cursor.executemany("INSERT INTO Inventory (product_id, quantity, last_restocked, min_stock_level) VALUES (?, ?, ?, ?)", inventory_data)
            
            # Orders
            orders = [
                (1, 2, '2024-01-20', 5499.99, 'Completed', 'Credit Card'),
                (2, 3, '2024-01-22', 12999.98, 'Completed', 'GCash'),
                (3, 4, '2024-01-25', 2999.99, 'Processing', 'Cash'),
                (4, 2, '2024-01-26', 4999.98, 'Pending', 'Debit Card'),
                (5, 3, '2024-01-28', 4499.98, 'Completed', 'GCash')
            ]
            cursor.executemany("INSERT INTO Orders (customer_id, employee_id, order_date, total_amount, status, payment_method) VALUES (?, ?, ?, ?, ?, ?)", orders)
            
            # Order details
            order_details = [
                (1, 1, 1, 5499.99, 5499.99),
                (2, 2, 1, 6799.99, 6799.99),
                (2, 6, 1, 8999.99, 8999.99),
                (3, 3, 1, 2999.99, 2999.99),
                (4, 1, 2, 5499.99, 10999.98),
                (5, 9, 2, 1899.99, 3799.98),
                (5, 7, 2, 499.99, 999.98)
            ]
            cursor.executemany("INSERT INTO OrderDetails (order_id, product_id, quantity, unit_price, subtotal) VALUES (?, ?, ?, ?, ?)", order_details)
            
            conn.commit()
        
        conn.close()
    
    def apply_styles(self):
        """Apply consistent styling to all UI components."""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Title.TLabel', 
                       font=('Arial', 16, 'bold'), 
                       background=self.colors['background'],
                       foreground=self.colors['text_dark'])
        style.configure('Heading.TLabel', 
                       font=('Arial', 12, 'bold'), 
                       background=self.colors['background'],
                       foreground=self.colors['text_dark'])
        style.configure('TButton', 
                       font=('Arial', 10), 
                       padding=5,
                       background=self.button_colors['update'],
                       foreground=self.colors['text_white'])
        style.configure('Treeview', 
                       font=('Arial', 10), 
                       rowheight=25,
                       background=self.colors['card_bg'],
                       fieldbackground=self.colors['card_bg'],
                       foreground=self.colors['text_dark'],
                       borderwidth=1,
                       relief='solid')
        style.configure('Treeview.Heading', 
                       font=('Arial', 10, 'bold'),
                       background=self.colors['border'],
                       foreground=self.colors['text_dark'],
                       relief='flat')
        style.map('Treeview.Heading',
                 background=[('active', self.colors['hover'])])
        
        style.configure('TCombobox',
                       fieldbackground=self.colors['card_bg'],
                       background=self.colors['card_bg'],
                       foreground=self.colors['text_dark'])
    
    def create_dashboard_section(self):
        """Create the dashboard section with business analytics and statistics."""
        dashboard_frame = tk.Frame(self.content_frame, bg=self.colors['background'])
        self.sections['Dashboard'] = dashboard_frame
        
        stats_frame_top = tk.Frame(dashboard_frame, bg=self.colors['background'])
        stats_frame_top.pack(fill='x', padx=20, pady=10)
        
        total_products, total_customers, total_orders, low_stock = self.get_dashboard_stats()
        total_revenue = self.get_total_revenue()
        avg_order_value = self.get_avg_order_value()
        
        stats_data_top = [
            ("Total Products", f"{total_products}", "+12%", self.colors['chart1']),
            ("Total Customers", f"{total_customers}", "+8%", self.colors['chart2']),
            ("Total Orders", f"{total_orders}", "+23%", self.colors['chart3']),
            ("Low Stock Items", f"{low_stock}", "-5%", self.colors['chart4'])
        ]
        
        self.stats_value_labels = []
        
        for label, value, change, color in stats_data_top:
            card = tk.Frame(stats_frame_top, bg=self.colors['card_bg'], relief='ridge', bd=1)
            card.pack(side='left', fill='both', expand=True, padx=5, ipadx=10, ipady=15)
            
            label_widget = tk.Label(card, text=label, bg=self.colors['card_bg'], 
                                   fg=self.colors['text_light'], font=('Arial', 11))
            label_widget.pack(anchor='w', padx=10, pady=(10, 5))
            
            value_widget = tk.Label(card, text=value, bg=self.colors['card_bg'], 
                                   fg=self.colors['text_dark'], font=('Arial', 28, 'bold'))
            value_widget.pack(anchor='w', padx=10)
            self.stats_value_labels.append(value_widget)
            
            change_color = self.colors['success'] if change.startswith('+') else self.colors['danger']
            change_widget = tk.Label(card, text=change, bg=self.colors['card_bg'], fg=change_color,
                                    font=('Arial', 10, 'bold'))
            change_widget.pack(anchor='w', padx=10, pady=(5, 10))
            
            accent = tk.Frame(card, bg=color, height=4)
            accent.pack(fill='x', side='bottom')
        
        stats_frame_bottom = tk.Frame(dashboard_frame, bg=self.colors['background'])
        stats_frame_bottom.pack(fill='x', padx=20, pady=10)
        
        revenue_card = tk.Frame(stats_frame_bottom, bg=self.colors['card_bg'], relief='ridge', bd=1)
        revenue_card.pack(side='left', fill='both', expand=True, padx=(5, 10), ipadx=20, ipady=15)
        
        tk.Label(revenue_card, text="Total Revenue", bg=self.colors['card_bg'], 
                fg=self.colors['text_light'], font=('Arial', 11)).pack(anchor='w', padx=10, pady=(10, 5))
        
        self.revenue_label = tk.Label(revenue_card, text=f"₱{total_revenue:,.2f}", 
                                     bg=self.colors['card_bg'], fg=self.colors['text_dark'], 
                                     font=('Arial', 32, 'bold'))
        self.revenue_label.pack(anchor='w', padx=10)
        
        tk.Label(revenue_card, text="➤ +18.2% from last month", bg=self.colors['card_bg'], 
                fg=self.colors['success'], font=('Arial', 10, 'bold')).pack(anchor='w', padx=10, pady=(5, 10))
        
        accent1 = tk.Frame(revenue_card, bg=self.colors['chart1'], height=4)
        accent1.pack(fill='x', side='bottom')
        
        avg_card = tk.Frame(stats_frame_bottom, bg=self.colors['card_bg'], relief='ridge', bd=1)
        avg_card.pack(side='left', fill='both', expand=True, padx=(10, 5), ipadx=20, ipady=15)
        
        tk.Label(avg_card, text="Average Order Value", bg=self.colors['card_bg'], 
                fg=self.colors['text_light'], font=('Arial', 11)).pack(anchor='w', padx=10, pady=(10, 5))
        
        self.avg_order_label = tk.Label(avg_card, text=f"₱{avg_order_value:,.2f}", 
                                       bg=self.colors['card_bg'], fg=self.colors['text_dark'], 
                                       font=('Arial', 24, 'bold'))
        self.avg_order_label.pack(anchor='w', padx=10)
        
        tk.Label(avg_card, text="➤ +5.4% from last month", bg=self.colors['card_bg'], 
                fg=self.colors['success'], font=('Arial', 10, 'bold')).pack(anchor='w', padx=10, pady=(5, 10))
        
        accent2 = tk.Frame(avg_card, bg=self.colors['chart2'], height=4)
        accent2.pack(fill='x', side='bottom')
        
        recent_frame = tk.Frame(dashboard_frame, bg=self.colors['background'])
        recent_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        recent_title = tk.Label(recent_frame, text="Recent Orders", bg=self.colors['background'], 
                               font=('Arial', 14, 'bold'), fg=self.colors['text_dark'])
        recent_title.pack(anchor='w', pady=(0, 10))
        
        table_frame = tk.Frame(recent_frame, bg=self.colors['card_bg'], relief='solid', bd=1)
        table_frame.pack(fill='both', expand=True)
        
        columns = ('order_id', 'customer', 'date', 'amount', 'status')
        self.recent_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=8)
        
        headings = ['Order ID', 'Customer', 'Date', 'Amount', 'Status']
        for col, heading in zip(columns, headings):
            self.recent_tree.heading(col, text=heading)
            self.recent_tree.column(col, width=120, anchor='center')
        
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.recent_tree.yview)
        self.recent_tree.configure(yscrollcommand=scrollbar.set)
        
        self.recent_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.load_recent_orders()
    
    def get_dashboard_stats(self):
        """
        Retrieve key performance indicators for dashboard.
        
        Returns:
            tuple: (total_products, total_customers, total_orders, low_stock)
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM Products")
        total_products = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Customers")
        total_customers = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Orders")
        total_orders = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Inventory WHERE quantity < min_stock_level")
        low_stock = cursor.fetchone()[0]
        
        conn.close()
        return total_products, total_customers, total_orders, low_stock
    
    def get_total_revenue(self):
        """
        Calculate total revenue from completed orders.
        
        Returns:
            float: Total revenue amount
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COALESCE(SUM(total_amount), 0) FROM Orders WHERE status = 'Completed'")
        total_revenue = cursor.fetchone()[0] or 0
        
        conn.close()
        return float(total_revenue)
    
    def get_avg_order_value(self):
        """
        Calculate average value of completed orders.
        
        Returns:
            float: Average order value
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COALESCE(AVG(total_amount), 0) FROM Orders WHERE status = 'Completed'")
        avg_value = cursor.fetchone()[0] or 0
        
        conn.close()
        return float(avg_value)
    
    def load_recent_orders(self):
        """Load the 10 most recent orders into dashboard table."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT o.order_id, 
                   c.first_name || ' ' || c.last_name as customer,
                   o.order_date,
                   o.total_amount,
                   o.status
            FROM Orders o
            JOIN Customers c ON o.customer_id = c.customer_id
            ORDER BY o.order_date DESC
            LIMIT 10
        ''')
        
        for item in self.recent_tree.get_children():
            self.recent_tree.delete(item)
        
        for row in cursor.fetchall():
            order_id, customer, date, amount, status = row
            self.recent_tree.insert('', 'end', values=(
                order_id, customer, date, f"₱{amount:,.2f}", status
            ))
        
        conn.close()
    
    def refresh_dashboard(self):
        """Refresh all dashboard statistics and data displays."""
        total_products, total_customers, total_orders, low_stock = self.get_dashboard_stats()
        total_revenue = self.get_total_revenue()
        avg_order_value = self.get_avg_order_value()
        
        if hasattr(self, 'stats_value_labels'):
            stats_values = [total_products, total_customers, total_orders, low_stock]
            for i, value in enumerate(stats_values):
                self.stats_value_labels[i].config(text=str(value))
        
        if hasattr(self, 'revenue_label'):
            self.revenue_label.config(text=f"₱{total_revenue:,.2f}")
        if hasattr(self, 'avg_order_label'):
            self.avg_order_label.config(text=f"₱{avg_order_value:,.2f}")
        
        self.load_recent_orders()
    
    def create_products_section(self):
        """Create product management interface with CRUD operations."""
        products_frame = tk.Frame(self.content_frame, bg=self.colors['background'])
        self.sections['Products'] = products_frame
        
        title_label = tk.Label(products_frame, text="Products Management", 
                              font=('Arial', 16, 'bold'), 
                              bg=self.colors['background'], 
                              fg=self.colors['card_header'])
        title_label.pack(anchor='w', padx=20, pady=(10, 20))
        
        left_frame = tk.Frame(products_frame, bg=self.colors['background'])
        left_frame.pack(side='left', fill='both', padx=20, pady=10)
        
        form_frame = tk.LabelFrame(left_frame, text="Product Details", 
                                  bg=self.colors['card_bg'], 
                                  fg=self.colors['card_header'],
                                  font=('Arial', 12, 'bold'), 
                                  padx=10, pady=10,
                                  relief='ridge', bd=1)
        form_frame.pack(fill='x', pady=(0, 10))
        
        fields = [
            ('product_name', 'Product Name:', 'entry'),
            ('category_id', 'Category:', 'combobox'),
            ('brand', 'Brand:', 'entry'),
            ('size', 'Size:', 'entry'),
            ('color', 'Color:', 'entry'),
            ('gender', 'Gender:', 'combobox'),
            ('price', 'Price (₱):', 'entry'),
            ('cost_price', 'Cost Price (₱):', 'entry'),
            ('description', 'Description:', 'text')
        ]
        
        self.product_vars = {}
        for i, (field, label, widget_type) in enumerate(fields):
            tk.Label(form_frame, text=label, bg=self.colors['card_bg'], 
                    fg=self.colors['text_dark']).grid(row=i, column=0, sticky='w', pady=5)
            
            if widget_type == 'entry':
                var = tk.StringVar()
                entry = tk.Entry(form_frame, textvariable=var, width=30, 
                                bg=self.colors['card_bg'], fg=self.colors['text_dark'],
                                insertbackground=self.colors['primary'])
                entry.grid(row=i, column=1, padx=5, pady=5)
                self.product_vars[field] = var
            
            elif widget_type == 'combobox':
                var = tk.StringVar()
                if field == 'category_id':
                    values = self.get_categories()
                    combobox = ttk.Combobox(form_frame, textvariable=var, values=values, width=27)
                elif field == 'gender':
                    combobox = ttk.Combobox(form_frame, textvariable=var, 
                                          values=['Men', 'Women', 'Unisex', 'Kids'], width=27)
                combobox.grid(row=i, column=1, padx=5, pady=5)
                self.product_vars[field] = var
            
            elif widget_type == 'text':
                text_widget = tk.Text(form_frame, height=4, width=30, 
                                     bg=self.colors['card_bg'], fg=self.colors['text_dark'],
                                     insertbackground=self.colors['primary'])
                text_widget.grid(row=i, column=1, padx=5, pady=5)
                self.product_vars[field] = text_widget
        
        button_frame = tk.Frame(form_frame, bg=self.colors['card_bg'])
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=15)
        
        buttons = [
            ("Add", self.add_product, self.button_colors['add'], self.button_colors['add_hover']),
            ("Update", self.update_product, self.button_colors['update'], self.button_colors['update_hover']),
            ("Delete", self.delete_product, self.button_colors['delete'], self.button_colors['delete_hover']),
            ("Clear", self.clear_product_form, self.button_colors['clear'], self.button_colors['clear_hover'])
        ]
        
        for text, command, color, hover_color in buttons:
            btn = tk.Button(button_frame, text=text, command=command, 
                           bg=color, fg=self.colors['text_white'],
                           padx=20, pady=6, font=('Arial', 10, 'bold'),
                           cursor='hand2', relief='flat', bd=0,
                           activebackground=hover_color)
            btn.pack(side='left', padx=5, ipadx=5)
            
            btn.bind("<Enter>", lambda e, b=btn, c=hover_color: b.config(bg=c))
            btn.bind("<Leave>", lambda e, b=btn, c=color: b.config(bg=c))
            
            btn.config(highlightbackground=color, highlightthickness=1)
        
        right_frame = tk.Frame(products_frame, bg=self.colors['background'])
        right_frame.pack(side='right', fill='both', expand=True, padx=20, pady=10)
        
        search_frame = tk.Frame(right_frame, bg=self.colors['background'])
        search_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(search_frame, text="Search:", bg=self.colors['background'], 
                fg=self.colors['text_dark'], font=('Arial', 10)).pack(side='left', padx=5)
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=30, 
                               bg=self.colors['card_bg'], fg=self.colors['text_dark'],
                               insertbackground=self.colors['primary'],
                               relief='solid', bd=1)
        search_entry.pack(side='left', padx=5)
        search_entry.bind('<KeyRelease>', lambda e: self.search_products())
        
        tree_frame = tk.Frame(right_frame, bg=self.colors['background'])
        tree_frame.pack(fill='both', expand=True)
        
        columns = ('product_id', 'product_name', 'brand', 'size', 'color', 'price', 'category')
        self.product_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=20)
        
        headings = ['ID', 'Product Name', 'Brand', 'Size', 'Color', 'Price', 'Category']
        for col, heading in zip(columns, headings):
            self.product_tree.heading(col, text=heading)
            self.product_tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.product_tree.yview)
        self.product_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        self.product_tree.pack(fill='both', expand=True)
        
        self.product_tree.bind('<<TreeviewSelect>>', self.on_product_select)
    
    def get_categories(self):
        """
        Retrieve list of product categories from database.
        
        Returns:
            list: Category names
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT category_name FROM Categories")
        categories = [row[0] for row in cursor.fetchall()]
        conn.close()
        return categories
    
    def load_products(self):
        """Load all products into the product management table."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.product_id, p.product_name, p.brand, p.size, p.color, p.price, c.category_name
            FROM Products p
            LEFT JOIN Categories c ON p.category_id = c.category_id
            ORDER BY p.product_id
        ''')
        
        if hasattr(self, 'product_tree'):
            for item in self.product_tree.get_children():
                self.product_tree.delete(item)
        
        for row in cursor.fetchall():
            self.product_tree.insert('', 'end', values=(
                row[0], row[1], row[2], row[3], row[4], f"₱{row[5]:,.2f}", row[6]
            ))
        
        conn.close()
    
    def add_product(self):
        """Add new product to database with inventory initialization."""
        try:
            product_name = self.product_vars['product_name'].get()
            category_name = self.product_vars['category_id'].get()
            brand = self.product_vars['brand'].get()
            size = self.product_vars['size'].get()
            color = self.product_vars['color'].get()
            gender = self.product_vars['gender'].get()
            price = float(self.product_vars['price'].get())
            cost_price = float(self.product_vars['cost_price'].get())
            description = self.product_vars['description'].get("1.0", "end-1c")
            
            if not product_name:
                messagebox.showerror("Error", "Product name is required!")
                return
            
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT category_id FROM Categories WHERE category_name = ?", (category_name,))
            result = cursor.fetchone()
            
            if result:
                category_id = result[0]
                
                cursor.execute('''
                    INSERT INTO Products (product_name, category_id, brand, size, color, gender, price, cost_price, description)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (product_name, category_id, brand, size, color, gender, price, cost_price, description))
                
                product_id = cursor.lastrowid
                
                cursor.execute('''
                    INSERT INTO Inventory (product_id, quantity, last_restocked, min_stock_level)
                    VALUES (?, 0, CURRENT_DATE, 10)
                ''', (product_id,))
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", "Product added successfully!")
                self.clear_product_form()
                self.load_products()
                if self.current_active_nav == 'Dashboard':
                    self.refresh_dashboard()
            else:
                messagebox.showerror("Error", "Category not found!")
                
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for price!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def on_product_select(self, event):
        """
        Handle product selection from table to populate form.
        
        Args:
            event: Treeview selection event
        """
        selected_item = self.product_tree.selection()
        if selected_item:
            values = self.product_tree.item(selected_item[0], 'values')
            
            self.clear_product_form()
            
            self.product_vars['product_name'].set(values[1])
            self.product_vars['brand'].set(values[2])
            self.product_vars['size'].set(values[3])
            self.product_vars['color'].set(values[4])
            
            price_str = values[5].replace('₱', '').replace(',', '')
            self.product_vars['price'].set(price_str)
            
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT c.category_name, p.gender, p.cost_price, p.description
                FROM Products p
                LEFT JOIN Categories c ON p.category_id = c.category_id
                WHERE p.product_id = ?
            ''', (values[0],))
            
            result = cursor.fetchone()
            if result:
                self.product_vars['category_id'].set(result[0])
                self.product_vars['gender'].set(result[1])
                self.product_vars['cost_price'].set(str(result[2]))
                self.product_vars['description'].delete("1.0", "end")
                self.product_vars['description'].insert("1.0", result[3] if result[3] else "")
            
            conn.close()
    
    def update_product(self):
        """Update selected product information in database."""
        selected_item = self.product_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a product to update!")
            return
        
        try:
            product_id = self.product_tree.item(selected_item[0], 'values')[0]
            product_name = self.product_vars['product_name'].get()
            category_name = self.product_vars['category_id'].get()
            brand = self.product_vars['brand'].get()
            size = self.product_vars['size'].get()
            color = self.product_vars['color'].get()
            gender = self.product_vars['gender'].get()
            price = float(self.product_vars['price'].get())
            cost_price = float(self.product_vars['cost_price'].get())
            description = self.product_vars['description'].get("1.0", "end-1c")
            
            if not product_name:
                messagebox.showerror("Error", "Product name is required!")
                return
            
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT category_id FROM Categories WHERE category_name = ?", (category_name,))
            result = cursor.fetchone()
            
            if result:
                category_id = result[0]
                
                cursor.execute('''
                    UPDATE Products 
                    SET product_name = ?, category_id = ?, brand = ?, size = ?, color = ?, 
                        gender = ?, price = ?, cost_price = ?, description = ?
                    WHERE product_id = ?
                ''', (product_name, category_id, brand, size, color, gender, price, cost_price, description, product_id))
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", "Product updated successfully!")
                self.load_products()
            else:
                messagebox.showerror("Error", "Category not found!")
                
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for price!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def delete_product(self):
        """Delete selected product from database with validation."""
        selected_item = self.product_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a product to delete!")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this product?"):
            product_id = self.product_tree.item(selected_item[0], 'values')[0]
            
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            try:
                cursor.execute("DELETE FROM Inventory WHERE product_id = ?", (product_id,))
                cursor.execute("DELETE FROM Products WHERE product_id = ?", (product_id,))
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", "Product deleted successfully!")
                self.clear_product_form()
                self.load_products()
                if self.current_active_nav == 'Dashboard':
                    self.refresh_dashboard()
                
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Cannot delete product with existing orders!")
                conn.rollback()
                conn.close()
    
    def clear_product_form(self):
        """Clear all product form fields."""
        for key, var in self.product_vars.items():
            if isinstance(var, tk.StringVar):
                var.set('')
            elif isinstance(var, tk.Text):
                var.delete("1.0", "end")
    
    def search_products(self):
        """Search products based on user input."""
        search_term = self.search_var.get().lower()
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.product_id, p.product_name, p.brand, p.size, p.color, p.price, c.category_name
            FROM Products p
            LEFT JOIN Categories c ON p.category_id = c.category_id
            WHERE LOWER(p.product_name) LIKE ? OR LOWER(p.brand) LIKE ? OR LOWER(c.category_name) LIKE ?
            ORDER BY p.product_id
        ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
        
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
        
        for row in cursor.fetchall():
            self.product_tree.insert('', 'end', values=(
                row[0], row[1], row[2], row[3], row[4], f"₱{row[5]:,.2f}", row[6]
            ))
        
        conn.close()
    
    def create_customers_section(self):
        """Create customer management interface with CRUD operations."""
        customers_frame = tk.Frame(self.content_frame, bg=self.colors['background'])
        self.sections['Customers'] = customers_frame
        
        title_label = tk.Label(customers_frame, text="Customers Management", 
                              font=('Arial', 16, 'bold'), 
                              bg=self.colors['background'], 
                              fg=self.colors['card_header'])
        title_label.pack(anchor='w', padx=20, pady=(10, 20))
        
        left_frame = tk.Frame(customers_frame, bg=self.colors['background'])
        left_frame.pack(side='left', fill='both', padx=20, pady=10)
        
        form_frame = tk.LabelFrame(left_frame, text="Customer Details", 
                                  bg=self.colors['card_bg'], 
                                  fg=self.colors['card_header'],
                                  font=('Arial', 12, 'bold'), 
                                  padx=10, pady=10,
                                  relief='ridge', bd=1)
        form_frame.pack(fill='x', pady=(0, 10))
        
        fields = [
            ('first_name', 'First Name:', 'entry'),
            ('last_name', 'Last Name:', 'entry'),
            ('email', 'Email:', 'entry'),
            ('phone', 'Phone:', 'entry'),
            ('address', 'Address:', 'text')
        ]
        
        self.customer_vars = {}
        for i, (field, label, widget_type) in enumerate(fields):
            tk.Label(form_frame, text=label, bg=self.colors['card_bg'], 
                    fg=self.colors['text_dark']).grid(row=i, column=0, sticky='w', pady=5)
            
            if widget_type == 'entry':
                var = tk.StringVar()
                entry = tk.Entry(form_frame, textvariable=var, width=30, 
                                bg=self.colors['card_bg'], fg=self.colors['text_dark'],
                                insertbackground=self.colors['primary'])
                entry.grid(row=i, column=1, padx=5, pady=5)
                self.customer_vars[field] = var
            
            elif widget_type == 'text':
                text_widget = tk.Text(form_frame, height=3, width=30, 
                                     bg=self.colors['card_bg'], fg=self.colors['text_dark'],
                                     insertbackground=self.colors['primary'])
                text_widget.grid(row=i, column=1, padx=5, pady=5)
                self.customer_vars[field] = text_widget
        
        button_frame = tk.Frame(form_frame, bg=self.colors['card_bg'])
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=15)
        
        buttons = [
            ("Add", self.add_customer, self.button_colors['add'], self.button_colors['add_hover']),
            ("Update", self.update_customer, self.button_colors['update'], self.button_colors['update_hover']),
            ("Delete", self.delete_customer, self.button_colors['delete'], self.button_colors['delete_hover']),
            ("Clear", self.clear_customer_form, self.button_colors['clear'], self.button_colors['clear_hover'])
        ]
        
        for text, command, color, hover_color in buttons:
            btn = tk.Button(button_frame, text=text, command=command, 
                           bg=color, fg=self.colors['text_white'],
                           padx=20, pady=6, font=('Arial', 10, 'bold'),
                           cursor='hand2', relief='flat', bd=0,
                           activebackground=hover_color)
            btn.pack(side='left', padx=5, ipadx=5)
            
            btn.bind("<Enter>", lambda e, b=btn, c=hover_color: b.config(bg=c))
            btn.bind("<Leave>", lambda e, b=btn, c=color: b.config(bg=c))
            
            btn.config(highlightbackground=color, highlightthickness=1)
        
        right_frame = tk.Frame(customers_frame, bg=self.colors['background'])
        right_frame.pack(side='right', fill='both', expand=True, padx=20, pady=10)
        
        search_frame = tk.Frame(right_frame, bg=self.colors['background'])
        search_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(search_frame, text="Search:", bg=self.colors['background'], 
                fg=self.colors['text_dark'], font=('Arial', 10)).pack(side='left', padx=5)
        self.customer_search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.customer_search_var, width=30, 
                               bg=self.colors['card_bg'], fg=self.colors['text_dark'],
                               insertbackground=self.colors['primary'],
                               relief='solid', bd=1)
        search_entry.pack(side='left', padx=5)
        search_entry.bind('<KeyRelease>', lambda e: self.search_customers())
        
        tree_frame = tk.Frame(right_frame, bg=self.colors['background'])
        tree_frame.pack(fill='both', expand=True)
        
        columns = ('customer_id', 'first_name', 'last_name', 'email', 'phone', 'registration_date')
        self.customer_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=20)
        
        headings = ['ID', 'First Name', 'Last Name', 'Email', 'Phone', 'Registration Date']
        for col, heading in zip(columns, headings):
            self.customer_tree.heading(col, text=heading)
            self.customer_tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.customer_tree.yview)
        self.customer_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        self.customer_tree.pack(fill='both', expand=True)
        
        self.customer_tree.bind('<<TreeviewSelect>>', self.on_customer_select)
    
    def load_customers(self):
        """Load all customers into the customer management table."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT customer_id, first_name, last_name, email, phone, registration_date
            FROM Customers
            ORDER BY customer_id
        ''')
        
        if hasattr(self, 'customer_tree'):
            for item in self.customer_tree.get_children():
                self.customer_tree.delete(item)
        
        for row in cursor.fetchall():
            self.customer_tree.insert('', 'end', values=row)
        
        conn.close()
    
    def add_customer(self):
        """Add new customer to database."""
        try:
            first_name = self.customer_vars['first_name'].get()
            last_name = self.customer_vars['last_name'].get()
            email = self.customer_vars['email'].get()
            phone = self.customer_vars['phone'].get()
            address = self.customer_vars['address'].get("1.0", "end-1c")
            
            if not first_name or not last_name:
                messagebox.showerror("Error", "First and last name are required!")
                return
            
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO Customers (first_name, last_name, email, phone, address)
                VALUES (?, ?, ?, ?, ?)
            ''', (first_name, last_name, email, phone, address))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Customer added successfully!")
            self.clear_customer_form()
            self.load_customers()
            if self.current_active_nav == 'Dashboard':
                self.refresh_dashboard()
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def on_customer_select(self, event):
        """
        Handle customer selection from table to populate form.
        
        Args:
            event: Treeview selection event
        """
        selected_item = self.customer_tree.selection()
        if selected_item:
            values = self.customer_tree.item(selected_item[0], 'values')
            
            self.clear_customer_form()
            
            self.customer_vars['first_name'].set(values[1])
            self.customer_vars['last_name'].set(values[2])
            self.customer_vars['email'].set(values[3])
            self.customer_vars['phone'].set(values[4])
            
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT address FROM Customers WHERE customer_id = ?", (values[0],))
            result = cursor.fetchone()
            
            if result and result[0]:
                self.customer_vars['address'].delete("1.0", "end")
                self.customer_vars['address'].insert("1.0", result[0])
            
            conn.close()
    
    def update_customer(self):
        """Update selected customer information in database."""
        selected_item = self.customer_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a customer to update!")
            return
        
        try:
            customer_id = self.customer_tree.item(selected_item[0], 'values')[0]
            first_name = self.customer_vars['first_name'].get()
            last_name = self.customer_vars['last_name'].get()
            email = self.customer_vars['email'].get()
            phone = self.customer_vars['phone'].get()
            address = self.customer_vars['address'].get("1.0", "end-1c")
            
            if not first_name or not last_name:
                messagebox.showerror("Error", "First and last name are required!")
                return
            
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE Customers 
                SET first_name = ?, last_name = ?, email = ?, phone = ?, address = ?
                WHERE customer_id = ?
            ''', (first_name, last_name, email, phone, address, customer_id))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Customer updated successfully!")
            self.load_customers()
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def delete_customer(self):
        """Delete selected customer from database with order validation."""
        selected_item = self.customer_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a customer to delete!")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this customer?"):
            customer_id = self.customer_tree.item(selected_item[0], 'values')[0]
            
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            try:
                cursor.execute("SELECT COUNT(*) FROM Orders WHERE customer_id = ?", (customer_id,))
                order_count = cursor.fetchone()[0]
                
                if order_count > 0:
                    messagebox.showerror("Error", "Cannot delete customer with existing orders!")
                    return
                
                cursor.execute("DELETE FROM Customers WHERE customer_id = ?", (customer_id,))
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", "Customer deleted successfully!")
                self.clear_customer_form()
                self.load_customers()
                if self.current_active_nav == 'Dashboard':
                    self.refresh_dashboard()
                
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
                conn.rollback()
                conn.close()
    
    def clear_customer_form(self):
        """Clear all customer form fields."""
        for key, var in self.customer_vars.items():
            if isinstance(var, tk.StringVar):
                var.set('')
            elif isinstance(var, tk.Text):
                var.delete("1.0", "end")
    
    def search_customers(self):
        """Search customers based on user input."""
        search_term = self.customer_search_var.get().lower()
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT customer_id, first_name, last_name, email, phone, registration_date
            FROM Customers
            WHERE LOWER(first_name) LIKE ? OR LOWER(last_name) LIKE ? OR LOWER(email) LIKE ?
            ORDER BY customer_id
        ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
        
        for item in self.customer_tree.get_children():
            self.customer_tree.delete(item)
        
        for row in cursor.fetchall():
            self.customer_tree.insert('', 'end', values=row)
        
        conn.close()
    
    def create_orders_section(self):
        """Create order management interface with cart functionality."""
        orders_frame = tk.Frame(self.content_frame, bg=self.colors['background'])
        self.sections['Orders'] = orders_frame
        
        title_label = tk.Label(orders_frame, text="Orders Management", 
                              font=('Arial', 16, 'bold'), 
                              bg=self.colors['background'], 
                              fg=self.colors['card_header'])
        title_label.pack(anchor='w', padx=20, pady=(10, 20))
        
        top_frame = tk.Frame(orders_frame, bg=self.colors['background'])
        top_frame.pack(fill='x', padx=20, pady=10)
        
        form_frame = tk.LabelFrame(top_frame, text="Order Details", 
                                  bg=self.colors['card_bg'], 
                                  fg=self.colors['card_header'],
                                  font=('Arial', 12, 'bold'), 
                                  padx=10, pady=10,
                                  relief='ridge', bd=1)
        form_frame.pack(side='left', fill='both', expand=True)
        
        tk.Label(form_frame, text="Customer:", bg=self.colors['card_bg'], 
                fg=self.colors['text_dark']).grid(row=0, column=0, sticky='w', pady=5)
        self.order_customer_var = tk.StringVar()
        self.order_customer_combo = ttk.Combobox(form_frame, textvariable=self.order_customer_var, width=30)
        self.order_customer_combo.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Status:", bg=self.colors['card_bg'], 
                fg=self.colors['text_dark']).grid(row=1, column=0, sticky='w', pady=5)
        self.order_status_var = tk.StringVar(value="Pending")
        status_combo = ttk.Combobox(form_frame, textvariable=self.order_status_var, 
                                   values=['Pending', 'Processing', 'Completed', 'Cancelled'], width=30)
        status_combo.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Payment Method:", bg=self.colors['card_bg'], 
                fg=self.colors['text_dark']).grid(row=2, column=0, sticky='w', pady=5)
        self.order_payment_var = tk.StringVar(value="Cash")
        payment_combo = ttk.Combobox(form_frame, textvariable=self.order_payment_var, 
                                    values=['Cash', 'Credit Card', 'Debit Card', 'GCash', 'PayMaya', 'Bank Transfer'], width=30)
        payment_combo.grid(row=2, column=1, padx=5, pady=5)
        
        product_frame = tk.LabelFrame(top_frame, text="Add Product", 
                                     bg=self.colors['card_bg'], 
                                     fg=self.colors['card_header'],
                                     font=('Arial', 12, 'bold'), 
                                     padx=10, pady=10,
                                     relief='ridge', bd=1)
        product_frame.pack(side='right', fill='both', padx=(20, 0))
        
        tk.Label(product_frame, text="Product:", bg=self.colors['card_bg'], 
                fg=self.colors['text_dark']).grid(row=0, column=0, sticky='w', pady=5)
        self.order_product_var = tk.StringVar()
        self.order_product_combo = ttk.Combobox(product_frame, textvariable=self.order_product_var, width=25)
        self.order_product_combo.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(product_frame, text="Quantity:", bg=self.colors['card_bg'], 
                fg=self.colors['text_dark']).grid(row=1, column=0, sticky='w', pady=5)
        self.order_quantity_var = tk.StringVar(value="1")
        quantity_spin = ttk.Spinbox(product_frame, from_=1, to=100, 
                                   textvariable=self.order_quantity_var, width=25)
        quantity_spin.grid(row=1, column=1, padx=5, pady=5)
        
        add_btn = tk.Button(product_frame, text="Add to Order", command=self.add_product_to_order, 
                           bg=self.button_colors['add'], fg=self.colors['text_white'], 
                           padx=15, pady=6, font=('Arial', 10, 'bold'),
                           cursor='hand2', relief='flat', bd=0,
                           activebackground=self.button_colors['add_hover'])
        add_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        add_btn.bind("<Enter>", lambda e, b=add_btn: b.config(bg=self.button_colors['add_hover']))
        add_btn.bind("<Leave>", lambda e, b=add_btn: b.config(bg=self.button_colors['add']))
        add_btn.config(highlightbackground=self.button_colors['add'], highlightthickness=1)
        
        middle_frame = tk.Frame(orders_frame, bg=self.colors['background'])
        middle_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        tree_frame = tk.Frame(middle_frame, bg=self.colors['background'])
        tree_frame.pack(fill='both', expand=True)
        
        columns = ('product_id', 'product_name', 'quantity', 'unit_price', 'subtotal')
        self.order_items_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=8)
        
        headings = ['Product ID', 'Product Name', 'Quantity', 'Unit Price', 'Subtotal']
        for col, heading in zip(columns, headings):
            self.order_items_tree.heading(col, text=heading)
            self.order_items_tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.order_items_tree.yview)
        self.order_items_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        self.order_items_tree.pack(fill='both', expand=True)
        
        bottom_frame = tk.Frame(orders_frame, bg=self.colors['background'])
        bottom_frame.pack(fill='x', padx=20, pady=10)
        
        self.order_total_var = tk.StringVar(value="Total: ₱0.00")
        total_label = tk.Label(bottom_frame, textvariable=self.order_total_var, 
                              font=('Arial', 12, 'bold'), 
                              bg=self.colors['background'], 
                              fg=self.colors['text_dark'])
        total_label.pack(side='left', padx=10)
        
        button_frame = tk.Frame(bottom_frame, bg=self.colors['background'])
        button_frame.pack(side='right')
        
        order_buttons = [
            ("Create Order", self.create_order, self.button_colors['add'], self.button_colors['add_hover']),
            ("Clear Order", self.clear_order, self.button_colors['clear'], self.button_colors['clear_hover']),
            ("Remove Item", self.remove_order_item, self.button_colors['delete'], self.button_colors['delete_hover'])
        ]
        
        for text, command, color, hover_color in order_buttons:
            btn = tk.Button(button_frame, text=text, command=command, 
                           bg=color, fg=self.colors['text_white'],
                           padx=20, pady=6, font=('Arial', 10, 'bold'),
                           cursor='hand2', relief='flat', bd=0,
                           activebackground=hover_color)
            btn.pack(side='left', padx=5, ipadx=5)
            
            btn.bind("<Enter>", lambda e, b=btn, c=hover_color: b.config(bg=c))
            btn.bind("<Leave>", lambda e, b=btn, c=color: b.config(bg=c))
            
            btn.config(highlightbackground=color, highlightthickness=1)
        
        self.order_items = []
    
    def load_order_customers(self):
        """Load customer list for order creation dropdown."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT first_name || ' ' || last_name FROM Customers")
        customers = [row[0] for row in cursor.fetchall()]
        conn.close()
        if hasattr(self, 'order_customer_combo'):
            self.order_customer_combo['values'] = customers
    
    def load_order_products(self):
        """Load product list for order creation dropdown."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT product_id, product_name, price FROM Products")
        products = cursor.fetchall()
        conn.close()
        
        self.product_info = {}
        product_names = []
        
        for product_id, product_name, price in products:
            display_name = f"{product_name} (₱{price:,.2f})"
            product_names.append(display_name)
            self.product_info[display_name] = (product_id, product_name, price)
        
        if hasattr(self, 'order_product_combo'):
            self.order_product_combo['values'] = product_names
    
    def add_product_to_order(self):
        """Add selected product to current order with quantity validation."""
        product_display = self.order_product_var.get()
        quantity_str = self.order_quantity_var.get()
        
        if not product_display:
            messagebox.showerror("Error", "Please select a product!")
            return
        
        try:
            quantity = int(quantity_str)
            if quantity <= 0:
                messagebox.showerror("Error", "Quantity must be positive!")
                return
            
            product_id, product_name, unit_price = self.product_info[product_display]
            subtotal = unit_price * quantity
            
            self.order_items.append({
                'product_id': product_id,
                'product_name': product_name,
                'quantity': quantity,
                'unit_price': unit_price,
                'subtotal': subtotal
            })
            
            self.order_items_tree.insert('', 'end', values=(
                product_id, product_name, quantity, f"₱{unit_price:,.2f}", f"₱{subtotal:,.2f}"
            ))
            
            self.update_order_total()
            
            self.order_product_var.set('')
            self.order_quantity_var.set('1')
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid quantity!")
    
    def update_order_total(self):
        """Recalculate and update order total amount."""
        total = sum(item['subtotal'] for item in self.order_items)
        self.order_total_var.set(f"Total: ₱{total:,.2f}")
    
    def remove_order_item(self):
        """Remove selected item from current order."""
        selected_item = self.order_items_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an item to remove!")
            return
        
        index = self.order_items_tree.index(selected_item[0])
        self.order_items.pop(index)
        self.order_items_tree.delete(selected_item[0])
        self.update_order_total()
    
    def clear_order(self):
        """Clear current order and reset form."""
        self.order_items = []
        for item in self.order_items_tree.get_children():
            self.order_items_tree.delete(item)
        self.update_order_total()
        self.order_customer_var.set('')
        self.order_status_var.set('Pending')
        self.order_payment_var.set('Cash')
    
    def create_order(self):
        """Process and save complete order to database."""
        if not self.order_customer_var.get():
            messagebox.showerror("Error", "Please select a customer!")
            return
        
        if not self.order_items:
            messagebox.showerror("Error", "Order must have at least one item!")
            return
        
        try:
            customer_name = self.order_customer_var.get()
            first_name, last_name = customer_name.split(' ', 1)
            
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute("SELECT customer_id FROM Customers WHERE first_name = ? AND last_name = ?", 
                         (first_name, last_name))
            customer_result = cursor.fetchone()
            
            if not customer_result:
                messagebox.showerror("Error", "Customer not found!")
                return
            
            customer_id = customer_result[0]
            
            cursor.execute("SELECT employee_id FROM Employees LIMIT 1")
            employee_result = cursor.fetchone()
            employee_id = employee_result[0] if employee_result else 1
            
            total = sum(item['subtotal'] for item in self.order_items)
            
            cursor.execute('''
                INSERT INTO Orders (customer_id, employee_id, total_amount, status, payment_method)
                VALUES (?, ?, ?, ?, ?)
            ''', (customer_id, employee_id, total, self.order_status_var.get(), self.order_payment_var.get()))
            
            order_id = cursor.lastrowid
            
            for item in self.order_items:
                cursor.execute('''
                    INSERT INTO OrderDetails (order_id, product_id, quantity, unit_price, subtotal)
                    VALUES (?, ?, ?, ?, ?)
                ''', (order_id, item['product_id'], item['quantity'], item['unit_price'], item['subtotal']))
                
                cursor.execute('''
                    UPDATE Inventory 
                    SET quantity = quantity - ?
                    WHERE product_id = ?
                ''', (item['quantity'], item['product_id']))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", f"Order created successfully! Order ID: {order_id}")
            self.refresh_dashboard()
            self.clear_order()
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def create_inventory_section(self):
        """Create inventory management interface with stock controls."""
        inventory_frame = tk.Frame(self.content_frame, bg=self.colors['background'])
        self.sections['Inventory'] = inventory_frame
        
        title_label = tk.Label(inventory_frame, text="Inventory Management", 
                              font=('Arial', 16, 'bold'), 
                              bg=self.colors['background'], 
                              fg=self.colors['card_header'])
        title_label.pack(anchor='w', padx=20, pady=(10, 20))
        
        top_frame = tk.Frame(inventory_frame, bg=self.colors['background'])
        top_frame.pack(fill='x', padx=20, pady=10)
        
        search_frame = tk.LabelFrame(top_frame, text="Search and Filter", 
                                    bg=self.colors['card_bg'], 
                                    fg=self.colors['card_header'],
                                    font=('Arial', 12, 'bold'), 
                                    padx=10, pady=10,
                                    relief='ridge', bd=1)
        search_frame.pack(fill='x')
        
        tk.Label(search_frame, text="Search:", bg=self.colors['card_bg'], 
                fg=self.colors['text_dark']).grid(row=0, column=0, sticky='w', padx=5)
        self.inventory_search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.inventory_search_var, width=30, 
                               bg=self.colors['card_bg'], fg=self.colors['text_dark'],
                               insertbackground=self.colors['primary'],
                               relief='solid', bd=1)
        search_entry.grid(row=0, column=1, padx=5)
        search_entry.bind('<KeyRelease>', lambda e: self.search_inventory())
        
        tk.Label(search_frame, text="Show:", bg=self.colors['card_bg'], 
                fg=self.colors['text_dark']).grid(row=0, column=2, sticky='w', padx=20)
        self.inventory_filter_var = tk.StringVar(value="All")
        filter_combo = ttk.Combobox(search_frame, textvariable=self.inventory_filter_var, 
                                   values=['All', 'Low Stock', 'Out of Stock'], width=15)
        filter_combo.grid(row=0, column=3, padx=5)
        filter_combo.bind('<<ComboboxSelected>>', lambda e: self.filter_inventory())
        
        button_frame = tk.Frame(search_frame, bg=self.colors['card_bg'])
        button_frame.grid(row=0, column=4, columnspan=2, padx=20, sticky='e')
        
        refresh_btn = tk.Button(button_frame, text="Refresh", command=self.refresh_inventory, 
                               bg=self.button_colors['update'], fg=self.colors['text_white'],
                               padx=15, pady=6, font=('Arial', 10, 'bold'),
                               cursor='hand2', relief='flat', bd=0,
                               activebackground=self.button_colors['update_hover'])
        refresh_btn.pack(side='left', padx=5)
        refresh_btn.bind("<Enter>", lambda e, b=refresh_btn: b.config(bg=self.button_colors['update_hover']))
        refresh_btn.bind("<Leave>", lambda e, b=refresh_btn: b.config(bg=self.button_colors['update']))
        refresh_btn.config(highlightbackground=self.button_colors['update'], highlightthickness=1)
        
        restock_btn = tk.Button(button_frame, text="Restock All Low Stock", command=self.restock_low_stock,
                               bg=self.button_colors['add'], fg=self.colors['text_white'],
                               padx=15, pady=6, font=('Arial', 10, 'bold'),
                               cursor='hand2', relief='flat', bd=0,
                               activebackground=self.button_colors['add_hover'])
        restock_btn.pack(side='left', padx=5)
        restock_btn.bind("<Enter>", lambda e, b=restock_btn: b.config(bg=self.button_colors['add_hover']))
        restock_btn.bind("<Leave>", lambda e, b=restock_btn: b.config(bg=self.button_colors['add']))
        restock_btn.config(highlightbackground=self.button_colors['add'], highlightthickness=1)
        
        main_frame = tk.Frame(inventory_frame, bg=self.colors['background'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        tree_frame = tk.Frame(main_frame, bg=self.colors['background'])
        tree_frame.pack(fill='both', expand=True)
        
        columns = ('inventory_id', 'product_name', 'brand', 'size', 'current_stock', 'min_stock', 'status')
        self.inventory_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=20)
        
        headings = ['ID', 'Product Name', 'Brand', 'Size', 'Current Stock', 'Min Stock', 'Status']
        for col, heading in zip(columns, headings):
            self.inventory_tree.heading(col, text=heading)
            self.inventory_tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.inventory_tree.yview)
        self.inventory_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        self.inventory_tree.pack(fill='both', expand=True)
        
        bottom_frame = tk.Frame(inventory_frame, bg=self.colors['background'])
        bottom_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(bottom_frame, text="Restock Quantity:", bg=self.colors['background'], 
                fg=self.colors['text_dark']).pack(side='left', padx=5)
        self.restock_quantity_var = tk.StringVar(value="10")
        restock_spin = ttk.Spinbox(bottom_frame, from_=1, to=1000, 
                                  textvariable=self.restock_quantity_var, width=10)
        restock_spin.pack(side='left', padx=5)
        
        restock_selected_btn = tk.Button(bottom_frame, text="Restock Selected", command=self.restock_selected,
                                        bg=self.button_colors['add'], fg=self.colors['text_white'],
                                        padx=15, pady=6, font=('Arial', 10, 'bold'),
                                        cursor='hand2', relief='flat', bd=0,
                                        activebackground=self.button_colors['add_hover'])
        restock_selected_btn.pack(side='left', padx=20)
        restock_selected_btn.bind("<Enter>", lambda e, b=restock_selected_btn: b.config(bg=self.button_colors['add_hover']))
        restock_selected_btn.bind("<Leave>", lambda e, b=restock_selected_btn: b.config(bg=self.button_colors['add']))
        restock_selected_btn.config(highlightbackground=self.button_colors['add'], highlightthickness=1)
    
    def refresh_inventory(self):
        """Refresh inventory view and reset filters."""
        self.load_inventory()
        self.inventory_search_var.set('')
        self.inventory_filter_var.set('All')
        messagebox.showinfo("Refreshed", "Inventory refreshed successfully!")
    
    def load_inventory(self):
        """Load inventory data with stock status indicators."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT i.inventory_id, p.product_name, p.brand, p.size, 
                   i.quantity, i.min_stock_level,
                   CASE 
                     WHEN i.quantity = 0 THEN 'Out of Stock'
                     WHEN i.quantity < i.min_stock_level THEN 'Low Stock'
                     ELSE 'In Stock'
                   END as status
            FROM Inventory i
            JOIN Products p ON i.product_id = p.product_id
            ORDER BY i.inventory_id
        ''')
        
        if hasattr(self, 'inventory_tree'):
            for item in self.inventory_tree.get_children():
                self.inventory_tree.delete(item)
        
        for row in cursor.fetchall():
            self.inventory_tree.insert('', 'end', values=row)
        
        conn.close()
    
    def search_inventory(self):
        """Search inventory with optional stock level filtering."""
        search_term = self.inventory_search_var.get().lower()
        filter_type = self.inventory_filter_var.get()
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        query = '''
            SELECT i.inventory_id, p.product_name, p.brand, p.size, 
                   i.quantity, i.min_stock_level,
                   CASE 
                     WHEN i.quantity = 0 THEN 'Out of Stock'
                     WHEN i.quantity < i.min_stock_level THEN 'Low Stock'
                     ELSE 'In Stock'
                   END as status
            FROM Inventory i
            JOIN Products p ON i.product_id = p.product_id
            WHERE (LOWER(p.product_name) LIKE ? OR LOWER(p.brand) LIKE ?)
        '''
        
        params = [f'%{search_term}%', f'%{search_term}%']
        
        if filter_type == 'Low Stock':
            query += ' AND i.quantity < i.min_stock_level AND i.quantity > 0'
        elif filter_type == 'Out of Stock':
            query += ' AND i.quantity = 0'
        
        query += ' ORDER BY i.inventory_id'
        
        cursor.execute(query, params)
        
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
        
        for row in cursor.fetchall():
            self.inventory_tree.insert('', 'end', values=row)
        
        conn.close()
    
    def filter_inventory(self):
        """Apply inventory filter based on selection."""
        self.search_inventory()
    
    def restock_selected(self):
        """Restock selected inventory item by specified quantity."""
        selected_item = self.inventory_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an item to restock!")
            return
        
        try:
            quantity = int(self.restock_quantity_var.get())
            if quantity <= 0:
                messagebox.showerror("Error", "Quantity must be positive!")
                return
            
            inventory_id = self.inventory_tree.item(selected_item[0], 'values')[0]
            
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE Inventory 
                SET quantity = quantity + ?, last_restocked = CURRENT_DATE
                WHERE inventory_id = ?
            ''', (quantity, inventory_id))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Inventory restocked successfully!")
            self.load_inventory()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid quantity!")
    
    def restock_low_stock(self):
        """Bulk restock all low stock items to safe levels."""
        if messagebox.askyesno("Confirm Restock", "Restock all low stock items?"):
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT inventory_id, min_stock_level, quantity 
                FROM Inventory 
                WHERE quantity < min_stock_level
            ''')
            
            low_stock_items = cursor.fetchall()
            restocked_count = 0
            
            for item in low_stock_items:
                inventory_id, min_stock, current_qty = item
                restock_qty = (min_stock + 20) - current_qty
                
                if restock_qty > 0:
                    cursor.execute('''
                        UPDATE Inventory 
                        SET quantity = quantity + ?, last_restocked = CURRENT_DATE
                        WHERE inventory_id = ?
                    ''', (restock_qty, inventory_id))
                    restocked_count += 1
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", f"{restocked_count} items restocked!")
            self.load_inventory()


def main():
    """
    Application entry point.
    
    Initializes the Tkinter main window and starts the application.
    """
    root = tk.Tk()
    app = ShoeShopManagementSystem(root)
    root.mainloop()


if __name__ == "__main__":
    main()