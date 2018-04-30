from flask import Flask, render_template, request, flash, redirect, url_for,session, flash
from flask_bootstrap import Bootstrap
from SelectBabyForm import SelectBabyForm
from BabyForm1 import BabyForm
from MotherForm import MotherForm


import json
import easygui

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.secret_key = 'development key'


currentInformation = {}


import GetPatientInfo

#import app1

@app.route('/motherresult', methods=['GET', 'POST'])
def motherResult():
    if request.method == 'POST':
        CODEFILE = "FHIR_resource_codes_1.txt"
        codes = GetPatientInfo.getCODETABLE(file=CODEFILE, page='mother')
        motherInformation = mapUDOHvaribleName(request.form, codes)
        currentInformation = session.get('currentInformation')
        #print("*****", currentInformation)
        currentInformation.update(motherInformation)
        motherInformation = json.dumps(currentInformation, indent=4, sort_keys=True)
        #print("mother result form is a ", type(request.form))
        #print("Dumpint mother info")
        #print(motherInformation)
        easygui.msgbox(motherInformation)
        return redirect('select')
        #return render_template('motherinfo.html', )



@app.route('/motherinfo/<pid>', methods=['POST', 'GET'])
def motherinfo(pid):
    currentPatient = pid
    print("mother is "+pid)
    form = MotherForm()
    if request.method == "GET":
        if form.validate() == False:
            form.preload(pid)
            #print(form.labels)
            #print(form.labels['birth_weight_grams_label'])
            print(form.mother_first_name)
            return render_template('mother.html', form=form, mother=pid)
        else:
            #print(bornWithDays.data)
            #bornWithDays = form.bornWithDays.data
            #babies = GetPatientInfo.getRecentBabies(bornInDays=bornWithDays)
            #print("bornWithDays: %s" % bornWithDays)
            #return render_template('babylist.html', babies=babies, bornWithinDays=bornWithDays)

            return render_template('blank.html', mother=pid)
    #if request.method == "POST":
        #print("Dumping form")
        #json.dumps(form)
        #return render_template('index.html', mother=pid)





@app.route('/babyresult', methods=['GET', 'POST'])
def babyResult():
    if request.method == 'POST':
        CODEFILE = "FHIR_resource_codes_1.txt"
        codes = GetPatientInfo.getCODETABLE(file=CODEFILE, page='baby')
        currentInformation = mapUDOHvaribleName(request.form, codes)
        session['currentInformation'] = currentInformation
        babyInformation = json.dumps(currentInformation, indent=4, sort_keys=True)
        #print("baby result form is a ", type(request.form))
        #print("Dumpint baby info")
        #print(babyInformation)
        easygui.msgbox(babyInformation)
        print( "The mother id", request.form['mother_id'])
        if request.form['mother_id'] == None or request.form['mother_id'] == '':
            easygui.msgbox("Mother ID required!")
            return redirect('baby/' + session.get('currentBaby'))
        return redirect('motherinfo/'+request.form['mother_id'])
        #return render_template('motherinfo.html', )


@app.route('/baby/<id>', methods=['GET', 'POST'])
def babyInfo(id):
    form = BabyForm()
    session['currentBaby'] = id
    if form.validate_on_submit():
        return render_template('baby1.html', form=form, baby=id)

    if request.method == "GET":
        if form.validate() == False:
            form.preload(id)
            #print(form.labels)
            #print(form.labels['birth_weight_grams_label'])
            #print(form.newborn_first_name)
            if form.mother_id == None:
                raise ValidationError
            return render_template('baby1.html', form=form, baby=id)
        else:
            #print(bornWithDays.data)
            #bornWithDays = form.bornWithDays.data
            #babies = GetPatientInfo.getRecentBabies(bornInDays=bornWithDays)
            #print("bornWithDays: %s" % bornWithDays)
            #return render_template('babylist.html', babies=babies, bornWithinDays=bornWithDays)
            return render_template('baby1.html', form=form, baby=id)
    #if request.method == "POST":
    #    print("Dumping form")
    #    json.dumps(form)
    #   return render_template('index.html', baby=id)


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



def mapUDOHvaribleName(dictionary, codes):
    d = {}
    for k in dictionary.keys():
        if k in codes.keys():
            UDOHname = codes[k]['UDOH_variable']
            if type(dictionary[k]) == unicode:
                item = dictionary[k].encode('ascii')
                print(item)
                comm = "d['%s'] = " % UDOHname +'\''+item+'\''
            else:
                comm = "d['%s'] = %s" % (UDOHname, dictionary[k])
            print("in mapUDOH: command is: %s, type(): %s" % (comm, type(dictionary[k])))
            exec(comm)
    return d





if __name__ == '__main__':
    app.run(debug=True)
