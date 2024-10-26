from flask import Flask, render_template

# Create a Flask Instance
app = Flask(__name__)
# it help flask to determine the root path of the application

# Create a route decorator

@app.route('/')
def index():
    first_name='John'
    favorite_pizza=['pepperoni','Cheese',"Mushrooms",41]
    stuff='this is Bold  text'
    return render_template('index.html',first_name=first_name,
                           stuff=stuff,favorite_pizza=favorite_pizza)

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
    return  render_template('user.html',user_name=name)

# create Custom Error Pages
# invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return  render_template('404.html'),404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return  render_template('500.html'),500


if __name__ == "__main__":
   app.run(debug=True)

