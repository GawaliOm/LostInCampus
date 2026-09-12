from flask import Flask, render_template, request
from extentions import db
from models.reportLost import LostItem
from models.reportFound import FoundItem


app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///lostincampus.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Function to load homepage

@app.route("/")
def home():
    return render_template("index.html")


# Function for reporting lost item

@app.route("/report/lost", methods = ["GET", "POST"])
def reportLost():

    if request.method == "POST":
        name = request.form["name"]
        item_name = request.form["item_name"]
        email = request.form["email"]
        class_name = request.form["class_name"]
        contact_number = request.form["contact_number"]
        description = request.form["description"]
        lost_location = request.form["lost_location"]
        lost_date = request.form["lost_date"]

        lost_item = LostItem(
            name=name,
            class_name=class_name,
            contact_number=contact_number,
            email=email,
            item_name=item_name,
            description=description,
            lost_location=lost_location,
            lost_date=lost_date
        )

        db.session.add(lost_item)
        db.session.commit()

        return "lost report recived"
    
    return render_template("reportLost.html")


# Function for reporting founded item

@app.route("/report/found", methods = ["GET", "POST"])
def reportfound():

    if request.method == "POST":
        name = request.form["name"]
        item_name = request.form["item_name"]
        email = request.form["email"]
        contact_number = request.form["contact_number"]
        description = request.form["description"]
        found_location = request.form["found_location"]
        found_date = request.form["found_date"]
        collection_place = request.form["collection_place"]


        found_item = FoundItem(
            name = name,
            item_name = item_name,
            email = email,
            contact_number = contact_number,
            description = description,
            found_location = found_location,
            found_date = found_date,
            collection_place = collection_place
        )

        db.session.add(found_item)
        db.session.commit()


        
        return "Found Report Sent"
    return render_template("reportFound.html")


# route to view lost items page

@app.route("/lost-items")
def lost_items():

    items = LostItem.query.filter_by(status="Active").all()

    return render_template("lostItems.html", lost_items=items)


# route for found items page

@app.route("/found-items")
def found_items():
    items = FoundItem.query.filter_by(status="Active").all()

    return render_template("foundItems.html", lost_items=items)

if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug = True)   