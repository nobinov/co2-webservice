@app.route('/login', methods=['GET','POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'admin' or request.form['password']!= 'admin':
			error = 'invalid username and password'
		else:
			session['logged_in'] = True
			return redirect(url_for('index'))
	return render_template('login.html',error = error, title='Login')

	if request.method =='POST':
		node_id = request.form['node_id']
		node_desc = request.form['node_desc']
		node_pos = request.form['node_pos']
		pop = "haha"
		return redirect(url_for('index'))


	