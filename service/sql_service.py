import sqlite3


class ProductService:
    table_name = "Products"

    def __init__(self, db_name='data_base.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Products tablosunun var olup olmadığını kontrol etme
        self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self.table_name}'")
        product_table = self.cursor.fetchone()

        # Eğer Products tablosu yoksa, oluşturma
        if not product_table:
            self.cursor.execute(f'''CREATE TABLE {self.table_name} (
                                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                product_url TEXT,
                                product_title TEXT,
                                product_price REAL,
                                product_category TEXT,
                                product_star_point REAL
                            )''')
        self.conn.commit()

    def get_products(self):
        self.cursor.execute(f"SELECT * FROM {self.table_name}")
        products = self.cursor.fetchall()
        return products

    def get_product(self, product_id):
        self.cursor.execute(f"SELECT * FROM {self.table_name} WHERE product_id = ?", (product_id,))
        product = self.cursor.fetchone()
        return product

    def add_product(self, product_data):
        self.cursor.execute(
            f"INSERT INTO {self.table_name} (product_url, product_title, product_price, product_category, "
            f"product_star_point) VALUES (?, ?, ?, ?, ?)",
            product_data)
        self.conn.commit()

    def update_product(self, product_id, product_data):
        self.cursor.execute(
            f"UPDATE {self.table_name} SET product_url = ?, product_title = ?, product_price = ?, product_category = "
            f"?, product_star_point = ? WHERE product_id = ?",
            (*product_data, product_id))
        self.conn.commit()

    def delete_product(self, product_id):
        self.cursor.execute(f"DELETE FROM {self.table_name} WHERE product_id = ?", (product_id,))
        self.conn.commit()

    def add_products_from_list(self, products_list):
        query = (f"INSERT INTO {self.table_name} (product_url, product_title, product_price, product_category, "
                 f"product_star_point) VALUES (?, ?, ?, ?, ?)")
        for product in products_list:
            self.cursor.execute(query, product)
        self.conn.commit()

    def delete_all_products(self):
        self.cursor.execute(f"DELETE FROM {self.table_name}")
        self.conn.commit()

    def __del__(self):
        self.conn.close()


class CommentService:
    table_name = "ProductComments"

    def __init__(self, db_name='data_base.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        # ProductComments tablosunun var olup olmadığını kontrol etme
        self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self.table_name}'")
        comment_table = self.cursor.fetchone()

        # Eğer ProductComments tablosu yoksa, oluşturma
        if not comment_table:
            self.cursor.execute(f'''CREATE TABLE {self.table_name} (
                                        comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        product_id INTEGER,
                                        comment TEXT,
                                        FOREIGN KEY(product_id) REFERENCES Products(product_id)
                                    )''')
        self.conn.commit()

    def get_comments_for_product(self, product_id):
        self.cursor.execute(f"SELECT * FROM {self.table_name} WHERE product_id = ?", (product_id,))
        comments = self.cursor.fetchall()
        return comments

    def add_comment_to_product(self, product_id, comment):
        self.cursor.execute(f"INSERT INTO {self.table_name} (product_id, comment) VALUES (?, ?)", (product_id, comment))
        self.conn.commit()

    def update_comment(self, comment_id, new_comment):
        self.cursor.execute(f"UPDATE {self.table_name} SET comment = ? WHERE comment_id = ?", (new_comment, comment_id))
        self.conn.commit()

    def delete_comment(self, comment_id):
        self.cursor.execute(f"DELETE FROM {self.table_name} WHERE comment_id = ?", (comment_id,))
        self.conn.commit()

    def add_comments_to_product(self, product_id, comments_list):
        query = f"INSERT INTO {self.table_name} (product_id, comment) VALUES (?, ?)"
        for comment in comments_list:
            self.cursor.execute(query, (product_id, comment))
        self.conn.commit()

    def delete_all_comments_for_product(self, product_id):
        self.cursor.execute(f"DELETE FROM {self.table_name} WHERE product_id = ?", (product_id,))
        self.conn.commit()

    def delete_all_comments(self):
        self.cursor.execute(f"DELETE FROM {self.table_name}")
        self.conn.commit()

    def __del__(self):
        self.conn.close()
