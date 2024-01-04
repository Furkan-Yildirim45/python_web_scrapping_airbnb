class Comment_Model:
    def __init__(self, product_id, name, comment_point, comment_text):
        self.comment_id = None  # Eklenecek olan veritabanında otomatik oluşturulacak
        self.product_id = product_id
        self.name = name
        self.comment_point = comment_point
        self.comment_text = comment_text