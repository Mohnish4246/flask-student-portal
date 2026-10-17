from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from wtforms.validators import DataRequired, Length,Email,EqualTo

class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3,max=50)
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6,max=100)
        ]
    )

    submit = SubmitField("Login")

# NEW: Registration form with validation matching LoginForm
class RegisterForm(FlaskForm):

    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3, max=50)
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6, max=100)
        ]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match.")
        ]
    )

    submit = SubmitField("Register")



class StudentForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[
            DataRequired(),
            Length(min=2,max=99)
        ]
    )
    course = StringField(
        "Course",
        validators=[
            DataRequired(),
            Length(min=2,max=99)
        ]
    )
    photo = FileField(
        "Photo",
        validators=[
            FileAllowed(    
                ["jpg","jpeg","png","gif"],
                "Only JPG, JPEG, PNG and GIF files are allowed."
            )
        ]
    )
    submit = SubmitField("Add Student")

class EditStudentForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[
            DataRequired(),
            Length(min=2,max=99)
        ]
    )
    course = StringField(
        "Course",
        validators=[
            DataRequired(),
            Length(min=2,max=99)
        ]
    )
    photo = FileField(
        "Photo",
        validators=[
            FileAllowed(    
                ["jpg","jpeg","png","gif"],
                "Only JPG, JPEG, PNG and GIF files are allowed."
            )
        ]
    )
    submit = SubmitField("Add Student")

class AssignCourseForm(FlaskForm):
    course_id = SelectField(
        "Course",
        coerce = int,
        validators=[
            DataRequired()
        ]
    )
    submit = SubmitField("Assign Course")