from flask import Flask

from flask_apscheduler import APScheduler
from config import zombi_name, check_interval_sec
import subprocess

app = Flask(__name__)

scheduler = APScheduler()


@scheduler.task('interval', id='check_zombi', seconds=check_interval_sec)
def check_zombi():
    print(f'This job is executed every 10 seconds. ${zombi_name}')
    cmd = "/usr/bin/ps -adef|/usr/bin/grep 'containerd-shim-runc-v2'|/usr/bin/grep -v 'grep'|/usr/bin/wc -l"
    data = subprocess.check_output(cmd, shell=True, text=True)
    print(f'data = ${data}')


if __name__ == '__main__':

    scheduler.init_app(app)

    scheduler.start()

    app.run()
