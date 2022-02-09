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
	result['DetectorDepth'] = round(float(input['ShBack']) + float(input['CollDep']) + float(input['CryDep']) + float(input['PMTDep']), 3)
	result['DetectorLength'] = float(input['ShSide'])*2 + float(input['CryLeng'])
	result['DetectorShift'] = round(result['DetectorDepth']/2 + float(input['Dist']),4)
	
	result['CollimatorShift'] = round(-result['DetectorDepth']/2 + float(input['CollDep'])/2, 4)
	result['CrystalShift'] = round(-result['DetectorDepth']/2 + float(input['CollDep']) + float(input['CryDep'])/2, 4)
	result['PMTShift'] = round(result['DetectorDepth']/2 - float(input['ShBack']) - float(input['PMTDep'])/2, 4)
	
	result['Xgap'] = float(input['HoleR'])*2 + float(input['Septa'])
	result['Ygap'] = result['Xgap'] * 1.732050807568877
	
	result['Xgaphalf'] = result['Xgap']/2
	result['Ygaphalf'] = result['Ygap']/2

	
	result['XRepeat'] = "%d" % (float(input['CryLeng'])//result['Xgap'])
	result['YRepeat'] = "%d" % (float(input['CryWid'])//result['Ygap'])
	return render_template('output.txt', result=result)

if __name__ == '__main__':
	app.run(debug = True)
