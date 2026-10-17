from flask import (
    Blueprint,
    jsonify,
    request
)

from database import (
    get_all_students,
    get_student_by_id,
    add_student,
    update_student,
    delete_student,
    get_user_by_username,
)
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from werkzeug.security import check_password_hash

api_bp = Blueprint(
    "api",__name__,url_prefix="/api"
)

@api_bp.route("/students",methods=["GET"])
@jwt_required()
def get_students():
    students = get_all_students()

    data = []

    for student in students:
        data.append({
            "id": student["id"],
            "name": student["name"],
            "course": student["course"],
            "photo": student["photo"]
        })

    return jsonify(data)

@api_bp.route("/students/<int:id>",methods=["GET"])
@jwt_required()
def get_student(id):
    student = get_student_by_id(id)

    if student is None:
        return jsonify({
            "error":"Student not Found"
        }), 404

    return jsonify({
            "id": student["id"],
            "name": student["name"],
            "course": student["course"],
            "photo": student["photo"]
    })

@api_bp.route("/students",methods=["POST"])
@jwt_required()
def create_student():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error":"JSON data is required"
        }), 400
    name = str(data.get("name","")).strip()
    course = str(data.get("course","")).strip()

    if not name:
        return jsonify({
            "error":"Name is required"
        }),400
    
    if not course:
        return jsonify({
            "error":"Course is required"
        }),400
    
    student_id = add_student(
        name,
        course,
        ""
    )
    return jsonify({
        "message":"Student created successfully",
        "id":student_id
    }),201

@api_bp.route("/students/<int:id>",methods=["PUT"])
@jwt_required()
def update_student_api(id):
    student = get_student_by_id(id)

    if student is None:
        return jsonify({
            "error":"No student Found"
        }),404
    
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error":"JSON data is required"
        }), 400
    
    name = str(data.get("name",student["name"])).strip()
    course = str(data.get("course",student["course"])).strip()

    if not name:
        return jsonify({
            "error":"Name is required"
        }),400
    
    if not course:
        return jsonify({
            "error":"Course is required"
        }),400
    update_student(
        id,name,course
    )
    return jsonify({
        "message":"Student updated successfully"
    })

@api_bp.route("/students/<int:id>",methods=["DELETE"])
@jwt_required()
def delete_student_api(id):
    student = get_student_by_id(id)

    if student is None:
        return jsonify({
            "error":"No student Found"
        }),404
    delete_student(id)
    return jsonify({
        "message":"Student deleted successfully"
    })

@api_bp.route("/login",methods=["POST"])
def api_login():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error":"JSON data is required"
        }), 400
    username = data.get("username")
    password = data.get("password")
    if not username:
        return jsonify({
            "error":"Username is required"
        }),400
    
    if not password:
        return jsonify({
            "error":"password is required"
        }),400
    user = get_user_by_username(username)

    if user is None:
        return jsonify({
            "error":"Invalid username"
        }),401

    if not check_password_hash(user["password"],password):
        return jsonify({
            "error":"Invalid password"
        }),401

    token = create_access_token(identity=str(user["id"]))
    return jsonify({
        "access_token":token
    })