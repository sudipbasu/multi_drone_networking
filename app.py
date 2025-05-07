from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import paho.mqtt.client as mqtt
from datetime import datetime, timedelta
import subprocess

app = Flask(__name__)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///drones.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model
class CommandLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    drone = db.Column(db.String(50), nullable=False)
    command = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

# MQTT config
mqtt_broker = "broker.hivemq.com"
mqtt_port = 1883
mqtt_client = mqtt.Client()
mqtt_client.connect(mqtt_broker, mqtt_port, 60)
mqtt_client.loop_start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/command", methods=["POST"])
def send_command():
    data = request.json
    command = data.get("command")
    drone = data.get("drone")

    if not command or not drone:
        return jsonify({"status": "error", "message": "Missing command or drone"}), 400

    if drone == "all":
        for i in range(1, 21):
            topic = f"drone/commands/{i}"
            mqtt_client.publish(topic, command)
            db.session.add(CommandLog(drone=str(i), command=command))
    else:
        topic = f"drone/commands/{drone}"
        mqtt_client.publish(topic, command)
        db.session.add(CommandLog(drone=drone, command=command))

    db.session.commit()
    return jsonify({"status": "Command sent", "command": command, "drone": drone})

@app.route("/history")
def history():
    logs = CommandLog.query.order_by(CommandLog.timestamp.desc()).all()
    return render_template("history.html", logs=logs)
#Drone_Dashboard
@app.route('/dashboard')
def dashboard():
    drones = []
    now = datetime.utcnow()
    two_minutes = timedelta(minutes=2)

    for i in range(1, 21):
        last_log = CommandLog.query.filter_by(drone=str(i)).order_by(CommandLog.timestamp.desc()).first()
        if last_log:
            last_command = last_log.command
            last_seen = last_log.timestamp.strftime('%d-%m-%Y %H:%M:%S')
            status = 'Online' if now - last_log.timestamp <= two_minutes else 'Offline'
        else:
            last_command = None
            last_seen = None
            status = 'Offline'

        drones.append({
            'id': i,
            'last_command': last_command,
            'last_seen': last_seen,
            'status': status
        })

    return render_template('dashboard.html', drones=drones)
#Drone_Dashboard_End

#Listener_Start
@app.route('/listener')
def listener():
    return render_template('listener.html')

@app.route('/start_listener', methods=['POST'])
def start_listener():
    data = request.get_json()
    drone_id = data.get('drone_id')
    if not drone_id:
        return jsonify({'message': 'Drone ID is required'}), 400
    try:
        # Run the python script in background
        subprocess.Popen(['python', 'drone_listener.py', str(drone_id)])
        return jsonify({'message': f'Listener started for Drone {drone_id}!'})
    except Exception as e:
        return jsonify({'message': f'Failed to start listener: {str(e)}'}), 500

#Listener_End
@app.route("/clear_history", methods=["POST"])
def clear_history():
    CommandLog.query.delete()
    db.session.commit()
    return redirect(url_for('history'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=False)
