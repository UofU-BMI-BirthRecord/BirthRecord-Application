#from flask_wtf import Form
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, TextAreaField, SelectField, StringField, TextField
from wtforms import DecimalField, BooleanField, HiddenField
from wtforms import validators, ValidationError

import GetPatientInfo
from WeightUtil import *
import easygui
import json

class MotherForm(FlaskForm):
    #values = {}
    #values['newborn_family_name_value'] = StringField()
    CODEFILE = "FHIR_resource_codes_1.txt"
    codes = GetPatientInfo.getCODETABLE(file=CODEFILE, page='mother')

    temp = BooleanField('Hi')

    #print(json.dumps(codes, indent=4))
    submit = SubmitField("Save and Report")

    fields = ['mother_family_name',
              'mother_first_name',
              'pre_weight',
              'pre_weight_grams',
              'pre_weight_lbs',
              'pre_weight_ozs',
              'delivery_weight',
              'delivery_weight_grams',
              'delivery_weight_lbs',
              'delivery_weight_ozs',
              'weight_gain',
              'weight_gain_grams',
              'weight_gain_lbs',
              'weight_gain_ozs',
              'pre_hypertension',
              'gestational_hypertension',
              'eclampsia',
              'pre_diabetes',
              'gestational_diabetes']

    for f in fields:
        field = codes[f]
        comm = f+" = "
        if field['datatype'].lower() == 'int':
            comm += "IntegerField('%s')" % field['desc']
        elif field['datatype'].lower() == 'string':
            comm += "StringField('%s')" % field['desc']
        elif field['datatype'].lower() == 'float':
            comm += "DecimalField('%s', [validateWeightInputs])" % field['desc']
        elif field['datatype'].lower() == 'boolean':
            comm += "BooleanField('%s')" % field['desc']
        print("Executing command: "+ comm)
        exec(comm)




    def preload(self, pid):



        mother, medInfo = GetPatientInfo.getPatientMedical(pid=pid, codes=self.codes)
        if mother.name[0].family != None:
            self.mother_family_name.data = mother.name[0].family
            #self.values['newborn_family_name_value.data'] = mother.name[0].family
        if mother.name[0].given[0] != None:
            self.mother_first_name.data = mother.name[0].given[0]

        print(json.dumps(medInfo, indent=4))
        print(self.codes['pre_weight'])
        '''
        value, unit = GetPatientInfo.getMedInfoValue(medInfo, "apgar1m_score_value")
        if value != None:
            self.apgar1m_score_value.data = value
        value, unit = GetPatientInfo.getMedInfoValue(medInfo, "apgar5m_score_value")
        if value != None:
            self.apgar5m_score_value.data = value
        value, unit = GetPatientInfo.getMedInfoValue(medInfo, "apgar10m_score_value")
        if value != None:
            self.apgar10m_score_value.data = value
        '''

        value1, unit = GetPatientInfo.getMedInfoValue(medInfo, "pre_weight")
        print(value1, unit)
        if value1 != None:
            vGrams, vLbs, vOzs = convertWeight(float(value1), unit)
            self.pre_weight_grams.data = vGrams
            self.pre_weight_lbs.data = vLbs
            self.pre_weight_ozs.data = vOzs

        value2, unit = GetPatientInfo.getMedInfoValue(medInfo, "delivery_weight")
        print(value2, unit)
        if value2 != None:
            vGrams, vLbs, vOzs = convertWeight(float(value2), unit)
            self.delivery_weight_grams.data = vGrams
            self.delivery_weight_lbs.data = vLbs
            self.delivery_weight_ozs.data = vOzs

        if value1 != None and value2 != None:
            (vG, vL, vO) = weightDifference(self.pre_weight_grams.data, self.pre_weight_lbs.data, self.pre_weight_ozs.data,
                                            self.delivery_weight_grams.data, self.delivery_weight_lbs.data,
                                            self.delivery_weight_ozs.data)
            self.weight_gain_grams.data = vG
            self.weight_gain_lbs.data = vL
            self.weight_gain_ozs.data = vO

        value, unit = GetPatientInfo.getMedInfoValue(medInfo, "pre_hypertension")
        if value != None:
            print(value, unit)
            self.pre_hypertension.data = value

        value, unit = GetPatientInfo.getMedInfoValue(medInfo, "gestational_hypertension")
        if value != None:
            print(value, unit)
            self.gestational_hypertension.data = value

        value, unit = GetPatientInfo.getMedInfoValue(medInfo, "eclampsia")
        if value != None:
            print(value, unit)
            self.eclampsia.data = value

        value, unit = GetPatientInfo.getMedInfoValue(medInfo, "pre_diabetes")
        if value != None:
            print(value, unit)
            self.pre_diabetes.data = value

        value, unit = GetPatientInfo.getMedInfoValue(medInfo, "gestational_diabetes")
        if value != None:
            print(value, unit)
            self.gestational_diabetes.data = value

    def validateWeightInputs(form, field):
        """
        Try to validate weight inputs, but seems not working for
        :param field:
        :return:
        """
        return validWeight(form.pre_weight_grams.data, form_pre_weight_lbs.data, form.pre_weight_ozs.data) and \
               validWeight(form.delivery_weight_grams.data, form_delivery_weight_lbs.data, form.delivery_weight_ozs.data) and \
               validWeight(form.weight_gain_grams.data, form_weight_gain_lbs.data, form.weight_gain_ozs.data)


        #self.motherid = GetPatientInfo.getMotherID(pid)
        #self.mother_id = '<input type="hidden" name="mother_id" value="%s">' %self.motherid
