from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
app = Flask(__name__)
# Add Database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# app.config['SECRET_KEY'] = "my super secret key that no one is suppose to know"

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Soni@123localhost/users'
db = SQLAlchemy(app)


if __name__ == "__main__":
    app.run(debug=True)
