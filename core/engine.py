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

    def purchase_processing(self,basket,cus_name):
        for p_id,qty in basket.items():
            product=self.search_product(p_id)
            if not product or product.quantity<qty:
                storage.log_missed_sale(self.connection, p_id, qty, cus_name)
                return {"status": "error", "message": f"Stock low for {p_id}"}
        try:
            s_id = storage.sales_processing(self.connection, basket, cus_name)
            return {"status": "success", "s_id": s_id}


        except Exception as e:
            return {"status": "error", "message": str(e)}


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

    def display_sales(self):
        out = storage.db_get_all_sales(self.connection)
        return out


    def dashboard_data(self):
        dash=storage.get_dashboard_data(self.connection)
        total=dash.get('total_revenue',0)
        customer=dash.get("top_customers",[])
        out_of_stock=dash.get('out_of_stock',0)
        best_seller=dash.get('best_sellers',[])
        worst_seller=dash.get('worst_sellers',[])
        unsold=dash.get('unsold')


        def status_check():
            if out_of_stock==0:
                description='healthy'
            elif out_of_stock <= 5:
                description='warning'
            else:
                description='critical'
            return description

        def high_roller():
            check=False
            if total>0 and customer:
                if float(customer[0]['spent'])/float(total)>0.5:
                    check=True
            return check

        status=status_check()
        highroller=high_roller()

        return {
            'total_revenue':total,
            'best_customer':customer,
            'status':status,
            'highroller':highroller,
            'best_seller':best_seller,
            'worst_seller':worst_seller,
            'unsold':unsold
        }


















