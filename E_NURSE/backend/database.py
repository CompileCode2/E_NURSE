from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# MongoDB connection string
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/e-nurse')

try:
    # Create MongoDB client with default Atlas TLS settings
    client = MongoClient(
        MONGODB_URI,
        serverSelectionTimeoutMS=5000
    )
    
    # Test the connection
    client.admin.command('ping')
    logger.info("Successfully connected to MongoDB")
    
    # Get database
    db = client.get_database()
    logger.info(f"Using database: {db.name}")
    
    # Create indexes
    logger.debug("Creating database indexes...")
    db.users.create_index('email', unique=True)
    db.patients.create_index('email', unique=True)
    db.diagnostics.create_index([('patient_id', 1), ('created_at', -1)])
    
    logger.info("Database indexes created successfully")
    
except ConnectionFailure as e:
    logger.error(f"Error connecting to MongoDB: {e}")
    raise

# Export the database instance
__all__ = ['db'] 