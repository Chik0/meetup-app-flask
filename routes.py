import json
import bcrypt
from meetup_app_flask import app, db
from flask import request

from meetup_app_flask.models.models import User


@app.route('/')
def index():
    return "O_O"


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        content = request.get_json(silent=True)
        if not content or not content['email'] or not content['password']:
            return json.dumps({'1': 'Invalid Request!'})
        user = db.session.query(User).filter(User.email == content['email']).all()
        if user:
            if bcrypt.checkpw(content['password'].encode('utf8'), user[0].password_hash.encode('utf8')):
                return json.dumps({'0': 'Successful Login'})
            else:
                return json.dumps({'2': "Invalid Password"})
        new_user = User(email=content['email'], password_hash=bcrypt.hashpw(content['password'].encode('utf8'), bcrypt.gensalt()))
        db.session.add(new_user)
        db.session.commit()
        return json.dumps({'0': 'Successful Registration'})
    return json.dumps({'1': 'Invalid Request!'})
