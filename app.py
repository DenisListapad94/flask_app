from datetime import datetime
from werkzeug.security import generate_password_hash
from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(500), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    pr = db.relationship('Profiles', backref='users', uselist=False)

    def __repr__(self):
        return f' users {self.id}'

class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    city = db.Column(db.String(50))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f' profiles {self.id}'


menu = [{'url': "/index", "field": 'Главная'},
        {'url': "/about", "field": 'О нас'},
        {'url': "/content", "field": 'Контент'},
        {'url': "/feedback", "field": 'Обратная связь'},
        {'url': "/register", "field": 'Регистация'},
        ]


@app.route("/index")
def index():
    users = []
    try:
        users = Users.query.all()
    except:
        print("error")
    return render_template('index.html', menu=menu, title=menu[0],users=users)


@app.route("/about")
def about():
    return render_template("about.html", menu=menu, title=menu[1])


@app.route("/content")
def content():
    return render_template("content.html", menu=menu, title=menu[2], name="user")


@app.route("/feedback", methods=['GET', 'POST'])
def feedback():
    return render_template("feedback.html", menu=menu, title=menu[3])


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            hash = generate_password_hash(request.form['psw'])
            user = Users(email=request.form['email'], password=hash)
            db.session.add(user)
            db.session.flush()

            prof = Profiles(name=request.form['name'], age=request.form['age'],
                            city=request.form['city'], user_id=user.id)
            db.session.add(prof)
            db.session.commit()
        except:
            db.session.rollback()
            print("error")

    return render_template("register.html", menu=menu, title=menu[4])


if __name__ == "__main__":
    app.run(debug=True)

# with app.test_request_context():
#     print(url_for("index"))
#     print(url_for("about"))
#     print(url_for("content",username="Kolya"))
