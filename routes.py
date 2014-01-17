from flask import Flask, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:frieder@localhost/decloud'

class sensor_value(db.Model):
	__tablename_='sensor_values'
	id = db.Column(db.Integer, primary_key=True)
	sensor_id = db.Column(db.Integer)
	value = db.Column(db.Integer)

@app.route('sensor_data/', methods = ["GET"])
def sensor_data():
	if request.method == 'GET':
		results = sensor_value.query.all()
		json_results = []
		for result in results:
			d = {"sensor_id":result.sensor_id,
			     "value":result.value)
			json_result.append(d)
		return jsonify(items=json_results)

if __name__ == '__main__':
  app.run(debug=True)
