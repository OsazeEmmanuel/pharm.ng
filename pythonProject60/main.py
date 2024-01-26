from flask import Flask, request, render_template, current_app, redirect, url_for, flash
from flask_bootstrap import Bootstrap4
from flask_login import UserMixin, login_user, login_required, logout_user, login_manager, LoginManager
from flask_sqlalchemy import SQLAlchemy
from forms import UserForm, ItemsForm
from werkzeug.security import generate_password_hash, check_password_hash





app = Flask(__name__)

db = SQLAlchemy()

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///drugs.db"
app.config["SECRET_KEY"] = "my_key"

db.init_app(app)

bootstrap = Bootstrap4(app)
loginmanager = LoginManager()
loginmanager.init_app(app)
loginmanager.login_view = "login"


class DrugstoreItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    img = db.Column(db.LargeBinary, nullable=False)
    category = db.Column(db.String, nullable=False)


with app.app_context():
    db.create_all()


class User2(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.Integer, nullable=False)

    # def get_reset_token(self, expires_sec=1800):
    #     s = Serializer(app.config['SECRET_KEY'], expires_sec)
    #     return s.dumps({'user_id': self.id}).decode('utf-8')
    #
    # @staticmethod
    # def verify_reset_token(token):
    #     s = Serializer(app.config['SECRET_KEY'])
    #     try:
    #         user_id = s.loads(token)['user_id']
    #     except:
    #         return None
    #     return db.session.execute(db.select(User).where(User.id == user_id))
    #         #User.query.get(user_id)
    #
    # def __repr__(self):
    #     return f"User({self.name}, {self.email})"



with app.app_context():
    db.create_all()


@loginmanager.user_loader
def load_user(user_id):
    return db.get_or_404(User2, user_id)


@app.route("/landing", methods=["POST", "GET"])
def landingpage():
    return "YOU WILL LOGIN AS SOON AS APP IS SET"

@app.route("/")
def home():
    return render_template("base.html")

@app.route("/add_item", methods=["POST", "GET"])
def add_item():
    form = ItemsForm()
    if form.validate_on_submit():
        # name = request.form.get("name")
        # category = request.form.get("category")
        # img = request.form.get("img")
        # item = DrugstoreItem(name=name, category=category, img=img)
        # db.session.add(item)
        # db.session.commit()
        return "Item Added"
    return render_template("items.html", form=form)

@app.route("/item_added", methods=["POST", "GET"])
def item_added():
    return "Item successfully added"


@app.route("/Signup", methods=["POST", "GET"])
def signup():
    form = UserForm()
    if request.method == "POST":
        user_email = request.form["email"]
        user = db.session.execute(db.select(User2).where(User2.email == user_email)).scalar()
        if user:
            flash("Account already exist for this email. Kindly login")
            return "Login"
        else:
            user_name = request.form["name"]
            user_password = request.form["password"]
            hashed_password = generate_password_hash(method="pbkdf2:sha1", salt_length=8, password=user_password)

            new_user = User2(name=user_name, email=user_email, password=hashed_password)

            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return "New User added"
    return render_template("signup.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    return render_template("base.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)