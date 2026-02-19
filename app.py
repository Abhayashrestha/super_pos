import os
from flask import Flask, render_template, request, redirect, flash, url_for,session
from werkzeug.utils import secure_filename
from data.storage import get_connection
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

@app.route("/add-product",methods=['POST'])
def add_product():
    if request.method=='POST':
        p_name=request.form.get("p_name")
        p_price=request.form.get("p_price")
        price=float(p_price)
        p_qty=request.form.get('p_qty')
        quantity=int(p_qty)
        p_category=request.form.get("p_category")
        p_image=request.files.get('p_image')
        if p_image and p_image.filename != '':
            filename = secure_filename(p_image.filename)
            p_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = 'default.jpg'
        product=Product(p_name,price,quantity,p_category,filename)
        engine.add_product(product)

        flash("Product added to inventory!", "success")
        return redirect(url_for('admin'))


@app.route('/')
def storefront():
    inventory=engine.display_product()
    return render_template('storefront.html',products=inventory)


@app.route('/buy/<int:p_id>',methods=['GET','POST'])
def buy_product(p_id):
    cus_name = 'guest'
    if request.method=="POST":
        quantity=request.form.get("quantity")
        try:
            qty=int(quantity)
            sale=engine.purchase_processing({p_id:qty},cus_name)
            if sale:
                flash(f"Success! Order #{sale} placed.", "success")
                return redirect(url_for('show_receipt', s_id=sale))
            else:
                flash('Transaction failed. Please try again.')

        except ValueError as e:
            flash(str(e), "warning")

        except Exception as e:
            flash("A system error occurred.", "danger")
            print(f"Error: {e}")

    return redirect(url_for('show_receipt'))

@app.route('/admin',methods=['GET','POST'])
def admin():
    inventory=engine.display_product()
    sale=engine.display_sales()
    return render_template('admin.html',products=inventory,sales=sale)



@app.route('/delete-product/<int:p_id>',methods=['POST'])
def delete_product(p_id):
    try:
        success = engine.delete_product(p_id)
        if success:
            flash("Product deleted successfully.", "success")
        else:
            flash("Could not delete. Check if product is linked to sales.", "danger")
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")

    return redirect(url_for('admin'))

@app.route('/update-stock/<int:p_id>',methods=['POST'])
def update_stock(p_id):
    try:
        if request.method=='POST':
            quantity=request.form.get('new_qty')
            qty=int(quantity)
            new_stock=engine.stock_management(p_id,qty)
            flash("Stock updated successfully.",'success')
        else:
            flash("could not update stock",'Failed')
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")

    return redirect(url_for('admin'))


@app.route('/lookup-receipt', methods=['POST'])
def lookup_receipt():  # Remove s_id from the arguments
    try:
        sale_id = request.form.get('s_id')
        if not sale_id:
            flash("No ID entered", "warning")
            return redirect(url_for('admin'))
        clean_id = int(sale_id)
        return redirect(url_for('show_receipt', s_id=clean_id))

    except ValueError:
        flash("Invalid Receipt ID. Numbers only.", "danger")
    except Exception as e:
        flash(f"System Error: {str(e)}", "danger")

    return redirect(url_for('admin'))

@app.route('/add_item_to_cart/<int:p_id>',methods=['POST'])
def add_item_to_cart(p_id):
    try:
        cart=session.get('cart',{})
        p_id_str=str(p_id)
        quantity=int(request.form.get('quantity'))
        cart[p_id_str]=cart.get(p_id_str,0)+quantity
        session['cart'] = cart
        session.modified = True
        flash("Item added to cart!")
        return redirect(url_for('storefront'))

    except Exception as e:
        flash(f"System Error: {str(e)}", "danger")

@app.route('/cart')
def view_cart():
    display=[]
    total=0
    cart=session.get('cart',{})
    for p_id,quantity in cart.items():
        product=engine.search_product(int(p_id))
        if product:
            subtotal=product.price*quantity
            total+=subtotal
            display.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
    return render_template('cart.html', items=display, total=total)

@app.route('/checkout',methods=['POST'])
def checkout():
    cart=session.get('cart',{})
    cus_name=request.form.get('customer_name','guest')
    try:
        clean_basket={int(key):v for key, v in cart.items()}
        sale=engine.purchase_processing(clean_basket,cus_name)
        if sale:
            flash("Purchase Successful")
            session.pop('cart',None)
            return redirect(url_for('show_receipt',s_id=sale))
    except ValueError as e:
        flash(f"Purchase Failed: {str(e)}", "danger")
        return redirect(url_for('storefront'))
    except Exception as e:
        flash(f"Purchase Failed: {str(e)}", "danger")
        return redirect(url_for('storefront'))

@app.route('/dashboard')
def dashboard():
    report=engine.dashboard_data()
    return render_template('dashboard.html',data=report)













if __name__ == "__main__":
    app.run(debug=True)





