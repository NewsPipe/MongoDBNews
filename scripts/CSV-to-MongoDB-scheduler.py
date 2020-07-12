import os
from crontab import CronTab

cron = CronTab(user='root')
job = cron.new(command='python CSV-to-MongoDB.py')
job.day.every(1)

cron.write()