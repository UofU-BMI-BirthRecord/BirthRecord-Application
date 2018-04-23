#from flask_wtf import Form
from flask.ext.wtf import Form
from wtforms import IntegerField, SubmitField, TextAreaField, SelectField, StringField, TextField, DecimalField, HiddenField, BooleanField
from wtforms import validators, ValidationError

import GetPatientInfo
import WeightUtil

class BabyForm(Form):
    #values = {}
    #values['newborn_family_name_value'] = StringField()
    CODEFILE = "FHIR_resource_codes_1.txt"
    codes = GetPatientInfo.getCODETABLE(file=CODEFILE, page='baby')

    submit = SubmitField("Save and Next")

    fields = ['newborn_family_name',
              'newborn_first_name',
              'birth_weight',
              'birth_weight_grams',
              'birth_weight_lbs',
              'birth_weight_ozs',
              'apgar10m_score',
              'apgar5m_score',
              'apgar1m_score']

    for f in fields:
        field = codes[f]
        comm = f + " = "
        if field['datatype'].lower() == 'int':
            comm += "IntegerField('%s')" % field['desc']
        elif field['datatype'].lower() == 'string':
            comm += "StringField('%s')" % field['desc']
        elif field['datatype'].lower() == 'float':
            comm += "DecimalField('%s')" % field['desc']
        elif field['datatype'].lower() == 'boolean':
            comm += "BooleanField('%s')" % field['desc']
        print("Executing command: " + comm)
        exec (comm)

    mother_id = StringField("Mother ID", [validators.DataRequired()])


    def preload(self, pid):
        """
        codes = GetPatientInfo.getCODETABLE(page='baby')
        self.labels = {}
        values = {}
        for code in codes.values():
            datatype = code['datatype']
            if datatype == 'text':
                self.labels[code['name']] = code['desc']
            else:
                values[code['name']] = datatype
        
        self.newborn_family_name_value = StringField()
        self.newborn_first_name_value = StringField()
        self.apgar1m_score_value = IntegerField()
        self.apgar5m_score_value = IntegerField()
        self.apgar10m_score_value = IntegerField()
        self.birth_weight_grams_value = DecimalField()
        self.birth_weight_lbs_value = DecimalField()
        self.birth_weight_ozs_value = DecimalField()
        """


        self.mother_id.data = GetPatientInfo.getMotherID(pid)

        baby, medInfo = GetPatientInfo.getPatientMedical(pid=pid, codes=self.codes)
        if baby == None:
            return
        if baby.name[0].family != None:
            self.newborn_family_name.data = baby.name[0].family
            #self.values['newborn_family_name_value.data'] = baby.name[0].family
        if baby.name[0].given[0] != None:
            self.newborn_first_name.data = baby.name[0].given[0]

        value, unit = GetPatientInfo.getMedInfoValue(medInfo, "apgar1m_score")
        if value != None:
            self.apgar1m_score.data = value
        value, unit = GetPatientInfo.getMedInfoValue(medInfo, "apgar5m_score")
        if value != None:
            self.apgar5m_score.data = value
        value, unit = GetPatientInfo.getMedInfoValue(medInfo, "apgar10m_score")
        if value != None:
            self.apgar10m_score.data = value

        value, unit = GetPatientInfo.getMedInfoValue(medInfo, "birth_weight")
        if value != None:
            vGrams, vLbs, vOzs = convertWeight(float(value), unit)
            self.birth_weight_grams.data = vGrams
            self.birth_weight_lbs.data = vLbs
            self.birth_weight_ozs.data = vOzs

        #self.motherid = GetPatientInfo.getMotherID(pid)
        #self.mother_id = '<input type="hidden" name="mother_id" value="%s">' %self.motherid
        self.mother_id.data = GetPatientInfo.getMotherID(pid)




