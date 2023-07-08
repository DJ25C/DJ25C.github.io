from . import db
from flask_login import UserMixin, current_user
import sys

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))

    def has_pick_for_week_and_game(self, week_number, game_number):
        week_class = getattr(sys.modules[__name__], f"Week{week_number}_picks")
        return week_class.query.filter_by(user=self, game_number=game_number).first() is not None

    def get_pick_for__week_and_game(self, week_number, game_number):
        week_class = getattr(sys.modules[__name__], f"Week{week_number}_picks")
        pick = week_class.query.filter_by(user=self, game_number=game_number).first()
        return pick.user_pick if pick else None


class Teams(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(50))
    team_abbr = db.Column(db.String(50))
    team_logo = db.Column(db.String(50))


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    news_1_link = db.Column(db.String(150))
    news_1_img = db.Column(db.String(150))
    news_1_heading = db.Column(db.String(150))
    news_2_link = db.Column(db.String(150))
    news_2_img = db.Column(db.String(150))
    news_2_heading = db.Column(db.String(150))
    news_3_link = db.Column(db.String(150))
    news_3_img = db.Column(db.String(150))
    news_3_heading = db.Column(db.String(150))
    news_4_link = db.Column(db.String(150))
    news_4_img = db.Column(db.String(150))
    news_4_heading = db.Column(db.String(150))


class Leaderboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    position = db.Column(db.Integer)
    user_name = db.Column(db.String(50))
    week1_points = db.Column(db.Integer)
    week2_points = db.Column(db.Integer)
    week3_points = db.Column(db.Integer)
    week4_points = db.Column(db.Integer)
    week5_points = db.Column(db.Integer)
    week6_points = db.Column(db.Integer)
    week7_points = db.Column(db.Integer)
    week8_points = db.Column(db.Integer)
    week9_points = db.Column(db.Integer)
    week10_points = db.Column(db.Integer)
    week11_points = db.Column(db.Integer)
    week12_points = db.Column(db.Integer)
    week13_points = db.Column(db.Integer)
    week14_points = db.Column(db.Integer)
    week15_points = db.Column(db.Integer)
    week16_points = db.Column(db.Integer)
    week17_points = db.Column(db.Integer)
    week18_points = db.Column(db.Integer)
    total_points = db.Column(db.Integer)


class Week1_picks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_name = db.Column(db.String(50), default=lambda: f"{User.query.get(current_user.id).first_name} {User.query.get(current_user.id).last_name}")
    user = db.relationship('User', backref='week1_picks')
    user_pick = db.Column(db.Integer)
    game_number = db.Column(db.Integer)
    selected_winner = db.Column(db.String(50))
    selected_difference = db.Column(db.Integer)

class Week1_results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_number = db.Column(db.Integer)
    game_day = db.Column(db.String(50))
    game_date = db.Column(db.String(50))
    game_time = db.Column(db.String(50))
    away_team_name = db.Column(db.String(50))
    home_team_name = db.Column(db.String(50))
    winner_team_name = db.Column(db.String(50))
    winner_team_abbr = db.Column(db.String(50))
    winner_homecourt = db.Column(db.String(50))
    points_difference = db.Column(db.Integer)

class Week1_scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(50))
    team_score = db.Column(db.Integer)


class Week2_picks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='week2_picks')
    user_name = db.Column(db.String(50), default=lambda: f"{User.query.get(current_user.id).first_name} {User.query.get(current_user.id).last_name}")
    user_pick = db.Column(db.Integer)
    game_number = db.Column(db.Integer)
    selected_winner = db.Column(db.String(50))
    selected_difference = db.Column(db.Integer)

class Week2_results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_number = db.Column(db.Integer)
    game_day = db.Column(db.String(50))
    game_date = db.Column(db.String(50))
    game_time = db.Column(db.String(50))
    away_team_name = db.Column(db.String(50))
    home_team_name = db.Column(db.String(50))
    winner_team_name = db.Column(db.String(50))
    winner_team_abbr = db.Column(db.String(50))
    winner_homecourt = db.Column(db.String(50))
    points_difference = db.Column(db.Integer)

class Week2_scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(50))
    team_score = db.Column(db.Integer)


class Week3_picks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='week3_picks')
    user_name = db.Column(db.String(50), default=lambda: f"{User.query.get(current_user.id).first_name} {User.query.get(current_user.id).last_name}")
    user_pick = db.Column(db.Integer)
    game_number = db.Column(db.Integer)
    selected_winner = db.Column(db.String(50))
    selected_difference = db.Column(db.Integer)

class Week3_results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_number = db.Column(db.Integer)
    game_day = db.Column(db.String(50))
    game_date = db.Column(db.String(50))
    game_time = db.Column(db.String(50))
    away_team_name = db.Column(db.String(50))
    home_team_name = db.Column(db.String(50))
    winner_team_name = db.Column(db.String(50))
    winner_team_abbr = db.Column(db.String(50))
    winner_homecourt = db.Column(db.String(50))
    points_difference = db.Column(db.Integer)

class Week3_scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(50))
    team_score = db.Column(db.Integer)


class Week4_picks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='week4_picks')
    user_name = db.Column(db.String(50), default=lambda: f"{User.query.get(current_user.id).first_name} {User.query.get(current_user.id).last_name}")
    user_pick = db.Column(db.Integer)
    game_number = db.Column(db.Integer)
    selected_winner = db.Column(db.String(50))
    selected_difference = db.Column(db.Integer)

class Week4_results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_number = db.Column(db.Integer)
    game_day = db.Column(db.String(50))
    game_date = db.Column(db.String(50))
    game_time = db.Column(db.String(50))
    away_team_name = db.Column(db.String(50))
    home_team_name = db.Column(db.String(50))
    winner_team_name = db.Column(db.String(50))
    winner_team_abbr = db.Column(db.String(50))
    winner_homecourt = db.Column(db.String(50))
    points_difference = db.Column(db.Integer)

class Week4_scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(50))
    team_score = db.Column(db.Integer)


class Week5_picks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='week5_picks')
    user_name = db.Column(db.String(50), default=lambda: f"{User.query.get(current_user.id).first_name} {User.query.get(current_user.id).last_name}")
    user_pick = db.Column(db.Integer)
    game_number = db.Column(db.Integer)
    selected_winner = db.Column(db.String(50))
    selected_difference = db.Column(db.Integer)

class Week5_results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_number = db.Column(db.Integer)
    game_day = db.Column(db.String(50))
    game_date = db.Column(db.String(50))
    game_time = db.Column(db.String(50))
    away_team_name = db.Column(db.String(50))
    home_team_name = db.Column(db.String(50))
    winner_team_name = db.Column(db.String(50))
    winner_team_abbr = db.Column(db.String(50))
    winner_homecourt = db.Column(db.String(50))
    points_difference = db.Column(db.Integer)

class Week5_scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(50))
    team_score = db.Column(db.Integer)


class Week6_picks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='week6_picks')
    user_name = db.Column(db.String(50), default=lambda: f"{User.query.get(current_user.id).first_name} {User.query.get(current_user.id).last_name}")
    user_pick = db.Column(db.Integer)
    game_number = db.Column(db.Integer)
    selected_winner = db.Column(db.String(50))
    selected_difference = db.Column(db.Integer)

class Week6_results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_number = db.Column(db.Integer)
    game_day = db.Column(db.String(50))
    game_date = db.Column(db.String(50))
    game_time = db.Column(db.String(50))
    away_team_name = db.Column(db.String(50))
    home_team_name = db.Column(db.String(50))
    winner_team_name = db.Column(db.String(50))
    winner_team_abbr = db.Column(db.String(50))
    winner_homecourt = db.Column(db.String(50))
    points_difference = db.Column(db.Integer)

class Week6_scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(50))
    team_score = db.Column(db.Integer)


class Week7_picks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='week7_picks')
    user_name = db.Column(db.String(50), default=lambda: f"{User.query.get(current_user.id).first_name} {User.query.get(current_user.id).last_name}")
    user_pick = db.Column(db.Integer)
    game_number = db.Column(db.Integer)
    selected_winner = db.Column(db.String(50))
    selected_difference = db.Column(db.Integer)

class Week7_results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_number = db.Column(db.Integer)
    game_day = db.Column(db.String(50))
    game_date = db.Column(db.String(50))
    game_time = db.Column(db.String(50))
    away_team_name = db.Column(db.String(50))
    home_team_name = db.Column(db.String(50))
    winner_team_name = db.Column(db.String(50))
    winner_team_abbr = db.Column(db.String(50))
    winner_homecourt = db.Column(db.String(50))
    points_difference = db.Column(db.Integer)

class Week7_scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(50))
    team_score = db.Column(db.Integer)


class Week8_picks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='week8_picks')
    user_name = db.Column(db.String(50), default=lambda: f"{User.query.get(current_user.id).first_name} {User.query.get(current_user.id).last_name}")
    user_pick = db.Column(db.Integer)
    game_number = db.Column(db.Integer)
    selected_winner = db.Column(db.String(50))
    selected_difference = db.Column(db.Integer)

class Week8_results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_number = db.Column(db.Integer)
    game_day = db.Column(db.String(50))
    game_date = db.Column(db.String(50))
    game_time = db.Column(db.String(50))
    away_team_name = db.Column(db.String(50))
    home_team_name = db.Column(db.String(50))
    winner_team_name = db.Column(db.String(50))
    winner_team_abbr = db.Column(db.String(50))
    winner_homecourt = db.Column(db.String(50))
    points_difference = db.Column(db.Integer)

class Week8_scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(50))
    team_score = db.Column(db.Integer)


class Week9_picks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='week9_picks')
    user_name = db.Column(db.String(50), default=lambda: f"{User.query.get(current_user.id).first_name} {User.query.get(current_user.id).last_name}")
    user_pick = db.Column(db.Integer)
    game_number = db.Column(db.Integer)
    selected_winner = db.Column(db.String(50))
    selected_difference = db.Column(db.Integer)

class Week9_results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_number = db.Column(db.Integer)
    game_day = db.Column(db.String(50))
    game_date = db.Column(db.String(50))
    game_time = db.Column(db.String(50))
    away_team_name = db.Column(db.String(50))
    home_team_name = db.Column(db.String(50))
    winner_team_name = db.Column(db.String(50))
    winner_team_abbr = db.Column(db.String(50))
    winner_homecourt = db.Column(db.String(50))
    points_difference = db.Column(db.Integer)

class Week9_scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(50))
    team_score = db.Column(db.Integer)


class Week10_picks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='week10_picks')
    user_name = db.Column(db.String(50), default=lambda: f"{User.query.get(current_user.id).first_name} {User.query.get(current_user.id).last_name}")
    user_pick = db.Column(db.Integer)
    game_number = db.Column(db.Integer)
    selected_winner = db.Column(db.String(50))
    selected_difference = db.Column(db.Integer)

class Week10_results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_number = db.Column(db.Integer)
    game_day = db.Column(db.String(50))
    game_date = db.Column(db.String(50))
    game_time = db.Column(db.String(50))
    away_team_name = db.Column(db.String(50))
    home_team_name = db.Column(db.String(50))
    winner_team_name = db.Column(db.String(50))
    winner_team_abbr = db.Column(db.String(50))
    winner_homecourt = db.Column(db.String(50))
    points_difference = db.Column(db.Integer)

class Week10_scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(50))
    team_score = db.Column(db.Integer)


class Week11_picks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='week11_picks')
    user_name = db.Column(db.String(50), default=lambda: f"{User.query.get(current_user.id).first_name} {User.query.get(current_user.id).last_name}")
    user_pick = db.Column(db.Integer)
    game_number = db.Column(db.Integer)
    selected_winner = db.Column(db.String(50))
    selected_difference = db.Column(db.Integer)

class Week11_results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_number = db.Column(db.Integer)
    game_day = db.Column(db.String(50))
    game_date = db.Column(db.String(50))
    game_time = db.Column(db.String(50))
    away_team_name = db.Column(db.String(50))
    home_team_name = db.Column(db.String(50))
    winner_team_name = db.Column(db.String(50))
    winner_team_abbr = db.Column(db.String(50))
    winner_homecourt = db.Column(db.String(50))
    points_difference = db.Column(db.Integer)

class Week11_scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(50))
    team_score = db.Column(db.Integer)


class Week12_picks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='week12_picks')
    user_name = db.Column(db.String(50), default=lambda: f"{User.query.get(current_user.id).first_name} {User.query.get(current_user.id).last_name}")
    user_pick = db.Column(db.Integer)
    game_number = db.Column(db.Integer)
    selected_winner = db.Column(db.String(50))
    selected_difference = db.Column(db.Integer)

class Week12_results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_number = db.Column(db.Integer)
    game_day = db.Column(db.String(50))
    game_date = db.Column(db.String(50))
    game_time = db.Column(db.String(50))
    away_team_name = db.Column(db.String(50))
    home_team_name = db.Column(db.String(50))
    winner_team_name = db.Column(db.String(50))
    winner_team_abbr = db.Column(db.String(50))
    winner_homecourt = db.Column(db.String(50))
    points_difference = db.Column(db.Integer)

class Week12_scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(50))
    team_score = db.Column(db.Integer)


class Week13_picks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='week13_picks')
    user_name = db.Column(db.String(50), default=lambda: f"{User.query.get(current_user.id).first_name} {User.query.get(current_user.id).last_name}")
    user_pick = db.Column(db.Integer)
    game_number = db.Column(db.Integer)
    selected_winner = db.Column(db.String(50))
    selected_difference = db.Column(db.Integer)

class Week13_results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_number = db.Column(db.Integer)
    game_day = db.Column(db.String(50))
    game_date = db.Column(db.String(50))
    game_time = db.Column(db.String(50))
    away_team_name = db.Column(db.String(50))
    home_team_name = db.Column(db.String(50))
    winner_team_name = db.Column(db.String(50))
    winner_team_abbr = db.Column(db.String(50))
    winner_homecourt = db.Column(db.String(50))
    points_difference = db.Column(db.Integer)

class Week13_scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(50))
    team_score = db.Column(db.Integer)


class Week14_picks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='week14_picks')
    user_name = db.Column(db.String(50), default=lambda: f"{User.query.get(current_user.id).first_name} {User.query.get(current_user.id).last_name}")
    user_pick = db.Column(db.Integer)
    game_number = db.Column(db.Integer)
    selected_winner = db.Column(db.String(50))
    selected_difference = db.Column(db.Integer)

class Week14_results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_number = db.Column(db.Integer)
    game_day = db.Column(db.String(50))
    game_date = db.Column(db.String(50))
    game_time = db.Column(db.String(50))
    away_team_name = db.Column(db.String(50))
    home_team_name = db.Column(db.String(50))
    winner_team_name = db.Column(db.String(50))
    winner_team_abbr = db.Column(db.String(50))
    winner_homecourt = db.Column(db.String(50))
    points_difference = db.Column(db.Integer)

class Week14_scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(50))
    team_score = db.Column(db.Integer)


class Week15_picks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='week15_picks')
    user_name = db.Column(db.String(50), default=lambda: f"{User.query.get(current_user.id).first_name} {User.query.get(current_user.id).last_name}")
    user_pick = db.Column(db.Integer)
    game_number = db.Column(db.Integer)
    selected_winner = db.Column(db.String(50))
    selected_difference = db.Column(db.Integer)

class Week15_results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_number = db.Column(db.Integer)
    game_day = db.Column(db.String(50))
    game_date = db.Column(db.String(50))
    game_time = db.Column(db.String(50))
    away_team_name = db.Column(db.String(50))
    home_team_name = db.Column(db.String(50))
    winner_team_name = db.Column(db.String(50))
    winner_team_abbr = db.Column(db.String(50))
    winner_homecourt = db.Column(db.String(50))
    points_difference = db.Column(db.Integer)

class Week15_scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(50))
    team_score = db.Column(db.Integer)


class Week16_picks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='week16_picks')
    user_name = db.Column(db.String(50), default=lambda: f"{User.query.get(current_user.id).first_name} {User.query.get(current_user.id).last_name}")
    user_pick = db.Column(db.Integer)
    game_number = db.Column(db.Integer)
    selected_winner = db.Column(db.String(50))
    selected_difference = db.Column(db.Integer)

class Week16_results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_number = db.Column(db.Integer)
    game_day = db.Column(db.String(50))
    game_date = db.Column(db.String(50))
    game_time = db.Column(db.String(50))
    away_team_name = db.Column(db.String(50))
    home_team_name = db.Column(db.String(50))
    winner_team_name = db.Column(db.String(50))
    winner_team_abbr = db.Column(db.String(50))
    winner_homecourt = db.Column(db.String(50))
    points_difference = db.Column(db.Integer)

class Week16_scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(50))
    team_score = db.Column(db.Integer)


class Week17_picks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='week17_picks')
    user_name = db.Column(db.String(50), default=lambda: f"{User.query.get(current_user.id).first_name} {User.query.get(current_user.id).last_name}")
    user_pick = db.Column(db.Integer)
    game_number = db.Column(db.Integer)
    selected_winner = db.Column(db.String(50))
    selected_difference = db.Column(db.Integer)

class Week17_results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_number = db.Column(db.Integer)
    game_day = db.Column(db.String(50))
    game_date = db.Column(db.String(50))
    game_time = db.Column(db.String(50))
    away_team_name = db.Column(db.String(50))
    home_team_name = db.Column(db.String(50))
    winner_team_name = db.Column(db.String(50))
    winner_team_abbr = db.Column(db.String(50))
    winner_homecourt = db.Column(db.String(50))
    points_difference = db.Column(db.Integer)

class Week17_scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(50))
    team_score = db.Column(db.Integer)


class Week18_picks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='week18_picks')
    user_name = db.Column(db.String(50), default=lambda: f"{User.query.get(current_user.id).first_name} {User.query.get(current_user.id).last_name}")
    user_pick = db.Column(db.Integer)
    game_number = db.Column(db.Integer)
    selected_winner = db.Column(db.String(50))
    selected_difference = db.Column(db.Integer)

class Week18_results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_number = db.Column(db.Integer)
    game_day = db.Column(db.String(50))
    game_date = db.Column(db.String(50))
    game_time = db.Column(db.String(50))
    away_team_name = db.Column(db.String(50))
    home_team_name = db.Column(db.String(50))
    winner_team_name = db.Column(db.String(50))
    winner_team_abbr = db.Column(db.String(50))
    winner_homecourt = db.Column(db.String(50))
    points_difference = db.Column(db.Integer)

class Week18_scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(50))
    team_score = db.Column(db.Integer)

