from flask import Blueprint, render_template, redirect, url_for, request
from .models import User, Course, Material, db
from .forms import LoginForm, RegistrationForm

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

