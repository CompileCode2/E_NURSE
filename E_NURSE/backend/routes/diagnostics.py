from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.diagnostic import Diagnostic
from models.patient import Patient
from bson import ObjectId

diagnostics_bp = Blueprint('diagnostics', __name__)

@diagnostics_bp.route('/', methods=['POST'])
@jwt_required()
def create_diagnostic():
    data = request.get_json()
    patient_id = data.get('patient_id')
    
    # Verify patient exists
    patient = Patient.find_by_id(patient_id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    
    # Create new diagnostic
    diagnostic = Diagnostic(
        patient_id=patient_id,
        symptoms=data['symptoms'],
        diagnosis=data['diagnosis'],
        treatment=data['treatment'],
        notes=data.get('notes', ''),
        created_by=get_jwt_identity()
    )
    
    diagnostic_id = diagnostic.save()
    return jsonify({'message': 'Diagnostic created successfully', 'id': str(diagnostic_id)}), 201

@diagnostics_bp.route('/patient/<patient_id>', methods=['GET'])
@jwt_required()
def get_patient_diagnostics(patient_id):
    # Verify patient exists
    patient = Patient.find_by_id(patient_id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    
    diagnostics = Diagnostic.find_by_patient_id(patient_id)
    return jsonify([diagnostic.to_dict() for diagnostic in diagnostics]), 200

@diagnostics_bp.route('/<diagnostic_id>', methods=['GET'])
@jwt_required()
def get_diagnostic(diagnostic_id):
    diagnostic = Diagnostic.find_by_id(diagnostic_id)
    if not diagnostic:
        return jsonify({'error': 'Diagnostic not found'}), 404
    
    return jsonify(diagnostic.to_dict()), 200

@diagnostics_bp.route('/<diagnostic_id>', methods=['PUT'])
@jwt_required()
def update_diagnostic(diagnostic_id):
    data = request.get_json()
    diagnostic = Diagnostic.find_by_id(diagnostic_id)
    
    if not diagnostic:
        return jsonify({'error': 'Diagnostic not found'}), 404
    
    # Update diagnostic information
    update_data = {
        'symptoms': data.get('symptoms', diagnostic['symptoms']),
        'diagnosis': data.get('diagnosis', diagnostic['diagnosis']),
        'treatment': data.get('treatment', diagnostic['treatment']),
        'notes': data.get('notes', diagnostic['notes'])
    }
    
    Diagnostic.update(diagnostic_id, update_data)
    return jsonify({'message': 'Diagnostic updated successfully'}), 200

@diagnostics_bp.route('/<diagnostic_id>', methods=['DELETE'])
@jwt_required()
def delete_diagnostic(diagnostic_id):
    diagnostic = Diagnostic.find_by_id(diagnostic_id)
    if not diagnostic:
        return jsonify({'error': 'Diagnostic not found'}), 404
    
    Diagnostic.delete(diagnostic_id)
    return jsonify({'message': 'Diagnostic deleted successfully'}), 200 