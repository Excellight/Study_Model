"""
Flask backend for Student Management System Pro
Provides REST API for the modern React dashboard
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from student import Student, StudentManager
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

manager = StudentManager()


def init_sample_data():
    """Initialize with sample students for development."""
    students_data = [
        {
            "name": "Alice Smith",
            "age": 20,
            "department": "Computer Science",
            "email": "alice@example.com",
            "scores": {"Mathematics": 85, "Physics": 92, "Programming": 78}
        },
        {
            "name": "Bob Johnson",
            "age": 22,
            "department": "Electrical Engineering",
            "email": "bob@example.com",
            "scores": {"Mathematics": 60, "Circuits": 75, "Thermodynamics": 65}
        },
        {
            "name": "Charlie Brown",
            "age": 21,
            "department": "Computer Science",
            "email": "charlie@example.com",
            "scores": {"Mathematics": 95, "Programming": 88, "Databases": 90}
        }
    ]
    
    for data in students_data:
        manager.add_student(data["name"], data["age"], data["department"], data["email"], data["scores"])


# ===== DASHBOARD ENDPOINTS =====

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    """Get dashboard KPI data."""
    try:
        return jsonify({
            'total_students': manager.get_total_students(),
            'class_average': round(manager.get_class_average(), 1),
            'passing_rate': round(manager.get_passing_rate(), 1),
            'top_performer': manager.get_top_performer_name() or 'N/A'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/dashboard/charts', methods=['GET'])
def get_dashboard_charts():
    """Get chart data for dashboard."""
    try:
        return jsonify({
            'student_averages': manager.get_student_averages_chart(),
            'department_distribution': manager.get_department_distribution(),
            'pass_fail_stats': manager.get_pass_fail_stats(),
            'grade_distribution': manager.get_grade_distribution()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/dashboard/recent-students', methods=['GET'])
def get_recent_students():
    """Get recently added students."""
    try:
        limit = request.args.get('limit', 5, type=int)
        return jsonify(manager.get_recent_students(limit)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ===== STUDENTS ENDPOINTS =====

@app.route('/api/students', methods=['GET'])
def get_students():
    """Get all students with optional filtering and pagination."""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '', type=str)
        department = request.args.get('department', '', type=str)
        grade = request.args.get('grade', '', type=str)
        status = request.args.get('status', '', type=str)
        sort_by = request.args.get('sort_by', 'name', type=str)
        
        return jsonify(manager.get_students_paginated(
            page, per_page, search, department, grade, status, sort_by
        )), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/students/<student_id>', methods=['GET'])
def get_student(student_id):
    """Get detailed information about a specific student."""
    try:
        student = manager.find_student(student_id)
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        result = student.to_dict()
        result['ranking'] = manager.get_student_ranking(student_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/students', methods=['POST'])
def create_student():
    """Add a new student."""
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['full_name', 'age', 'department', 'email', 'scores']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Validate age
        if not isinstance(data['age'], int) or data['age'] < 1:
            return jsonify({'error': 'Invalid age'}), 400
        
        # Validate scores
        scores = data.get('scores', {})
        if len(scores) < 3:
            return jsonify({'error': 'At least 3 subjects required'}), 400
        
        for subject, score in scores.items():
            if not isinstance(score, (int, float)) or not (0 <= score <= 100):
                return jsonify({'error': f'Invalid score for {subject}'}), 400
        
        student = manager.add_student(
            data['full_name'],
            data['age'],
            data['department'],
            data['email'],
            scores
        )
        return jsonify(student.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/students/<student_id>', methods=['PUT'])
def update_student(student_id):
    """Update a student's information and/or scores."""
    try:
        data = request.json
        student = manager.find_student(student_id)
        
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        manager.update_student(student_id, data)
        updated = manager.find_student(student_id)
        return jsonify(updated.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/students/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    """Delete a student."""
    try:
        if manager.delete_student(student_id):
            return jsonify({'message': 'Student deleted successfully'}), 200
        return jsonify({'error': 'Student not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ===== RANKINGS ENDPOINTS =====

@app.route('/api/rankings', methods=['GET'])
def get_rankings():
    """Get student rankings by average score."""
    try:
        return jsonify({'rankings': manager.get_rankings()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ===== PERFORMANCE ENDPOINTS =====

@app.route('/api/performance/analytics', methods=['GET'])
def get_performance_analytics():
    """Get performance analytics and statistics."""
    try:
        return jsonify({
            'class_average': round(manager.get_class_average(), 2),
            'highest_average': round(manager.get_highest_average(), 2) if manager.get_total_students() > 0 else 0,
            'lowest_average': round(manager.get_lowest_average(), 2) if manager.get_total_students() > 0 else 0,
            'highest_subject_score': manager.get_highest_subject_score(),
            'lowest_subject_score': manager.get_lowest_subject_score(),
            'passing_students': manager.get_passing_count(),
            'failing_students': manager.get_failing_count(),
            'total_students': manager.get_total_students()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ===== DEPARTMENTS ENDPOINTS =====

@app.route('/api/departments', methods=['GET'])
def get_departments():
    """Get department statistics."""
    try:
        stats = manager.get_department_stats()
        return jsonify({'departments': stats}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ===== REPORTS ENDPOINTS =====

@app.route('/api/reports/class-performance', methods=['GET'])
def get_class_report():
    """Get class performance report."""
    try:
        return jsonify({
            'summary': manager.get_performance_analytics_data(),
            'students': [s.to_dict() for s in manager.students],
            'generated_at': datetime.now().isoformat()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/reports/student/<student_id>', methods=['GET'])
def get_student_report(student_id):
    """Get individual student report."""
    try:
        student = manager.find_student(student_id)
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        return jsonify({
            'student': student.to_dict(),
            'ranking': manager.get_student_ranking(student_id),
            'generated_at': datetime.now().isoformat()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ===== HEALTH CHECK =====

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()}), 200


# ===== ERROR HANDLERS =====

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    init_sample_data()
    app.run(debug=True, port=5000)
