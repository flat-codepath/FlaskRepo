from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import  date
import mysql

# Create a Flask Instance
app = Flask(__name__)  # it help flask to determine the root path of the application
# Add Database
# Old SQLite DB
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123@localhost/our_users'
# secretkey
app.config['SECRET_KEY'] = "my super secret key that no one is suppose to know"
# initialize the Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Create Model
class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    # Do some password stuff
    password_hash = db.Column(db.String(400))

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # create A string
    def __repr__(self):
        return f'<User {self.name}>'


@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = users.query.get_or_404(id)
    name = None
    form = UserForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("user Delete Successfully")
        our_users = users.query.order_by(users.id)
        return render_template('add_user.html', form=form, name=name, our_users=our_users)
    except:
        flash("Whoops! there is a problem deleting the user id")
        our_users = users.query.order_by(users.id)
        return render_template('add_user.html', form=form, name=name, our_users=our_users)


# 5.Create a Form Class
class NameForm(FlaskForm):
    name = StringField("what's  your Name", validators=[DataRequired()])
    submit = SubmitField('Submit')


class PasswordForm(FlaskForm):
    email = StringField("what's Your Email", validators=[DataRequired()])
    password_hash = PasswordField("What's Your password", validators=[DataRequired()])
    submit = SubmitField("submit")


class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    favorite_color = StringField('Favorite Color')
    password_hash = PasswordField('password', validators=[DataRequired(),
                                                          EqualTo('password_hash2', message='passwords must match')])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('submit')


# Create a route decorator
@app.route('/')
def index():
    first_name = 'John'
    favorite_pizza = ['pepperoni', 'Cheese', "Mushrooms", 41]
    stuff = 'this is Bold  text'
    flash("Wellcome to Our Webpage")
    return render_template('index.html', first_name=first_name,
                           stuff=stuff, favorite_pizza=favorite_pizza)


'''FILTERS
safe
capitalize
lower
upper
title
trim
striptags
'''


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', user_name=name)


# create Custom Error Pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# Internal Server Error
# @app.errorhandler(500)
# def page_not_found(e):
#     return render_template('505.html')


# Create Name Page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NameForm()
    # Validation Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted successfully")
    return render_template('name.html', name=name, form=form)


@app.route('/test_pw', methods=['GET', 'POST'])
def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()
    # Validation Form
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data

        
        
        pw_to_check =users.query.filter_by(email=email).first()
        # passes =check_password_hash(pw_to_check.password_hash)
        # flash("Form Submitted successfully")
    return render_template('test_pw.html', email=email, password=password, form=form,pw_to_check=pw_to_check,passed=passed)


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        try:
            db.session.commit()
            flash('User Updated Successfully!')
            return render_template("update.html", form=form, name_to_update=name_to_update)
        except:
            flash('Error looks Like There Was a Probelm try again')
            return render_template("update.html", form=form, name_to_update=name_to_update)
    else:
        return render_template("update.html", form=form, name_to_update=name_to_update)


@app.route('/user/add', methods=["GET", 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        print('valid data----------------------')
        user = users.query.filter_by(email=form.email.data).first()
        print(user)
        if user is None:
            # Hash the password!!!
            hash_pw = generate_password_hash(form.password_hash.data, 'pbkdf2:sha256')
            user = users(name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data,
                         password_hash=hash_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
        form.password_hash.data = ''
        flash('User added Successfully')
    our_users = users.query.order_by(users.id)
    return render_template('add_user.html', form=form, name=name, our_users=our_users)

@app.route('/date')
def get_current_date():
   favorite_pizza={
        "john":"pepperoni",
        "Mary":"Cheese",
        "Tim":"Mushroom",
    }
   return favorite_pizza
   # return {'Date':date.today()}








with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)

# MigrationDatabase
# pip install Flask-Migrate

# step 1 initial the migrations folder
# flask db init

# step 2
#  Perform database migrations.
# flask db migrate -m "intial migration"
# flask db upgrade

# Options:
#   init            Creates a new migration repository.
#   list-templates  List available templates.
#   merge           Merge two revisions together, creating a new revision file
#   migrate         Autogenerate a new revision file (Alias for 'revision...
#   revision        Create a new revision file.
#   show            Show the revision denoted by the given symbol.
#   stamp           'stamp' the revision table with the given revision;...
#   upgrade         Upgrade to a later version

# flask db migrate -m "intital migrations"


# Hasing Password
# >>> u2=users()
# >>> u2.password='cat'
# >>> u2.password_hash
# 'scrypt:32768:8:1$RTshoVoKWvRoD1WC$28a0309004d521c04203ffbf28d456fa7f26f0873141381c793e169c7b156337b3ba68ad9716292b9c65ccdd5d01f9a2fffed5b5beb8494e26b8abd8d2248c04'
# >>> u.verify_password('cat')
# True
