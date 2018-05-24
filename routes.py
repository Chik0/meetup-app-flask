import json
import datetime
import bcrypt
from meetup_app_flask import app, db
from flask import request

from meetup_app_flask.models.models import User, Location


@app.route('/')
def index():
    return "O_O"


@app.route('/login', methods=['POST'])
def login():
    """
    Request Example
    {
        "email": "example@email.com",
        "password": "qwerty123"
    }
    """
    if request.method == 'POST':
        content = request.get_json(silent=True)
        if not content or not content.get('email', False) or not content.get('password', False):
            return json.dumps({
                'code': '1',
                'msg': 'Invalid Request'
            })
        user = db.session.query(User).filter(User.email == content['email']).first()
        if user:
            if bcrypt.checkpw(content['password'].encode('utf8'), user[0].password.decode().encode('utf-8')):
                return json.dumps({
                    'code': '0',
                    'msg': 'Successful Login',
                    'user': {
                        'id': user.id,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name
                    }
                })
            else:
                return json.dumps({
                    'code': '2',
                    'msg': 'Invalid Password'
                })
        new_user = User(email=content['email'], password=bcrypt.hashpw(content['password'].encode('utf8'), bcrypt.gensalt()))
        db.session.add(new_user)
        db.session.commit()
        new_user = db.session.query(User).filter(User.email == content['email']).first()
        return json.dumps({
            'code': '0',
            'msg': 'Successful Registration',
            'user': {
                'id': new_user.id,
                'email': new_user.email,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name
            }
        })
    return json.dumps({
        'code': '1',
        'msg': 'Invalid Request'
    })


@app.route('/user-locations', methods=['POST'])
def user_locations():
    """
    Request Example
    {
        "user_id": 5
    }
    """
    if request.method == 'POST':
        content = request.get_json(silent=True)
        if not content or not content.get('user_id', False):
            return json.dumps({
                'code': '1',
                'msg': 'Invalid Request'
            })
        user = db.session.query(User).filter(User.id == content['user_id']).first()
        if not user:
            return json.dumps({
                'code': '2',
                'msg': 'User Not Found'
            })
        locations = db.session.query(Location).filter(Location.user_id == user.id).all()
        loc_dict = {
            'code': '0',
            'msg': 'successful request',
            'locations': []
        }
        for loc in locations:
            loc_dict['locations'].append({
                'create_date': loc.create_date.strftime("%Y-%m-%d %H:%M"),
                'lng': loc.long,
                'lat': loc.lat

            })
        return json.dumps(loc_dict)

@app.route('/save-location', methods=['POST'])
def save_location():
    """
    Request
    {
        "user_id": 6,
        "lng": 44.44,
        "lat": 45.45
    }
    """
    if request.method == 'POST':
        content = request.get_json(silent=True)
        if not content or not content.get('user_id', False) or not content.get('lng', False) or not content.get('lat', False):
            return json.dumps({
                'code': '1',
                'msg': 'Invalid Request'
            })
        try:
            new_loc = Location(create_date=datetime.datetime.now(),
                               long=content['lng'],
                               lat=content['lat'],
                               user_id=content['user_id'])
            db.session.add(new_loc)
            db.session.commit()
            return json.dumps({
                'code': '0',
                'msg': 'Location Saved'
            })
        except:
            return json.dumps({
                'code': '2',
                'msg': 'Error while writing ro database'
            })

@app.route('/map-locations', methods=['POST'])
def map_locations():
    """
        Request Example
        {
            "user_id": 5
        }
        """
    if request.method == 'POST':
        content = request.get_json(silent=True)
        if not content or not content.get('user_id', False):
            return json.dumps({
                'code': '1',
                'msg': 'Invalid Request'
            })
        user = db.session.query(User).filter(User.id == content['user_id']).first()
        if not user:
            return json.dumps({
                'code': '2',
                'msg': 'User Not Found'
            })
        locations = db.session.query(Location).filter(Location.user_id != user.id).order_by(Location.create_date.desc()).all()
        users = []
        loc_dict = {
            'code': '0',
            'msg': 'successful request',
            'locations': []
        }
        for loc in locations:
            if loc.user_id not in users:
                users.append(loc.user_id)
                loc_dict['locations'].append({
                    'name': user.first_name,
                    'surname': user.last_name,
                    'message': user.message,
                    'lat': loc.lat,
                    'lng': loc.long,
                    'create_date': loc.create_date.strftime("%Y-%m-%d %H:%M")
                })
        return json.dumps(loc_dict)

@app.route('/save-message', methods=['POST'])
def save_messages():
    """
        Request Example
        {
            "user_id": 5,
            "name": "asdasd",
            "surname": "asdasdaognaeg",
            "message": "asdasdsda"
        }
        """
    if request.method == 'POST':
        content = request.get_json(silent=True)
        if not content or not content.get('user_id', False) or not content.get('name', False) or not content.get('surname', False) or not content.get('message', False):
            return json.dumps({
                'code': '1',
                'msg': 'Invalid Request'
            })
        user = db.session.query(User).filter(User.id == content['user_id']).first()
        if not user:
            return json.dumps({
                'code': '2',
                'msg': 'User Not Found'
            })
        try:
            user.first_name = content.get('name', '')
            user.last_name = content.get('surname', '')
            user.message = content.get('message', '')
            db.session.commit()
            return json.dumps({
                'code': '0',
                'msg': 'User data updated'
            })
        except:
            return json.dumps({
                'code': '3',
                'msg': 'DB update error'
            })
