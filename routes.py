from flask import Flask, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:frieder@localhost/decloud'

class sensor_values(db.Model):
	__tablename__='sensor_values'
	id = db.Column(db.Integer, primary_key=True)
	sensor_id = db.Column(db.Integer)
	value = db.Column(db.Integer)
	
	def __init__(self, sensor_id, value):
		self.sensor_id = sensor_id
		self.value = value

@app.route('/sensor_data/', methods = ["GET", "POST"])
def sensor_data():
	if request.method == 'GET':
		results = sensor_values.query.all()
		json_results = []
		for result in results:
			d = {"sensor_id":result.sensor_id,
			     "value":result.value}
			json_results.append(d)
		return jsonify(items=json_results)
	if request.method == 'POST':
		global db
		db.session.add(sensor_data(request.json["sensor_id"],request.json["value"]))
		db.commit()

if __name__ == '__main__':
  app.run(debug=True)
