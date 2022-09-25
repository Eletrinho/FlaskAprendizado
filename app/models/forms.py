from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    remember_me = BooleanField("remember_me")

class RegisterForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    name = StringField("name", validators=[DataRequired()])
    email = EmailField("email", validators=[DataRequired()])

class PostForm(FlaskForm):
    content = TextAreaField("content", validators=[DataRequired(), Length(min=3, max=200)])