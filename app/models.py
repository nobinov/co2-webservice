from app import db

class Node(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	desc = db.Column(db.String(100), index=True)
	pos = db.Column(db.String(20), index=True)
	last_time = db.Column(db.String(30), index=True)
	last_dataid = db.Column(db.Integer, index=True)
	data = db.relationship('Data', backref='source', lazy='dynamic')

	def __repr__(self):
		return '%r' % (self.id)

class Data(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	timestamp = db.Column(db.String(30), index=True)
	data_co2 = db.Column(db.String(15), index=True)
	data_temp = db.Column(db.String(15), index=True)
	data_hum = db.Column(db.String(15), index=True)
	data_light = db.Column(db.String(15), index=True)
	node_id = db.Column(db.Integer, db.ForeignKey('node.id'))

	def __repr__(self):
		return '%r' % (self.id)