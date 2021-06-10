#Libraries
import numpy as np
import pandas as pd
import requests as req
import json as json
from pathlib import Path
from dateutil import parser as par
from datetime import datetime
import argparse

#Set up command line arguments for latitude/longitude
parser = argparse.ArgumentParser(description="""This tool is envisoned to be a server side 
                                 application that sends users notifications about available
                                 vaccine slots at regular daily intervals. This removes the
                                 need for a user to manually check the vaccine rebooking site 
                                 for dosage slots.""")
parser.add_argument('-lat', '--latitude', default = 45.3640192,
                      help= 'Geological latitude, defaults to downtown Ottawa',
                      type = float)
parser.add_argument('-lng', '--longitude', default = -75.710464,
                      help= 'Geological longitude, defaults to downtown Ottawa',
                      type = float)
#Parse arguments 
args = parser.parse_args()
latitude = args.latitude
longitude = args.longitude

print('Given latitude: ',latitude,' Given longitude: ',longitude)

#Set path
cwd = Path.cwd()
path = cwd.__str__()

#Read in the cfg file. change this to Config instead of Config-dev on local
with open(path+'/Config-dev.json') as f:
  config_data = json.load(f)

#This section looks at existing appointment details
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
dose_2_dttime = par.parse(booking2['start'])

file = open("Vax_Sched.txt","w")
#This section searches for locations close to the user in Ottawa
search_url = 'https://api.covaxonbooking.ca/public/locations/search'
headers = {
    'authority': 'api.covaxonbooking.ca',
    'accept': 'application/json',
    'origin': 'https://vaccine.covaxonbooking.ca',
    'referer': 'https://vaccine.covaxonbooking.ca/'
}
payload = {
    #!TODO allow users to pass latitude and longitude values to the tool instead of defaulting downtown 
    "location":{"lat":latitude,"lng":longitude},
    "fromDate":datetime.today().strftime('%Y-%m-%d'),
    "vaccineData":"WyJhMWQ0dDAwMDAwMDFqZGtBQUEiXQ==",
    "doseNumber":2,
    "limit":20,
    "cursor":"",
    "locationType":"CombinedBooking",
    "url":"https://vaccine.covaxonbooking.ca/manage/location-select"}
ex = req.post(search_url, headers=headers, json= payload)
search = ex.json()

print('Current dose 2 booking date: ', str(dose_2_dttime))
coordinates= 'Given latitude: ',latitude,' Given longitude: ',longitude
coordinates= str(coordinates)
file.write(coordinates+ '\n')

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
