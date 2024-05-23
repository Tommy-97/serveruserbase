# app.py
from datetime import datetime

from flask import Flask, jsonify, request

from base import calculate_production_time, change_priority
from license import main as check_license
from models import SessionLocal, User, engine

app = Flask(__name__)


@app.before_request
def check_license_before_request():
    if not check_license():
        return jsonify({"error": "Please purchase a license to use this software."}), 403


@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    session = SessionLocal()
    new_user = User(
        login=data['login'],
        password=data['password'],
        phone=data['phone'],
        email=data['email'],
        name=data['name'],
        surname=data['surname'],
        role_id=data['role_id']
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    session.close()
    return jsonify({"id": new_user.id})


@app.route('/api/users', methods=['GET'])
def get_users():
    session = SessionLocal()
    users = session.query(User).all()
    session.close()
    return jsonify([{"id": user.id, "login": user.login} for user in users])


@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    equipment = data['equipment']
    work_type = data['work_type']
    start_time = datetime.fromisoformat(data['start_time'])
    required_operations = data['required_operations']

    end_time = calculate_production_time(
        equipment, work_type, start_time, required_operations)
    return jsonify({"end_time": end_time.isoformat()})


@app.route('/api/change_priority', methods=['POST'])
def change_priority_endpoint():
    data = request.get_json()
    operation_id = data['operation_id']
    new_priority = data['new_priority']

    change_priority(operation_id, new_priority)
    return jsonify({"status": "success"})


if __name__ == '__main__':
    if check_license():
        app.run(debug=True)
    else:
        print("Please purchase a license to use this software.")
