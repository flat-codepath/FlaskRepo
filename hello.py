from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# Create a Flask Instance
app = Flask(__name__)
app.config['SECRET_KEY'] = "my super secret key that no one is suppose to know"


# it help flask to determine the root path of the application

# 5.Create a Form Class
class NameForm(FlaskForm):
    name = StringField("what's  your Name", validators=[DataRequired()])
    submit = SubmitField('Submit')


# Create a route decorator
@app.route('/')
def index():
    first_name = 'John'
    favorite_pizza = ['pepperoni', 'Cheese', "Mushrooms", 41]
    stuff = 'this is Bold  text'
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
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

# Create Name Page
@app.route('/name',methods=['GET','POST'])
def name():
    name=None
    form=NameForm()
    # Validation Form
    if form.validate_on_submit():
        name =form.name.data
        # form.name.data=''

    return  render_template('name.html',name=name,form=form)

if __name__ == "__main__":
    app.run(debug=True)
