from enum import ProductType
from models.product import Product
from tests import BaseTestModelCase
import util

class TestProductModel(BaseTestModelCase):
    def test_add(self):
        product = Product()
        product.title = "title"
        product.descr = "desc"
        product.type = ProductType.MATERIAL
        product.updated_at = product.inserted_at = util.utcnow()
        self.db.add(product)
        self.db.commit()
        self.assertTrue(True)