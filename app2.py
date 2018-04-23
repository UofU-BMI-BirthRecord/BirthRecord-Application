from flask import Flask, render_template, request, flash
from SelectBabyForm import SelectBabyForm
from BabyForm import BabyForm

import json

app = Flask(__name__)
app.secret_key = 'development key'



import GetPatientInfo

import app1

@app.route('/motherinfo/<pid>', methods=['POST', 'GET'])
def motherinfo(pid):
    currentPatient = pid
    obs = app1.getPatientObservations(currentPatient, 'weight')
    recentWeight = app1.getRecent(obs)
    weight = app1.getValueQuantity(recentWeight)
    obs = app1.getPatientObservations(currentPatient, 'height')
    recentHeight = app1.getRecent(obs)
    height = app1.getValueQuantity(recentHeight)
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




@app.route('/babyresult', methods=['GET', 'POST'])
def babyResult():
    if request.method == 'POST':
        babyInformation = json.dumps(request.form)
        print("Dumpint baby info")
        print(babyInformation)
        return render_template('motherinfo.html')


@app.route('/baby/<id>', methods=['GET', 'POST'])
def babyInfo(id):
    form = BabyForm()

    if request.method == "GET":
        if form.validate() == False:
            form.preload(id)
            print(form.labels)
            print(form.labels['birth_weight_grams_label'])
            print(form.newborn_first_name_value)
            return render_template('baby.html', form=form, baby=id)
        else:
            #print(bornWithDays.data)
            #bornWithDays = form.bornWithDays.data
            #babies = GetPatientInfo.getRecentBabies(bornInDays=bornWithDays)
            #print("bornWithDays: %s" % bornWithDays)
            #return render_template('babylist.html', babies=babies, bornWithinDays=bornWithDays)

            return render_template('blank.html', baby=id)
    if request.method == "POST":
        print("Dumping form")
        json.dumps(form)
        return render_template('index.html', baby=id)


@app.route('/select', methods = ['GET', 'POST'])
def select():
    form = SelectBabyForm()
    bornWithDays = form.bornWithDays

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('selectbaby.html', form=form)
        else:
            print(bornWithDays.data)
            bornWithDays = form.bornWithDays.data
            babies = GetPatientInfo.getRecentBabies(bornInDays=bornWithDays)
            print("bornWithDays: %s" % bornWithDays)
            return render_template('babylist.html', babies=babies, bornWithinDays=bornWithDays)
    if request.method == 'GET':
        return render_template('selectbaby.html', form=form)





if __name__ == '__main__':
    app.run(debug=True)
