#from flask_wtf import Form
from flask.ext.wtf import Form
from wtforms import IntegerField, SubmitField, TextAreaField, SelectField, StringField, TextField, DecimalField
from wtforms import validators, ValidationError

import GetPatientInfo
import test3

class BabyForm(Form):
    #values = {}
    #values['newborn_family_name_value'] = StringField()

    submit = SubmitField("Save and Next")
    newborn_family_name_value = StringField()
    newborn_first_name_value = StringField()
    apgar1m_score_value = IntegerField()
    apgar5m_score_value = IntegerField()
    apgar10m_score_value = IntegerField()
    birth_weight_grams_value = DecimalField()
    birth_weight_lbs_value = DecimalField()
    birth_weight_ozs_value = DecimalField()



    def preload(self, pid):
        codes = GetPatientInfo.getCODETABLE(page='baby')
        self.labels = {}
        values = {}
        for code in codes.values():
            datatype = code['datatype']
            if datatype == 'text':
                self.labels[code['name']] = code['desc']
            else:
                values[code['name']] = datatype
        """
        self.newborn_family_name_value = StringField()
        self.newborn_first_name_value = StringField()
        self.apgar1m_score_value = IntegerField()
        self.apgar5m_score_value = IntegerField()
        self.apgar10m_score_value = IntegerField()
        self.birth_weight_grams_value = DecimalField()
        self.birth_weight_lbs_value = DecimalField()
        self.birth_weight_ozs_value = DecimalField()
        """



        baby, medInfo = GetPatientInfo.getPatientMedical(pid=pid)
        if baby.name[0].family != None:
            self.newborn_family_name_value.data = baby.name[0].family
            #self.values['newborn_family_name_value.data'] = baby.name[0].family
        if baby.name[0].given[0] != None:
            self.newborn_first_name_value.data = baby.name[0].given[0]

        value, unit = GetPatientInfo.getMedInfoValue(medInfo, "apgar1m_score_value")
        if value != None:
            self.apgar1m_score_value.data = value
        value, unit = GetPatientInfo.getMedInfoValue(medInfo, "apgar5m_score_value")
        if value != None:
            self.apgar5m_score_value.data = value
        value, unit = GetPatientInfo.getMedInfoValue(medInfo, "apgar10m_score_value")
        if value != None:
            self.apgar10m_score_value.data = value

        value, unit = GetPatientInfo.getMedInfoValue(medInfo, "birth_weight_value")
        if value != None:
            vGrams, vLbs, vOzs = convertWeight(float(value), unit)
            self.birth_weight_grams_value.data = vGrams
            self.birth_weight_lbs_value.data = vLbs
            self.birth_weight_ozs_value.data = vOzs

        self.motherid = GetPatientInfo.getMotherID(pid)

def convertWeight(value, unit):
    unit = unit.lower()
    if unit == 'grams' or unit == 'gram':
        vGrams = value
    elif unit == 'kilograms' or unit == 'kgs' or unit == 'kg':
        vGrams = value * 1000
    elif unit == 'pounds' or unit == 'pound' or unit == 'lbs' or unit == 'lb':
        vGrams = value * 453.6
    else:
        print("invalid weight unit: " % unit)
        vGrams = 0
    vOzs = vGrams / 453.6 * 16
    vLbs = int(vOzs / 16)
    vOzs = int(vOzs) - vLbs * 16
    return (vGrams, vLbs, vOzs)

def validateWeigth(vGrams, vLbs, vOzs, fixed):
    """
    if fixed == 1, only vGrams is valid, calculate vLbs and vOzs
    if fixed == 2, vLbs and vOzs are valid, calculate vGrams
    :param vGrams:
    :param vLbs:
    :param vOzs:
    :param fixed:
    :return:
    """
    if fixed == 1:
        vOzs = vGrams / 453.6
        vLbs = int(vOzs / 16)
        vOzs = int(vOzs) - vLbs * 16
        return (vGrams, vLbs, vOzs)
    elif fixed == 2:
        vGrams = int((vLbs * 16 + vOzs) * 453.6)
        return (vGrams, vLbs, vOzs)
    else:
        print("Not valid fixed weight values")
        return (vGrams, vLbs, vOzs)





