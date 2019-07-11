from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

# class LoginForm(FlaskForm):
    # username = StringField('Username', validators=[DataRequired()])
    # password = PasswordField('Password', validators=[DataRequired()])
    # remember_me = BooleanField('Remember Me')
    # submit = SubmitField('Sign In')

class ChooseChart(FlaskForm):
    symbols = StringField('Symbols ', validators=[DataRequired()])
    range = StringField('Range (1..30)', validators=[DataRequired()])
    interval = StringField('Interval, minutes:')
    submit_chart = SubmitField('Draw a chart')
    submit_save = SubmitField('Save')
