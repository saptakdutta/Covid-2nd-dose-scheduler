import numpy as np
import pandas as pd
import argparse
from pathlib import Path

#Set up command line arguments for latitude/longitude
parser = argparse.ArgumentParser(description="""This tool reads a csv containing client info and determines what timespan we run the Scheduler for""")
parser.add_argument('-cfg', '--config', default = 'Clients-dev.csv',
                      help= 'Points to the CSV storing client data',
                      type = str)

#Parse arguments 
args = parser.parse_args()
clients_file = args.config

#Set path
cwd = Path.cwd()
path = cwd.__str__()

clients = pd.read_csv(clients_file)
clients['Search spots before'] = pd.to_datetime(clients['Search spots before'])
clients = clients.sort_values(by='Search spots before')

print(clients)
