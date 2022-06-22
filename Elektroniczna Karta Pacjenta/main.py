import streamlit as st
import database as db
import datetime as dt
import charts

cont = st.container()

patients = db.getAllPatients()

with st.sidebar:
    f_name = st.text_input('Family name', '')
    buttons = []
    for pat in patients:
        if (f_name != '' and f_name.upper() not in pat['name'][0]['family'].upper()):
            continue
        name = ''
        if ('given' in pat['name'][0]):
            for giv in pat['name'][0]['given']:
                name += giv + ' '
        if ('family' in pat['name'][0]):
            name += pat['name'][0]['family']
        buttons.append(st.button(name))

with st.spinner('Fetching data...'):        
    for i, button in enumerate(buttons):
        if (button):
            db.active = i
    if(db.active != -1):
        pat = patients[db.active]
        name = ''
        if ('prefix' in pat['name'][0]):
            for pref in pat['name'][0]['prefix']:
                name += pref + ' '
        if ('given' in pat['name'][0]):
            for giv in pat['name'][0]['given']:
                name += giv + ' '
        if ('family' in pat['name'][0]):
            name += pat['name'][0]['family']
        cont.title(name)
        cont.markdown('**Gender:** ' + pat['gender'])
        cont.markdown('**Birth date:** ' + pat['birthDate'])
        cont.markdown('**Identifier:** ' + pat['identifier'][0]['value'])
        col1, col2 = cont.columns(2)
        radSwitch = col1.radio('Information', ('Observations', 'Medications'))
        date1 = col2.date_input('Starting', value=dt.date(2000,1,1))
        date2 = col2.date_input('Ending')
        if(radSwitch == 'Observations'):
            select = col1.selectbox('Observation type', db.options)
            obrvs = db.getObservation(pat['id'], date1, date2, select)
            if(not obrvs):
                cont.markdown('# Nothing to show :(')
            else:
                cont.markdown('# Observations')
                cont.markdown(db.formatObservations(obrvs), unsafe_allow_html=True)
                if (select != 'All'):
                    x, y, lab = charts.genChartData(obrvs)
                    #print(x, y)
                    cont.write('')
                    cont.bokeh_chart(charts.makeChart(x, y, lab))
        elif(radSwitch == 'Medications'):
            select = col1.selectbox('Observation type', '')
            meds = db.getMedicine(pat['id'], date1, date2)
            if(not meds):
                cont.markdown('# Nothing to show :(')
            else:
                cont.markdown('# Medications')
                cont.markdown(db.formatMedications(meds), unsafe_allow_html=True)
    else:
        cont.markdown('# No patient selected. Use the sidebar menu to the left!')






    
