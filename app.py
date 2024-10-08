from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, current_user, roles_required, hash_password
from flask_mailman import Mail
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap5
import config

app = Flask(__name__)
Bootstrap5(app)
app.config.from_object(config)
db= SQLAlchemy(app)
migrate = Migrate(app, db)

roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True)
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    webauthn = db.relationship('WebAuth', backref='user', uselist=False)

class WebAuth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    teacher = db.relationship('User', backref='course_taught',)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    course = db.relationship('Course', backref='enrollments')
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    student = db.relationship('User', backref='enrollments')
    grade = db.Column(db.Float(40), nullable=True)


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

mail = Mail(app)

@app.route('/')
@login_required
def index():
    courses_count = Course.query.count()
    students_count = User.query.join(User.roles).filter(Role.name == 'Student').count()
    teachers_count = User.query.join(User.roles).filter(Role.name == 'Teacher').count()
    return render_template('index.html', courses_count=courses_count, students_count=students_count, teachers_count=teachers_count)

@app.route('/courses')
@login_required
def courses():
    if current_user.has_role('Admin') or current_user.has_role('Teacher'):
        courses = Course.query.all()
    else:
        courses = [current_user.enrollments for enrollment in current_user.enrollments]
    return render_template('courses.html', courses=courses)

@app.route('/course/<int:course_id>')
@login_required
def course_details(course_id):
    course = Course.query.get_or_404(course_id)
    return render_template('course_details.html', course=course)

@app.route('/create_course', methods=['GET','POST'])
@roles_required('Admin')
def create_course():
    if request.method == 'POST':
        name = request.form['name']
        teacher_id = request.form['teacher_id']
        course = Course(name=name, teacher_id=teacher_id)
        db.session.add(course)
        db.session.commit()
        flash('Course created successfully')
        return redirect(url_for('courses'))
    teachers = User.query.join(User.roles).filter(Role.name =='Teacher').all()
    return render_template('create_course.html', teachers=teachers)

@app.route('/enroll/<int:course_id>')
@roles_required('Student')
def enroll(course_id):
    course = Course.query.get_or_404(course_id)
    if Enrollment.query.filter_by(student_id=current_user.id, course_id=course_id).first():
        flash('You are already enrolled in this course')
    else:
        enrollment = Enrollment(course_id=course_id, student_id=current_user.id)
        db.session.add(enrollment)
        db.session.commit()
        flash('You have enrolled successfully')
    return redirect(url_for('course_details', course_id=course_id))

@app.route('/grade/<int:enrollment_id>', methods=['GET','POST'])
@roles_required('Teacher')
def grade(enrollment_id):
    enrollment = Enrollment.query.get_or_404(enrollment_id)
    if enrollment.course.teacher_id != current_user.id:
        flash('You are not the teacher of this course')
        return redirect(url_for('courses'))
    grade = request.form.get('grade')
    enrollment.grade = float(grade)
    db.session.commit()
    flash('Grade submitted successfully')
    return redirect(url_for('course_details', course_id=enrollment.course_id))


    


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        #Create roles
        user_datastore.find_or_create_role(name='Admin', description='Administrator')
        user_datastore.find_or_create_role(name='Teacher', description='Teacher')
        user_datastore.find_or_create_role(name='Student', description='Student')

        #Create users
        if not user_datastore.find_user(email='chatelobenna@gmail.com'):
            hashed_password = hash_password('Mypassword')
            user_datastore.create_user(email='chatelobenna@gmail.com', password=hashed_password, roles=[user_datastore.find_role('Admin')])
            db.session.commit()

        if not user_datastore.find_user(email='ronohbenard48@gmail.com'):
            hashed_password = hash_password('Mypassword')
            user_datastore.create_user(email='ronohbenard48@gmail.com', password=hashed_password, roles=[user_datastore.find_role('Teacher')])
            db.session.commit()
        if not user_datastore.find_user(email='biikate48@gmail.com'):
            hashed_password = hash_password('Mypassword')
            user_datastore.create_user(email='biikate48@gmail.com', password=hashed_password, roles=[user_datastore.find_role('Teacher')])
            db.session.commit()
        if not user_datastore.find_user(email='carolinecherono30@gmail.com'):
            hashed_password = hash_password('Mypassword')
            user_datastore.create_user(email='carolinecherono30@gmail.com', password=hashed_password, roles=[user_datastore.find_role('Student')])
            db.session.commit()

    app.run(debug=True, port=5001)
 