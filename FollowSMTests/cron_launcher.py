from crontab import CronTab

# using cron to start bot every hour
my_cron = CronTab(user='bot')
job = my_cron.new(command='python ./FollowSM/app/bitmex_main.py')
job.hour.every(1)

my_cron.write()
