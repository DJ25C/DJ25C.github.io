from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import *
from datetime import datetime, timezone
from pytz import timezone
import requests

views = Blueprint('views', __name__)

# Define the limit date and time with the specified time zone
time_zone = timezone('America/Mexico_City')

LIMIT_DATE_WEEK_1_TNF = time_zone.localize(datetime(2023, 8, 1, 22, 40, 0))
LIMIT_DATE_WEEK_1 = time_zone.localize(datetime(2023, 8, 1, 22, 40, 0))
LIMIT_DATE_WEEK_2_TNF = time_zone.localize(datetime(2023, 8, 1, 22, 40, 0))
LIMIT_DATE_WEEK_2 = time_zone.localize(datetime(2023, 8, 1, 23, 50, 0))

def current_week_number_update():
    current_datetime = datetime.now(time_zone)
    # Year, Month, Day, Hour, Minute, Second
    limit_dates = {
        1: time_zone.localize(datetime(2023, 9, 14, 0, 0, 0)),
        2: time_zone.localize(datetime(2023, 9, 21, 0, 0, 0)),
        3: time_zone.localize(datetime(2023, 9, 28, 0, 0, 0)),
        4: time_zone.localize(datetime(2023, 10, 5, 0, 0, 0)),
        5: time_zone.localize(datetime(2023, 10, 12, 0, 0, 0)),
        6: time_zone.localize(datetime(2023, 10, 19, 0, 0, 0)),
        7: time_zone.localize(datetime(2023, 10, 26, 0, 0, 0)),
        8: time_zone.localize(datetime(2023, 11, 2, 0, 0, 0)),
        9: time_zone.localize(datetime(2023, 11, 9, 0, 0, 0)),
        10: time_zone.localize(datetime(2023, 11, 16, 0, 0, 0)),
        11: time_zone.localize(datetime(2023, 11, 23, 0, 0, 0)),
        12: time_zone.localize(datetime(2023, 11, 30, 0, 0, 0)),
        13: time_zone.localize(datetime(2023, 12, 7, 0, 0, 0)),
        14: time_zone.localize(datetime(2023, 12, 14, 0, 0, 0)),
        15: time_zone.localize(datetime(2023, 12, 21, 0, 0, 0)),
        16: time_zone.localize(datetime(2023, 12, 28, 0, 0, 0)),
        17: time_zone.localize(datetime(2024, 1, 5, 0, 0, 0)),
        18: time_zone.localize(datetime(2024, 1, 12, 0, 0, 0))
    }

    current_week_number = 1
    for week_number, limit_date in limit_dates.items():
        if current_datetime > limit_date:
            current_week_number = week_number + 1

    return current_week_number

def get_base_scores():
    current_week_number = current_week_number_update()
    return globals()[f'Week{current_week_number}_scores'].query.all()

def get_base_results():
    current_week_number = current_week_number_update()
    return globals()[f'Week{current_week_number}_results'].query.all()


@views.route('/', methods=['GET', 'POST'])
def home():
    base_scores = get_base_scores()
    base_results = get_base_results()
    news = News.query.all()
    teams = Teams.query.all()

    return render_template('home.html', user=current_user, base_scores=base_scores, base_results=base_results, news=news, teams=teams)


@views.route('/leaderboard')
@login_required
def leaderboard():
    base_scores = get_base_scores()
    base_results = get_base_results()
    leaderboard_data = Leaderboard.query.all()
    teams = Teams.query.all()

    return render_template('leaderboard.html', user=current_user, base_scores=base_scores, base_results=base_results, leaderboard_data=leaderboard_data, teams=teams)


@views.route("/week1")
@login_required
def week1():
    current_datetime = datetime.now(time_zone)
    base_scores = get_base_scores()
    base_results = get_base_results()
    teams = Teams.query.all()

    return render_template('week1.html', user=current_user, current_datetime=current_datetime, limit_date_TNF=LIMIT_DATE_WEEK_1_TNF, limit_date=LIMIT_DATE_WEEK_1, time_zone=time_zone, base_scores=base_scores, base_results=base_results, teams=teams)

@views.route('/week1-leaderboard')
@login_required
def week1_leaderboard():
    base_scores = get_base_scores()
    base_results = get_base_results()
    leaderboard_data = Leaderboard.query.order_by(Leaderboard.week1_points.desc()).all()
    week_picks = Week1_picks.query.all()
    week_results = Week1_results.query.all()
    teams = Teams.query.all()

    
    return render_template('week1_leaderboard.html', user=current_user, base_scores=base_scores, base_results=base_results, leaderboard_data=leaderboard_data, week_picks=week_picks, week_results=week_results, teams=teams)

@views.route('/save-week1-picks', methods=['POST'])
@login_required
def save_week1_form():
    current_datetime = datetime.now(time_zone)
    if request.method == 'POST':
        if current_datetime > LIMIT_DATE_WEEK_1:
            flash('La fecha límite para hacer picks de esta semana ha expirado.', category='error')
            return redirect(url_for('views.week1'))
        
        # Get the user object from current_user
        user = current_user

        # Iterate through the game picks
        for game_number in range(1, 17):
            # Construct the input name based on the game number
            input_name = f'week-1_game-{game_number}_winner'

            # Get the selected winner for the current game
            user_pick = request.form.get(input_name)
            if user_pick:
                # Extract the word between the second last "_" and last "-"
                split_values = user_pick.split('_')
                split_values2 = split_values[-2].split('-')
                if len(split_values2) >= 1:
                    selected_winner = split_values2[-1]
                split_values = user_pick.split('-')
                if len(split_values) >= 1:
                    selected_difference = int(split_values[-1])  # Extract the difference value
                else:
                    selected_winner = None
                    selected_difference = None

                # Check if the user already made a pick for the current game
                existing_pick = Week1_picks.query.filter_by(user=user, game_number=game_number).first()

                if existing_pick:
                    if selected_winner is not None and len(selected_winner) > 1:
                        # Overwrite the existing pick with the new selection
                        existing_pick.selected_winner = selected_winner
                        existing_pick.selected_difference = selected_difference
                        existing_pick.user_pick = user_pick
                else:
                    # Create a new instance of the Week1 model with the user, selected winner, and game number
                    week1_pick = Week1_picks(user=user, user_pick=user_pick, game_number=game_number, selected_winner=selected_winner, selected_difference=selected_difference)
                    # Add the new pick to the database
                    db.session.add(week1_pick)
            else:
                selected_winner = None
                selected_difference = None

                # Check if the user already made a pick for the current game
                existing_pick = Week1_picks.query.filter_by(user=user, game_number=game_number).first()

                if existing_pick:
                    existing_pick.selected_winner = selected_winner
                    existing_pick.selected_difference = selected_difference
                    existing_pick.user_pick = None

                else:
                    # Create a new instance of the Week1 model with the user, selected winner, and game number
                    week1_pick = Week1_picks(user=user, user_pick=None, game_number=game_number, selected_winner=selected_winner, selected_difference=selected_difference)
                    # Add the new pick to the database
                    db.session.add(week1_pick)

        # Commit all the picks to the database
        db.session.commit()

        # Optionally, you can redirect to another page or render a template
        flash('Tus picks se han guardado con éxito!', category='success')
        return redirect(url_for('views.week1'))

    return redirect(url_for('views.week1'))



@views.route("/week2")
@login_required
def week2():
    current_datetime = datetime.now(time_zone)
    base_scores = get_base_scores()
    base_results = get_base_results()
    teams = Teams.query.all()

    return render_template('week2.html', user=current_user, current_datetime=current_datetime, limit_date=LIMIT_DATE_WEEK_2, time_zone=time_zone, base_scores=base_scores, base_results=base_results, teams=teams)

@views.route('/week2-leaderboard')
@login_required
def week2_leaderboard():
    base_scores = get_base_scores()
    base_results = get_base_results()
    leaderboard_data = Leaderboard.query.order_by(Leaderboard.week2_points.desc()).all()
    week_picks = Week2_picks.query.all()
    week_results = Week2_results.query.all()
    teams = Teams.query.all()
    
    return render_template('week2_leaderboard.html', user=current_user, base_scores=base_scores, base_results=base_results, leaderboard_data=leaderboard_data, week_picks=week_picks, week_results=week_results, teams=teams)

@views.route('/save-week2-picks', methods=['POST'])
@login_required
def save_week2_form():
    current_datetime = datetime.now(time_zone)
    if request.method == 'POST':
        if current_datetime > LIMIT_DATE_WEEK_2:
            flash('La fecha límite para hacer picks de esta semana ha expirado.', category='error')
            return redirect(url_for('views.week2'))
        
        # Get the user object from current_user
        user = current_user

        # Iterate through the game picks
        for game_number in range(1, 17):
            # Construct the input name based on the game number
            input_name = f'week-2_game-{game_number}_winner'

            # Get the selected winner for the current game
            user_pick = request.form.get(input_name)
            if user_pick:
                # Extract the word between the second last "_" and last "-"
                split_values = user_pick.split('_')
                split_values2 = split_values[-2].split('-')
                if len(split_values2) >= 1:
                    selected_winner = split_values2[-1]
                split_values = user_pick.split('-')
                if len(split_values) >= 1:
                    selected_difference = int(split_values[-1])  # Extract the difference value
                else:
                    selected_winner = None
                    selected_difference = None

                # Check if the user already made a pick for the current game
                existing_pick = Week2_picks.query.filter_by(user=user, game_number=game_number).first()

                if existing_pick:
                    if selected_winner is not None and len(selected_winner) > 1:
                        # Overwrite the existing pick with the new selection
                        existing_pick.selected_winner = selected_winner
                        existing_pick.selected_difference = selected_difference
                        existing_pick.user_pick = user_pick
                else:
                    # Create a new instance of the Week2 model with the user, selected winner, and game number
                    week2_pick = Week2_picks(user=user, user_pick=user_pick, game_number=game_number, selected_winner=selected_winner, selected_difference=selected_difference)
                    # Add the new pick to the database
                    db.session.add(week2_pick)
            else:
                selected_winner = None
                selected_difference = None

                # Check if the user already made a pick for the current game
                existing_pick = Week2_picks.query.filter_by(user=user, game_number=game_number).first()

                if existing_pick:
                    existing_pick.selected_winner = selected_winner
                    existing_pick.selected_difference = selected_difference
                    existing_pick.user_pick = None

                else:
                    # Create a new instance of the Week2 model with the user, selected winner, and game number
                    week2_pick = Week2_picks(user=user, user_pick=None, game_number=game_number, selected_winner=selected_winner, selected_difference=selected_difference)
                    # Add the new pick to the database
                    db.session.add(week2_pick)

        # Commit all the picks to the database
        db.session.commit()

        # Optionally, you can redirect to another page or render a template
        flash('Tus picks se han guardado con éxito!', category='success')
        return redirect(url_for('views.week2'))

    return redirect(url_for('views.week2'))


LIMIT_DATE_WEEK_3 = time_zone.localize(datetime(2023, 8, 1, 23, 50, 0))
@views.route("/week3")
@login_required
def week3():
    current_datetime = datetime.now(time_zone)
    base_scores = get_base_scores()
    base_results = get_base_results()
    teams = Teams.query.all()

    return render_template('week3.html', user=current_user, current_datetime=current_datetime, limit_date=LIMIT_DATE_WEEK_3, time_zone=time_zone, base_scores=base_scores, base_results=base_results, teams=teams)

@views.route('/week3-leaderboard')
@login_required
def week3_leaderboard():
    base_scores = get_base_scores()
    base_results = get_base_results()
    leaderboard_data = Leaderboard.query.order_by(Leaderboard.week3_points.desc()).all()
    week_picks = Week3_picks.query.all()
    week_results = Week3_results.query.all()
    teams = Teams.query.all()

    def count_game_numbers(user_id):
        game_numbers = [pick.game_number for pick in week_picks if pick.user_id == user_id]
        return len(set(game_numbers))
    
    return render_template('week3_leaderboard.html', user=current_user, base_scores=base_scores, base_results=base_results, leaderboard_data=leaderboard_data, week_picks=week_picks, week_results=week_results, teams=teams, count_game_numbers=count_game_numbers)

@views.route('/save-week3-picks', methods=['POST'])
@login_required
def save_week3_form():
    current_datetime = datetime.now(time_zone)
    if request.method == 'POST':
        if current_datetime > LIMIT_DATE_WEEK_3:
            flash('La fecha límite para hacer picks de esta semana ha expirado.', category='error')
            return redirect(url_for('views.week3'))
        
        # Get the user object from current_user
        user = current_user

        # Iterate through the game picks
        for game_number in range(1, 17):
            # Construct the input name based on the game number
            input_name = f'week-3_game-{game_number}_winner'

            # Get the selected winner for the current game
            user_pick = request.form.get(input_name)
            if user_pick:
                # Extract the word between the second last "_" and last "-"
                split_values = user_pick.split('_')
                split_values2 = split_values[-2].split('-')
                if len(split_values2) >= 1:
                    selected_winner = split_values2[-1]
                split_values = user_pick.split('-')
                if len(split_values) >= 1:
                    selected_difference = int(split_values[-1])  # Extract the difference value
                else:
                    selected_winner = None
                    selected_difference = None

                # Check if the user already made a pick for the current game
                existing_pick = Week3_picks.query.filter_by(user=user, game_number=game_number).first()

                if existing_pick:
                    if selected_winner is not None and len(selected_winner) > 1:
                        # Overwrite the existing pick with the new selection
                        existing_pick.selected_winner = selected_winner
                        existing_pick.selected_difference = selected_difference
                        existing_pick.user_pick = user_pick
                else:
                    # Create a new instance of the Week3 model with the user, selected winner, and game number
                    week3_pick = Week3_picks(user=user, user_pick=user_pick, game_number=game_number, selected_winner=selected_winner, selected_difference=selected_difference)
                    # Add the new pick to the database
                    db.session.add(week3_pick)
            else:
                selected_winner = None
                selected_difference = None

                # Check if the user already made a pick for the current game
                existing_pick = Week3_picks.query.filter_by(user=user, game_number=game_number).first()

                if existing_pick:
                    existing_pick.selected_winner = selected_winner
                    existing_pick.selected_difference = selected_difference
                    existing_pick.user_pick = None

                else:
                    # Create a new instance of the Week3 model with the user, selected winner, and game number
                    week3_pick = Week3_picks(user=user, user_pick=None, game_number=game_number, selected_winner=selected_winner, selected_difference=selected_difference)
                    # Add the new pick to the database
                    db.session.add(week3_pick)

        # Commit all the picks to the database
        db.session.commit()

        # Optionally, you can redirect to another page or render a template
        flash('Tus picks se han guardado con éxito!', category='success')
        return redirect(url_for('views.week3'))

    return redirect(url_for('views.week3'))


LIMIT_DATE_WEEK_4 = time_zone.localize(datetime(2023, 8, 1, 23, 50, 0))
@views.route("/week4")
@login_required
def week4():
    current_datetime = datetime.now(time_zone)
    base_scores = get_base_scores()
    base_results = get_base_results()
    teams = Teams.query.all()

    return render_template('week4.html', user=current_user, current_datetime=current_datetime, limit_date=LIMIT_DATE_WEEK_4, time_zone=time_zone, base_scores=base_scores, base_results=base_results, teams=teams)

@views.route('/week4-leaderboard')
@login_required
def week4_leaderboard():
    base_scores = get_base_scores()
    base_results = get_base_results()
    leaderboard_data = Leaderboard.query.order_by(Leaderboard.week4_points.desc()).all()
    week_picks = Week4_picks.query.all()
    week_results = Week4_results.query.all()
    teams = Teams.query.all()

    def count_game_numbers(user_id):
        game_numbers = [pick.game_number for pick in week_picks if pick.user_id == user_id]
        return len(set(game_numbers))
    
    return render_template('week4_leaderboard.html', user=current_user, base_scores=base_scores, base_results=base_results, leaderboard_data=leaderboard_data, week_picks=week_picks, week_results=week_results, teams=teams, count_game_numbers=count_game_numbers)

@views.route('/save-week4-picks', methods=['POST'])
@login_required
def save_week4_form():
    current_datetime = datetime.now(time_zone)
    if request.method == 'POST':
        if current_datetime > LIMIT_DATE_WEEK_4:
            flash('La fecha límite para hacer picks de esta semana ha expirado.', category='error')
            return redirect(url_for('views.week4'))
        
        # Get the user object from current_user
        user = current_user

        # Iterate through the game picks
        for game_number in range(1, 17):
            # Construct the input name based on the game number
            input_name = f'week-4_game-{game_number}_winner'

            # Get the selected winner for the current game
            user_pick = request.form.get(input_name)
            if user_pick:
                # Extract the word between the second last "_" and last "-"
                split_values = user_pick.split('_')
                split_values2 = split_values[-2].split('-')
                if len(split_values2) >= 1:
                    selected_winner = split_values2[-1]
                split_values = user_pick.split('-')
                if len(split_values) >= 1:
                    selected_difference = int(split_values[-1])  # Extract the difference value
                else:
                    selected_winner = None
                    selected_difference = None

                # Check if the user already made a pick for the current game
                existing_pick = Week4_picks.query.filter_by(user=user, game_number=game_number).first()

                if existing_pick:
                    if selected_winner is not None and len(selected_winner) > 1:
                        # Overwrite the existing pick with the new selection
                        existing_pick.selected_winner = selected_winner
                        existing_pick.selected_difference = selected_difference
                        existing_pick.user_pick = user_pick
                else:
                    # Create a new instance of the Week4 model with the user, selected winner, and game number
                    week4_pick = Week4_picks(user=user, user_pick=user_pick, game_number=game_number, selected_winner=selected_winner, selected_difference=selected_difference)
                    # Add the new pick to the database
                    db.session.add(week4_pick)
            else:
                selected_winner = None
                selected_difference = None

                # Check if the user already made a pick for the current game
                existing_pick = Week4_picks.query.filter_by(user=user, game_number=game_number).first()

                if existing_pick:
                    existing_pick.selected_winner = selected_winner
                    existing_pick.selected_difference = selected_difference
                    existing_pick.user_pick = None

                else:
                    # Create a new instance of the Week4 model with the user, selected winner, and game number
                    week4_pick = Week4_picks(user=user, user_pick=None, game_number=game_number, selected_winner=selected_winner, selected_difference=selected_difference)
                    # Add the new pick to the database
                    db.session.add(week4_pick)

        # Commit all the picks to the database
        db.session.commit()

        # Optionally, you can redirect to another page or render a template
        flash('Tus picks se han guardado con éxito!', category='success')
        return redirect(url_for('views.week4'))

    return redirect(url_for('views.week4'))


LIMIT_DATE_WEEK_5 = time_zone.localize(datetime(2023, 8, 1, 23, 50, 0))
@views.route("/week5")
@login_required
def week5():
    current_datetime = datetime.now(time_zone)
    base_scores = get_base_scores()
    base_results = get_base_results()
    teams = Teams.query.all()

    return render_template('week5.html', user=current_user, current_datetime=current_datetime, limit_date=LIMIT_DATE_WEEK_5, time_zone=time_zone, base_scores=base_scores, base_results=base_results, teams=teams)

@views.route('/week5-leaderboard')
@login_required
def week5_leaderboard():
    base_scores = get_base_scores()
    base_results = get_base_results()
    leaderboard_data = Leaderboard.query.order_by(Leaderboard.week5_points.desc()).all()
    week_picks = Week5_picks.query.all()
    week_results = Week5_results.query.all()
    teams = Teams.query.all()

    def count_game_numbers(user_id):
        game_numbers = [pick.game_number for pick in week_picks if pick.user_id == user_id]
        return len(set(game_numbers))
    
    return render_template('week5_leaderboard.html', user=current_user, base_scores=base_scores, base_results=base_results, leaderboard_data=leaderboard_data, week_picks=week_picks, week_results=week_results, teams=teams, count_game_numbers=count_game_numbers)

@views.route('/save-week5-picks', methods=['POST'])
@login_required
def save_week5_form():
    current_datetime = datetime.now(time_zone)
    if request.method == 'POST':
        if current_datetime > LIMIT_DATE_WEEK_5:
            flash('La fecha límite para hacer picks de esta semana ha expirado.', category='error')
            return redirect(url_for('views.week5'))
        
        # Get the user object from current_user
        user = current_user

        # Iterate through the game picks
        for game_number in range(1, 17):
            # Construct the input name based on the game number
            input_name = f'week-5_game-{game_number}_winner'

            # Get the selected winner for the current game
            user_pick = request.form.get(input_name)
            if user_pick:
                # Extract the word between the second last "_" and last "-"
                split_values = user_pick.split('_')
                split_values2 = split_values[-2].split('-')
                if len(split_values2) >= 1:
                    selected_winner = split_values2[-1]
                split_values = user_pick.split('-')
                if len(split_values) >= 1:
                    selected_difference = int(split_values[-1])  # Extract the difference value
                else:
                    selected_winner = None
                    selected_difference = None

                # Check if the user already made a pick for the current game
                existing_pick = Week5_picks.query.filter_by(user=user, game_number=game_number).first()

                if existing_pick:
                    if selected_winner is not None and len(selected_winner) > 1:
                        # Overwrite the existing pick with the new selection
                        existing_pick.selected_winner = selected_winner
                        existing_pick.selected_difference = selected_difference
                        existing_pick.user_pick = user_pick
                else:
                    # Create a new instance of the Week5 model with the user, selected winner, and game number
                    week5_pick = Week5_picks(user=user, user_pick=user_pick, game_number=game_number, selected_winner=selected_winner, selected_difference=selected_difference)
                    # Add the new pick to the database
                    db.session.add(week5_pick)
            else:
                selected_winner = None
                selected_difference = None

                # Check if the user already made a pick for the current game
                existing_pick = Week5_picks.query.filter_by(user=user, game_number=game_number).first()

                if existing_pick:
                    existing_pick.selected_winner = selected_winner
                    existing_pick.selected_difference = selected_difference
                    existing_pick.user_pick = None

                else:
                    # Create a new instance of the Week5 model with the user, selected winner, and game number
                    week5_pick = Week5_picks(user=user, user_pick=None, game_number=game_number, selected_winner=selected_winner, selected_difference=selected_difference)
                    # Add the new pick to the database
                    db.session.add(week5_pick)

        # Commit all the picks to the database
        db.session.commit()

        # Optionally, you can redirect to another page or render a template
        flash('Tus picks se han guardado con éxito!', category='success')
        return redirect(url_for('views.week5'))

    return redirect(url_for('views.week5'))


LIMIT_DATE_WEEK_6 = time_zone.localize(datetime(2023, 8, 1, 23, 50, 0))
@views.route("/week6")
@login_required
def week6():
    current_datetime = datetime.now(time_zone)
    base_scores = get_base_scores()
    base_results = get_base_results()
    teams = Teams.query.all()

    return render_template('week6.html', user=current_user, current_datetime=current_datetime, limit_date=LIMIT_DATE_WEEK_6, time_zone=time_zone, base_scores=base_scores, base_results=base_results, teams=teams)

@views.route('/week6-leaderboard')
@login_required
def week6_leaderboard():
    base_scores = get_base_scores()
    base_results = get_base_results()
    leaderboard_data = Leaderboard.query.order_by(Leaderboard.week6_points.desc()).all()
    week_picks = Week6_picks.query.all()
    week_results = Week6_results.query.all()
    teams = Teams.query.all()

    def count_game_numbers(user_id):
        game_numbers = [pick.game_number for pick in week_picks if pick.user_id == user_id]
        return len(set(game_numbers))
    
    return render_template('week6_leaderboard.html', user=current_user, base_scores=base_scores, base_results=base_results, leaderboard_data=leaderboard_data, week_picks=week_picks, week_results=week_results, teams=teams, count_game_numbers=count_game_numbers)

@views.route('/save-week6-picks', methods=['POST'])
@login_required
def save_week6_form():
    current_datetime = datetime.now(time_zone)
    if request.method == 'POST':
        if current_datetime > LIMIT_DATE_WEEK_6:
            flash('La fecha límite para hacer picks de esta semana ha expirado.', category='error')
            return redirect(url_for('views.week6'))
        
        # Get the user object from current_user
        user = current_user

        # Iterate through the game picks
        for game_number in range(1, 17):
            # Construct the input name based on the game number
            input_name = f'week-6_game-{game_number}_winner'

            # Get the selected winner for the current game
            user_pick = request.form.get(input_name)
            if user_pick:
                # Extract the word between the second last "_" and last "-"
                split_values = user_pick.split('_')
                split_values2 = split_values[-2].split('-')
                if len(split_values2) >= 1:
                    selected_winner = split_values2[-1]
                split_values = user_pick.split('-')
                if len(split_values) >= 1:
                    selected_difference = int(split_values[-1])  # Extract the difference value
                else:
                    selected_winner = None
                    selected_difference = None

                # Check if the user already made a pick for the current game
                existing_pick = Week6_picks.query.filter_by(user=user, game_number=game_number).first()

                if existing_pick:
                    if selected_winner is not None and len(selected_winner) > 1:
                        # Overwrite the existing pick with the new selection
                        existing_pick.selected_winner = selected_winner
                        existing_pick.selected_difference = selected_difference
                        existing_pick.user_pick = user_pick
                else:
                    # Create a new instance of the Week6 model with the user, selected winner, and game number
                    week6_pick = Week6_picks(user=user, user_pick=user_pick, game_number=game_number, selected_winner=selected_winner, selected_difference=selected_difference)
                    # Add the new pick to the database
                    db.session.add(week6_pick)
            else:
                selected_winner = None
                selected_difference = None

                # Check if the user already made a pick for the current game
                existing_pick = Week6_picks.query.filter_by(user=user, game_number=game_number).first()

                if existing_pick:
                    existing_pick.selected_winner = selected_winner
                    existing_pick.selected_difference = selected_difference
                    existing_pick.user_pick = None

                else:
                    # Create a new instance of the Week6 model with the user, selected winner, and game number
                    week6_pick = Week6_picks(user=user, user_pick=None, game_number=game_number, selected_winner=selected_winner, selected_difference=selected_difference)
                    # Add the new pick to the database
                    db.session.add(week6_pick)

        # Commit all the picks to the database
        db.session.commit()

        # Optionally, you can redirect to another page or render a template
        flash('Tus picks se han guardado con éxito!', category='success')
        return redirect(url_for('views.week6'))

    return redirect(url_for('views.week6'))


""" @views.route('/week1-simulator')
@login_required
def week1_simulator():
    leaderboard_data = Leaderboard.query.order_by(Leaderboard.week1_points.desc()).all()
    week_picks = Week1_picks.query.all()
    week_results = Week1_results.query.all()
    teams = Teams.query.all()

    def count_game_numbers(user_id):
        game_numbers = [pick.game_number for pick in week_picks if pick.user_id == user_id]
        return len(set(game_numbers))
    
    return render_template('week1_simulator.html', user=current_user, week_picks=week_picks, leaderboard_data=leaderboard_data, count_game_numbers=count_game_numbers, week_results=week_results, teams=teams) """