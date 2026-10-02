import os
import sys

# Ensure project root in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app
from extentions import db
from models.reportLost import LostItem
from models.reportFound import FoundItem

def seed():
    with app.app_context():
        # Drop and recreate all tables
        db.drop_all()
        db.create_all()

        print("Seeding initial Lost & Found items...")

        lost_items = [
            LostItem(
                name="Rohan Sharma",
                class_name="CS-3A",
                contact_number="+91 98765 43210",
                email="rohan.s@campus.edu",
                item_name="AirPods Pro in White Case",
                description="Left on Reading Table #4 in Library. Case has a small blue sticker on bottom.",
                image_url="https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?auto=format&fit=crop&w=600&q=80",
                lost_location="Main Library 2nd Floor",
                lost_date="2026-09-28",
                status="Active"
            ),
            LostItem(
                name="Om Gawali",
                class_name="TE-IT",
                contact_number="+91 91234 56789",
                email="om.gawali@campus.edu",
                item_name="Student ID Card - Om Gawali",
                description="Blue lanyard with campus emblem. Contains Student ID card #2024-IT-088.",
                image_url="https://images.unsplash.com/photo-1578574577315-3fbeb0cecdc2?auto=format&fit=crop&w=600&q=80",
                lost_location="College Canteen Ground",
                lost_date="2026-09-29",
                status="Active"
            ),
            LostItem(
                name="Ananya Kulkarni",
                class_name="SE-MECH",
                contact_number="+91 99887 76655",
                email="ananya.k@campus.edu",
                item_name="Casio Scientific Calculator",
                description="Black scientific calculator. Has silver initial 'A.K.' marked on back cover.",
                image_url="https://images.unsplash.com/photo-1611125832047-1d7ad1e8e48b?auto=format&fit=crop&w=600&q=80",
                lost_location="Engineering Lecture Hall 102",
                lost_date="2026-09-27",
                status="Active"
            )
        ]

        found_items = [
            FoundItem(
                name="Library Staff",
                contact_number="+91 98000 11111",
                email="library@campus.edu",
                item_name="AirPods Pro Case (White)",
                description="Found white Apple AirPods case left on table #4 on 2nd floor.",
                image_url="https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?auto=format&fit=crop&w=600&q=80",
                found_location="Main Library 2nd Floor",
                found_date="2026-09-28",
                collection_place="Main Library Circulation Counter",
                status="Active"
            ),
            FoundItem(
                name="Security Gate 1 Office",
                contact_number="+91 98000 22222",
                email="security@campus.edu",
                item_name="Student ID Card (Om Gawali)",
                description="Found student ID card with blue lanyard near canteen walkway.",
                image_url="https://images.unsplash.com/photo-1578574577315-3fbeb0cecdc2?auto=format&fit=crop&w=600&q=80",
                found_location="College Canteen Entrance",
                found_date="2026-09-29",
                collection_place="Main Security Guard Desk at Gate 1",
                status="Active"
            )
        ]

        for item in lost_items:
            db.session.add(item)
        for item in found_items:
            db.session.add(item)

        db.session.commit()
        print("Successfully seeded Lost & Found items!")

if __name__ == "__main__":
    seed()
