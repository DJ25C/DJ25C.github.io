import requests
from bs4 import BeautifulSoup
from datetime import datetime
from .models import *

def scrape_news(app):
    url_NFL = 'https://www.nfl.com/'
    url_NFL_news = 'https://www.nfl.com/news/'
    response_NFL = requests.get(url_NFL)
    response_NFL_news = requests.get(url_NFL_news)
    soup_NFL = BeautifulSoup(response_NFL.content, 'html.parser')
    soup_NFL_news = BeautifulSoup(response_NFL_news.content, 'html.parser')

    # News 1 Link
    news_1_link = soup_NFL.find('div', class_='d3-o-centerpiece__hero').find('a')['href']
    # News 1 Image
    news_1_img = soup_NFL.find('figure', class_='d3-o-media-object__figure').find('img')['src']
    news_1_img = news_1_img.replace("/t_lazy", "")
    # News 1 Heading
    news_1_heading = soup_NFL.find('h3', class_='d3-o-media-object__title').text

    # News 2 Link
    news_2_link = soup_NFL_news.find_all('div', class_='d3-l-col__col-4')[0].find('a')['href']
    # News 2 Image
    news_2_img = soup_NFL_news.find_all('figure', class_='d3-o-media-object__figure')[0].find('img')['src']
    news_2_img = news_2_img.replace("/t_lazy", "").replace("mobile", "3_4_desktop_2x")
    # News 2 Heading
    news_2_heading = soup_NFL_news.find_all('h3', class_='d3-o-media-object__title')[0].text

    # News 3 Link
    news_3_link = soup_NFL_news.find_all('div', class_='d3-l-col__col-4')[1].find('a')['href']
    # News 3 Image
    news_3_img = soup_NFL_news.find_all('figure', class_='d3-o-media-object__figure')[1].find('img')['src']
    news_3_img = news_3_img.replace("/t_lazy", "").replace("mobile", "3_4_desktop_2x")
    # News 3 Heading
    news_3_heading = soup_NFL_news.find_all('h3', class_='d3-o-media-object__title')[1].text

    # News 4 Link
    news_4_link = soup_NFL_news.find_all('div', class_='d3-l-col__col-4')[2].find('a')['href']
    # News 4 Image
    news_4_img = soup_NFL_news.find_all('figure', class_='d3-o-media-object__figure')[2].find('img')['src']
    news_4_img = news_4_img.replace("/t_lazy", "").replace("mobile", "3_4_desktop_2x")
    # News 4 Heading
    news_4_heading = soup_NFL_news.find_all('h3', class_='d3-o-media-object__title')[2].text
    news_entry = News(
        news_1_link=news_1_link,
        news_1_img=news_1_img,
        news_1_heading=news_1_heading,
        news_2_link=news_2_link,
        news_2_img=news_2_img,
        news_2_heading=news_2_heading,
        news_3_link=news_3_link,
        news_3_img=news_3_img,
        news_3_heading=news_3_heading,
        news_4_link=news_4_link,
        news_4_img=news_4_img,
        news_4_heading=news_4_heading
    )
    with app.app_context():
        db.session.query(News).delete()
        # Add the News object to the database session
        db.session.add(news_entry)
        db.session.commit()
    current_time = datetime.now()
    print('NEWS Table Updated at:', current_time)

def scrape_scores(app, week_number):
    with app.app_context():
        Scores = globals()[f"Week{week_number}_scores"]

        url_NFL_scores = f'https://www.espn.com/nfl/scoreboard/_/week/{week_number}/year/2022/seasontype/2'
        response_NFL_scores = requests.get(url_NFL_scores)
        soup_NFL_scores = BeautifulSoup(response_NFL_scores.content, 'html.parser')
        url_NFL_scores_23 = f'https://www.espn.com/nfl/scoreboard/_/week/{week_number}/year/2023/seasontype/2'
        response_NFL_scores_23 = requests.get(url_NFL_scores_23)
        soup_NFL_scores_23 = BeautifulSoup(response_NFL_scores_23.content, 'html.parser')

        team_name_divs = soup_NFL_scores.find_all('div', class_='ScoreCell__TeamName ScoreCell__TeamName--shortDisplayName truncate db')
        team_score_divs = soup_NFL_scores.find_all('div', class_='ScoreCell__Score h4 clr-gray-01 fw-heavy tar ScoreCell_Score--scoreboard pl2')
        team_div_number = len(team_name_divs)

        scores = {}
        if len(team_score_divs) < team_div_number:
            for team in range(team_div_number):
                team_name = team_name_divs[team].text.strip().lower()
                scores[team_name] = 0
        else:
            for team in range(team_div_number):
                team_name = team_name_divs[team].text.strip().lower()
                team_score = team_score_divs[team].text
                scores[team_name] = team_score

        db.session.query(Scores).delete()
        for team_name, team_score in scores.items():
            score = Scores(team_name=team_name, team_score=team_score)
            db.session.add(score)

        db.session.commit()
        
        current_time = datetime.now()

        print('SCORES Updated at:', current_time)
        results(week_number)
        leaderboard()
        print('Week Number: ', week_number)


teams = {
'bills': 'BUF',
'saints': 'NO',
'browns': 'CLE',
'49ers': 'SF',
'steelers': 'PIT',
'eagles': 'PHI',
'colts': 'IND',
'patriots': 'NE',
'ravens': 'BAL',
'jaguars': 'JAX',
'giants': 'NYG',
'chiefs': 'KC',
'raiders': 'LV',
'packers': 'GB',
'buccaneers': 'TB',
'broncos': 'DEN',
'rams': 'LA',
'falcons': 'ATL',
'panthers': 'CAR',
'bears': 'CHI',
'bengals': 'CIN',
'lions': 'DET',
'texans': 'HOU',
'dolphins': 'MIA',
'jets': 'NYJ',
'commanders': 'WAS',
'titans': 'TEN',
'cardinals': 'ARI',
'chargers': 'LAC',
'vikings': 'MIN',
'cowboys': 'DAL',
'seahawks': 'SEA'
}

def check_team_name(variable, team_name):
    if team_name not in teams:
        print(f"\nError: Invalid {variable} '{team_name}'\n")

def check_winner_homecourt(variable, winner_homecourt):
    if winner_homecourt not in ['home', 'away', 'tie']:
        print(f"\nError: Invalid {variable} '{winner_homecourt}'\n")

def check_points_difference(variable, points_difference):
    if points_difference not in [6, 7]:
        print(f"\nError: Invalid {variable} '{points_difference}'\n")

def results(week_number):
     # Import the necessary classes dynamically
    Week = globals()[f"Week{week_number}_results"]
    existing_results = Week.query.all()
    Scores = globals()[f"Week{week_number}_scores"]
    if Week.query.count() > 16:
        print("Already 16 results in the table")
    else:
        results = [
            Week(game_number=1, game_day='Sab', game_date='06/01', game_time='TBD', away_team_name='browns', home_team_name='bengals', winner_team_name='', winner_team_abbr='', winner_homecourt='', points_difference=''),
            Week(game_number=2, game_day='Sab', game_date='06/01', game_time='TBD', away_team_name='vikings', home_team_name='lions', winner_team_name='', winner_team_abbr='', winner_homecourt='', points_difference=''),
            Week(game_number=3, game_day='Sab', game_date='06/01', game_time='TBD', away_team_name='bears', home_team_name='packers', winner_team_name='', winner_team_abbr='', winner_homecourt='', points_difference=''),
            Week(game_number=4, game_day='Sab', game_date='06/01', game_time='TBD', away_team_name='jaguars', home_team_name='titans', winner_team_name='', winner_team_abbr='', winner_homecourt='', points_difference=''),
            Week(game_number=5, game_day='Sab', game_date='06/01', game_time='TBD', away_team_name='texans', home_team_name='colts', winner_team_name='', winner_team_abbr='', winner_homecourt='', points_difference=''),
            Week(game_number=6, game_day='Sab', game_date='06/01', game_time='TBD', away_team_name='broncos', home_team_name='raiders', winner_team_name='', winner_team_abbr='', winner_homecourt='', points_difference=''),
            Week(game_number=7, game_day='Sab', game_date='06/01', game_time='TBD', away_team_name='bills', home_team_name='dolphins', winner_team_name='', winner_team_abbr='', winner_homecourt='', points_difference=''),
            Week(game_number=8, game_day='Sab', game_date='06/01', game_time='TBD', away_team_name='jets', home_team_name='patriots', winner_team_name='', winner_team_abbr='', winner_homecourt='', points_difference=''),
            Week(game_number=9, game_day='Sab', game_date='06/01', game_time='TBD', away_team_name='falcons', home_team_name='saints', winner_team_name='', winner_team_abbr='', winner_homecourt='', points_difference=''),
            Week(game_number=10, game_day='Sab', game_date='06/01', game_time='TBD', away_team_name='eagles', home_team_name='giants', winner_team_name='', winner_team_abbr='', winner_homecourt='', points_difference=''),
            Week(game_number=11, game_day='Sab', game_date='06/01', game_time='TBD', away_team_name='seahawks', home_team_name='cardinals', winner_team_name='', winner_team_abbr='', winner_homecourt='', points_difference=''),
            Week(game_number=12, game_day='Sab', game_date='06/01', game_time='TBD', away_team_name='chiefs', home_team_name='chargers', winner_team_name='', winner_team_abbr='', winner_homecourt='', points_difference=''),
            Week(game_number=13, game_day='Sab', game_date='06/01', game_time='TBD', away_team_name='rams', home_team_name='49ers', winner_team_name='', winner_team_abbr='', winner_homecourt='', points_difference=''),
            Week(game_number=14, game_day='Sab', game_date='06/01', game_time='TBD', away_team_name='cowboys', home_team_name='commanders', winner_team_name='', winner_team_abbr='', winner_homecourt='', points_difference=''),
            Week(game_number=15, game_day='Sab', game_date='06/01', game_time='TBD', away_team_name='buccaneers', home_team_name='panthers', winner_team_name='', winner_team_abbr='', winner_homecourt='', points_difference=''),
            Week(game_number=16, game_day='Sab', game_date='06/01', game_time='TBD', away_team_name='steelers', home_team_name='ravens', winner_team_name='', winner_team_abbr='', winner_homecourt='', points_difference='')
        ]
        for result in existing_results:
            existing_result = Week.query.filter_by(game_number=result.game_number).first()

            home_score = Scores.query.filter_by(team_name=existing_result.home_team_name).first()
            away_score = Scores.query.filter_by(team_name=existing_result.away_team_name).first()

            if home_score.team_score == 0 and away_score.team_score == 0:
                result.winner_team_name = ''
                result.winner_team_abbr = ''
                result.winner_homecourt = ''
                result.points_difference = ''
            else:
                if home_score.team_score > away_score.team_score:
                    result.winner_team_name = existing_result.home_team_name
                elif home_score.team_score < away_score.team_score:
                    result.winner_team_name = existing_result.away_team_name
                else:
                    result.winner_team_name = ""  # Set an empty winner_team_name if scores are equal
                
                point_difference = abs(home_score.team_score - away_score.team_score)
                result.points_difference = 7 if point_difference >= 7 else 6
                
                result.winner_team_name = result.winner_team_name.lower().strip()
                result.winner_team_abbr = teams.get(result.winner_team_name)
                if result.winner_team_name == existing_result.home_team_name:
                    result.winner_homecourt = "home"
                elif result.winner_team_name == existing_result.away_team_name:
                    result.winner_homecourt = "away"
                else:
                    result.winner_homecourt = "tie"
                
                check_winner_homecourt("Winner homecourt", result.winner_homecourt)
                check_points_difference("Points difference", result.points_difference)
            
            if existing_result:
                existing_result.winner_team_abbr = result.winner_team_abbr
                existing_result.winner_team_name = result.winner_team_name
                existing_result.winner_homecourt = result.winner_homecourt
                existing_result.points_difference = result.points_difference
            else:
                db.session.add(result)
                
        db.session.commit()

        print('RESULTS Updated')


def leaderboard():
    db.session.query(Leaderboard).delete()
    leaderboard_entries = {}

    for week_number in range(1, 4):
        # Retrieve the corresponding picks and results for the week
        picks = globals()[f"Week{week_number}_picks"].query.all()
        results = globals()[f"Week{week_number}_results"].query.all()
        users = User.query.all()

        for user in users:
            user_id = user.id
            user_name = user.first_name + ' ' + user.last_name
            user_points = 0  # Initialize points for each week's picks

            for pick in picks:
                if pick.user_id == user_id:
                    game_number = pick.game_number
                    selected_winner = pick.selected_winner
                    selected_difference = pick.selected_difference

                    for result in results:
                        if result.game_number == game_number:
                            if selected_winner == result.winner_homecourt:
                                user_points += 2  # Accumulate points for correct winner
                                if selected_difference == result.points_difference:
                                    user_points += 1  # Accumulate points for correct difference
                                    break  # Break the loop after finding a match
                            elif result.winner_homecourt == 'tie' and selected_difference == result.points_difference:
                                user_points += 1
                                break

            user_week_key = (user_id, week_number)  # Create a tuple key for user and week
            leaderboard_entry = leaderboard_entries.get(user_id)

            if leaderboard_entry:
                # Update the points for the corresponding week
                setattr(leaderboard_entry, f"week{week_number}_points", user_points)
            else:
                # Create a new leaderboard entry for the user
                leaderboard_entry = leaderboard_entries[user_id] = Leaderboard(
                    user_id=user_id,
                    user_name=user_name,
                )
                setattr(leaderboard_entry, f"week{week_number}_points", user_points)

    # Assign position based on the order of total points
    leaderboard_entries = list(leaderboard_entries.values())

    for entry in leaderboard_entries:
        total_points = 0
        for week_number in range(1, 4):
            week_points = getattr(entry, f"week{week_number}_points") or 0
            setattr(entry, f"week{week_number}_points", week_points)  # Update week_points column
            total_points += week_points
        setattr(entry, "total_points", total_points)

    # Sort leaderboard_entries based on the total points in descending order
    leaderboard_entries.sort(key=lambda x: x.total_points, reverse=True)

    position = 1
    for entry in leaderboard_entries:
        entry.position = position
        position += 1

        # Add the leaderboard entry to the session
        db.session.add(entry)

    # Commit the changes to the database
    db.session.commit()

    print('LEADERBOARD Updated')
