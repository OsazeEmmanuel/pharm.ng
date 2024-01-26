from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, EmailField, SelectField, FileField
from wtforms.validators import DataRequired


class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")


class ItemsForm(FlaskForm):
    mychoices = ["Tablets", "Syrups", "Inhalers", "Diapers", "Others"]
    name = StringField("Item Name", validators=[DataRequired()])
    category = SelectField("Item Category",choices=mychoices, validators=[DataRequired()])
    img = FileField("Image Upload", validators=[DataRequired()])
    submit = SubmitField("Add item")
