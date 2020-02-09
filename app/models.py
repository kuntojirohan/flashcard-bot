from app import db, _update_db
import random


class User(db.Model):
    """The User table is used to store all the details regarding the user,
       it has mainly 2 methods, one to get a new review of flashcards and another to stop reviewing the flashcard.
    """
    __tablename__ = "users"

    phone_number = db.Column(db.Text, primary_key=True)
    flashcards = db.relationship(
        "Flashcard",
        backref="user",
        primaryjoin="User.phone_number == Flashcard.user_id",
    )
    current_review_id = db.Column(db.Integer(), db.ForeignKey("flashcards.id"))
    current_review = db.relationship(
        "Flashcard", foreign_keys=[current_review_id])
    creating_flashcards = db.Column(db.Boolean)

    def __init__(self, phone_number):
        self.phone_number = phone_number
        self.creating_flashcards = False

    def get_new_review(self):
        if not self.flashcards:
            return None
        new_review = random.choice(self.flashcards)
        self.current_review_id = new_review.id
        _update_db(self)
        return new_review

    def stop_reviewing(self):
        self.current_review = None
        _update_db(self)
        return self


class Flashcard(db.Model):
    """Flashcard table stores the flashcard details, basically the front and back sides.
    """
    __tablename__ = "flashcards"

    id = db.Column(db.Integer, primary_key=True)
    front = db.Column(db.Text())
    back = db.Column(db.Text())
    user_id = db.Column(db.Text(), db.ForeignKey("users.phone_number"))

    def __init__(self, user_id, front, back):
        self.user_id = user_id
        self.front = front
        self.back = back
