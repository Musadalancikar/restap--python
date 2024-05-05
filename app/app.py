from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'  # SQLite veritabanı dosyası
db = SQLAlchemy(app)

# Öğrenci modeli
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    std_number = db.Column(db.String(20), unique=True)
    grades = db.relationship('Grade', backref='student', lazy=True)

# Not modeli
class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10))
    value = db.Column(db.Integer)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)

# API rotası
@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    student_list = []
    for student in students:
        grades = student.grades
        grade_dict = {}
        for grade in grades:
            if grade.code in grade_dict:
                grade_dict[grade.code].append(grade.value)
            else:
                grade_dict[grade.code] = [grade.value]
        for code, values in grade_dict.items():
            if len(values) > 1:
                average_value = sum(values) / len(values)
                student_list.append({
                    'name': student.name,
                    'surname': student.surname,
                    'std_number': student.std_number,
                    'code': code,
                    'average_value': average_value
                })
            else:
                student_list.append({
                    'name': student.name,
                    'surname': student.surname,
                    'std_number': student.std_number,
                    'code': code,
                    'value': values[0]
                })
    return jsonify({'students': student_list})

if __name__ == '__main__':
    app.run(debug=True)
