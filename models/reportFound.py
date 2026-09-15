from extentions import db


class FoundItem(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    found_location = db.Column(db.String(200), nullable=False)
    found_date = db.Column(db.String(20), nullable=False)
    collection_place = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default="Active")