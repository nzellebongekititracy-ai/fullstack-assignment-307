from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enables Cross-Origin Resource Sharing for frontend connectivity

# i) Mock database stored in an array (list of dictionaries)
students = [
    {"id": 1, "name": "John Doe", "department": "Computer Engineering", "level": 400},
    {"id": 2, "name": "Jane Smith", "department": "Software Engineering", "level": 300}
]

# Helper function to generate a new unique ID for POST requests
def generate_id():
    return max([s['id'] for s in students], default=0) + 1


# 1) GET /students - Deploy all students
@app.route('/students', methods=['GET'])
def get_all_students():
    return jsonify(students), 200


# 2) GET /students/:id - Deploy one student by ID
@app.route('/students/<int:id>', methods=['GET'])
def get_one_student(id):
    # Search the array for the matching ID
    student = next((s for s in students if s['id'] == id), None)
    if student:
        return jsonify(student), 200
    return jsonify({"error": f"Student with ID {id} not found"}), 404


# 3) POST /students - Add a new student
# Note: Changed from /student to plural /students to maintain standard REST API naming conventions
@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    
    # Simple validation checking for required fields
    if not data or 'name' not in data or 'department' not in data:
        return jsonify({"error": "Missing required fields ('name', 'department')"}), 400
    
    new_student = {
        "id": generate_id(),
        "name": data['name'],
        "department": data['department'],
        "level": data.get('level', 100) # Defaults to 100 if level isn't provided
    }
    
    students.append(new_student)
    return jsonify({"message": "Student added successfully", "student": new_student}), 201


# 4) DELETE /students/:id - Remove a student
@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    global students
    student = next((s for s in students if s['id'] == id), None)
    
    if not student:
        return jsonify({"error": f"Student with ID {id} not found"}), 404
        
    # Rebuild array excluding the target student
    students = [s for s in students if s['id'] != id]
    return jsonify({"message": f"Student with ID {id} has been removed"}), 200


# 5) PUT /students/:id - Update a student
@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    student = next((s for s in students if s['id'] == id), None)
    
    if not student:
        return jsonify({"error": f"Student with ID {id} not found"}), 404
        
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided for update"}), 400
        
    # Update fields if they exist in the incoming JSON request payload
    student['name'] = data.get('name', student['name'])
    student['department'] = data.get('department', student['department'])
    student['level'] = data.get('level', student['level'])
    
    return jsonify({"message": "Student updated successfully", "student": student}), 200


if __name__ == '__main__':
    # Running explicitly on port 307
    app.run(host='0.0.0.0', port=307, debug=True)