from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField,IntegerField,DecimalField,SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from RetailBank.models import userstore,Customer,Account

class Loginform(FlaskForm):
	login = StringField('Login',validators=[DataRequired(),Length(min=2, max=20)])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Login')

class NewCustomerForm(FlaskForm):
	ssd_id=IntegerField('Customer SSD Id',validators=[DataRequired()])
	customer_name=StringField('Customer Name',validators=[DataRequired()])
	customer_age=StringField('Customer Age', validators=[DataRequired()])
	customer_address=StringField('Customer Address',validators=[DataRequired()])
	customer_state=StringField('Customer State',validators=[DataRequired()])
	customer_city=StringField('Customer City',validators=[DataRequired()])
	submit = SubmitField('Create')

class DeleteCustomerForm(FlaskForm):
	cus_id=StringField('Delete Customer Account',validators=[DataRequired()])
	submit = SubmitField('Delete')

class UpdateCustomerForm(FlaskForm):
	customer_name=StringField('New Customer Name')
	customer_age=StringField('New Customer Age')
	customer_address=StringField('New Customer Address')
	customer_state=StringField('New Customer State')
	customer_city=StringField('New Customer City')
	submit = SubmitField('Update')

class SearchCustomerForm(FlaskForm):
	cus_id=StringField('Enter Customer ssd_id',validators=[DataRequired()])
	submit=SubmitField('Search')

class NewAccountForm(FlaskForm):
	customer_id=IntegerField('Account ID  ',validators=[DataRequired()])
	account_type=StringField('Account type (Savings or Current) ',validators=[DataRequired()])
	deposit_amount=IntegerField('Deposit Amount ',validators=[DataRequired()])
	submit=SubmitField('Submit')

class DeleteAccountForm(FlaskForm):
	customer_id=customer_id=IntegerField('Customer SSN_ID  ',validators=[DataRequired()])
	submit=SubmitField('Delete')

