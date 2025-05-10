<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
   
</head>
<body>

<h1>🚁 Multi-Drone Command Center</h1>

<p>A comprehensive drone management system built with Flask that allows centralized control of multiple drones through MQTT protocol, featuring real-time monitoring, command history, and visual simulation.</p>

<h2>🌟 Features</h2>

<h3>🎮 Core Functionality</h3>
<ul>
    <li>🔢 Control up to 20 drones simultaneously</li>
    <li>📡 Individual or group command broadcasting</li>
    <li>🔄 Supported commands: Takeoff, Land, Movement controls, Hover</li>
</ul>

<h3>📊 Monitoring & Analytics</h3>
<ul>
    <li>📈 Real-time status dashboard</li>
    <li>🕒 Command execution history with timestamps</li>
    <li>💾 CSV export capability</li>
    <li>✈️ Visual flight path simulation</li>
</ul>

<h2>🛠️ Installation</h2>

<h3>Prerequisites</h3>
<ul>
    <li>Python 3.7+</li>
    <li>pip package manager</li>
</ul>

<h3>Setup Instructions</h3>
<pre><code># Clone repository
git clone https://github.com/sudipbasu/multi_drone_networking.git
cd multi_drone_networking

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt

# Initialize database
python -c "from app import db; db.create_all()"

# Run application
python app.py
</code></pre>

<p>Access the web interface at: <code>http://localhost:5000</code></p>

<h2>📂 Project Structure</h2>
<pre>
drone-control/
├── app.py                # Flask application core
├── drone_listener.py     # MQTT command listener
├── requirements.txt      # Dependency list
├── drones.db             # Database file (created after first run)
└── templates/
    ├── index.html        # Main control interface
    ├── dashboard.html    # Status monitoring
    ├── history.html      # Command logs
    └── listener.html     # Listener activation
</pre>

<h2>🔧 Configuration</h2>

<h3>Environment Variables</h3>
<p>Create a <code>.env</code> file to customize:</p>
<pre><code>FLASK_SECRET_KEY=your_secret_key
MQTT_BROKER=broker.hivemq.com
MQTT_PORT=1883
DATABASE_URI=sqlite:///drones.db
</code></pre>

<h3>MQTT Settings</h3>
<p>Modify in <code>app.py</code>:</p>
<pre><code>mqtt_broker = os.getenv('MQTT_BROKER', 'broker.hivemq.com')
mqtt_port = int(os.getenv('MQTT_PORT', 1883))
</code></pre>

<h2>🚀 Deployment</h2>

<h3>Production Setup</h3>
<ol>
    <li>Using a WSGI server:
<pre><code>pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
</code></pre>
    </li>
    <li>Setting up a dedicated MQTT broker (Mosquitto)</li>
    <li>Configuring proper SSL certificates</li>
</ol>

<p><strong>Note:</strong> This system currently simulates drone behavior. For actual drone integration, hardware-specific adapters and safety protocols must be implemented. Always comply with local drone regulations.</p>

<h2>📜 License</h2>
<p>MIT License - See <a href="LICENSE">LICENSE</a> file for details</p>

<h2>🤝 Contributing</h2>
<ol>
    <li>Fork the repository</li>
    <li>Create your feature branch (<code>git checkout -b feature/AmazingFeature</code>)</li>
    <li>Commit your changes (<code>git commit -m 'Add some AmazingFeature'</code>)</li>
    <li>Push to the branch (<code>git push origin feature/AmazingFeature</code>)</li>
    <li>Open a Pull Request</li>
</ol>

<h2>📧 Contact</h2>
<p>For questions or support: <a href="mailto:sudipbasu845@gmail.com">sudipbasu845@gmail.com</a></p>

</body>
</html>
