from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Email

class SalesStaffForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    active = BooleanField('Active', default=True)
    store_id = IntegerField('Store ID', validators=[DataRequired()])
    manager_id = IntegerField('Manager ID', validators=[DataRequired()])
