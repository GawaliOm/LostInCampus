import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash
from extentions import db
from models.reportLost import LostItem
from models.reportFound import FoundItem
from utils.uploader import save_uploaded_image, delete_uploaded_image
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "lostincampus_admin_secret_key_2026")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///lostincampus.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Inject current datetime into all templates (for footer copyright year)
@app.context_processor
def inject_now():
    return {'now': datetime.now()}


# Home Page: Recent Lost and Found Reports
@app.route("/")
def home():
    recent_lost = LostItem.query.filter_by(status="Active").order_by(LostItem.id.desc()).limit(6).all()
    recent_found = FoundItem.query.filter_by(status="Active").order_by(FoundItem.id.desc()).limit(6).all()
    return render_template("index.html", recent_lost=recent_lost, recent_found=recent_found)

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
        image = request.files.get("image")

        image_url = save_uploaded_image(image, folder="lostincampus/lost")

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

        return redirect(url_for("lost_items"))

    return render_template("reportLost.html")

# Report Found Item
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
        image = request.files.get("image")

        image_url = save_uploaded_image(image, folder="lostincampus/found")

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

        return redirect(url_for("found_items"))

    return render_template("reportFound.html")

# View Lost Items Directory
@app.route("/lost-items")
def lost_items():
    items = LostItem.query.order_by(LostItem.id.desc()).all()
    return render_template("lostItems.html", lost_items=items)

# View Found Items Directory
@app.route("/found-items")
def found_items():
    items = FoundItem.query.order_by(FoundItem.id.desc()).all()
    return render_template("foundItems.html", found_items=items)

# Lost Item Details
@app.route("/lost/<int:id>")
def lost_detail(id):
    item = db.get_or_404(LostItem, id)
    return render_template("lost_detail.html", item=item)

# Found Item Details
@app.route("/found/<int:id>")
def found_detail(id):
    item = db.get_or_404(FoundItem, id)
    return render_template("found_detail.html", item=item)

# Delete Report (User Verification by Email)
@app.route("/delete/<report_type>/<int:id>", methods=["GET", "POST"])
def delete_report(report_type, id):
    if report_type == "lost":
        item = db.get_or_404(LostItem, id)
    elif report_type == "found":
        item = db.get_or_404(FoundItem, id)
    else:
        return "Invalid report type"

    if request.method == "POST":
        email = request.form["email"]

        if email.strip().lower() != item.email.strip().lower():
            return render_template(
                "delete_report.html",
                error="Email address does not match the report.",
                report_type=report_type,
                id=id
            )

        if item.image_url:
            delete_uploaded_image(item.image_url, folder=f"lostincampus/{report_type}")

        db.session.delete(item)
        db.session.commit()

        if report_type == "lost":
            return redirect(url_for("lost_items"))
        else:
            return redirect(url_for("found_items"))

    return render_template("delete_report.html", report_type=report_type, id=id)

# ----------------------------------------------------
# ADMIN PANEL WITH PASSWORD PROTECTION ('admin123')
# ----------------------------------------------------
@app.route("/admin", methods=["GET", "POST"])
def admin():
    error = None
    if request.method == "POST":
        password = request.form.get("password", "").strip()
        if password == "admin123":
            session["admin_logged_in"] = True
            return redirect(url_for("admin"))
        else:
            error = "Invalid password. Access denied."

    # Check if admin is authenticated
    if not session.get("admin_logged_in"):
        return render_template("admin_login.html", error=error)

    all_lost = LostItem.query.order_by(LostItem.id.desc()).all()
    all_found = FoundItem.query.order_by(FoundItem.id.desc()).all()
    return render_template("admin.html", lost_items=all_lost, found_items=all_found)

@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin"))

@app.route("/admin/delete/<report_type>/<int:id>", methods=["POST"])
def admin_delete(report_type, id):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin"))

    if report_type == "lost":
        item = db.get_or_404(LostItem, id)
    elif report_type == "found":
        item = db.get_or_404(FoundItem, id)
    else:
        return "Invalid report type", 400

    if item.image_url:
        delete_uploaded_image(item.image_url, folder=f"lostincampus/{report_type}")

    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("admin"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)