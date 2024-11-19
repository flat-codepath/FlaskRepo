from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask application
app = Flask(__name__)

# Configure the database URI
# Replace with your actual MySQL database details
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123@localhost/college'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional, to disable tracking modifications

# Initialize the SQLAlchemy object
db = SQLAlchemy(app)

# Example model to test the connection
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

# Route to test the database connection
@app.route('/')
def index():
    # Just a simple query to test the database connection
    users = User.query.all()
    return f"Users in the database: {[user.username for user in users]}"

# Create the database tables (use this only once, for testing)
@app.before_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
