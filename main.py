from flask import Flask, render_template, request
from sqlalchemy import Column, Integer, String, Numeric, create_engine, text

app = Flask(__name__, template_folder="template")

conn_str = "mysql://root:Wilson02!@localhost/180Final"
engine = create_engine(conn_str, echo=True)
connection = engine.connect()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/', methods = ["GET"])
def create_account():
    return render_template("register.html")

@app.route('/register', methods = ["POST"])
def create_account_type():
    connection.execute(text("INSERT INTO cset160 VALUES (:name, :email, :username, :password, :userID, :account_type)"), request.form)
    connection.commit()
    return render_template("register.html")

# ##look at all accounts/filter
# @app.route('/accounts', methods=["GET", "POST"])
# def accounts():
#     cset160 = connection.execute(text("select * from cset160")).all()
#     if request.method == "POST":
#         if request.form["button"] == "teacher":
#             cset160 = connection.execute(text("select * from cset160 where Account_Type = 'Teacher' ;")).all()
#             return render_template("accounts.html", cset160=cset160)
#         elif request.form["button"] == "student":
#             cset160 = connection.execute(text("select * from cset160 where Account_Type = 'Student'; ")).all()
#             return render_template("accounts.html", cset160=cset160)
#     return render_template("accounts.html", cset160=cset160[:10])


if __name__ == '__main__':
    app.run(debug=True)