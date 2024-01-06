from model.comment_model import Comment_Model
from model.product_model import Product_Model
from service.sql_service import ProductService, CommentService


def test_product_service():
    # Ürün servisi oluştur
    product_service = ProductService()

    # Bir ürün ekleyelim
    product_data = Product_Model('www.example.com/product1', 'Product 1', 49.99, 'Category A', 4.5)
    product_service.add_product(product_data)

    # Eklenen ürünün veritabanında olup olmadığını kontrol et
    products = product_service.get_products()
    assert len(products) == 1
    assert products[0].product_title == 'Product 1'

    # Ürünü güncelleyelim
    updated_product_data = Product_Model('www.example.com/updated-product1', 'Updated Product 1', 59.99, 'Category B',
                                         4.8)
    updated_product = product_service.update_product(1, updated_product_data)
    assert updated_product[2] == 'Updated Product 1'

    # Ürünü silelim
    product_service.delete_product(1)

    # Ürünün veritabanında silindiğini kontrol et
    products = product_service.get_products()
    assert len(products) == 0


def test_comment_service():
    # Yorum servisi oluştur
    comment_service = CommentService()

    # Yorumlar ekleyelim
    comments_list = [
        Comment_Model(1, 'John Doe', 4.5, 'Good product'),
        Comment_Model(1, 'Jane Smith', 3.0, 'Bad product'),
        Comment_Model(1, 'Alice Johnson', 4.0, 'Average product')
    ]
    comment_service.add_comments_to_product(comments_list)

    # Eklenen yorumların veritabanında olup olmadığını kontrol et
    comments = comment_service.get_comments_for_product(1)
    assert len(comments) == 3

    # Yorum güncelleyelim
    updated_comment = Comment_Model(product_id=1, name='John Doe', comment_point=4.5, comment_text='Updated comment')
    comment_service.update_comment(updated_comment)

    # Güncellenen yorumun veritabanında olup olmadığını kontrol et
    updated_comments = comment_service.get_comments_for_product(1)
    print(updated_comments)

    # Yorumu silelim
    comment_service.delete_comment(1)

    # Yorumun veritabanından silindiğini kontrol et
    comments = comment_service.get_comments_for_product(1)
    assert len(comments) == 2


# Testleri çalıştır
test_product_service()
test_comment_service()
