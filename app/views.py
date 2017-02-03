from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from datetime import datetime
from app import app, db
from .models import Node, Data
from sqlalchemy import desc
from functools import wraps
from .forms import LoginForm, AddNodeForm, LoginForm3, NodeManForm, EditNodeForm, RESTSimForm
import time

app.secret_key = "adjhaldksjah"

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

@app.errorhandler(400):
def bad_request(error):
	return render_template('400.html'), 400

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
	nd_list = []
	nodes = Node.query.all()
	alldata = Data.query.order_by(desc('id')).all()

	for n in nodes:
		nd = []
		d = Data.query.get(n.last_dataid)
		nd.append(n.id)
		nd.append(n.desc)
		nd.append(n.pos)
		nd.append(n.last_time)
		nd.append(d.data_co2)
		nd.append(d.data_temp)
		nd.append(d.data_hum)
		nd.append(d.data_light)

		nd_list.append(nd)
		#flash(nd)

	#flash(nd_list)

	return render_template('data_display.html',nodes=nodes, alldata=alldata, session=session, nd_list=nd_list, title='Data Display')

@app.route('/node_management', methods=['GET','POST'])
#@login_required
def node_management():
	nodes = Node.query.all()
	form = NodeManForm()
	sel_nodeID = ""
	sel_node = ""
	btn_edit = ""
	btn_delete = ""
	btn_add = ""

	if form.validate_on_submit():
		if form.add.data == True:
			return redirect(url_for('node_add'))
		else :
			sel_nodeID = request.form['data']
			btn_edit = form.edit.data
			btn_delete = form.delete.data

			sel_node = Node.query.get(sel_nodeID)

			#delete node
			if btn_delete==True:
				db.session.delete(sel_node)
				db.session.commit()
				flash ('delete node, ID: %s' %(sel_nodeID))
			#edit node
			elif btn_edit ==True:
				return redirect(url_for('node_edit', node_id = sel_nodeID))

	flash(sel_nodeID)
	flash(btn_edit)
	flash(btn_delete)
	flash(btn_add)

	return render_template('node_management.html', nodes=nodes, title='Node Management Interface', form=form)

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
		return redirect(url_for('node_management'))
	return render_template('node_add.html', title='Node Add', pop=pop, form=form)	

@app.route('/node_edit/<int:node_id>', methods=['GET','POST'])
def node_edit(node_id):
	node = Node.query.get(node_id)
	if node == None:
		return render_template('404.html')
	else:
		form = EditNodeForm()
		form.node_desc.data = node.desc
		form.node_pos.data = node.pos

		if form.validate_on_submit():
			new_n_desc = form.node_desc.data
			new_n_pos = form.node_pos.data

			node.desc = new_n_desc
			node.pos = new_n_pos
			db.session.commit()
			flash('edit node "%s" information' %(str(node.id)))
			return redirect(url_for('node_management'))
		return render_template('node_edit.html', node=node, form=form)
	


@app.route('/api/v01/get/data',methods=['GET'])
def api_data_getAll():
	allData = Data.query.order_by(desc('id')).all()

	allData_json = []

	for d in allData:
		data = {
		'id' : d.id,
		'timestamp' : d.timestamp,
		'co2' : d.data_co2,
		'temp' : d.data_temp,
		'hum' : d.data_hum,
		'light' : d.data_light,
		'source' : d.node_id
		}
		allData_json.append(data)
		#return jsonify(d)
		#flash(d)
	return jsonify({'data' : allData_json})

@app.route('/api/v01/get/data/<int:node_id>',methods=['GET'])
def api_data_get(node_id):
	node_available = Node.query.get(node_id)
	if node_available == None:
		return jsonify({'data' : 'node ' + str(node_id) + ' doesnt exist'})
	else:
		allData = Data.query.filter(Data.node_id==node_id).order_by(desc('id')).all()

		allData_json = []

		for d in allData:
			data = {
			'id' : d.id,
			'timestamp' : d.timestamp,
			'co2' : d.data_co2,
			'temp' : d.data_temp,
			'hum' : d.data_hum,
			'light' : d.data_light,
			'source' : d.node_id
			}
			allData_json.append(data)
			#return jsonify(d)
			#flash(d)
		return jsonify({'data' : allData_json})


@app.route('/api/v01/get/node',methods=['GET'])
def api_node_get():
	allNode = Node.query.order_by(desc('id')).all()

	allNode_json = []

	for n in allNode:
		node = {
		'id' : n.id,
		'desc' : n.desc,
		'pos' : n.pos,
		'last_time' : n.last_time,
		'last_dataid' : n.last_dataid
		}
		allNode_json.append(node)
		#return jsonify(d)
		#flash(d)
	return jsonify({'node' : allNode_json})

@app.route('/api/v01/post/data/add',methods=['POST'])
def api_data_add():
	if not request.json:
		abort(400)
	nid = request.json['id']
	ts = request.json['timestamp']
	co2 = request.json['co2']
	temp = request.json['temp']
	hum = request.json['hum']
	light = request.json['light']

	node = Node.query.get(nid)
	if node == None:
		return jsonify({'update':'failed'})
	else:
		insert = Data(timestamp=ts,
						data_co2=co2,
						data_temp=temp,
						data_hum=hum,
						data_light=light,
						node_id=nid)
		db.session.add(insert)
		db.session.commit()

		#udpate last updated in node table
		#node = Node.query.get(insert.node_id)
		node.last_time = ts
		node.last_dataid = insert.id
		db.session.commit()

		return jsonify({'updated':insert.id})


@app.route('/api/v01/post/node/add',methods=['POST'])
def api_node_add():
	if not request.json:
		abort(400)
	n_id = request.json['id']	
	n_desc = request.json['desc']
	n_pos = request.json['pos']
	n_lt = "None"
	n_did = "None"


	node = Node.query.get(n_id)
	if node == None:
		insert = Node(id=n_id,
			desc=n_desc,
			pos=n_pos,
			last_time=n_lt,
			last_dataid=n_did)
		db.session.add(insert)
		db.session.commit()
		return jsonify({'new node':insert.id})
		
	else:
		return jsonify({'new node':'already exist'})

@app.route('/api/v01/post/node/edit',methods=['POST'])
def api_node_edit():
	if not request.json:
		abort(400)
	n_id = request.json['id']	
	new_n_desc = request.json['desc']
	new_n_pos = request.json['pos']

	node = Node.query.get(n_id)
	if node == None:
		return jsonify({'edit node':'not found'})

	else:
		node.desc = new_n_desc
		node.pos = new_n_pos
		db.session.commit()
		return jsonify({'edit node':node.id})

@app.route('/api/v01/post/node/delete',methods=['POST'])
def api_node_delete():
	if not request.json:
		abort(400)
	n_id = request.json['id']	

	node = Node.query.get(n_id)
	if node == None:
		return jsonify({'delete node':'not found'})

	else:
		db.session.delete(node)
		db.session.commit()
		return jsonify({'delete node':node.id})



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

@app.route('/node_edit2', methods=['GET','POST'])
def node_edit2():
	return render_template('node_edit.html', title='Node Edit')

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'node data': node_data})