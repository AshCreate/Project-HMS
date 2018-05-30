from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from HMS.models import User
from flask_login import current_user
from flask_table import Table, Col


class SignupForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=3, max=20)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    number = StringField('Phone Number', validators=[DataRequired(), Length(min=9, max=20)])
    gender = SelectField('Gender', choices=[('M', 'Male'),
                                            ('F', 'Female')])
    password = PasswordField('Password', validators=[DataRequired()])
    cpassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        student = User.query.filter_by(email=email.data).first()
        if student:
            raise ValidationError('Account with this email already exists')

    def validate_number(self, number):
        student = User.query.filter_by(number=number.data).first()
        if student:
            raise ValidationError('Student with this number already exists')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class AnnouncementForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')


class AddRoomForm(FlaskForm):
    room_num = StringField('Room Number', validators=[DataRequired()])
    beds = SelectField('Number of occupants allowed', choices=[(1, 'One in a room'),
                                                               (2, 'Two in a room'),
                                                               (3, 'Three in a room'),
                                                               (4, 'Four in a room')], coerce=int)
    price = IntegerField('Price', validators=[DataRequired()])
    submit = SubmitField('Add Room')


class EditRoomForm(FlaskForm):
    room_num = SelectField('Number of occupants allowed', choices=[(1, 'One in a room'),
                                                                   (2, 'Two in a room'),
                                                                   (3, 'Three in a room'),
                                                                   (4, 'Four in a room')])
    beds = SelectField('Number of occupants allowed', choices=[(1, 'One in a room'),
                                                               (2, 'Two in a room'),
                                                               (3, 'Three in a room'),
                                                               (4, 'Four in a room')])
    price = IntegerField('Price', validators=[DataRequired()])
    submit = SubmitField('Update Room')


class UpdateAccountForm(FlaskForm):
    firstname = StringField('Firstname',
                            validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Lastname',
                           validators=[DataRequired(), Length(min=2, max=20)])
    number = StringField('Phone Number',
                         validators=[DataRequired(), Length(min=9, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_number(self, number):
        if number.data != current_user.number:
            user = User.query.filter_by(number=number.data).first()
            if user:
                raise ValidationError('That number is taken.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
