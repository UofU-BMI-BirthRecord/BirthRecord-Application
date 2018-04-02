from flask_wtf import Form
from wtforms import IntegerField, TextField, SubmitField
from wtforms import validators, ValidationError

class SelectBabyForm(Form):
    bornWithDays = IntegerField("Get babies born with days")
    submit = SubmitField("Get Newborns")