from flask import Blueprint, app, jsonify, request, render_template, session, redirect, url_for, flash
from app.models import Registro

# Crear un Blueprint para organizar las rutas
bp = Blueprint('main', __name__)


# API Endpoints
@bp.route('/')
def index():
    return jsonify({'message': 'Hello World API Cac-movies'})

@bp.route('/api/users/', methods=['POST'])
def create_user():
    data = request.json
    new_user = Registro(name=data['name'], email=data['email'], password=data['password'], rol=data['rol'])
    new_user.save()
    return jsonify({'message': 'User created successfully'}), 201

@bp.route('/api/users/', methods=['GET'])
def get_all_users():
    users = Registro.get_all()
    return jsonify([user.serialize() for user in users])

@bp.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = Registro.get_by_id(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(user.serialize())

@bp.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = Registro.get_by_id(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    data = request.json
    user.name = data['name']
    user.email = data['email']
    user.password = data['password']
    user.rol = data['rol']
    user.save()
    return jsonify({'message': 'User updated successfully'})

@bp.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = Registro.get_by_id(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    user.delete()
    return jsonify({'message': 'User deleted successfully'})
