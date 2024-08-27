from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField 
from wtforms.fields import DateField

class AdvancedSearch(FlaskForm):
    manufacturingDateFilter = DateField(
        render_kw={"placeholder": "Manufacuring date"})
    priceFilter = IntegerField(
        render_kw={"placeholder": "Price"})
    submit = SubmitField("Advanced Search")
