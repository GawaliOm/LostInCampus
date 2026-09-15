from flask import Flask, render_template, request

from extentions import db
from models.reportLost import LostItem
from models.reportFound import FoundItem

from dotenv import load_dotenv

import cloudinary
import os

from cloudinary.uploader import upload, destroy


app = Flask(__name__)


load_dotenv()


cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///lostincampus.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/")
def home():
    return render_template("index.html")


# Report Lost Item
@app.route("/report/lost", methods=["GET", "POST"])
def reportLost():

    if request.method == "POST":

        name = request.form["name"]
        class_name = request.form["class_name"]
        contact_number = request.form["contact_number"]
        email = request.form["email"]

        item_name = request.form["item_name"]
        description = request.form["description"]

        lost_location = request.form["lost_location"]
        lost_date = request.form["lost_date"]

        image = request.files["image"]

        image_url = None

        if image and image.filename:

            result = upload(
                image,
                folder="lostincampus/lost"
            )

            image_url = result["secure_url"]



        lost_item = LostItem(
            name=name,
            class_name=class_name,
            contact_number=contact_number,
            email=email,
            item_name=item_name,
            description=description,
            image_url=image_url,
            lost_location=lost_location,
            lost_date=lost_date
        )

        db.session.add(lost_item)
        db.session.commit()

        return "Lost report received"


    return render_template("reportLost.html")


@app.route("/report/found", methods=["GET", "POST"])
def reportfound():

    if request.method == "POST":

        name = request.form["name"]
        contact_number = request.form["contact_number"]
        email = request.form["email"]

        item_name = request.form["item_name"]
        description = request.form["description"]

        found_location = request.form["found_location"]
        found_date = request.form["found_date"]
        collection_place = request.form["collection_place"]

        image = request.files["image"]

        image_url = None

        if image and image.filename:
            result = upload(
                image,
                folder="lostincampus/found"
        )

            image_url = result["secure_url"]

        found_item = FoundItem(
            name=name,
            contact_number=contact_number,
            email=email,
            item_name=item_name,
            description=description,
            image_url=image_url,
            found_location=found_location,
            found_date=found_date,
            collection_place=collection_place
        )

        db.session.add(found_item)
        db.session.commit()

        return "Found Report Sent"


    return render_template("reportFound.html")


@app.route("/lost-items")
def lost_items():

    items = LostItem.query.filter_by(status="Active").all()

    return render_template(
        "lostItems.html",
        lost_items=items
    )

@app.route("/found-items")
def found_items():

    items = FoundItem.query.filter_by(status="Active").all()

    return render_template(
        "foundItems.html",
        found_items=items
    )


@app.route("/lost/<int:id>")
def lost_detail(id):

    item = LostItem.query.get_or_404(id)

    return render_template(
        "lost_detail.html",
        item=item
    )


@app.route("/found/<int:id>")
def found_detail(id):

    item = FoundItem.query.get_or_404(id)

    return render_template(
        "found_detail.html",
        item=item
    )


@app.route("/delete/<report_type>/<int:id>", methods=["GET", "POST"])
def delete_report(report_type, id):

    if report_type == "lost":
        item = LostItem.query.get_or_404(id)

    elif report_type == "found":
        item = FoundItem.query.get_or_404(id)

    else:
        return "Invalid report type"

    if request.method == "POST":

        email = request.form["email"]

        if email != item.email:
            return render_template(
                "delete_report.html",
                error="Email does not match the report.",
                report_type=report_type,
                id=id
            )

        # Delete image from Cloudinary
        if item.image_url:

            try:
                public_id = item.image_url.split("/")[-1]
                public_id = public_id.rsplit(".", 1)[0]

                if report_type == "lost":
                    public_id = "lostincampus/lost/" + public_id
                else:
                    public_id = "lostincampus/found/" + public_id

                destroy(public_id)

            except Exception:
                pass

        # Delete report from database
        db.session.delete(item)
        db.session.commit()

        return "Report deleted successfully."

    return render_template(
        "delete_report.html",
        report_type=report_type,
        id=id
    )



if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)