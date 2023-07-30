# Import Flask framework and SQLAlchemy library
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

# Create an app instance
app = Flask(__name__)

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///farmers.db'

# Create a database instance
db = SQLAlchemy(app)


# Define a model for farmers
class Farmer(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), nullable=False)
  phone = db.Column(db.String(10), nullable=False)
  location = db.Column(db.String(50), nullable=False)
  land_size = db.Column(db.Float, nullable=False)

  def __repr__(self):
    return f'<Farmer {self.name}>'


# Define a model for tractor owners
class TractorOwner(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), nullable=False)
  phone = db.Column(db.String(10), nullable=False)
  location = db.Column(db.String(50), nullable=False)
  tractor_type = db.Column(db.String(50), nullable=False)
  availability = db.Column(db.Boolean, default=True)

  def __repr__(self):
    return f'<TractorOwner {self.name}>'


# Create the database tables
    with app.app_context():
      db.create_all()
    return app


# Define a route for adding a new farmer
@app.route('/farmers', methods=['POST'])

def display():
  return render_template('farmers.html')
  
def add_farmer():
  # Get the request data
  data = request.get_json()
  # Validate the data
  if not data or not data.get('name') or not data.get('phone') or not data.get(
      'location') or not data.get('land_size'):
    return jsonify({'message': 'Invalid data'}), 400
  # Create a new farmer object
  farmer = Farmer(name=data['name'],
                  phone=data['phone'],
                  location=data['location'],
                  land_size=data['land_size'])
  # Add the farmer to the database
  db.session.add(farmer)
  db.session.commit()
  # Return a success message
  return jsonify({'message': 'Farmer added successfully'}), 201


# Define a route for adding a new tractor owner
@app.route('/tractor_owners', methods=['POST'])
def add_tractor_owner():
  # Get the request data
  data = request.get_json()
  # Validate the data
  if not data or not data.get('name') or not data.get('phone') or not data.get(
      'location') or not data.get('tractor_type'):
    return jsonify({'message': 'Invalid data'}), 400
  # Create a new tractor owner object
  tractor_owner = TractorOwner(name=data['name'],
                               phone=data['phone'],
                               location=data['location'],
                               tractor_type=data['tractor_type'])
  # Add the tractor owner to the database
  db.session.add(tractor_owner)
  db.session.commit()
  # Return a success message
  return jsonify({'message': 'Tractor owner added successfully'}), 201


# Define a route for getting all farmers
@app.route('/farmers', methods=['GET'])
def get_farmers():
  # Query the database for all farmers
  farmers = Farmer.query.all()
  # Convert the farmers to a list of dictionaries
  farmers_list = [{
    'id': f.id,
    'name': f.name,
    'phone': f.phone,
    'location': f.location,
    'land_size': f.land_size
  } for f in farmers]
  # Return the farmers list as JSON
  return jsonify({'farmers': farmers_list}), 200


# Define a route for getting all tractor owners
@app.route('/tractor_owners', methods=['GET'])
def get_tractor_owners():
  # Query the database for all tractor owners
  tractor_owners = TractorOwner.query.all()
  # Convert the tractor owners to a list of dictionaries
  tractor_owners_list = [{
    'id': t.id,
    'name': t.name,
    'phone': t.phone,
    'location': t.location,
    'tractor_type': t.tractor_type,
    'availability': t.availability
  } for t in tractor_owners]
  # Return the tractor owners list as JSON
  return jsonify({'tractor_owners': tractor_owners_list}), 200


# Define a route for finding a suitable tractor owner for a farmer based on location and land size
@app.route('/match', methods=['POST'])
def match_farmer_tractor_owner():
  # Get the request data
  data = request.get_json()
  # Validate the data
  if not data or not data.get('farmer_id'):
    return jsonify({'message': 'Invalid data'}), 400
  # Get the farmer by id
  farmer = Farmer.query.get(data['farmer_id'])
  # Check if the farmer exists
  if not farmer:
    return jsonify({'message': 'Farmer not found'}), 404
  # Find a tractor owner who is available, has the same location as the farmer, and has a tractor type that can handle the farmer's land size
  tractor_owner = TractorOwner.query.filter_by(
    availability=True, location=farmer.location).filter(
      TractorOwner.tractor_type.in_(
        ['small', 'medium', 'large'] if farmer.land_size <= 10 else
        ['medium', 'large'] if farmer.land_size <= 20 else ['large'])).first()
  # Check if a tractor owner is found
  if not tractor_owner:
    return jsonify({'message': 'No suitable tractor owner found'}), 404
  # Return the tractor owner details as JSON
  return jsonify({
    'tractor_owner': {
      'id': tractor_owner.id,
      'name': tractor_owner.name,
      'phone': tractor_owner.phone,
      'location': tractor_owner.location,
      'tractor_type': tractor_owner.tractor_type
    }
  }), 200


# Run the app
if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
