from flask import Flask, render_template
import requests
import json
from collections import defaultdict
from datetime import date, datetime
from time import strftime

# Fetch data from API endpoint, return result as a dictionary
def get_data(endpoint):
  URL = 'https://gbfs.urbansharing.com/oslobysykkel.no/' + endpoint
  PARAMS = { 'headers':'Client-Identifier: are3k-codetest'}
  r = requests.get(url = URL, params = PARAMS)
  response = r.json()
  return response

# fetch necessary data and merge to the finished dictionary of stations
# with statuses
def create_list():
  # create emtpy dictionaries to hold the API data
  stations = {}
  statuses = {}
  
  # create empty list to hold display data
  station_status = []
  
  # fetch data from API, return ERROR if fail
  try: 
    stations_data = get_data('station_information.json')
  except:
    error = {"ERROR":"Cannot fetch station information."} 
    return error
  try: 
    statuses_data = get_data('station_status.json')
  except:
    error = {"ERROR":"Cannot fetch station status."} 
    return error
  
  # create dictionaries from both datatypes, using station_id 
  # as common key
  for station in stations_data["data"]["stations"]:
    stations[station["station_id"]] = station
  
  for status in statuses_data["data"]["stations"]:
    statuses[status["station_id"]] = status
  
  # create list containing only data to display
  for station in stations:
    if station in statuses:
      # if a station is not in use, don't list it
      if not statuses[station]["is_installed"]:
        break
      
      # if a station is closed for renting, set available bikes to zero
      if not statuses[station]["is_renting"]:
        free_bikes = 0
      else:
        free_bikes = statuses[station]["num_bikes_available"]
      
      # if a station is closed for returning, 
      # set available docks to zero
      if not statuses[station]["is_renting"]:
        free_docks = 0
      else:
        free_docks = statuses[station]["num_docks_available"]

      this_station_status = {
        "name":stations[station]["name"],
        "address":stations[station]["address"],
        "latitude":stations[station]["lat"],
        "longitude":stations[station]["lon"],
        "capacity":stations[station]["capacity"],
        "bikes_available":free_bikes,
        "docks_available":free_docks,
        "is_installed":statuses[station]["is_installed"],
        }
    station_status.append(this_station_status)
  
  # return list sorted by station name
  station_status.sort(key=lambda x: x['name'], reverse=False)
  return station_status
  
app = Flask(__name__)

@app.route("/")
def hello_world():
  # create the combined list of station and status data
  station_status = create_list()

  # set and format a time to display when status was fetched
  now = datetime.now()
  now = now.strftime("%b %d %Y %H:%M:%S")

  # render the web page
  if len(station_status) > 1:
    return render_template('cycleupdate.html', station_status=station_status, now=now)
  else:
    return render_template('cycleupdate_e.html', error_message=station_status, now=now)