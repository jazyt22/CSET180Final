from flask import Flask, render_template, request, url_for
from sqlalchemy import Column, Integer, String, Numeric, create_engine, text

app = Flask(__name__, template_folder='template')

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


@app.route('/register', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        conn.execute(text("INSERT INTO register VALUES (:name, :email, :username, :password, :userID, :account_type)"),request.form)
        conn.commit()
    return render_template("register.html")





if __name__ == '__main__':
    app.run(debug=True)