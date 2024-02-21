from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for

from utils import (loadClubs, loadCompetitions, updateBookedPlaces,
                   initializeBookedPlaces, sortCompetitionsDate)


# def loadClubs():
#     with open('clubs.json') as c:
#         listOfClubs = json.load(c)['clubs']
#         return listOfClubs


# def loadCompetitions():
#     with open('competitions.json') as comps:
#         listOfCompetitions = json.load(comps)['competitions']
#         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()
pastCompetitions, presentCompetitions = sortCompetitionsDate(competitions)
placesBooked = initializeBookedPlaces(competitions, clubs)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    """Checks if the email address is correct, if email is false, error
    message displays a list of competitions.
    """
    try:
        club = [
            club for club in clubs if club['email'] == request.form['email']][0]
        return render_template(
            'welcome.html', club=club, pastCompetitions=pastCompetitions,
            presentCompetitions=presentCompetitions)
    except IndexError:
        if request.form['email'] == '':
            flash("Please enter your email.", 'error')
        else:
            flash("No account related to this email.", 'error')
        return render_template('index.html'), 401


@app.route('/book/<competition>/<club>')
def book(competition, club):
    # if foundClub is empty, it will be None instead of an error:
    foundClub = [c for c in clubs if c['name'] == club][0]

    try:
        # Find the competition with the given name
        foundCompetition = [
            c for c in competitions if c['name'] == competition][0]
        # Check if the competition is already over
        if datetime.strptime(foundCompetition['date'],
                             '%Y-%m-%d %H:%M:%S') < datetime.now():
            flash("This competition is over.", 'error')
            status_code = 400

        else:
            return render_template(
                'booking.html', club=foundClub, competition=foundCompetition)

    except IndexError:
        flash("Something went wrong-please try again", 'error')
        status_code = 404

    return render_template(
        'welcome.html', club=foundClub, pastCompetitions=pastCompetitions,
        presentCompetitions=presentCompetitions), status_code


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [
        c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]

    try:
        placesRequired = int(request.form['places'])

        if placesRequired > int(club['points']):
            flash("You don't have enough points.", 'error')

        elif placesRequired > int(competition['numberOfPlaces']):
            flash('Not enough places available.', 'error')

        elif placesRequired > 12:
            flash(
                "You can't book more than 12 places in a competition.", 'error'
            )

        else:
            try:
                updateBookedPlaces(
                    competition, club, placesBooked, placesRequired)
                competition[
                    'numberOfPlaces'] = int(
                        competition['numberOfPlaces']) - placesRequired
                club['points'] = int(club['points']) - (placesRequired)
                flash('Great-booking complete!')
                return render_template(
                    'welcome.html', club=club,
                    pastCompetitions=pastCompetitions,
                    presentCompetitions=presentCompetitions)

            except ValueError as errorMessage:
                flash(errorMessage, 'error')

    except ValueError:
        flash('Please enter a number between 0 and 12.', 'error')

    return render_template(
        'booking.html', club=club, competition=competition), 400


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
