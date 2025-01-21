from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:0511@localhost/universitydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class Students(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roll_number = db.Column(db.String(20), nullable=False, unique=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.subject_id'), nullable=True)
    grade = db.Column(db.String(2), nullable=True)

    subject = db.relationship('Subjects', backref=db.backref('students', lazy=True))

    def as_dict(self):
        return {
            'student_id': self.student_id,
            'name': self.name,
            'roll_number': self.roll_number,
            'subject_name': self.subject.subject_name if self.subject else 'undefined',
            'grade': self.grade
        }

class Subjects(db.Model):
    subject_id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(100), nullable=False)

    def as_dict(self):
        return {
            'subject_id': self.subject_id,
            'subject_name': self.subject_name
        }

class Staff(db.Model):
    staff_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=True)
    contact_number = db.Column(db.String(20), nullable=True)

    def as_dict(self):
        return {
            'staff_id': self.staff_id,
            'name': self.name,
            'position': self.position,
            'contact_number': self.contact_number
        }

class HostelMealPlans(db.Model):
    meal_id = db.Column(db.Integer, primary_key=True)
    meal_plan = db.Column(db.String(50), nullable=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=True)

    student = db.relationship('Students', backref=db.backref('meal_plans', lazy=True))

    def as_dict(self):
        return {
            'meal_id': self.meal_id,
            'meal_plan': self.meal_plan,
            'student_id': self.student_id
        }

# Routes

@app.route('/')
def index():
    subjects = Subjects.query.all()  # Get all subjects to display in the form
    return render_template('index.html', subjects=subjects)

@app.route('/students')
def students():
    name_filter = request.args.get('name')
    if name_filter:
        students_data = Students.query.filter(Students.name.like(f'%{name_filter}%')).all()
    else:
        students_data = Students.query.all()
    return jsonify([student.as_dict() for student in students_data])

@app.route('/staff')
def staff():
    name_filter = request.args.get('name')
    if name_filter:
        staff_data = Staff.query.filter(Staff.name.like(f'%{name_filter}%')).all()
    else:
        staff_data = Staff.query.all()
    return jsonify([staff.as_dict() for staff in staff_data])

@app.route('/add_student', methods=['POST'])
def add_student():
    try:
        name = request.form.get('name')
        roll_number = request.form.get('roll_number')
        subject_id = request.form.get('subject_id')
        grade = request.form.get('grade')

        # Debug log
        print(f"Adding student: Name={name}, Roll Number={roll_number}, Subject ID={subject_id}, Grade={grade}")

        # Check if the data is correct
        if not name or not roll_number or not subject_id or not grade:
            return render_template('index.html', error="Error: Missing form data")

        # Check if subject exists
        subject = Subjects.query.get(subject_id)
        if not subject:
            return render_template('index.html', error="Error: Invalid Subject ID")

        # Create and add new student
        new_student = Students(name=name, roll_number=roll_number, subject_id=subject_id, grade=grade)
        db.session.add(new_student)
        db.session.commit()

        return render_template('index.html', success="Student added successfully!")
    except Exception as e:
        print(f"Error adding student: {e}")
        db.session.rollback()
        return render_template('index.html', error=f"Error: {e}")

@app.route('/add_staff', methods=['POST'])
def add_staff():
    try:
        name = request.form.get('name')
        position = request.form.get('position')
        contact_number = request.form.get('contact_number')

        # Debug log
        print(f"Adding staff: Name={name}, Position={position}, Contact Number={contact_number}")

        # Check if the data is correct
        if not name or not position or not contact_number:
            return render_template('index.html', error="Error: Missing staff form data")

        # Create and add new staff
        new_staff = Staff(name=name, position=position, contact_number=contact_number)
        db.session.add(new_staff)
        db.session.commit()

        return render_template('index.html', success="Staff added successfully!")
    except Exception as e:
        print(f"Error adding staff: {e}")
        db.session.rollback()
        return render_template('index.html', error=f"Error: {e}")

@app.route('/add_meal_plan', methods=['POST'])
def add_meal_plan():
    try:
        student_id = request.form.get('student_id')
        meal_plan = request.form.get('meal_plan')

        # Debug log
        print(f"Adding meal plan: Student ID={student_id}, Meal Plan={meal_plan}")

        # Check if the data is correct
        if not student_id or not meal_plan:
            return render_template('index.html', error="Error: Missing meal plan form data")

        # Check if student exists
        student = Students.query.get(student_id)
        if not student:
            return render_template('index.html', error="Error: Invalid Student ID")

        # Create and add new meal plan
        new_meal_plan = HostelMealPlans(student_id=student_id, meal_plan=meal_plan)
        db.session.add(new_meal_plan)
        db.session.commit()

        return render_template('index.html', success="Meal plan added successfully!")
    except Exception as e:
        print(f"Error adding meal plan: {e}")
        db.session.rollback()
        return render_template('index.html', error=f"Error: {e}")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure tables are created
    app.run(debug=True)
