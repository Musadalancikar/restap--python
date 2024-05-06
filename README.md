# STUDENT REST API

## GEREKSİNİMLER

-Python 3.8+, Flask, SQLite

## Açıklama

Proje öğrenci verilerinden oluşan bir REST API uygulamasıdır. Eğer aynı öğrenciye ve aynı ders koduna ait birden fazla ders notu varsa bu notların ortalamasını kaydeden bir çalışmadır.

## Kurulum

Öncelikle gereksinimlerin yüklü olduğundan emin olun. Python, Flask ve veritabanı bağlantısı için flask_sqlalchemy yüklememiz gerek. Proje Visual Studio Code IDE kullanılmıştır.
```
pip install Flask
pip install Flask-SQLAlchemy
```
## Uygulama

students.db adında bir veritabanı oluşturulur. Öğrenci id, isim, soyisim, okul numarası ve sınıfların tabloları oluşturulur.
```
# Öğrenci modeli
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    std_number = db.Column(db.String(20), unique=True)
    grades = db.relationship('Grade', backref='student', lazy=True)
```
Ardından öğrencinin notlarının yer aldığı ayrı tablo oluşturulur.
```
# Not modeli
class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10))
    value = db.Column(db.Integer)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
```

Sonrasında bir öğrencinin aynı dersten birden fazla notu varsa bunun ortalaması alıp saklayan uygulaması yapılır. Öğrenci bilgilerini getiren bir endpoint eklenir.
```
# API rotası - Öğrenci bilgilerini getiren endpoint
@app.route('/students', methods=['GET'])
def get_students():
```
Yeni bir öğrenci eklemek uygulaması ve endpointi eklenir.
```
# Yeni öğrenci ve not eklemek için API rotası
@app.route('/students', methods=['POST'])
def add_student():
```
Powershell kısmından yeni bir öğrenci ekleme yapılır.
```
Invoke-WebRequest -Uri "http://127.0.0.1:5000/students" -Method POST -ContentType "application/json" -Body '{
    "name": "Ali",
    "surname": "Veli",
    "std_number": "20230001",
    "grades": [
        {"code": "MAT101", "value": 85},
        {"code": "PHY201", "value": 78},
        {"code": "CHEM301", "value": 92}
    ]
}'
```
