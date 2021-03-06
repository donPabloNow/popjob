import wtforms
from wtforms import Form, BooleanField, StringField, PasswordField, validators, SubmitField, FieldList, RadioField, \
    SelectField
from wtforms_components import SelectMultipleField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import ValidationError
from flask_login import current_user
from models import User
from flask_wtf import FlaskForm
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from bson import json_util
import json


class LoginForm(Form):
    email = StringField("Email", validators=[validators.DataRequired()])
    password = PasswordField("Password", validators=[validators.DataRequired()])
    remember_me = BooleanField("Remember me?", default=True)
    submit = SubmitField('Invia')


def validate(self):
    if not super(LoginForm, self).validate():
        return False

        self.email = User.authenticate(self.email.data, self.password.data)
        if not self.user:
            self.email.errors.append("Invalid email or password.")
            return False

        return True


class RegistrationForm(Form):
    name = StringField('Name', [validators.Regexp('^[A-Za-z]', message="Name must contains only letters")])
    surname = StringField('Surname', [validators.Length(min=4, max=25)])
    email = StringField('Email', validators=[validators.Length(min=6, max=35)]) #da cambiare con EmailField
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Password must match')
    ])
    confirm = PasswordField('Repeat Password')

class RemoveSkillsForm(FlaskForm):
    skillRemove = SelectField('')
    option = StringField()
    submitR = SubmitField('Remove')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired(), validators.Length(min=2, max=20)])
    email = StringField('Email')
    picture = FileField()
    owned_skills = SelectMultipleField('Programming Language',
                                       choices=(
                                           ('Programming Languages', (
                                               ('asm', 'Assembly'),
                                               ('c', 'C'),
                                               ('cpp', 'C++'),
                                               ('java', 'Java'),
                                               ('js', 'JavaScript'),
                                               ('sql', 'SQL'),
                                               ('plsql', 'PL/SQL'),
                                               ('python', 'Python'),
                                               ('php', 'PHP'),
                                               ('ruby', 'Ruby'),
                                               ('swift', 'Swift')
                                           )),
                                           ('Soft Skills', (
                                               ('pm', 'Project Management'),
                                               ('tw', 'Teamwork'),
                                               ('potato', 'Potato')
                                           ))
                                       ), render_kw={"data-placeholder": "Select all your skills..."})

    skills = owned_skills
    submitNS = SubmitField('Update')
    submitU = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.objects(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.objects(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[validators.DataRequired()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[validators.DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[validators.DataRequired(), validators.EqualTo('password')])
    submit = SubmitField('Reset Password')


class QuizForm(FlaskForm):
    option1 = RadioField()
    submit = SubmitField('send answers')


class SearchSkillsForm(FlaskForm):
    skills = SelectField(u'Skills', choices=[(' ', ' '), ('asm', 'Assembly'), ('java', 'Java'),
                                             ('php', 'PHP'), ('plsql', 'PLSQL'),
                                             ('cpp', 'C++'), ('c', 'C'),
                                             ('sql', 'SQL'), ('python', 'Python'),
                                             ('ruby', 'Ruby'), ('swift', 'Swift')],
                         render_kw={"data-placeholder": "Select a Programming Language"})
    submit = SubmitField('Search')


class ResultsSkills():
    resultskills = SelectField(u'Skills', choices=[('asm', 'Assembly'), ('java', 'Java'),
                                                   ('php', 'PHP'), ('plsql', 'PLSQL'),
                                                   ('cpp', 'C++'), ('c', 'C'),
                                                   ('sql', 'SQL'), ('python', 'Python'),
                                                   ('ruby', 'Ruby'), ('swift', 'Swift')])


class RegCompanyForm(Form):
    nation_type = SelectField(u'Nation', choices=[(' ', ' '), ('Italia', 'Italia'), ('Stati Uniti', 'Stati Uniti'),
                                                  ('Regno Unito', 'Regno Unito'), ('Giappone', 'Giappone')])
    NameCompany = StringField('Name Company',
                              validators=[validators.Regexp('^[A-Za-z]', message="Name must contains only letters")])
    PartitaIva = StringField('PartitaIva', validators=[validators.Length(min=6, max=35)])
    Telefono = StringField('Telefono')
    email = StringField('email', validators=[validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Password must match')
    ])
    confirm = PasswordField('Repeat Password')
    NameResponsabile = StringField('NameResponsabile')
    SurnameResponsabile = StringField('SurnameResponsabile', )
