from flask import Flask, render_template, request, url_for, flash, redirect, session
from sqlalchemy import Column, Integer, String, Numeric, create_engine, text

app = Flask(__name__, template_folder='template')
app.secret_key = 'Wilson02!'
app.debug = True

conn_str = "mysql://root:Wilson02!@localhost/180Final"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()


def p(str):
    abc = "abcdefghijklmnopqrstuvwxyz"
    sum = 0
    for char in str:
        sum += abc.find(char) + 1
    return sum


@app.route('/')
def home():
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        password = p(password)
        user = conn.execute(text("SELECT * FROM register WHERE email=:email"), {'email': email}).fetchone()
        if user is not None:
            flash("An account with this email already exists.")
            return redirect(url_for('create_account'))
        else:
            conn.execute(
                text("INSERT INTO register VALUES (:name, :email, :username, :password, :userID, :account_type)"),
                request.form)
            conn.commit()
            flash("Account created successfully.")
            return redirect(url_for('home'))
    return render_template("register.html")


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if password == 'bobbyS' or password == 'Asing!' or password == 'password' or password == 'musicFun5' or password == 'Budders23!':
            password = password
        else:
            password = password
        query = text("SELECT * FROM register WHERE username = :username AND password = :password")
        params = {"username": username, "password": password}
        result = conn.execute(query, params)
        user = result.fetchone()
        if user is None:
            return render_template('login.html')
        else:
            session['name'] = user[0]
            session['email'] = user[1]
            session['username'] = user[2]
            session['userID'] = user[4]
            session['account_type'] = user[5]
            session['logged_in'] = True
            if user[5] == 'Admin':
                acc = conn.execute(text("SELECT userID FROM register"))
                return redirect(url_for('admin', acc=acc))
            elif user[5] == 'vendor':
                acc = conn.execute(text("SELECT userID FROM register"))
                return redirect(url_for('vendor', acc=acc))
            else:
                acc = conn.execute(text("SELECT userID FROM register"))
                return redirect(url_for('customer', acc=acc))
    else:
        return render_template('login.html')


# Customer
@app.route('/customer')
def customer():
    query = text("SELECT * FROM products")
    result = conn.execute(query)
    products = []
    for row in result:
        products.append(row)
    return render_template('customer.html', products=products)


# vendor

@app.route('/vendor')
def vendor():
    session_id = session.get('userID')
    query = text("SELECT * FROM products WHERE vendor_id = :session_id")
    result = conn.execute(query, {'session_id': session_id})
    products = []
    for row in result:
        products.append(row)
    return render_template('vendor.html', products=products)


# vendor add products
@app.route('/v_add', methods=['GET'])
def ven_add():
    return render_template('vendor_add_product.html')


@app.route('/vendor_product', methods=['POST'])
def v_add_product():
    max_product = text("select max(itemID) from products")
    max_id = conn.execute(max_product).fetchone()[0]
    new_id = max_id + 1 if max_id is not None else 1

    title = request.form['title']
    description = request.form['description']
    image = request.form['image']
    category = request.form['category']
    colors = request.form['colors']
    sizes = request.form['sizes']
    inventory = request.form['inventory']
    price = request.form['price']
    itemID = request.form['itemID']
    discount_price = request.form['discount_price']
    vendor_id = session.get('userID')

    x = text("INSERT INTO products (title, description, image, category, colors,"
             " sizes, inventory, price, itemID, discount_price, vendor_id) VALUES "
             "(:title, :description, :image, :category, :colors, :sizes, :inventory, :price, :itemID"
             ", :discount_price, :vendor_id)")
    y = {"title": title, "description": description, "image": image, "category": category, "colors": colors,
         "sizes": sizes, "inventory": inventory, "price": price, "itemID": new_id, "discount_price": discount_price,
         "vendor_id": vendor_id}
    conn.execute(x, y)
    conn.commit()

    return render_template('vendor_add_product.html')


# admin
@app.route('/admin')
def admin():
    query = text("SELECT * FROM products")
    result = conn.execute(query)
    products = []
    for row in result:
        products.append(row)
    return render_template('admin.html', products=products)


@app.route('/add_product', methods=['GET'])
def add_product():
    return render_template('add_product.html')


@app.route('/add_product', methods=['POST'])
def add():
    conn.execute(text("INSERT INTO products VALUES (:title, :description, :image, :category, :colors,"
                      " :sizes, :inventory, :price, :itemID, :discount_price, :vendor_id)"), request.form)
    conn.commit()
    return render_template('add_product.html')


##look at all products/filter both admin and vendor
@app.route('/view_products', methods=['GET'])
def view():
    return render_template('view_products.html')


@app.route('/view_products', methods=['POST'])
def view_products():
    products = conn.execute(text("select * from products")).all()
    if request.method == "POST":
        if request.form["button"] == "My Products":
            user_id = session.get("userID")
            products = conn.execute(text("select * from products where vendor_id = vendor_id"),
                                    {"vendor_id": user_id}).all()
            conn.execute(products)
            conn.commit()
            return render_template("view_products.html", products=products)
        elif request.form["button"] == "All Products":
            products = conn.execute(text("SELECT * FROM products;")).all()
            return render_template("view_products.html", products=products)
        return render_template("view_products.html", products=products[:10])


##edit products both admin and vendor
@app.route('/edit_product', methods=["GET"])
def edit():
    return render_template("edit_product.html")


@app.route('/edit_product', methods=["POST"])
def edit_product():
    conn.execute(text("update products set itemID = :itemID, title = :title, description = :description, "
                      "image = :image, category = :category, colors = :colors, sizes = :sizes, inventory = :inventory,"
                      "price = :price, itemID = :itemID, discount_price = :discount_price"
                      " where itemID = :itemID"), request.form)
    conn.commit()
    return render_template("edit_product.html")


##delete products
@app.route('/delete', methods=["GET"])
def delete():
    return render_template("delete.html")


@app.route('/delete', methods=["POST"])
def delete_exams():
    conn.execute(text("Delete from products where itemID = :itemID"), request.form)
    conn.commit()
    return render_template("delete.html")


# #my accounts page
# @app.route('/my_account', methods = [])
# def account():
#     return render_template('accounts.html')

@app.route('/accounts', methods=['GET', 'POST'])
def my_account():
    if 'username' in session:
        username = ['username']
        x = text("SELECT * FROM register WHERE username = :username")
        y = {'username': username}
        with engine.connect() as conn:
            accounts = conn.execute(x, y).fetchall()
            return render_template("accounts.html", accounts=accounts)
    else:
        return redirect(url_for('login'))


# #chat
# @app.route('/chat')
# def display():
#     return render_template('chat.html')
#
#
# @app.route('/chat', methods=['GET', 'POST'])
# def chat():
#     if request.method == 'POST':
#         user_username = request.form['user_username']
#         send_username = request.form['send_username']
#         account_type = request.form['account_type']
#         message = request.form['message']
#         query = text("INSERT INTO chat (user_username,send_username,account_type,"
#                      "message) VALUES(:user_username, :send_username, :account_type, :message)")
#         param = {"user_username": user_username, "send_username": send_username, "account_type": account_type,
#                  "message": message}
#         with engine.connect() as conn:
#             conn.execute(query, param)
#             conn.commit()
#         return redirect(url_for('show', send_username=send_username))
#     else:
#         return redirect('chat')
#
#
# @app.route('/show', methods=['GET', 'POST'])
# def show():
#     if request.method == 'POST':
#         send_username = session.get('username')
#         query = text("SELECT * FROM chat where send_username = :send_username")
#         params = {'send_username': send_username}
#         with engine.connect() as conn:
#             chats = conn.execute(query, params)
#             message = []
#             for row in chats:
#                 message.append(row)
#         return render_template('chat.html', chats=chats, user_username=user_username)
#     else:
#         return render_template('chat.html')

# #CART




# @app.route('/add_to_cart', methods=['POST', 'GET'])
# def add_to_cart(conn = engine.connect()):
#     if request.method == 'POST':
#         query = text("SELECT * FROM products")
#         resul = conn.execute(query)
#         products = []
#         for row in resul:
#             products.append(row)
#         max_id_query = text("SELECT MAX(cart_id) AS max_id FROM finalcarts")
#         result = conn.execute(max_id_query).fetchone()
#         max_id = result[0] if result[0] is not None else 1
#
#         # Convert max_id to an integer
#         max_id = int(max_id)
#         new_id = max_id + 1
#
#         cart_id = new_id
#
#         itemID = request.form['id']
#         image = request.form['image']
#         price = request.form['price']
#         amount = request.form['amount']
#         shopper_id = session['userID']
#         status = 'open'
#
#         # Check if the user already has an open cart
#         open_cart_query = text("SELECT cart_id FROM finalcarts WHERE shopper_id = :shopper_id AND status = 'open'")
#         open_cart_result = conn.execute(open_cart_query, {"shopper_id": shopper_id}).fetchone()
#         if open_cart_result:
#             cart_id = open_cart_result[0]  # Use the existing cart_id
#
#             # Check if the item already exists in the cart
#             existing_item_query = text("SELECT * FROM finalcarts WHERE cart_id = :cart_id AND itemID = :itemID")
#             existing_item_result = conn.execute(existing_item_query,
#                                                 {"cart_id": cart_id, "itemID": itemID}).fetchone()
#             if existing_item_result:
#                 # Item already exists, increase the amount
#                 existing_amount = int(existing_item_result[4])  # Accessing amount using index position
#                 new_amount = existing_amount + int(amount)
#
#                 update_query = text("UPDATE finalcarts SET amount = :new_amount "
#                                     "WHERE cart_id = :cart_id AND itemID = :itemID")
#                 update_params = {
#                     "new_amount": new_amount,
#                     "cart_id": cart_id,
#                     "itemID": itemID
#                 }
#                 with engine.connect() as conn:
#                     conn.execute(update_query, update_params)
#                     conn.commit()
#             else:
#                 # Item does not exist, add it to the cart
#                 query = text("INSERT INTO finalcarts (cart_id, itemID, image, price, amount, shopper_id, status) "
#                              "VALUES (:cart_id, :itemID, :image, :price, :amount, :shopper_id, :status)")
#                 params = {
#                     "cart_id": cart_id,
#                     "itemID": itemID,
#                     'image': image,
#                     "price": price,
#                     "amount": amount,
#                     "shopper_id": shopper_id,
#                     "status": status
#                 }
#                 with engine.connect() as conn:
#                     conn.execute(query, params)
#                     conn.commit()
#                 return redirect(url_for('products'))
#         else:
#             # Create a new cart
#             query = text("INSERT INTO finalcarts (cart_id, itemID, image, price, amount, shopper_id, status) "
#                          "VALUES (:cart_id, :itemID, :image, :price, :amount, :shopper_id, :status)")
#             params = {
#                 "cart_id": cart_id,
#                 "itemID": itemID,
#                 'image': image,
#                 "price": price,
#                 "amount": amount,
#                 "shopper_id": shopper_id,
#                 "status": status
#             }
#             with engine.connect() as conn:
#                 conn.execute(query, params)
#                 conn.commit()
#
#         return redirect(url_for('products.html'))

@app.route('/add_to_cart', methods=['POST', 'GET'])
def add_to_cart(conn=engine.connect()):
    if request.method == 'POST':
        query = text("SELECT * FROM products")
        resul = conn.execute(query)
        products = []
        for row in resul:
            products.append(row)
        max_id_query = text("SELECT MAX(cart_id) AS max_id FROM finalcarts")
        result = conn.execute(max_id_query).fetchone()
        max_id = result[0] if result[0] is not None else 1

        # Convert max_id to an integer
        max_id = int(max_id)
        new_id = max_id + 1

        cart_id = new_id

        itemID = request.form['itemID']
        image = request.form['image']
        price = request.form['price']
        amount = request.form['amount']
        shopper_id = session['userID']
        status = 'open'

        # Check if the user already has an open cart
        open_cart_query = text("SELECT cart_id FROM finalcarts WHERE shopper_id = :shopper_id AND status = 'open'")
        open_cart_result = conn.execute(open_cart_query, {"shopper_id": shopper_id}).fetchone()
        if open_cart_result:
            cart_id = open_cart_result[0]  # Use the existing cart_id

            # Check if the item already exists in the cart
            existing_item_query = text("SELECT * FROM finalcarts WHERE cart_id = :cart_id AND itemID = :itemID")
            existing_item_result = conn.execute(existing_item_query,
                                                {"cart_id": cart_id, "itemID": itemID}).fetchone()
            if existing_item_result:
                # Item already exists, increase the amount
                existing_amount = int(existing_item_result[4])  # Accessing amount using index position
                new_amount = existing_amount + int(amount)

                update_query = text("UPDATE finalcarts SET amount = :new_amount "
                                    "WHERE cart_id = :cart_id AND itemID = :itemID")
                update_params = {
                    "new_amount": new_amount,
                    "cart_id": cart_id,
                    "itemID": itemID
                }
                with engine.connect() as conn:
                    conn.execute(update_query, update_params)
                    conn.commit()
            else:
                # Item does not exist, add it to the cart
                query = text("INSERT INTO finalcarts (cart_id, itemID, image, price, amount, shopper_id, status) "
                             "VALUES (:cart_id, :itemID, :image, :price, :amount, :shopper_id, :status)")
                params = {
                    "cart_id": cart_id,
                    "itemID": itemID,
                    'image': image,
                    "price": price,
                    "amount": amount,
                    "shopper_id": shopper_id,
                    "status": status
                }
                with engine.connect() as conn:
                    conn.execute(query, params)
                    conn.commit()
            return redirect(url_for('view_products'))
        else:
            # Create a new cart
            query = text("INSERT INTO finalcarts (cart_id, itemID, image, price, amount, shopper_id, status) "
                         "VALUES (:cart_id, :itemID, :image, :price, :amount, :shopper_id, :status)")
            params = {
                "cart_id": cart_id,
                "itemID": itemID,
                'image': image,
                "price": price,
                "amount": amount,
                "shopper_id": shopper_id,
                "status": status
            }
            with engine.connect() as conn:
                conn.execute(query, params)
                conn.commit()
    return redirect(url_for('view_products'))


@app.route('/view_cart')
def view_cart():
    if 'userID' in session:
        shopper_id = session['userID']
        with engine.connect() as conn:
            query = text("SELECT * FROM finalcarts WHERE shopper_id = :shopper_id AND status = 'open'")
            items = conn.execute(query, {"shopper_id": shopper_id}).fetchall()
# Retrieve cart items for the logged-in user
        cart_query = text("SELECT * FROM finalcarts WHERE shopper_id = :shopper_id AND status = 'open'")
        cart_items = conn.execute(cart_query, {"shopper_id": shopper_id}).fetchall()

        return render_template('cart.html', cart_items=cart_items)


@app.route('/remove_from_cart/<int:item_id>', methods=['POST'])
def remove_from_cart(item_id):
    if 'id' in session:
        shopper_id = session['id']

        # Remove item from the cart
        remove_query = text("DELETE FROM finalcarts WHERE item_id = :item_id AND shopper_id = :shopper_id")
        conn.execute(remove_query, {"item_id": item_id, "shopper_id": shopper_id})
        conn.commit()

        return redirect(url_for('view_cart'))



# @app.route('/submit_order/<int:cart_id>', methods=['POST'])
# def submit_order(cart_id):
#     # Update the cart status to 'closed' in the database
#     query = text("UPDATE cart SET status = 'closed' WHERE cart_id = :cart_id")
#     conn.execute(query, {"cart_id": cart_id})
#     conn.commit()
#
#     # Flash a success message
#     flash("Order submitted successfully.")
#
#     # Redirect to the customer view page
#     return redirect(url_for('customer'))
#
#






if __name__ == '__main__':
    app.run(debug=True)
