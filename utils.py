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
