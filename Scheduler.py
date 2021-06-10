
import numpy as np
import pandas as pd
import requests as req
import json as json
from pathlib import Path
from dateutil import parser

cwd = Path.cwd()
path = cwd.__str__()

with open(path+'/Config.json') as f:
  config_data = json.load(f)

url = 'https://api.covaxonbooking.ca/public/appointments/get'
headers = {
    'authority': 'api.covaxonbooking.ca',
    'accept': 'application/json',
    'origin': 'https://vaccine.covaxonbooking.ca',
    'referer': 'https://vaccine.covaxonbooking.ca/'
}
payload = {
    'confirmationCode': config_data['ConfirmationCode'],
    'email': config_data['Email'],
    'url': 'https://vaccine.covaxonbooking.ca/manage'
}
ex = req.post(url, headers=headers, json= payload)
rtrn = ex.json()
booking2 = rtrn['appointments'][1]
dose_2_dttime = parser.parse(booking2['start'])

file = open("Vax_Sched.txt","w")

search_url = 'https://api.covaxonbooking.ca/public/locations/search'
headers = {
    'authority': 'api.covaxonbooking.ca',
    'accept': 'application/json',
    'origin': 'https://vaccine.covaxonbooking.ca',
    'referer': 'https://vaccine.covaxonbooking.ca/'
}
payload = {
    "location":{"lat":45.3640192,"lng":-75.710464},
    "fromDate":"2021-06-09",
    "vaccineData":"WyJhMWQ0dDAwMDAwMDFqZGtBQUEiXQ==",
    "doseNumber":2,
    "limit":20,
    "cursor":"",
    "locationType":"CombinedBooking",
    "url":"https://vaccine.covaxonbooking.ca/manage/location-select"}
ex = req.post(search_url, headers=headers, json= payload)
search = ex.json()

print('Current boking date: ', str(dose_2_dttime))

line0 = 'Current boking date: ', str(dose_2_dttime)
line0 = str(line0)
file.write(line0+ '\n')
file.write('\n')

for i in range(len(search['locations'])):
    location_ID = search['locations'][i]['extId']
    availability_url = 'https://api.covaxonbooking.ca/public/locations/'+location_ID+'/availability'
    headers = {
        'authority': 'api.covaxonbooking.ca',
        'accept': 'application/json',
        'origin': 'https://vaccine.covaxonbooking.ca',
        'referer': 'https://vaccine.covaxonbooking.ca/'
    }
    payload = {'startDate':'2021-09-25',
            'endDate':'2021-11-24',
            'vaccineData':'WyJhMWQ0dDAwMDAwMDFqZGtBQUEiXQ==',
            'doseNumber':2,
            'url':'https://vaccine.covaxonbooking.ca/manage/appointment-select'}
    ex = req.post(availability_url, headers=headers, json= payload)
    availability = ex.json()
    availability = pd.DataFrame(availability['availability'])
    
    suitable_avail = pd.to_datetime(availability['date'][availability['available'] == True])
    suitable_avail = suitable_avail.reset_index()['date']
    
    #Console output
    print('Name:', search['locations'][i]['name'])
    print('Location:', search['locations'][i]['displayAddress']) 
    print('extId:', search['locations'][i]['extId']) 
    print('# of available days:', len(availability['date'][availability['available'] == True])) 
    print('suitable days:')
    
    #Text output
    line1 = 'Name:', search['locations'][i]['name']
    line1 = str(line1)
    file.write(line1+ '\n')
    line2 = 'Location:', search['locations'][i]['displayAddress']
    line2 = str(line2)
    file.write(line2+ '\n')
    line3 = 'extId:', search['locations'][i]['extId']
    line3 = str(line3)
    file.write(line3+ '\n')
    line4 = '# of available days:', len(availability['date'][availability['available'] == True])
    line4 = str(line4)
    file.write(line4 + '\n')
    line5 = 'suitable days'
    file.write(line5+'\n')
    
    #Only print the suitable days (i.e. days before your already booked appointment)
    for j in range(len(suitable_avail)):
        if (suitable_avail[j] < pd.to_datetime(config_data['PreferredAptDate'])):
            print(suitable_avail[j])
            
            line6 = suitable_avail[j]
            line6 = str(line6)
            file.write(line6 + '\n')
    print('\n')
    
    file.write(' '+'\n')

file.close()
# %%
