from meetup_app_flask import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    message = db.Column(db.String(500))
    password = db.Column(db.Binary)

    def __repr__(self):
        return '<User {}>'.format(self.email)


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    create_date = db.Column(db.DateTime)

    long = db.Column(db.Float)
    lat = db.Column(db.Float)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", backref=db.backref('user', uselist=False))
