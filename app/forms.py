from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField, PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length

class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class LoginForm2():
	username = StringField('username', validators=[DataRequired()])
	password = StringField('password', validators=[DataRequired()])
	remember_me = BooleanField('remember_me', default=False)

class EditNodeForm(Form):
	node_desc = TextAreaField('node_desc', default="tes", validators=[Length(min=0, max=100)])
	node_pos = StringField('node_pos',default="tes",validators=[Length(min=0, max=20)])

class AddNodeForm(Form):
	node_id = StringField('node_id',validators=[DataRequired()])
	node_desc = TextAreaField('node_desc', validators=[Length(min=0, max=100)])
	node_pos = StringField('node_pos', validators=[Length(min=0, max=20)])

class NodeManForm(Form):
	add = SubmitField('Add New Node')
	edit = SubmitField('Edit')
	deactivate = SubmitField('Deactivate')
	activate = SubmitField('Activate')
	delete = SubmitField('Delete')
	username = StringField('username')
	password = PasswordField('password')
	inputan = StringField('inputan')
	remember_me = BooleanField('remember_me', default=False)
	tes = SubmitField('submit')
	h_edit = HiddenField('aaa', default="uuuuuu")


class LoginForm3(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
    tes = SubmitField('submit')

class RESTSimForm(Form):
	node_id = StringField('node_id')
	data_co2 = StringField('data_co2')
	data_temp = StringField('data_temp')
	data_hum = StringField('data_hum')
	data_light = StringField('data_light') 