from database import db
from bson import ObjectId
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class Patient:
    collection = db.patients
    
    def __init__(self, name, email, phone, age, gender, medical_history=None, created_by=None):
        logger.debug(f"Initializing Patient with data: name={name}, email={email}, phone={phone}, age={age}, gender={gender}")
        self.name = name
        self.email = email
        self.phone = phone
        self.age = age
        self.gender = gender
        self.medical_history = medical_history or []
        self.created_by = created_by
        self.created_at = datetime.utcnow()
    
    def save(self):
        try:
            patient_data = {
                'name': self.name,
                'email': self.email,
                'phone': self.phone,
                'age': self.age,
                'gender': self.gender,
                'medical_history': self.medical_history,
                'created_by': self.created_by,
                'created_at': self.created_at
            }
            logger.debug(f"Saving patient data: {patient_data}")
            result = self.collection.insert_one(patient_data)
            logger.info(f"Patient saved successfully with ID: {result.inserted_id}")
            return result.inserted_id
        except Exception as e:
            logger.error(f"Error saving patient: {str(e)}")
            raise
    
    @staticmethod
    def find_by_email(email):
        try:
            logger.debug(f"Finding patient by email: {email}")
            result = Patient.collection.find_one({'email': email})
            if result:
                logger.debug(f"Found existing patient with email: {email}")
            else:
                logger.debug(f"No patient found with email: {email}")
            return result
        except Exception as e:
            logger.error(f"Error finding patient by email: {str(e)}")
            raise
    
    @staticmethod
    def find_by_id(patient_id):
        try:
            logger.debug(f"Finding patient by ID: {patient_id}")
            result = Patient.collection.find_one({'_id': ObjectId(patient_id)})
            if result:
                logger.debug(f"Found patient with ID: {patient_id}")
            else:
                logger.debug(f"No patient found with ID: {patient_id}")
            return result
        except Exception as e:
            logger.error(f"Error finding patient by ID: {str(e)}")
            return None
    
    @staticmethod
    def get_all():
        try:
            logger.debug("Getting all patients")
            patients = list(Patient.collection.find())
            logger.debug(f"Found {len(patients)} patients")
            return patients
        except Exception as e:
            logger.error(f"Error getting all patients: {str(e)}")
            raise
    
    @staticmethod
    def update(patient_id, update_data):
        try:
            logger.debug(f"Updating patient {patient_id} with data: {update_data}")
            result = Patient.collection.update_one(
                {'_id': ObjectId(patient_id)},
                {'$set': update_data}
            )
            logger.info(f"Patient {patient_id} updated successfully")
            return result
        except Exception as e:
            logger.error(f"Error updating patient: {str(e)}")
            raise
    
    @staticmethod
    def delete(patient_id):
        try:
            logger.debug(f"Deleting patient: {patient_id}")
            result = Patient.collection.delete_one({'_id': ObjectId(patient_id)})
            logger.info(f"Patient {patient_id} deleted successfully")
            return result
        except Exception as e:
            logger.error(f"Error deleting patient: {str(e)}")
            raise
    
    def to_dict(self):
        return {
            'id': str(self._id) if hasattr(self, '_id') else None,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'age': self.age,
            'gender': self.gender,
            'medical_history': self.medical_history,
            'created_at': self.created_at.isoformat() if self.created_at else None
        } 