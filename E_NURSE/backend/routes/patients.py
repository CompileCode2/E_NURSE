from flask import Blueprint, request, jsonify
from models.patient import Patient
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

patients_bp = Blueprint('patients', __name__)

@patients_bp.route('/', methods=['POST'])
def create_patient():
    try:
        # Log the incoming request
        logger.debug("Received request to create patient")
        logger.debug(f"Request headers: {dict(request.headers)}")
        
        # Get and validate request data
        data = request.get_json()
        if not data:
            logger.error("No JSON data received in request")
            return jsonify({'error': 'No data provided'}), 400
            
        logger.debug(f"Received patient data: {data}")
        
        # Validate required fields
        required_fields = ['name', 'email', 'phone', 'age', 'gender']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            logger.error(f"Missing required fields: {missing_fields}")
            return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400
        
        # Check if patient already exists
        existing_patient = Patient.find_by_email(data['email'])
        if existing_patient:
            logger.warning(f"Patient with email {data['email']} already exists")
            return jsonify({'error': 'Patient with this email already exists'}), 400
        
        # Create new patient
        try:
            patient = Patient(
                name=data['name'],
                email=data['email'],
                phone=data['phone'],
                age=data['age'],
                gender=data['gender'],
                medical_history=data.get('medical_history', '')
            )
            logger.debug("Patient object created successfully")
        except Exception as e:
            logger.error(f"Error creating Patient object: {str(e)}")
            return jsonify({'error': f'Invalid patient data: {str(e)}'}), 400
        
        # Save the patient
        try:
            patient_id = patient.save()
            logger.info(f"Patient saved successfully with ID: {patient_id}")
            return jsonify({
                'message': 'Patient created successfully',
                'id': str(patient_id)
            }), 201
        except Exception as e:
            logger.error(f"Error saving patient to database: {str(e)}")
            return jsonify({'error': f'Database error: {str(e)}'}), 500
            
    except Exception as e:
        logger.error(f"Unexpected error in create_patient: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@patients_bp.route('/', methods=['GET'])
def get_patients():
    patients = Patient.get_all()
    return jsonify([patient.to_dict() for patient in patients]), 200

@patients_bp.route('/<patient_id>', methods=['GET'])
def get_patient(patient_id):
    try:
        patient = Patient.find_by_id(patient_id)
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        return jsonify(patient.to_dict()), 200
    except Exception as e:
        logger.error(f"Error getting patient: {str(e)}")
        return jsonify({'error': 'Invalid patient ID'}), 400

@patients_bp.route('/<patient_id>', methods=['PUT'])
def update_patient(patient_id):
    data = request.get_json()
    patient = Patient.find_by_id(patient_id)
    
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    
    # Update patient information
    update_data = {
        'name': data.get('name', patient['name']),
        'phone': data.get('phone', patient['phone']),
        'age': data.get('age', patient['age']),
        'gender': data.get('gender', patient['gender']),
        'medical_history': data.get('medical_history', patient['medical_history'])
    }
    
    Patient.update(patient_id, update_data)
    return jsonify({'message': 'Patient updated successfully'}), 200

@patients_bp.route('/<patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    patient = Patient.find_by_id(patient_id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    
    Patient.delete(patient_id)
    return jsonify({'message': 'Patient deleted successfully'}), 200 