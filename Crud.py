from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

users = {}
user_id_counter = 1

@app.route('/users', methods=['POST'])
def create_user():
    global user_id_counter
    user_data = request.get_json()
    
    if 'username' not in user_data or 'password' not in user_data or 'active' not in user_data:
        return jsonify({"error": "Missing user data"}), 400
    
    username = user_data['username']
    password = user_data['password']
    active = user_data['active']
    
    hashed_password = generate_password_hash(password)
    user_id = user_id_counter
    users[user_id] = {'username': username, 'password': hashed_password, 'active': active}
    user_id_counter += 1
    return jsonify({"id": user_id, "user": users[user_id]}), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def read_user(user_id):
    user = users.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"id": user_id, "user": user})

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user_data = request.get_json()
    
    if 'username' not in user_data and 'password' not in user_data and 'active' not in user_data:
        return jsonify({"error": "No data provided to update"}), 400
    
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    
    user = users[user_id]
    if 'username' in user_data:
        user['username'] = user_data['username']
    if 'password' in user_data:
        user['password'] = generate_password_hash(user_data['password'])
    if 'active' in user_data:
        user['active'] = user_data['active']
    
    return jsonify({"id": user_id, "user": user})

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    del users[user_id]
    return jsonify({"message": "User deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
