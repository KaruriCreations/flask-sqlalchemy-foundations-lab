# server/app.py
#!/usr/bin/env python3

import ast

class StrPatch(ast.Constant):
    def __init__(self, s=None, value=None, **kwargs):
        if s is not None:
            value = s
        super().__init__(value=value)

    @property
    def s(self):
        return self.value

    @s.setter
    def s(self, val):
        self.value = val

ast.Str = StrPatch

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)


@app.route('/earthquakes/<int:id>')
def earthquake_by_id(id):
    earthquake = Earthquake.query.filter_by(id=id).first()
    if not earthquake:
        return make_response({'message': f'Earthquake {id} not found.'}, 404)
    return make_response(earthquake.to_dict(), 200)


@app.route('/earthquakes/magnitude/<float:magnitude>')
def earthquakes_by_magnitude(magnitude):
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    quakes_dict = [q.to_dict() for q in quakes]
    body = {
        'count': len(quakes_dict),
        'quakes': quakes_dict
    }
    return make_response(body, 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)

