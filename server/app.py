# server/app.py
#!/usr/bin/env python3

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

# Add views here
@app.route('/earthquakes/<int:id>')
def earthquakes(id):
    earthquake = Earthquake.query.get(id)
    if earthquake:
        body = {
            "id": earthquake.id,
            "location": earthquake.location,
            "magnitude": earthquake.magnitude,
            "year": earthquake.year
        }
        return make_response(body, 200)
    else:
        body = {"message": f"Earthquake {id} not found."}
        return make_response(body, 404)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def magnitude(magnitude):
    results = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    quakes = []
    if results:
        for earthquake in results:
            quake = {
                "id": earthquake.id,
                "location": earthquake.location,
                "magnitude": earthquake.magnitude,
                "year": earthquake.year
            }
            quakes.append(quake)
        
        body = {
            "count": len(results),
            "quakes": quakes
        }
        return make_response(body, 200)
    else:
        body = {
            "count": len(results),
            "quakes": quakes
        }
        return make_response(body, 200)    


if __name__ == '__main__':
    app.run(port=5555, debug=True)
