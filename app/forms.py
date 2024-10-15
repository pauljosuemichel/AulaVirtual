from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, FieldList, FormField
from wtforms.validators import DataRequired, Length

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


class MaterialForm(FlaskForm):
    title = StringField('Título del Material', validators=[DataRequired()])
    file = FileField('Subir Archivo', validators=[DataRequired()])
    submit = SubmitField('Subir')

from wtforms import TextAreaField, FieldList, FormField

class QuestionForm(FlaskForm):
    question = StringField('Pregunta', validators=[DataRequired()])
    answer = StringField('Respuesta', validators=[DataRequired()])

class ExamForm(FlaskForm):
    title = StringField('Título del Examen', validators=[DataRequired()])
    questions = FieldList(FormField(QuestionForm), min_entries=1, max_entries=10)
    submit = SubmitField('Crear Examen')
