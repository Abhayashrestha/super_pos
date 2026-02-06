from flask import Flask,render_template
from core.engine import Catalog
from data.storage import get_connection

app=Flask(__name__)

database=get_connection()
engine=Catalog(database)

@app.route("/receipt/<int:s_id>")
def show_receipt(s_id):
    data_bundle=engine.get_sale_receipt(s_id)
    print(f"TYPE CHECK: {type(data_bundle['obj'])}")
    return render_template(
        "receipt.html",
        sale=data_bundle['obj'],
        qr=data_bundle['qr']
    )

if __name__ == "__main__":
    app.run(debug=True)





