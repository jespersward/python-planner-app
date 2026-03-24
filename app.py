from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from collections import defaultdict
from datetime import date

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

    def __repr__(self):
        return f"<Event {self.title}>"


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
    events = Event.query.order_by(Event.date, Event.start_time).all() # Retrieves all rows from Event-table in correct order
    
    # Creating grouped events to fix structure of events
    # All events on the same day will be shown in the same "box"
    grouped_events = defaultdict(list)
    today_events = []

    today_str = date.today().isoformat()

    for event in events:
        if event.date == today_str:
            today_events.append(event)
        else:
            grouped_events[event.date].append(event)

    return render_template(
        "index.html",
        today_events = today_events,
        grouped_events = grouped_events
    ) # Render index.html and give access to variable "events"

# Adds delete-route
@app.route("/delete/<int:event_id>")
def delete_event(event_id):
    event = Event.query.get_or_404(event_id) # Retrieve event with ID, if non-exsistant show 404-error
    db.session.delete(event)
    db.session.commit()
    return redirect("/")

@app.route("/edit/<int:event_id>", methods=["GET", "POST"])
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)

    if request.method == "POST":
        event.title         = request.form["title"]
        event.date          = request.form["date"]
        event.start_time    = request.form["start_time"]
        event.end_time      = request.form["end_time"]
        event.description   = request.form["description"]

        db.session.commit()

        return redirect("/")
    return render_template("edit_event.html", event = event)

if __name__ == "__main__":
    # If db does not exist, create it:
    with app.app_context():
        db.create_all()
    app.run(debug=True)



