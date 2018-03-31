''' Implements database models for The Europa project. '''

import datetime
import enum

from flask_sqlalchemy import SQLAlchemy

# Define formats to use when serializing / deserializing data into and from
# the defined models.
SERIALIZABLE_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'

# Define SQLAlchemy here, with the application context to be loaded in later.
db = SQLAlchemy()

def from_datetime(source=None):
    ''' Attempts to format an input datetime object into a string. '''
    if source:
        return datetime.datetime.strftime(source, SERIALIZABLE_DATE_FORMAT)
    return None

def to_datetime(source=None):
    ''' Attempts to format an input string into a datetime object. '''
    if source:
        return datetime.datetime.strptime(source, SERIALIZABLE_DATE_FORMAT)
    return None


class VesselSize(enum.Enum):
    ''' Define supported types for the Target Category type. '''
    POT_TWELVE_CM = '12CM Plant Pot'


class SensorCategory(enum.Enum):
    ''' Define supported types for the Sensor Category type. '''
    TEMPERATURE_AMBIENT = 'Ambient Temperature Sensor'
    TEMPERATURE_SOIL = 'Soil Temperature Sensor'
    HUMIDITY_AMBIENT = 'Ambient Humidity Sensor'
    MOISTURE_SOIL = 'Soil Moisture Sensor'


class SensorUnits(enum.Enum):
    ''' Define supported types for the Sensor Units type. '''
    DEGREES = 'Degrees'
    BOOLEAN = 'Boolean (On / Off)'
    PERCENT = 'Percent'


class Vessel(db.Model):
    ''' Implements the Vessels model for Europa. '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    size = db.Column(db.Enum(VesselSize), nullable=False)
    location = db.Column(db.String(200), unique=False, nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    deleted = db.Column(db.DateTime)

    # Enforce a unique constraint between location and name.
    __table_args__ = (
        db.UniqueConstraint('name', 'location'),
    )

    def for_json(self):
        ''' Provide a result in a JSON serializable format. '''
        return {
            'id': self.id,
            'name': self.name,
            'size': str(self.size),
            'location': self.location,
            'created': from_datetime(self.created),
            'deleted': from_datetime(self.deleted),
        }


class Plant(db.Model):
    ''' Implements the Plants model for Europa. '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=False, nullable=False)
    description = db.Column(db.String(200), unique=False, nullable=True)
    vessel_id = db.Column(db.Integer, db.ForeignKey('vessel.id'), nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    deleted = db.Column(db.DateTime)

    # Map the reverse for the relationship.
    vessel = db.relationship('Vessel', backref='plants')

    # Enforce a unique constraint between name and vessel.
    __table_args__ = (
        db.UniqueConstraint('name', 'vessel_id'),
    )

    def for_json(self):
        ''' Provide a result in a JSON serializable format. '''
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'vessel': self.vessel.name,
            'created': from_datetime(self.created),
            'deleted': from_datetime(self.deleted),
        }


class Sensor(db.Model):
    ''' Implements the Sensors model for Europa. '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=False, nullable=False)
    category = db.Column(db.Enum(SensorCategory), nullable=False)
    units = db.Column(db.Enum(SensorUnits), nullable=False)
    vessel_id = db.Column(db.Integer, db.ForeignKey('vessel.id'), nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    deleted = db.Column(db.DateTime)

    # Map the reverse for the relationship.
    vessel = db.relationship('Vessel', backref='sensors')


class SensorData(db.Model):
    ''' Implements the Sensors Data model for Europa. '''
    id = db.Column(db.BigInteger, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'), nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # Map the reverse for the relationship.
    sensor = db.relationship('Sensor', backref='data_points')
