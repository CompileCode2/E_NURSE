from database import db
from bson import ObjectId
from datetime import datetime

class Diagnostic:
    collection = db.diagnostics
    
    def __init__(self, patient_id, symptoms, diagnosis, treatment, notes='', created_by=None):
        self.patient_id = patient_id
        self.symptoms = symptoms
        self.diagnosis = diagnosis
        self.treatment = treatment
        self.notes = notes
        self.created_by = created_by
        self.created_at = datetime.utcnow()
    
    def save(self):
        diagnostic_data = {
            'patient_id': self.patient_id,
            'symptoms': self.symptoms,
            'diagnosis': self.diagnosis,
            'treatment': self.treatment,
            'notes': self.notes,
            'created_by': self.created_by,
            'created_at': self.created_at
        }
        result = self.collection.insert_one(diagnostic_data)
        return result.inserted_id
    
    @staticmethod
    def find_by_id(diagnostic_id):
        try:
            return Diagnostic.collection.find_one({'_id': ObjectId(diagnostic_id)})
        except:
            return None
    
    @staticmethod
    def find_by_patient_id(patient_id):
        return list(Diagnostic.collection.find({'patient_id': patient_id}).sort('created_at', -1))
    
    @staticmethod
    def update(diagnostic_id, update_data):
        Diagnostic.collection.update_one(
            {'_id': ObjectId(diagnostic_id)},
            {'$set': update_data}
        )
    
    @staticmethod
    def delete(diagnostic_id):
        Diagnostic.collection.delete_one({'_id': ObjectId(diagnostic_id)})
    
    def to_dict(self):
        return {
            'id': str(self._id) if hasattr(self, '_id') else None,
            'patient_id': self.patient_id,
            'symptoms': self.symptoms,
            'diagnosis': self.diagnosis,
            'treatment': self.treatment,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'created_by': self.created_by
        } 