from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
from datetime import timedelta
import logging
from routes.patients import patients_bp
from routes.auth import auth_bp
from routes.predictions import predictions_bp
from routes.health import health_bp
from config import Config

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Configure CORS to allow requests from frontend
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# JWT Configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET', 'your-secret-key')  # Change in production
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
jwt = JWTManager(app)

# MongoDB Configuration
app.config['MONGO_URI'] = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/e-nurse')

# Import and register blueprints
app.register_blueprint(patients_bp, url_prefix='/api/patients')
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(predictions_bp, url_prefix='/api/predictions')
app.register_blueprint(health_bp, url_prefix='/api/health')

@app.route('/')
def home():
    return {'message': 'Welcome to E-Nurse API'}

if __name__ == '__main__':
    logger.info("Starting E-Nurse API server...")
    app.run(debug=True, port=5000) 