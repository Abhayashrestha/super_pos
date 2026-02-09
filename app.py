import os
from flask import Flask, render_template, request, redirect, flash
from werkzeug.utils import secure_filename
from data.storage import get_connection, db_add_product # Added your DB function
from core.engine import Catalog, Product


app=Flask(__name__)
app.secret_key = "asdfghjklasdfghjkl"
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
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

@app.route("/add-product",methods=['GET','POST'])
def add_product():
    if request.method=='POST':
        p_name=request.form.get("p_name")
        p_price=request.form.get("p_price")
        p_qty=request.form.get('p_qty')
        p_category=request.form.get("p_category")
        p_image=request.files.get('p_image')
        if p_image and p_image.filename != '':
            filename = secure_filename(p_image.filename)
            p_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = 'default.jpg'
        product=Product(p_name,p_price,p_qty,p_category,filename)
        engine.add_product(product)

        flash("Product added to inventory!", "success")
        return redirect('/')

    return render_template('add_product.html')

@app.route('/')
def storefront():
    inventory=engine.display_product()
    return render_template('storefront.html',products=inventory)




if __name__ == "__main__":
    app.run(debug=True)





