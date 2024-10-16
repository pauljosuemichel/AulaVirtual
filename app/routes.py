import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from .models import User, Course, Material, db
from .forms import LoginForm, RegistrationForm, MaterialForm, CourseForm, AssignStudentForm, UploadMaterialForm
from flask_login import current_user, login_required, login_user, logout_user

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
    # usuario ya está autenticado, redirigir a la página de inicio
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    
    # validacion
    if form.validate_on_submit():
        # Buscar al usuario en la base de datos
        user = User.query.filter_by(username=form.username.data).first()
        
        # Verificar si el usuario existe y la contraseña es correcta
        if user and user.password == form.password.data:  # NOTA: Aquí deberías usar hashing
            login_user(user)  # Autenticar al usuario
            flash('Has iniciado sesión correctamente.', 'success')
            return redirect(url_for('main.index'))  # Redirigir después del login exitoso
        else:
            flash('Nombre de usuario o contraseña incorrectos.', 'danger')
    
    # Renderizar la plantilla de login
    return render_template('login.html', form=form)

@main.route('/courses')
def courses():
    courses = Course.query.all()
    return render_template('courses.html', courses=courses)



# Ruta para crear un curso
@main.route('/create_course', methods=['GET', 'POST'])
@login_required
def create_course():
    form = CourseForm()

    # validacion del formulario
    if form.validate_on_submit():
        # Crear un nuevo curso
        new_course = Course(name=form.name.data)
        db.session.add(new_course)
        db.session.commit()
        
        flash('Curso creado exitosamente.', 'success')
        return redirect(url_for('main.courses'))
    
    return render_template('create_course.html', form=form)




@main.route('/assign_student/<int:course_id>', methods=['GET', 'POST'])
@login_required
def assign_student(course_id):
    course = Course.query.get_or_404(course_id)
    form = AssignStudentForm()
    
    # Poblamos el SelectField con los usuarios (estudiantes) que no están asignados a este curso
    form.student.choices = [(student.id, student.username) for student in User.query.all() if student not in course.students]
    
    if form.validate_on_submit():
        student = User.query.get(form.student.data)
        if student:
            # Asignar el estudiante al curso
            course.students.append(student)
            db.session.commit()
            flash(f'Estudiante {student.username} asignado al curso {course.name}.', 'success')
            return redirect(url_for('main.courses'))
    
    return render_template('assign_student.html', form=form, course=course)




@main.route('/upload_material/<int:course_id>', methods=['GET', 'POST'])
@login_required
def upload_material(course_id):
    course = Course.query.get_or_404(course_id)
    form = UploadMaterialForm()

    if form.validate_on_submit():
        # Guardar el archivo en el servidor
        file = form.file.data
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Crear el nuevo material y guardarlo en la base de datos
        material = Material(title=form.title.data, file_path=file_path, course_id=course.id)
        db.session.add(material)
        db.session.commit()

        flash('Material subido exitosamente.', 'success')
        return redirect(url_for('main.courses'))

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


@main.route('/view_students/<int:course_id>')
@login_required
def view_students(course_id):
    course = Course.query.get_or_404(course_id)
    students = course.students  # Obtener los estudiantes asignados a este curso
    
    return render_template('view_students.html', course=course, students=students)

