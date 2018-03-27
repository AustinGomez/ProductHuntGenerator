from app import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    tagline = db.Column(db.String(1000))
    description = db.Column(db.String(2000))
    image = db.Column(db.String(200))

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "tagline": self.tagline.strip(),
            "description": self.description,
            "image": self.image
        }