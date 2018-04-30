from flask_wtf import FlaskForm
from wtforms import IntegerField, TextField, SubmitField
from wtforms import validators, ValidationError



class SelectBabyForm(FlaskForm):
    bornWithDays = IntegerField("Search for Babies Born Within:")
    submit = SubmitField("Search")
