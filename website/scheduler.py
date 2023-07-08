from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from pytz import timezone

scheduler = BackgroundScheduler(daemon=True)

def schedule_news_update(app):
    from .webscraper import scrape_news
    scheduler.add_job(
        func=scrape_news,
        args=(app,),
        trigger=IntervalTrigger(minutes=30),
        id='scrape_news',
        replace_existing=False
    )
    if not scheduler.running:
        scheduler.start()


def schedule_scores_results_leaderboard_update(app):
    print("scores_results_update")
    from .webscraper import scrape_scores

    def week_number_update():
        print("week_number_update--")
        time_zone = timezone('America/Mexico_City')
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

        week_number = 1
        for week, limit_date in limit_dates.items():
            if current_datetime > limit_date:
                week_number = week + 1

        scrape_scores(app, week_number)
    end_date = datetime(2024, 7, 7, 20, 35)
    # Create separate CronTrigger objects for each schedule
    cron_schedule_thu = CronTrigger(day_of_week='thu', hour='18-21', minute='20/10', timezone=timezone('America/Mexico_City'), end_date=end_date)
    cron_schedule_sat = CronTrigger(day_of_week='sat', hour='18-21', minute='*/10', timezone=timezone('America/Mexico_City'), end_date=end_date)
    cron_schedule_sun = CronTrigger(day_of_week='sun', hour='11-21', minute='20/10', timezone=timezone('America/Mexico_City'), end_date=end_date)
    cron_schedule_mon = CronTrigger(day_of_week='mon', hour='18-21', minute='20/10', timezone=timezone('America/Mexico_City'), end_date=end_date)

    # Add the triggers to the scheduler
    scheduler.add_job(
        func=week_number_update,
        trigger=cron_schedule_thu,
        id='thursday_update',
        replace_existing=False
    )
    scheduler.add_job(
        func=week_number_update,
        trigger=cron_schedule_sat,
        id='saturday_update',
        replace_existing=False
    )
    scheduler.add_job(
        func=week_number_update,
        trigger=cron_schedule_sun,
        id='sunday_update',
        replace_existing=False
    )
    scheduler.add_job(
        func=week_number_update,
        trigger=cron_schedule_mon,
        id='monday_update',
        replace_existing=False
    )
    # Start the scheduler if it's not already running
    if not scheduler.running:
        scheduler.start()
    """ scrape_scores(app,5) """

def start_scheduler(app):
    print("start scheduler")
    schedule_news_update(app)
    schedule_scores_results_leaderboard_update(app)