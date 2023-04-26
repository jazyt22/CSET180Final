from flask import Flask, render_template, request
from sqlalchemy import Column, Integer, String, Numeric, create_engine, text

app = Flask(__name__, template_folder='template')

conn_str = "mysql://root:Wilson02!@localhost/180Final"
engine = create_engine(conn_str, echo=True)
connection = engine.connect()

@app.route('/')
def home():
    return render_template('home.html')

#regitser account
@app.route('/reg', methods = ["GET"])
def create_account():
    return render_template("register.html")

@app.route('/register', methods = ["POST"])
def create_account_type():
    connection.execute(text("INSERT INTO cset160 VALUES (:name, :email, :username, :password, :userID, :account_type)"), request.form)
    connection.commit()
    return render_template("register.html")


if __name__ == '__main__':
    app.run(debug=True)