from flask import Flask, render_template

# Create a Flask Instance
app = Flask(__name__)
# it help flask to determine the root path of the application

# Create a route decorator

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user/<name>')
def user(name):
    return f"<h2>hello {name}</h1>"

if __name__ == "__main__":
   app.run()
