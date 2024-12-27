from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from app.tasks import check_price_changes
from apscheduler.triggers.cron import CronTrigger

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        check_price_changes,
        trigger=CronTrigger(hour='*/8'),  # 每8小时执行一次
        id='check_prices',
        max_instances=1,
        replace_existing=True
    )
    scheduler.start()