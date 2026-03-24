from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Create an SQL-file
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///planner.db"
db = SQLAlchemy(app) # Connect db to the Flask-app

# Create class which defines a table in db.
class Event(db.Model):
    id          = db.Column(db.Integer, primary_key = True) #Unique identifier for each activity
    title       = db.Column(db.String(100)) # <-- Title, max 100 chars
    date        = db.Column(db.String(20))
    start_time  = db.Column(db.String(10))
    end_time    = db.Column(db.String(10))
    description = db.Column(db.Text)

@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    # If db does not exist, create it:
    with app.app_context():
        db.create_all()
    app.run(debug=True)