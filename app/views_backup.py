from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from datetime import datetime
from app import app, db
from .models import Node, Data
from sqlalchemy import desc
from forms import EditNode
from functools import wraps
from .forms import LoginForm, AddNodeForm, LoginForm3, NodeManForm
import time

app.secret_key = "adjhaldksjah"

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('You need login first')
			return redirect(url_for('login'))
	return wrap 


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:page>', methods=['GET', 'POST'])
def index():
	#nodes = Node.query.all()
	return render_template('index.html', title='Home', session=session)

@app.route('/login', methods=['GET','POST'])
def login():
	error = None

	form = LoginForm()
	if form.validate_on_submit():
		flash('Login requested for Username="%s", remember_me=%s' %(form.username.data, str(form.remember_me.data)))
		if form.username.data != 'admin' and form.password.data != 'admin' :
			error = 'invalid username and password'
			flash(error)
		else :
			session['logged_in'] = True
			return redirect(url_for('index'))

	return render_template('login.html',error = error, title='Login', form=form)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('Logged Out')
	return redirect(url_for('index'))


# for data I/O channel

@app.route('/data_display', methods=['GET'])
@login_required
def data_display():
	datalist = []
	nodes = Node.query.all()
	alldata = Data.query.order_by(desc('timestamp')).all()
	return render_template('data_display.html',nodes=nodes, alldata=alldata, session=session, title='Data Display')

@app.route('/node_management', methods=['GET','POST'])
#@login_required
def node_management():
	nodes = Node.query.all()
	pop = ""
	n_in = ""
	n_edit = ""
	n_delete = ""
	form = NodeManForm()
	#if form.validate_on_submit():
	if form.validate_on_submit():
		#flash('Login requested for Username="%s", remember_me=%s' %(form.username.data, str(form.remember_me.data)))
		n_in = form.h_edit.data
		n_edit = request.form['edit']
		n_delete = request.form['delete']
		pop='0'
	#flash(form.tes.data)
	#flash(request.form['data'])
	flash('edit %s delete %s' %(n_edit, n_delete))
	flash(form.h_edit.data)
	flash(form.edit.data)
	flash(form.delete.data)
	flash('syalala')

	return render_template('node_management.html', nodes=nodes, title='Node Management Interface', pop=pop, form=form)

@app.route('/node_add', methods=['GET','POST'])
def node_add():
	pop = ""
	form = AddNodeForm()
	if form.validate_on_submit():
		n_id = form.node_id.data
		n_desc = form.node_desc.data
		n_pos = form.node_pos.data
		n_lt = "None"
		n_did = "None"

		insert = Node(id=n_id,
						desc=n_desc,
						pos=n_pos,
						last_time=n_lt,
						last_dataid=n_did)
		db.session.add(insert)
		db.session.commit()

		flash('add new node : "%s"' %(str(form.node_id.data)))
		return redirect(url_for('index'))
	return render_template('node_add.html', title='Node Edit', pop=pop, form=form)	

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'node data': node_data})

@app.route('/api/v01/post',methods=['POST'])
def api_postdata():
	if not request.json:
		abort(400)
	nid = request.json['id']
	ts = request.json['timestamp']
	co2 = request.json['co2']
	temp = request.json['temp']
	hum = request.json['hum']
	light = request.json['light']

	#return jsonify({'a':nid})

	#a = models.Data.query.all()

	insert = Data(timestamp=ts,
						data_co2=co2,
						data_temp=temp,
						data_hum=hum,
						data_light=light,
						node_id=nid)
	db.session.add(insert)
	db.session.commit()

	#udpate last updated in node table
	node = Node.query.get(insert.node_id)
	node.last_time = 'syalala'
	node.last_dataid = insert.id

	return jsonify({'updated':insert.id})



@app.route('/edit', methods=['GET', 'POST'])
def edit():
	form = EditNode()
	if form.validate_on_submit():
		flash('saved!')
		return redirect(url_for('edit'))
	else:
		return redirect(url_for('edit'))

@app.route('/edits', methods=['GET', 'POST'])
def edits():
	return render_template('edit.html')

