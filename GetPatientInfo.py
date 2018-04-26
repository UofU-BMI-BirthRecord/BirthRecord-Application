from fhirclient import client
import json
import requests
import dateutil.parser
import requests
import datetime
import pytz
import fhirclient.models.patient as p
import fhirclient.models.bundle as b
import fhirclient.models.procedure as prod
import fhirclient.models.observation as ob
import fhirclient.models.condition as con
import fhirclient.models.encounter as enc
import csv

settings = {
    'app_id': 'my_web_app',
    'api_base': 'https://api-v5-stu3.hspconsortium.org/DBMIBC/open/'
}
smart = client.FHIRClient(settings=settings)

pid = "cf-1522104153916"
patient = p.Patient.read(pid, smart.server)
print(patient)

bundle = requests.get('https://api-v5-stu3.hspconsortium.org/DBMIBC/open/Patient?birthdate>=2018-01-01')  # Not working
data = json.loads(bundle.text)
print(data)

CODES = {}
CODES['weight'] = {'system': "http://loinc.org", "code": "LP18015-5"}
CODES['height'] = {'system': "http://loinc.org", "code": "8302-2"}
CODES['birthWeigth'] = {'system': "http://loinc.org", "code": "8339-4"}
CODES['apgarScore'] = {'system': "http://loinc.org", "code": "9274-2"}



def getNextURL(links):
    """
    Helper function for getAllPatients, get the next url so we can loop to get all resources
    :param links:
    :return:
    """
    if type(links) == list:
        for link in links:
            if link.relation == 'next':
                return link.url
    return None

def getAllRecentBabies(server=smart.server, targetnumber=1000, bornInDays=500):
    bundle = b.Bundle.read_from('Patient', server)
    targetGap = datetime.timedelta(days=bornInDays)
    res = []
    while len(res) < targetnumber:
        if bundle is None or bundle.entry is None:
            return res
        for entry in bundle.entry:
            pt = entry.resource
            if pt.name is None:
                name = "Name None"
            else:
                name = pt.name[0].as_json()
            if pt.birthDate is None:
                dob = "DOB None"
            else:
                dob = pt.birthDate.date

            print(len(res), pt.id, name, dob)
            if dob == 'DOB None':
                continue

            if type(dob) == datetime.date:
                gap = datetime.date.today() - dob
                #stop =  > targetGap
            if type(dob) == datetime.datetime:
                gap =datetime.datetime.now(tz=pytz.utc) - dob  # Make now as a datetime timezone-aware,
                #stop =  > targetGap
            #print("stop is ", stop)

            if gap > targetGap:
                continue

            print("Add patient: ", name, dob)

            res.append(pt)

        nexturl = getNextURL(bundle.link)
        if nexturl is None:
            return res
        data = requests.get(nexturl)     # request from a URL, not by fhirclient
        if data is None or data.text is None:
            return res
        bundle = b.Bundle(jsondict=json.loads(data.text))


def getRecentBabies(bornInDays=10, server=smart.server):
    today = datetime.date.today()
    targetDay = today - datetime.timedelta(days=bornInDays)
    # default count per page is 10 and the maximum count is 50 to prevent system overload by the FHIR server.
    # If there are more than 50 babies born, special treatment is need to read page by page.
    search = p.Patient.where(struct={'birthdate': ">%s" % targetDay, '_count': '50', '_sort': '-birthdate'})
    patients = search.perform_resources(smart.server)
    print(len(patients))
    return patients


CODEFILE = "FHIR_resource_codes.txt"
def getCODETABLE(file=CODEFILE, page=''):
    codeTable = {}
    with open(file) as f:
        reader = csv.DictReader(f, delimiter='\t')
        if page == '':
            for row in reader:
                if row['page'] != '':
                    codeTable[row['name']] = row
        else:
            for row in reader:
                if row['page'] == page:
                    codeTable[row['name']] = row

    return codeTable
CODETABLE = getCODETABLE(CODEFILE)


def getMedicalInfo(resource, type, codes):
    r_code = resource.code.coding
    for code in codes:
        c = codes[code]
        if c['resource'] != type:
            continue
        #print("try: ", c)
        for rc in r_code:
            #print(rc.as_json())
            if rc.code == c['code'] and rc.system == c['system']:
                #print (c['name'], resource.as_json())
                return (c['name'], resource.as_json())
    return (None, None)

def getPatientMedical(pid, server=smart.server, codes=CODETABLE):
    medInfo = {}
    search = p.Patient.where(struct={'_id': pid})
    patients = search.perform_resources(server)
    if len(patients) > 1:
        print("Too many patients")
    if len(patients) < 1:
        print("no patient!")
        return (None, medInfo)
    pt = patients[0]
    search = ob.Observation.where(struct={'subject': pid})
    conditions = search.perform_resources(smart.server)
    #print(codes[''])
    for condition in conditions:
        name, res = getMedicalInfo(condition, 'obs', codes)
        if name != None:
           medInfo[name] = res
    search = con.Condition.where(struct={'subject': pid})
    conditions = search.perform_resources(smart.server)
    #print(codes[''])
    for condition in conditions:
        name, res = getMedicalInfo(condition, 'condition', codes)
        if name != None:
           medInfo[name] = res
    return pt, medInfo


def getMedInfoValue(medInfo, name):
    if name not in medInfo:
        return None, None
    info = medInfo[name]
    #print(info)
    if info['resourceType'] == 'Observation':
        try:
            value = info['valueQuantity']['value']
        except:
            value = None
        try:
            unit = info['valueQuantity']['unit']
        except:
            unit = None
        return value, unit
    else:
        return True, None



def getMotherID(pid):
    """
    From a child's pid, search its birth Encounter which is a part of the mother's encount,
    find the mother's pid
    :param pid:
    :return:
    """
    search = enc.Encounter.where(struct={'subject': pid})
    encounters = search.perform_resources(smart.server)
    motherEncounter = None
    try:
        for encounter in encounters:
            if encounter.reason[0].coding[0].code == '169836001' \
                    and encounter.reason[0].coding[0].system == 'http://snomed.info/sct' \
                    and encounter.partOf != None:
                # print(encounter.partOf.reference.split('/')[1])
                motherEncounter = encounter.partOf.reference.split('/')[1]
    except:
        motherEncounter = None
    if motherEncounter == None:
        return None
    search = enc.Encounter.where(struct={'_id': motherEncounter})
    encounters = search.perform_resources(smart.server)
    motherID = encounters[0].subject.reference.split('/')[1]
    return motherID



#today = datetime.date.today()
#print(today)
#yesterday = today - datetime.timedelta(days=30)
#print(yesterday)
#res = getRecentBabies()
#res2 = getAllRecentBabies()
#print(res[0].as_json())
#print(res2[0].as_json())


#newbabies = getAllRecentBabies(smart.server, 100, 10)

#for baby in newbabies:
#    print ("%s, %s" %(baby.name[0].given[0].encode('utf-8'), baby.name[0].family.encode('utf-8')))
#    print(baby.birthDate.date)