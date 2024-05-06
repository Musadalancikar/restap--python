from flask import Flask, jsonify, request
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

# API rotası - Öğrenci bilgilerini getiren endpoint
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

# Yeni öğrenci ve not eklemek için API rotası
@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    name = data.get('name')
    surname = data.get('surname')
    std_number = data.get('std_number')
    grades = data.get('grades')

    # Veritabanına yeni öğrenciyi ekle
    new_student = Student(name=name, surname=surname, std_number=std_number)
    db.session.add(new_student)
    db.session.commit()

    # Her bir ders notu için ortalama değeri hesapla ve kaydet
    for grade_data in grades:
        code = grade_data.get('code')
        value = grade_data.get('value')
        new_grade = Grade(code=code, value=value, student_id=new_student.id)
        db.session.add(new_grade)
    db.session.commit()

    return jsonify({'message': 'Student and grades added successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)
