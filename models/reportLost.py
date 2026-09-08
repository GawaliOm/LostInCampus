from extentions import db 

class LostItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable = False)
    class_name = db.Column(db.String(20), nullable = False)
    contact_number = db.Column(db.String(15), nullable = False)
    email = db.Column(db.String(70), nullable = False)
    item_name = db.Column(db.String(50), nullable = False)
    description = db.Column(db.String(100), nullable = False)
    lost_location = db.Column(db.String(100), nullable = False)
    lost_date = db.Column(db.String(40), nullable = False)
    status = db.Column(db.String(20), default = "Active")
