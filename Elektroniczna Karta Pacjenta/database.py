from fhirpy import SyncFHIRClient
import datetime as dt

client = SyncFHIRClient('http://localhost:8080/baseR4')

active = -1

optionsDict = {
    'Body Height' : 'Body Height',
    'Pain Severity' : 'Pain severity - 0-10 verbal numeric rating [Score] - Reported',
    'Body Weight' : 'Body Weight',
    'Body Mass Index' : 'Body Mass Index',
    'Body mass index (BMI) [Percentile]' : 'Body mass index (BMI) [Percentile] Per age and gender',
    'Blood Pressure' : 'Blood Pressure',
    'Oral temperature' : 'Oral temperature',
    'Leukocytes [#/volume] in Blood' : 'Leukocytes [#/volume] in Blood by Automated count',
    'Erythrocytes [#/volume] in Blood' : 'Erythrocytes [#/volume] in Blood by Automated count',
    'Hemoglobin [Mass/volume] in Blood' : 'Hemoglobin [Mass/volume] in Blood',
    'Hematocrit [Volume Fraction] of Blood' : 'Hematocrit [Volume Fraction] of Blood by Automated count',
    'MCV [Entitic volume]' : 'MCV [Entitic volume] by Automated count',
    'MCH [Entitic mass]' : 'MCH [Entitic mass] by Automated count',
    'Erythrocyte distribution width [Entitic volume]' : 'Erythrocyte distribution width [Entitic volume] by Automated count',
    'Platelets [#/volume] in Blood' : 'Platelets [#/volume] in Blood by Automated count',
    'Platelet distribution width [Entitic volume] in Blood' : 'Platelet distribution width [Entitic volume] in Blood by Automated count',
    'Platelet mean volume [Entitic volume] in Blood' : 'Platelet mean volume [Entitic volume] in Blood by Automated count',
    'All' : 'All',
    'Tobacco smoking status NHIS' : 18,
    'MCHC [Mass/volume]' : 'MCHC [Mass/volume] by Automated count',
    'Glucose' : 'Glucose'
}

options = ('All', 'Body Height', 'Pain Severity', 'Body Weight', 'Body Mass Index',
           'Body mass index (BMI) [Percentile]', 'Blood Pressure', 'Oral temperature',
           'Leukocytes [#/volume] in Blood', 'Erythrocytes [#/volume] in Blood',
           'Hemoglobin [Mass/volume] in Blood', 'Hematocrit [Volume Fraction] of Blood',
           'MCV [Entitic volume]', 'MCH [Entitic mass]', 'MCHC [Mass/volume]', 'Erythrocyte distribution width [Entitic volume]',
           'Platelets [#/volume] in Blood', 'Platelet distribution width [Entitic volume] in Blood',
           'Platelet mean volume [Entitic volume] in Blood', 'Glucose')

def getAllPatients():
    return client.resources('Patient').elements('id','name','gender','birthDate','identifier').fetch_all()
    #resources = resources.search(name='Turcotte120')

def getObservation(id, dateFrom, dateTo, type):
    observations =  client.resources('Observation').elements('id','code','valueQuantity','effectiveDateTime','subject','component','valueCodeableConcept').sort('date').fetch_all()
    toRet = list()
    for obrv in observations:
        if(obrv['subject']['reference'].split('/')[1] == id):
            date = tuple(map(int, obrv['effectiveDateTime'].split('T')[0].split('-')))
            if(dt.date(date[0], date[1], date[2]) >= dateFrom and dt.date(date[0], date[1], date[2]) <= dateTo):
                if(optionsDict[type] == 'All' or obrv['code']['coding'][0]['display'] == optionsDict[type]):
                    toRet.append(obrv)
    return toRet

def getMedicine(id, dateFrom, dateTo):
    meds = client.resources('MedicationRequest').elements('id','medicationCodeableConcept','subject','authoredOn').fetch_all()
    toRet = list()
    for med in meds:
        if(med['subject']['reference'].split('/')[1] == id):
            date = tuple(map(int, med['authoredOn'].split('T')[0].split('-')))
            if(dt.date(date[0], date[1], date[2]) >= dateFrom and dt.date(date[0], date[1], date[2]) <= dateTo):
                toRet.append(med)
    return toRet

def formatObservations(observations):
    table = [f"|NO|OBSERVATION|DATE|","|--|--|--|"]
    for i, obrv in enumerate(observations):
        obr = '**' + obrv['code']['coding'][0]['display']
        if('valueQuantity' in obrv):
            if(obrv['valueQuantity']['unit'][0] != '{'):
                obr += ':**<br>' + (str(obrv['valueQuantity']['value']) + ' ' + obrv['valueQuantity']['unit'])
            else:
                obr += ':**<br>' + (str(obrv['valueQuantity']['value']))
        elif('component' in obrv):
            obr += ':**'
            for com in obrv['component']:
                obr += '<br>**' + (com['code']['coding'][0]['display'])
                if(com['valueQuantity']['unit'][0] != '{'):
                    obr += ':**<br>' + (str(com['valueQuantity']['value']) + ' ' + com['valueQuantity']['unit'])
                else:
                    obr += ':**<br>' + (str(com['valueQuantity']['value']))
        else:
            obr += ':**<br>' + (obrv['valueCodeableConcept']['coding'][0]['display'])
        date = obrv['effectiveDateTime'].split('T')
        table.append(f'|{i+1}|{obr}|{date[0]}<br>{date[1]}|')
    table = '\n'.join(table)
    return table

def formatMedications(medications):
    table = [f"|NO|MEDICATION|DATE|","|--|--|--|"]
    for i, meds in enumerate(medications):
        med = meds['medicationCodeableConcept']['coding'][0]['display']
        date = meds['authoredOn'].split('T')
        table.append(f'|{i+1}|{med}|{date[0]}<br>{date[1]}|')
    table = '\n'.join(table)
    return table

'''for pat in getAllPatients():
    name = ''
    if ('prefix' in pat['name'][0]):
        for pref in pat['name'][0]['prefix']:
            name += pref + ' '
    if ('given' in pat['name'][0]):
        for giv in pat['name'][0]['given']:
            name += giv + ' '
    if ('family' in pat['name'][0]):
        name += pat['name'][0]['family']
    print(name)
    print(pat['gender'])
    print(pat['birthDate'])
    print(pat['identifier'][0]['value'])
    id = pat['id']

print(id)
for obrv in getObservation(id):
    print(obrv['id'])
    print(obrv['code']['coding'][0]['display'])
    if('valueQuantity' in obrv):
        if(obrv['valueQuantity']['unit'][0] != '{'):
            print(str(obrv['valueQuantity']['value']) + ' ' + obrv['valueQuantity']['unit'])
        else:
            print(str(obrv['valueQuantity']['value']))
    elif('component' in obrv):
        for com in obrv['component']:
            print(com['code']['coding'][0]['display'])
            if(com['valueQuantity']['unit'][0] != '{'):
                print(str(com['valueQuantity']['value']) + ' ' + com['valueQuantity']['unit'])
            else:
                print(str(com['valueQuantity']['value']))
    else:
        print(obrv['valueCodeableConcept']['coding'][0]['display'])
        
    date = obrv['effectiveDateTime'].split('T')
    print(date[0] + ' ' + date[1].split('.')[0])
    
for med in getMedicine(id):
    print(med['id'])
    print(med['medicationCodeableConcept']['coding'][0]['display'])
    date = med['authoredOn'].split('T')
    print(date[0] + ' ' + date[1])'''