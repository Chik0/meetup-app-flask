from meetup_app_flask import app, db
from meetup_app_flask.models import models


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': models.User}
