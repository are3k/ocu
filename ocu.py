from flask import Flask, render_template
import requests
import json
from collections import defaultdict

# Fetch data from API endpoint, return result as a json object
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
    return "ERROR: Cannot fetch station information. Try refreshing page"
  try: 
    statuses_data = get_data('station_status.json')
  except:
    return "ERROR: Cannot fetch station status. Try refreshing page"
  
  # create dictionaries from both datatypes, using station_id as common key
  for station in stations_data["data"]["stations"]:
    stations[station["station_id"]] = station
  
  for status in statuses_data["data"]["stations"]:
    statuses[status["station_id"]] = status
  
  # create list containing only data to display
  for station in stations:
    if station in statuses:
      this_station_status = [
        stations[station]["name"],
        stations[station]["address"],
        stations[station]["lat"],
        stations[station]["lon"],
        stations[station]["capacity"],
        statuses[station]["num_bikes_available"],
        statuses[station]["num_docks_available"],
        statuses[station]["is_installed"],
        statuses[station]["is_renting"],
        statuses[station]["is_returning"],
      ]
    station_status.append(this_station_status)
  # return list sorted by first column in station list
  station_status.sort()
  return station_status
  
app = Flask(__name__)

@app.route("/")
def hello_world():
  station_status = create_list()
  return render_template('cycleupdate.html', station_status=station_status)