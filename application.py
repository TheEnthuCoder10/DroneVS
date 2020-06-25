from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.sql import exists
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)


# Product Class/Model
class Drone(db.Model):
    count = db.Column(db.Integer, primary_key=True)
    DroneID = db.Column(db.String(100), unique=True)
    FCVolt_V1 = db.Column(db.Float)
    FCVolt_V2 = db.Column(db.Float)
    FCPres = db.Column(db.Float)
    FCCurr = db.Column(db.Float)

    def __init__(self, DroneID, FCVolt_V1, FCVolt_V2, FCPres, FCCurr):
        self.DroneID = DroneID
        self.FCVolt_V1 = FCVolt_V1
        self.FCVolt_V2 = FCVolt_V2
        self.FCPres = FCPres
        self.FCCurr = FCCurr


# Drone Schema
class DroneSchema(ma.Schema):
    class Meta:
        fields = ('count', 'DroneID', 'FCVolt_V1', 'FCVolt_V2', 'FCPres', 'FCCurr')


# Init schema
drones_schema = DroneSchema(many=True)


# Create a drone
@app.route('/api/v1/droneList', methods=['POST'])
def add_drone():
    DroneID = request.json['DroneID']
    FCVolt_V1 = request.json['FCVolt_V1']
    FCVolt_V2 = request.json['FCVolt_V2']
    FCPres = request.json['FCPres']
    FCCurr = request.json['FCCurr']

    new_drone = Drone(DroneID, FCVolt_V1, FCVolt_V2, FCPres, FCCurr)

    db.session.add(new_drone)
    db.session.commit()

    return jsonify({"Success": True})


# Get entire list of drones
@app.route('/api/v1/droneList', methods=['GET'])
def get_droneList():
    if request.method == 'GET':
        all_drones = Drone.query.all()
        result = drones_schema.dump(all_drones)
        return jsonify(result)

    return jsonify({'GET Request': 'Failure'})


# Get Specific Drone
@app.route('/api/v1/droneList/<DroneID>', methods=['GET'])
def get_DRONE(DroneID):
    if request.method == 'GET':
        get_drone = Drone.query.filter_by(DroneID=DroneID).first()
        if not get_drone:
            return jsonify({'DroneRunning': False, 'Error': 'The specified drone is not found!'})

        get_drone_data = {'DroneID': get_drone.DroneID, 'FCCurr': get_drone.FCCurr, 'FCPres': get_drone.FCPres,
                          'FCVolt_V2': get_drone.FCVolt_V2, 'FCVolt_V1': get_drone.FCVolt_V1, 'DroneRunning': True}

        return jsonify({'Details': get_drone_data})

    return jsonify({'GET Request': 'Failure'})


@app.route('/api/v1/droneList/<DroneID>', methods=['PUT'])
def update_DRONE(DroneID):
    update_drone = Drone.query.filter_by(DroneID=DroneID).first()

    if not update_drone:
        return jsonify({'Error': 'No drone found!'})

    FCVolt_V1 = request.json['FCVolt_V1']
    FCVolt_V2 = request.json['FCVolt_V2']
    FCPres = request.json['FCPres']
    FCCurr = request.json['FCCurr']

    update_drone.FCVolt_V1 = FCVolt_V1
    update_drone.FCVolt_V2 = FCVolt_V2
    update_drone.FCPres = FCPres
    update_drone.FCCurr = FCCurr

    db.session.commit()

    return jsonify({'Success!': 'The specified drone has been updated!'})


@app.route('/api/v1/droneList/<DroneID>', methods=['DELETE'])
def delete_DRONE(DroneID):
    delete_drone = Drone.query.filter_by(DroneID=DroneID).first()
    if not delete_drone:
        return jsonify({'Error': 'The specified drone is not found!'})

    db.session.delete(delete_drone)
    db.session.commit()

    return jsonify({'Success!': 'The specified drone has been deleted!'})


# Run Server
if __name__ == '__main__':
    app.run(debug=True)
