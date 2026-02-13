from .model import Product,Sale,LineItem
from data import storage
from services.services import ReceiptService

class Catalog:
    def __init__(self,connection):
        self.connection=connection

    def add_product(self,product_instance):
        new=storage.db_add_product(self.connection,product_instance)
        return new


    def search_product(self,product_id):
        find=storage.db_view_product(self.connection,product_id)
        return find

    def display_product(self):
        out=storage.db_view_all_product(self.connection)
        return out


    def delete_product(self,product_id):
        delete=storage.db_delete_product(self.connection,product_id)
        return delete

    def purchase_processing(self, product_id, requested_quantity,cus_name):
        s_id=storage.sales_processing(self.connection,product_id,requested_quantity,cus_name)
        return s_id

    def receipt_processing(self, s_id):
        receipt=storage.db_get_receipt(self.connection,s_id)
        return receipt

    def stock_management(self,p_id,quantity):
        new_stock=storage.db_modify_stock(self.connection,p_id,quantity)
        return new_stock

    def get_sale_receipt(self, s_id):
        receipt_obj = storage.db_get_receipt(self.connection, s_id)
        qr_string = ReceiptService.generate_qr(receipt_obj)

        return {
            "obj": receipt_obj,
            "qr": qr_string
        }




















