import json
from datetime import datetime


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


def sortCompetitionsDate(comps):
    past = []
    present = []

    for comp in comps:
        compDate = datetime.strptime(comp['date'], '%Y-%m-%d %H:%M:%S')
        if compDate < datetime.now():
            past.append(comp)
        elif compDate >= datetime.now():
            present.append(comp)

    return past, present


def initializeBookedPlaces(comps, clubsList):
    places = []
    for comp in comps:
        for club in clubsList:
            places.append(
                {'competition': comp['name'], 'booked': [0, club['name']]})

    return places


def updateBookedPlaces(competition, club, placesBooked, placesRequired):
    for item in placesBooked:
        if item['competition'] == competition['name'] and item[
                'booked'][1] == club['name']:
            if item['booked'][0] + placesRequired <= 12:
                item['booked'][0] += placesRequired
                break
            else:
                raise ValueError(
                    "You can't book more than 12 places in a competition.")

    return placesBooked
