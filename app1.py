from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_script import Manager, Shell
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from dateutil.parser import parse
import requests


from fhirclient import client
import json, requests


settings = {
    'app_id': 'my_web_app',
    'api_base': 'https://api-v5-stu3.hspconsortium.org/DBMIBC/open/'
}
smart = client.FHIRClient(settings=settings)

import fhirclient.models.patient as p
#patient = p.Patient.read('hca-pat-1', smart.server)
#patient = p.Patient.read('cf-1517843572299', smart.server)
patient = p.Patient.read('cf-1518386133147', smart.server)
#patient.birthDate.isostring
# '1963-06-12'
print(smart.human_name(patient.name[0]))
#print(patient.toString())
# 'Christy Ebert'

bundle = requests.get('https://api-v5-stu3.hspconsortium.org/DBMIBC/open/Condition?patient=cf-1518386133147')
bundle = requests.get('https://api-v5-stu3.hspconsortium.org/DBMIBC/open/Observation?patient=16952')
data = json.loads(bundle.text)
print(data)
print(data['entry'][1]['resource']['code'])
#'15938005'


HSPC_OPEN_END = "https://api-v5-stu3.hspconsortium.org/DBMIBC/open/"
CODES = {}
CODES['weight'] = {'system': "http://loinc.org", "code": "LP18015-5"}
CODES['height'] = {'system': "http://loinc.org", "code": "8302-2"}

def codeMatched(code, codes):
    if code['system'] == codes['system'] and code['code'] == codes['code']:
        return True
    else:
        return False

def getPatientObservations(patient, key):
    bundle = requests.get(HSPC_OPEN_END+'Observation?patient='+patient)
    observations = json.loads(bundle.text)
    res = []
    if observations['total'] == 0:
         return res
    for obs in observations['entry']:
        codes = obs['resource']['code']
        for code in codes['coding']:
            if codeMatched(code, CODES[key.lower()]):
                res.append(obs['resource'])
                break
    return res


def getObservations(observations, key):
    res = []
    for obs in observations['entry']:
        codes = obs['resource']['code']
        for code in codes['coding']:
            if codeMatched(code, CODES[key.lower()]):
                res.append(obs['resource'])
                break
    return res

def getRecent(data):
    if data == None or len(data) == 0:
        return None
    latest = None
    datum = None
    for d in data:
        last = parse(d['meta']['lastUpdated'])
        if latest == None:
            latest = last
            datum = d
        elif latest < last:
            latest = last
            datum = d
    return datum

def getValueQuantity(datum):
    res = None
    if datum == None:
        res = None
    elif 'valueQuantity' in datum:
        if 'value' in datum['valueQuantity'] and 'unit' in datum['valueQuantity']:
            res = {}
            res['value'] = datum['valueQuantity']['value']
            res['unit'] = datum['valueQuantity']['unit'].encode('utf-8')
        else:
            res = None
    else:
        res = None
    return res

weightObses = getObservations(data, 'weight')
weightObs = getRecent(weightObses)
print("%s taken at %s: %g %s" % ("Weight", weightObs['meta']['lastUpdated'], weightObs['valueQuantity']['value'], weightObs['valueQuantity']['unit']))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

currentPatient = "16952"



@app.route('/motherinfo', methods=['POST', 'GET'])
def motherinfo():
    currentPatient = "16952"
    obs = getPatientObservations(currentPatient, 'weight')
    recentWeight = getRecent(obs)
    weight = getValueQuantity(recentWeight)
    obs = getPatientObservations(currentPatient, 'height')
    recentHeight = getRecent(obs)
    height = getValueQuantity(recentHeight)
    print(height)
    print(weight)
    #weightvalue = weight['value']
    #weightunit = weight['unit']
    #heightvalue = height['value']
    #heightunit = height['unit']
    #print(weightvalue, weightunit, heightvalue, heightunit)
    errors = None
    if request.method == 'POST':
        heightvalue = request.form['height']
        weightvalue = request.form['weight']
        return redirect(url_for('motherRiskFactor'))
    return render_template('motherinfo.html', weight=weight, height=height)


@app.route('/motherriskfactor', methods=['POST', 'GET'])
def motherRiskFactor():
    return render_template('motherriskfactor.html')

if __name__ == '__main__':
    app.run(debug=True)
