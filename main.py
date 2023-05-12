from flask import Flask, render_template, request, url_for, flash, redirect,session
from sqlalchemy import Column, Integer, String, Numeric, create_engine, text

app = Flask(__name__, template_folder='template')
app.secret_key = 'Wilson02!'

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
    return render_template('home.html')

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
            conn.execute(text("INSERT INTO register VALUES (:name, :email, :username, :password, :userID, :account_type)"), request.form)
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




#vendor

@app.route('/vendor')
def vendor():
    session_id = session.get('userID')
    query = text("SELECT * FROM products WHERE vendor_id = :session_id")
    result = conn.execute(query, {'session_id': session_id})
    products = []
    for row in result:
        products.append(row)
    return render_template('vendor.html', products=products)


#vendor add products
@app.route('/v_add', methods = ['GET'])
def ven_add():
    return render_template('vendor_add_product.html')
@app.route('/vendor_product', methods = ['POST'])
def v_add_product():
    max_product = text("select max(itemID) from products")
    max_id = conn.execute(max_product).fetchone()[0]
    new_id = max_id + 1 if max_id is not None else 1

    title = request.form['title']
    description = request.form ['description']
    image = request.form ['image']
    category = request.form ['category']
    colors = request.form ['colors']
    sizes = request.form ['sizes']
    inventory = request.form ['inventory']
    price = request.form ['price']
    itemID = request.form ['itemID']
    discount_price = request.form ['discount_price']
    vendor_id = session.get('userID')

    x = text("INSERT INTO products (title, description, image, category, colors,"
              " sizes, inventory, price, itemID, discount_price, vendor_id) VALUES "
              "(:title, :description, :image, :category, :colors, :sizes, :inventory, :price, :itemID"
              ", :discount_price, :vendor_id)")
    y = {"title": title, "description": description, "image" : image, "category" : category, "colors" : colors,
        "sizes" : sizes, "inventory" : inventory, "price" : price, "itemID" : new_id, "discount_price" : discount_price,
        "vendor_id" : vendor_id}
    conn.execute(x,y)
    conn.commit()

    return render_template('vendor_add_product.html')


#admin
@app.route('/admin')
def admin():
    query = text("SELECT * FROM products")
    result = conn.execute(query)
    products = []
    for row in result:
        products.append(row)
    return render_template('admin.html', products=products)
@app.route('/add_product', methods = ['GET'])
def add_product():
    return render_template('add_product.html')


@app.route('/add_product', methods = ['POST'])
def add():
    conn.execute(text("INSERT INTO products VALUES (:title, :description, :image, :category, :colors,"
                      " :sizes, :inventory, :price, :itemID, :discount_price, :vendor_id)"), request.form)
    conn.commit()
    return render_template('add_product.html')


##look at all products/filter both admin and vendor
@app.route('/view_products', methods=['GET'])
def view():
    return render_template('view_products.html')

@app.route('/view_products', methods=[ 'POST'])
def view_products():
    products = conn.execute(text("select * from products")).all()
    if request.method == "POST":
        if request.form["button"] == "My Products":
            user_id = session.get("userID")
            products = conn.execute(text("select * from products where vendor_id = vendor_id"), {"vendor_id" : user_id}).all()
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
@app.route('/delete', methods = ["GET"])
def delete():
    return render_template("delete.html")

@app.route('/delete', methods=["POST"])
def delete_exams():
    conn.execute(text("Delete from products where itemID = :itemID"), request.form)
    conn.commit()
    return render_template("delete.html")


##my accounts page
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





if __name__ == '__main__':
    app.run(debug=True)