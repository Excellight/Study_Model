import uuid
from typing import Dict, List, Tuple, Optional

class Student:
    """Represents a student with personal details and academic scores."""

    def __init__(self, student_id: str, full_name: str, age: int, department: str, email: str, scores: Dict[str, float]):
        """Initialize a Student object.

        Args:
            student_id: Unique identifier for the student
            full_name: Full name of the student
            age: Age of the student
            department: Department the student belongs to
            email: Student's email address
            scores: Dictionary of subject-score pairs
        """
        self.student_id = student_id
        self.full_name = full_name
        self.age = age
        self.department = department
        self.email = email
        self.scores = scores
        self.created_at = None

    def calculate_total_score(self) -> float:
        """Calculate the sum of all scores for the student."""
        return sum(self.scores.values()) if self.scores else 0.0

    def calculate_average_score(self) -> float:
        """Calculate the average score for the student."""
        if not self.scores:
            return 0.0
        return self.calculate_total_score() / len(self.scores)

    def assign_grade(self) -> str:
        """Assign a letter grade based on the student's average score."""
        average = self.calculate_average_score()
        if average >= 90:
            return 'A'
        elif average >= 80:
            return 'B'
        elif average >= 70:
            return 'C'
        elif average >= 60:
            return 'D'
        else:
            return 'F'

    def determine_pass_fail(self) -> str:
        """Determine if the student passed or failed (average >= 50)."""
        return 'PASS' if self.calculate_average_score() >= 50 else 'FAIL'

    def find_highest_subject_score(self) -> Tuple[Optional[str], Optional[float]]:
        """Find the highest score and its subject."""
        if not self.scores:
            return None, None
        subject = max(self.scores, key=self.scores.get)
        return subject, self.scores[subject]

    def find_lowest_subject_score(self) -> Tuple[Optional[str], Optional[float]]:
        """Find the lowest score and its subject."""
        if not self.scores:
            return None, None
        subject = min(self.scores, key=self.scores.get)
        return subject, self.scores[subject]

    def update_subject_score(self, subject: str, new_score: float) -> bool:
        """Update the score for a specific subject.

        Args:
            subject: The name of the subject to update
            new_score: The new score for the subject (0-100)

        Returns:
            bool: True if updated successfully, False otherwise
        """
        if 0 <= new_score <= 100:
            if subject in self.scores:
                self.scores[subject] = new_score
                return True
            else:
                raise ValueError(f"Subject '{subject}' not found for {self.full_name}.")
        else:
            raise ValueError("Score must be between 0 and 100.")

    def add_subject_score(self, subject: str, score: float) -> bool:
        """Add a new subject and score for the student."""
        if 0 <= score <= 100:
            self.scores[subject] = score
            return True
        else:
            raise ValueError("Score must be between 0 and 100.")

    def to_dict(self) -> dict:
        """Convert student to dictionary for JSON serialization."""
        highest_sub, highest_score = self.find_highest_subject_score()
        lowest_sub, lowest_score = self.find_lowest_subject_score()
        
        return {
            'student_id': self.student_id,
            'full_name': self.full_name,
            'age': self.age,
            'department': self.department,
            'email': self.email,
            'scores': self.scores,
            'total_score': round(self.calculate_total_score(), 2),
            'average_score': round(self.calculate_average_score(), 2),
            'grade': self.assign_grade(),
            'status': self.determine_pass_fail(),
            'highest_subject': {'subject': highest_sub, 'score': highest_score},
            'lowest_subject': {'subject': lowest_sub, 'score': lowest_score}
        }


class StudentManager:
    """Manages a collection of Student objects."""

    def __init__(self):
        """Initialize the StudentManager."""
        self.students: List[Student] = []

    def add_student(self, full_name: str, age: int, department: str, email: str, scores: Dict[str, float]) -> Student:
        """Add a new student to the system.

        Args:
            full_name: Full name of the student
            age: Age of the student
            department: Department the student belongs to
            email: Student's email address
            scores: Dictionary of subject-score pairs (must have at least 3 subjects)

        Returns:
            Student: The created student object

        Raises:
            ValueError: If scores contain fewer than 3 subjects or invalid scores
        """
        if len(scores) < 3:
            raise ValueError("At least 3 subjects required for a new student.")
        
        for subject, score in scores.items():
            if not isinstance(score, (int, float)) or not (0 <= score <= 100):
                raise ValueError(f"Invalid score for {subject}: must be between 0 and 100.")
        
        student_id = self._generate_unique_id()
        student = Student(student_id, full_name, age, department, email, scores)
        self.students.append(student)
        return student

    def find_student(self, student_id: str) -> Optional[Student]:
        """Find a student by ID."""
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None

    def delete_student(self, student_id: str) -> bool:
        """Delete a student by ID."""
        for i, student in enumerate(self.students):
            if student.student_id == student_id:
                self.students.pop(i)
                return True
        return False

    def update_student(self, student_id: str, data: dict) -> None:
        """Update a student's information."""
        student = self.find_student(student_id)
        if not student:
            raise ValueError("Student not found.")
        
        if 'full_name' in data:
            student.full_name = data['full_name']
        if 'age' in data:
            student.age = data['age']
        if 'department' in data:
            student.department = data['department']
        if 'email' in data:
            student.email = data['email']
        
        if 'scores' in data:
            new_scores = data['scores']
            for subject, score in new_scores.items():
                if isinstance(score, (int, float)) and 0 <= score <= 100:
                    student.scores[subject] = score
                else:
                    raise ValueError(f"Invalid score for {subject}.")

    def get_total_students(self) -> int:
        """Get the total number of students."""
        return len(self.students)

    def get_class_average(self) -> float:
        """Get the overall class average."""
        if not self.students:
            return 0.0
        total = sum(s.calculate_average_score() for s in self.students)
        return total / len(self.students)

    def get_passing_rate(self) -> float:
        """Get the percentage of passing students."""
        if not self.students:
            return 0.0
        passing = sum(1 for s in self.students if s.determine_pass_fail() == 'PASS')
        return (passing / len(self.students)) * 100

    def get_passing_count(self) -> int:
        """Get the number of passing students."""
        return sum(1 for s in self.students if s.determine_pass_fail() == 'PASS')

    def get_failing_count(self) -> int:
        """Get the number of failing students."""
        return sum(1 for s in self.students if s.determine_pass_fail() == 'FAIL')

    def get_top_performer_name(self) -> Optional[str]:
        """Get the name of the highest-performing student."""
        if not self.students:
            return None
        top = max(self.students, key=lambda s: s.calculate_average_score())
        return top.full_name

    def get_top_performer(self) -> Optional[Student]:
        """Get the highest-performing student."""
        if not self.students:
            return None
        return max(self.students, key=lambda s: s.calculate_average_score())

    def get_lowest_performer(self) -> Optional[Student]:
        """Get the lowest-performing student."""
        if not self.students:
            return None
        return min(self.students, key=lambda s: s.calculate_average_score())

    def get_highest_average(self) -> float:
        """Get the highest student average score."""
        if not self.students:
            return 0.0
        return max(s.calculate_average_score() for s in self.students)

    def get_lowest_average(self) -> float:
        """Get the lowest student average score."""
        if not self.students:
            return 0.0
        return min(s.calculate_average_score() for s in self.students)

    def get_highest_subject_score(self) -> dict:
        """Get the highest subject score across all students."""
        if not self.students:
            return {'subject': None, 'score': 0, 'student': None}
        
        max_score = 0
        max_subject = None
        max_student = None
        
        for student in self.students:
            subject, score = student.find_highest_subject_score()
            if score and score > max_score:
                max_score = score
                max_subject = subject
                max_student = student.full_name
        
        return {'subject': max_subject, 'score': max_score, 'student': max_student}

    def get_lowest_subject_score(self) -> dict:
        """Get the lowest subject score across all students."""
        if not self.students:
            return {'subject': None, 'score': 0, 'student': None}
        
        min_score = float('inf')
        min_subject = None
        min_student = None
        
        for student in self.students:
            subject, score = student.find_lowest_subject_score()
            if score and score < min_score:
                min_score = score
                min_subject = subject
                min_student = student.full_name
        
        return {'subject': min_subject, 'score': min_score, 'student': min_student}

    def get_rankings(self) -> List[dict]:
        """Get students ranked by average score (highest to lowest)."""
        ranked = sorted(self.students, key=lambda s: s.calculate_average_score(), reverse=True)
        return [
            {
                'rank': i + 1,
                'student_id': s.student_id,
                'full_name': s.full_name,
                'department': s.department,
                'average_score': round(s.calculate_average_score(), 2),
                'grade': s.assign_grade(),
                'status': s.determine_pass_fail()
            }
            for i, s in enumerate(ranked)
        ]

    def get_department_distribution(self) -> dict:
        """Get the number of students per department."""
        distribution = {}
        for student in self.students:
            distribution[student.department] = distribution.get(student.department, 0) + 1
        return distribution

    def get_department_stats(self) -> dict:
        """Get detailed statistics per department."""
        depts = {}
        for student in self.students:
            dept = student.department
            if dept not in depts:
                depts[dept] = {'students': [], 'count': 0, 'avg_performance': 0}
            depts[dept]['students'].append(student)
            depts[dept]['count'] += 1
        
        stats = {}
        for dept, data in depts.items():
            avg_perf = sum(s.calculate_average_score() for s in data['students']) / data['count']
            passing = sum(1 for s in data['students'] if s.determine_pass_fail() == 'PASS')
            stats[dept] = {
                'student_count': data['count'],
                'average_performance': round(avg_perf, 2),
                'pass_rate': round((passing / data['count']) * 100, 2)
            }
        return stats

    def get_pass_fail_stats(self) -> dict:
        """Get pass/fail statistics."""
        passing = self.get_passing_count()
        failing = self.get_failing_count()
        total = self.get_total_students()
        
        return {
            'passing': passing,
            'failing': failing,
            'total': total,
            'pass_percentage': round((passing / total * 100) if total > 0 else 0, 2)
        }

    def get_grade_distribution(self) -> dict:
        """Get distribution of grades."""
        grades = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
        for student in self.students:
            grade = student.assign_grade()
            grades[grade] += 1
        return grades

    def get_student_averages_chart(self) -> dict:
        """Get data for student averages chart."""
        return {
            'labels': [s.full_name for s in self.students],
            'data': [round(s.calculate_average_score(), 2) for s in self.students]
        }

    def get_recent_students(self, limit: int = 5) -> List[dict]:
        """Get recently added students."""
        recent = self.students[-limit:] if len(self.students) > limit else self.students
        return [
            {
                'student_id': s.student_id,
                'full_name': s.full_name,
                'department': s.department,
                'age': s.age,
                'average_score': round(s.calculate_average_score(), 2),
                'grade': s.assign_grade(),
                'status': s.determine_pass_fail()
            }
            for s in reversed(recent)
        ]

    def get_students_paginated(self, page: int, per_page: int, search: str = '', 
                              department: str = '', grade: str = '', status: str = '', 
                              sort_by: str = 'name') -> dict:
        """Get paginated, filtered, and sorted students."""
        filtered = self.students[:]
        
        if search:
            search_lower = search.lower()
            filtered = [s for s in filtered if search_lower in s.full_name.lower() or search_lower in s.student_id.lower()]
        
        if department:
            filtered = [s for s in filtered if s.department.lower() == department.lower()]
        
        if grade:
            filtered = [s for s in filtered if s.assign_grade() == grade.upper()]
        
        if status:
            filtered = [s for s in filtered if s.determine_pass_fail() == status.upper()]
        
        # Sort
        if sort_by == 'average':
            filtered.sort(key=lambda s: s.calculate_average_score(), reverse=True)
        elif sort_by == 'grade':
            grade_order = {'A': 5, 'B': 4, 'C': 3, 'D': 2, 'F': 1}
            filtered.sort(key=lambda s: grade_order[s.assign_grade()], reverse=True)
        else:  # default: name
            filtered.sort(key=lambda s: s.full_name)
        
        total = len(filtered)
        start = (page - 1) * per_page
        end = start + per_page
        paginated = filtered[start:end]
        
        return {
            'data': [s.to_dict() for s in paginated],
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page
        }

    def get_student_ranking(self, student_id: str) -> Optional[int]:
        """Get the rank of a specific student."""
        rankings = self.get_rankings()
        for rank_data in rankings:
            if rank_data['student_id'] == student_id:
                return rank_data['rank']
        return None

    def get_performance_analytics_data(self) -> dict:
        """Get all performance analytics."""
        return {
            'class_average': round(self.get_class_average(), 2),
            'highest_average': round(self.get_highest_average(), 2),
            'lowest_average': round(self.get_lowest_average(), 2),
            'passing_students': self.get_passing_count(),
            'failing_students': self.get_failing_count(),
            'total_students': self.get_total_students()
        }

    def _generate_unique_id(self) -> str:
        """Generate a unique 8-character uppercase ID."""
        while True:
            new_id = str(uuid.uuid4())[:8].upper()
            if not any(s.student_id == new_id for s in self.students):
                return new_id
