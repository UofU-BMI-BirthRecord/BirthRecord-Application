def convertWeight(value, unit):
    unit = unit.lower()
    if unit == 'grams' or unit == 'gram':
        vGrams = int(value)
    elif unit == 'kilograms' or unit == 'kgs' or unit == 'kg':
        vGrams = int(value * 1000)
    elif unit == 'pounds' or unit == 'pound' or unit == 'lbs' or unit == 'lb':
        vGrams = int(value * 453.6)
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


def weightDifference(vG1, vL1, vO1, vG2, vL2, vO2):
    """
    Get the difference as weight2 - weight2
    :param vG1:
    :param vL1:
    :param vO1:
    :param vG2:
    :param vL2:
    :param vO2:
    :return:
    """
    vG = vG1 - vG2
    vL = vL1 - vL2
    vO = vO1 - vO2
    return (vG, vL, vO)

def validWeight(vG, vL, vO):
    if vG == None and vL == None and vO == None:
        return True
    if vG == None or vL == None or vO == None:
        return False
    # Now vG, vL and vO are numbers
    L, O = validateWeigth(vG, vL, vO, 1)
    if (abs(L - vL) < 0.01) and (abs(O - vO) < 0.01):
        return True
    else:
        raise ValidationError('Inconsistent grams vs lbs and ozs')

def validateWeightInputs(form, field):
    return validWeight(form.pre_weight_grams.data, form.pre_weight_lbs.data, form.pre_weight_ozs.data) and \
           validWeight(form.delivery_weight_grams.data, form.delivery_weight_lbs.data, form.delivery_weight_ozs.data) and \
           validWeight(form.weight_gain_grams.data, form.weight_gain_lbs.data, form.weight_gain_ozs.data)
