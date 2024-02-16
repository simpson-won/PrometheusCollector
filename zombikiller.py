from flask import Flask

from flask_apscheduler import APScheduler
from config import zombi_name, check_interval_sec
import subprocess
import daemon

app = Flask(__name__)

scheduler = APScheduler()


def get_docker_ps() -> list:
    cmd = "/usr/bin/docker ps"
    id_list = []
    try:
        all_lines = subprocess.check_output(cmd, shell=True, text=True)
        if len(all_lines) > 20:
            for line in all_lines.split("\n"):
                if len(line) > 10:
                    id_list.append(line.split(' ')[0])
        id_list.remove("CONTAINER")
    except Exception:
        print('')
    return id_list


def get_ps():
    pid_map = {}
    try:
        cmd = f"/usr/bin/ps aux | /usr/bin/grep '{zombi_name}' | /usr/bin/grep -v 'grep'"
        or_line = subprocess.check_output(cmd, shell=True, text=True)
        if len(or_line) > 0:
            lines = or_line.split("\n")
            cnt = 0
            for line in lines:
                if len(line) > 1:
                    ps_infos = line.split()
                    if len(ps_infos) > 1:
                        print(f'ps_infos = {ps_infos}')
                        docker_id = ps_infos[14][0:12]
                        pid = ps_infos[1]
                        print(f'{cnt} : pid       = {pid}')
                        print(f'{cnt} : docker_id = {docker_id}')
                        pid_map[docker_id]=pid
                cnt += 1
    except Exception as e:
        print('')
    return pid_map


@scheduler.task('interval', id='check_zombi', seconds=check_interval_sec)
def check_zombi():
    print(f'This job is executed every 10 seconds. = {zombi_name}')
    id_list = get_docker_ps()
    print(f'id_list = {id_list}')
    pid_map = get_ps()
    print(f'pid_map = {pid_map}')
    kill_id_list = []
    for id in id_list:
        if id not in pid_map.keys():
            kill_id_list.append(id)
    for kill_id in kill_id_list:
        print(f'kill_id = {kill_id}')


def main():
    scheduler.init_app(app)
    scheduler.start()
    app.run()


if __name__ == '__main__':
    with daemon.DaemonContext():
        main()
