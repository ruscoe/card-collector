from . import db


class Collection(db.Model):
    __tablename__ = "collections"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    sets = db.relationship(
        "Set",
        backref="collection",
        cascade="all, delete-orphan",
        lazy=True,
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "sets": [set_.to_dict() for set_ in self.sets],
        }


class Set(db.Model):
    __tablename__ = "sets"

    id = db.Column(db.Integer, primary_key=True)
    collection_id = db.Column(db.Integer, db.ForeignKey("collections.id"), nullable=False)
    name = db.Column(db.String, nullable=False)
    cards = db.relationship(
        "Card",
        backref="set",
        cascade="all, delete-orphan",
        lazy=True,
    )

    def to_dict(self):
        return {
            "id": self.id,
            "collectionId": self.collection_id,
            "name": self.name,
            "cards": [card.to_dict() for card in self.cards],
        }


class Card(db.Model):
    __tablename__ = "cards"

    id = db.Column(db.Integer, primary_key=True)
    set_id = db.Column(db.Integer, db.ForeignKey("sets.id"), nullable=False)
    name = db.Column(db.String, nullable=False)
    number = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "setId": self.set_id,
            "set": self.set.name if self.set is not None else None,
            "name": self.name,
            "number": self.number,
        }
