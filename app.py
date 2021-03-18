from flask import Flask, request, render_template
from jinja2 import Template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def getdata():
	return render_template('index.html')

@app.route('/view', methods=['POST', 'GET'])
def submit():
	input = request.form
	
	result = {**input}
	
	result['DetectorWidth'] = float(input['ShSide'])*2 + float(input['CryWid'])
	result['DetectorDepth'] = float(input['ShBack']) + float(input['CollDep']) + float(input['CryDep']) + float(input['PMTDep'])
	result['DetectorLength'] = float(input['ShSide'])*2 + float(input['CryLeng'])
	result['DetecotrShift'] = result['DetectorDepth']/2 + float(input['Dist'])
	
	result['CollimatorShift'] = -result['DetectorDepth']/2 + float(input['CollDep'])/2	
	result['CrystalShift'] = -result['DetectorDepth']/2 + float(input['CollDep']) + float(input['CryDep'])/2
	result['PMTShift'] = result['DetectorDepth']/2 - float(input['ShBack']) - float(input['PMTDep'])/2
	
	result['Xgap'] = float(input['HoleR'])*2 + float(input['Septa'])
	result['Ygap'] = result['Xgap'] * 1.732050807568877
	
	result['Xgaphalf'] = result['Xgap']/2
	result['Ygaphalf'] = result['Ygap']/2

	
	result['XRepeat'] = "%d" % (float(input['CryLeng'])//result['Xgap'])
	result['YRepeat'] = "%d" % (float(input['CryWid'])//result['Ygap'])
	return render_template('output.txt', result=result)

if __name__ == '__main__':
	app.run(debug = True)
