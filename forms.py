from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, RadioField, SelectField
from wtforms.validators import DataRequired, NumberRange, Length

class ChooseChart(FlaskForm):
    symbols = StringField('Symbol ', validators=[DataRequired(), Length(min=1, max=8)])
    range = IntegerField('Range,(1..30)', validators=[DataRequired(),NumberRange(min=1, max=30, message='must(1..30)')])
    interval = SelectField('Interval, minutes (2, 5, 15 or 60):',
            choices = [('2', '2 minutes'), ('5', '5 minutes'), ('15', '15 minutes'), ('60', '60 minutes')])
    submit_chart = SubmitField('Draw a chart')
    submit_save = SubmitField('Save') ######### ????

class SettingsOfCompany(FlaskForm):
    symbols_list = StringField('List of companies(symbol with separates) ', validators=[DataRequired(), Length(min=1, max=50)])
    submit_setting_save = SubmitField('Save Settings') 
