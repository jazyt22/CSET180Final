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
        if password == 'bobbyS' or password == 'Asing!':
            password = password
        else:
            password = p(password)
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
            if user[5] == 'admin':
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



# @app.route('/vendor')
# def vendor():
#     session_id = session.get('id')
#     query = text("SELECT * FROM register WHERE vendor_id = :session_id")
#     result = conn.execute(query, {'session_id': session_id})
#     products = []
#     for row in result:
#         products.append(row)
#     return render_template('vendor.html', products=products)

# @app.route('/admin')
# def customer():
#     query = text("SELECT * FROM register")
#     result = conn.execute(query)
#     products = []
#     for row in result:
#         products.append(row)
#     return render_template('admin.html', products=products)





if __name__ == '__main__':
    app.run(debug=True)