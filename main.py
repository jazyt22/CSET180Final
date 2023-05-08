from flask import Flask, render_template, request, url_for, flash, redirect
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
#
# # Define a function to check if the email already exists in the database
# def check_email_exists(email):
#     cursor = conn_str.cursor()
#     cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
#     user = cursor.fetchone()
#     cursor.close()
#     if user is not None:
#         return True
#     else:
#         return False


#regitser account

# @app.route('/register', methods=['GET', 'POST'])
# def create_account():
#     if request.method == 'POST':
#         conn.execute(text("INSERT INTO register VALUES (:name, :email, :username, :password, :userID, :account_type)"),request.form)
#         conn.commit()
#     return render_template("register.html")


@app.route('/register', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        email = request.form['email']
        # Check if the email already exists in the database
        user = conn.execute(text("SELECT * FROM register WHERE email=:email"), {'email': email}).fetchone()
        if user is not None:
            flash("An account with this email already exists.")
            return redirect(url_for('create_account'))
        else:
            conn.execute(text("INSERT INTO register VALUES (:name, :email, :username, :password, :userID, :account_type)"),request.form)
            conn.commit()
            flash("Account created successfully.")
            return redirect(url_for('home'))
    return render_template("register.html")


#
# ##login
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == "POST":
#         username = request.form['username']
#         password = request.form['password']
#         if password == 'bobbyS' or 'Asing!':
#             password = password
#     else:
#         password = p(password)
#     message = text("SELECT * FROM register WHERE username = :username AND password = :password")
#     info = {"username": username, "password": password}
#     solution = conn.execute(message,info)
#     account = solution.fetchone()
#     if account is None:
#         return render_template('index.html')
#     else:
#         session['name'] = account[0]
#         session['email'] = account[1]
#         session['username'] = account[2]
#         session['password'] = account[3]
#         session['userID'] = account[4]
#         session['account_type'] = account[5]
#
#

if __name__ == '__main__':
    app.run(debug=True)