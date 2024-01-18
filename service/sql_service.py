import sqlite3

from model.comment_model import Comment_Model
from model.product_model import Product_Model


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
        product_list = []
        for product in products:
            # Bu kısımda Product_Model oluştururken uygun parametreleri geçmeniz gerekiyor
            product_instance = Product_Model(product[0], product[1], product[2], product[3], product[4], product[5])
            product_list.append(product_instance)
        return product_list

    def get_products_with_comments(self):
        comment_service = CommentService()
        product_ids_with_comments = comment_service.get_product_ids_with_comments()

        products_with_comments = []
        for product_id in product_ids_with_comments:
            product = self.get_product(product_id)
            products_with_comments.append(product)

        return products_with_comments

    def get_products_by_location(self, location):
        self.cursor.execute(f"SELECT * FROM {self.table_name} WHERE product_title LIKE ?", ('%' + location + '%',))
        products = self.cursor.fetchall()
        product_list = []
        for product in products:
            # Eksik olan product_category ve product_star_point'u da ekledim
            product_instance = Product_Model(product[0], product[1], product[2], product[3], product[4], product[5])
            product_list.append(product_instance)
        return product_list

    def get_products_by_price_range(self, min_price, max_price):
        query = """SELECT * FROM Products WHERE product_price BETWEEN ? AND ?"""
        self.cursor.execute(query, (min_price, max_price))
        products = self.cursor.fetchall()
        product_list = []
        for product in products:
            product_instance = Product_Model(*product)  # Tüm sütunları kullanarak Product_Model oluştur
            product_list.append(product_instance)
        return product_list

    def get_products_cheaper_than(self, price):
        self.cursor.execute(
            f"SELECT * FROM {self.table_name} WHERE product_price < ?",
            (price,))
        products = self.cursor.fetchall()
        product_list = []
        for product in products:
            product_instance = Product_Model(product[0], product[1], product[2], product[3], product[4], product[5])
            product_list.append(product_instance)
        return product_list

    def get_products_pricier_than(self, price):
        self.cursor.execute(
            f"SELECT * FROM {self.table_name} WHERE product_price > ?",
            (price,))
        products = self.cursor.fetchall()
        product_list = []
        for product in products:
            product_instance = Product_Model(product[0], product[1], product[2], product[3], product[4], product[5])
            product_list.append(product_instance)
        return product_list

    def get_product(self, product_id):
        self.cursor.execute(f"SELECT * FROM {self.table_name} WHERE product_id = ?", (product_id,))
        product_data = self.cursor.fetchone()

        if product_data:
            # Tuple'dan Product_Model'e dönüşüm, her bir veriyi ayrı olarak geçiyoruz
            product = Product_Model(product_data[0], product_data[1], product_data[2], product_data[3], product_data[4],
                                    product_data[5])
            return product
        else:
            return None  # Ürün bulunamadıysa None döndür

    def add_product(self, product):
        self.cursor.execute(
            f"INSERT INTO {self.table_name} (product_url, product_title, product_price, product_category, "
            f"product_star_point) VALUES (?, ?, ?, ?, ?)",
            (product.product_url, product.product_title, product.product_price,
             product.product_category, product.product_star_point))
        self.conn.commit()

    def update_product(self, product_id, updated_product_data):
        self.cursor.execute(
            f"UPDATE {self.table_name} SET product_url = ?, product_title = ?, product_price = ?, product_category = "
            f"?, product_star_point = ? WHERE product_id = ?",
            (updated_product_data.product_url, updated_product_data.product_title,
             updated_product_data.product_price, updated_product_data.product_category,
             updated_product_data.product_star_point, product_id,))
        self.conn.commit()

        # Güncellenen ürünü döndür
        self.cursor.execute(f"SELECT * FROM {self.table_name} WHERE product_id = ?", (product_id,))
        updated_product = self.cursor.fetchone()
        return updated_product

    def delete_product(self, product_id):
        self.cursor.execute(f"DELETE FROM {self.table_name} WHERE product_id = ?", (product_id,))
        self.conn.commit()

    def delete_all_products(self):
        confirmation = input("Tüm ürünleri silmek istediğinize emin misiniz? (E/H): ")
        if confirmation.lower() == 'e':
            self.cursor.execute(f"DELETE FROM {self.table_name}")
            self.conn.commit()
            print("Tüm ürünler başarıyla silindi.")
        else:
            print("İşlem iptal edildi.")

    def get_most_reviewed_product(self):
        # En çok yorumlanan ürünü bulma
        query = """SELECT Products.product_id, Products.product_url, Products.product_title,
                          Products.product_price, Products.product_category, Products.product_star_point,
                          COUNT(ProductComments.comment_id) AS comment_count
                   FROM Products
                   LEFT JOIN ProductComments ON Products.product_id = ProductComments.product_id
                   GROUP BY Products.product_id
                   ORDER BY comment_count DESC
                   LIMIT 1"""

        self.cursor.execute(query)
        most_reviewed_product_data = self.cursor.fetchone()

        if most_reviewed_product_data:
            # comment_count'ı alarak geri kalan parametreleri Product_Model'e geçir
            most_reviewed_product = Product_Model(
                most_reviewed_product_data[0],  # product_id
                most_reviewed_product_data[1],  # product_url
                most_reviewed_product_data[2],  # product_title
                most_reviewed_product_data[3],  # product_price
                most_reviewed_product_data[4],  # product_category
                most_reviewed_product_data[5],  # product_star_point
            )
            return most_reviewed_product
        else:
            return None

    def get_highest_rated_product(self):
        # En yüksek oy alan ürünü bulma
        query = """SELECT * FROM Products
                   ORDER BY product_star_point DESC
                   LIMIT 1"""

        self.cursor.execute(query)
        highest_rated_product_data = self.cursor.fetchone()

        if highest_rated_product_data:
            highest_rated_product = Product_Model(*highest_rated_product_data)
            return highest_rated_product
        else:
            return None

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
                                        name TEXT,
                                        comment_point REAL,
                                        comment_text TEXT,
                                        FOREIGN KEY(product_id) REFERENCES Products(product_id)
                                    )''')
        self.conn.commit()

    def get_comments_for_product(self, product_id):
        self.cursor.execute(f"SELECT * FROM {self.table_name} WHERE product_id = ?", (product_id,))
        comment_data = self.cursor.fetchall()

        comments = []
        for comment_tuple in comment_data:
            comment = Comment_Model(*comment_tuple)  # Tuple'ı Comment_Model'e dönüştür
            comments.append(comment)

        return comments

    def get_product_ids_with_comments(self):
        self.cursor.execute(
            f"SELECT DISTINCT product_id FROM {self.table_name} WHERE comment_text != 'Henüz değerlendirme mevcut değil.'")
        product_ids = self.cursor.fetchall()
        return [product_id[0] for product_id in product_ids]

    def add_comment_to_product(self, comment):
        self.cursor.execute(f"INSERT INTO {self.table_name} (product_id, name, comment_point, comment_text) VALUES (?, ?, ?, ?)",
                            (comment.product_id, comment.name, comment.comment_point, comment.comment_text))
        self.conn.commit()

    def update_comment(self, comment):
        self.cursor.execute(f"UPDATE {self.table_name} SET comment_text = ? WHERE comment_id = ?",
                            (comment.comment_text, comment.comment_id))
        self.conn.commit()

    def delete_comment(self, comment_id):
        self.cursor.execute(f"DELETE FROM {self.table_name} WHERE comment_id = ?", (comment_id,))
        self.conn.commit()

    def add_comments_to_product(self, comments_list,product_id):
        query = f"INSERT INTO {self.table_name} (product_id, name, comment_point, comment_text) VALUES (?, ?, ?, ?)"
        if comments_list is not None:
            for comment in comments_list:
                self.cursor.execute(query,
                                    (comment.product_id, comment.name, comment.comment_point, comment.comment_text))
            self.conn.commit()
        else:
            # Eğer comments_list None ise, "Henüz değerlendirme mevcut değil." yorumunu kaydet
            default_comment = "Henüz değerlendirme mevcut değil."
            self.cursor.execute(query, (product_id, None, None, default_comment))
            self.conn.commit()

    def delete_all_comments_for_product(self, product_id):
        self.cursor.execute(f"DELETE FROM {self.table_name} WHERE product_id = ?", (product_id,))
        self.conn.commit()

    def delete_all_comments(self):
        self.cursor.execute(f"DELETE FROM {self.table_name}")
        self.conn.commit()

    def __del__(self):
        self.conn.close()
