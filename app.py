from flask import Flask, render_template, request, redirect
#render_template shows HTML-pages
#request reads data from forms
#redirect sends user to another page
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


# Adds route for the event form
@app.route("/addevent", methods=["GET", "POST"])
def add_event():
    if request.method == "POST":            # Has user sent the form?
        title       = request.form["title"]
        date        = request.form["date"]
        start_time  = request.form["start_time"]
        end_time    = request.form["end_time"]
        description = request.form["description"]

        new_event = Event(
            title = title,
            date = date,
            start_time = start_time,
            end_time = end_time,
            description = description
            )
        
        # Save userdata to db
        db.session.add(new_event) # Add object in session
        db.session.commit()        # Write to SQLite

        return redirect("/") # Sends user back to homepage after save
    
    return render_template("addevent.html")

# Adds route to Homepage
@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    # If db does not exist, create it:
    with app.app_context():
        db.create_all()
    app.run(debug=True)