from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import User, Course, Material, db
from .forms import LoginForm, RegistrationForm, MaterialForm
from flask_login import current_user, login_required

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)

@main.route('/courses')
def courses():
    courses = Course.query.all()
    return render_template('courses.html', courses=courses)


main = Blueprint('main', __name__)

@main.route('/course/<int:course_id>/materials', methods=['GET', 'POST'])
@login_required
def upload_material(course_id):
    form = MaterialForm()
    course = Course.query.get_or_404(course_id)

    if request.method == 'POST' and form.validate_on_submit():
        # Aquí puedes añadir la lógica para guardar el archivo en el servidor
        material = Material(title=form.title.data, file_path="ruta_del_archivo", course_id=course.id)
        db.session.add(material)
        db.session.commit()
        flash('Material subido con éxito')
        return redirect(url_for('main.course_detail', course_id=course.id))

    return render_template('upload_material.html', form=form, course=course)



@main.route('/course/<int:course_id>/exam', methods=['GET', 'POST'])
@login_required
def create_exam(course_id):
    form = ExamForm()
    course = Course.query.get_or_404(course_id)

    if request.method == 'POST' and form.validate_on_submit():
        # Lógica para guardar las preguntas en la base de datos
        exam = Exam(title=form.title.data, course_id=course.id)
        db.session.add(exam)
        db.session.commit()

        # Guardar cada pregunta
        for question_form in form.questions:
            question = Question(question=question_form.question.data, answer=question_form.answer.data, exam_id=exam.id)
            db.session.add(question)

        db.session.commit()
        flash('Examen creado con éxito')
        return redirect(url_for('main.course_detail', course_id=course.id))

    return render_template('create_exam.html', form=form, course=course)
