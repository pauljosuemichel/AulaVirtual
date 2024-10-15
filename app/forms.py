from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, FieldList, FormField, SelectField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileAllowed, FileField

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=150)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=150)])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class CourseForm(FlaskForm):
    name = StringField('Nombre del Curso', validators=[DataRequired()])
    submit = SubmitField('Crear Curso')

class AssignStudentForm(FlaskForm):
    student = SelectField('Seleccionar Estudiante', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Asignar Estudiante')


class UploadMaterialForm(FlaskForm):
    title = StringField('Título del Material', validators=[DataRequired()])
    file = FileField('Archivo', validators=[DataRequired()])
    submit = SubmitField('Subir Material')


class MaterialForm(FlaskForm):
    title = StringField('Título del Material', validators=[DataRequired()])
    file = FileField('Archivo', validators=[DataRequired(), FileAllowed(['pdf', 'docx', 'pptx', 'zip', 'jpg', 'png'], 'Solo se permiten archivos con extensiones: pdf, docx, pptx, zip, jpg, png')])
    submit = SubmitField('Subir')

class QuestionForm(FlaskForm):
    question = StringField('Pregunta', validators=[DataRequired()])
    answer = StringField('Respuesta', validators=[DataRequired()])

class ExamForm(FlaskForm):
    title = StringField('Título del Examen', validators=[DataRequired()])
    questions = FieldList(FormField(QuestionForm), min_entries=1, max_entries=10)
    submit = SubmitField('Crear Examen')
